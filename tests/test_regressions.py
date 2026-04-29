import json
import sys
import unittest
from contextlib import ExitStack
from datetime import date, datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from digest_clock import digest_today
from digest_postprocess import count_chinese_chars, summary_needs_repair
from digest_pipeline_gemini import (
    BOARD_SCORE_SYSTEM,
    _candidate_pool,
    _finalize_digest_item,
    _is_chinese_entry,
    _selection_reason,
)
import fetch_and_save
import fetch_feeds
from fetch_feeds import FeedEntry, fetch_all_entries, load_seen_urls
from fetch_opml import fetch_opml_metadata
from filter_entries import FilteredEntry, filter_and_dedup
from rss_curation import curate_entries
from source_policy import select_with_source_policy, source_profile
from source_reports import refresh_latest_report, refresh_weekly_report, render_source_report
from site_builder import build


class FetchFeedsTests(unittest.IsolatedAsyncioTestCase):
    def test_load_seen_urls_reads_utf8_archive(self) -> None:
        with TemporaryDirectory() as tmpdir:
            archive = Path(tmpdir)
            archive.joinpath("2026-04-28.json").write_text(
                json.dumps({"urls": ["https://example.com/安全"]}, ensure_ascii=False),
                encoding="utf-8",
            )

            with patch("fetch_feeds.ARCHIVE_DIR", archive):
                seen = load_seen_urls("2026-04-28")

        self.assertEqual(seen, {"https://example.com/安全"})

    async def test_max_per_category_applies_after_recency_sort(self) -> None:
        if fetch_feeds.httpx is None:
            self.skipTest("httpx is not installed in this Python environment")

        feeds = {"security": ["feed-a", "feed-b"]}
        base = datetime(2026, 4, 22, tzinfo=timezone.utc)
        results = {
            "feed-a": [
                FeedEntry("older-1", "https://a/1", "summary text long enough", "", base.replace(hour=1)),
                FeedEntry("older-2", "https://a/2", "summary text long enough", "", base.replace(hour=2)),
            ],
            "feed-b": [
                FeedEntry("newer-1", "https://b/1", "summary text long enough", "", base.replace(hour=3)),
                FeedEntry("newer-2", "https://b/2", "summary text long enough", "", base.replace(hour=4)),
            ],
        }

        async def fake_fetch(_semaphore, _client, url):
            return results[url]

        with patch("fetch_feeds._fetch_one_bounded", side_effect=fake_fetch):
            entries, _health = await fetch_all_entries(
                feeds,
                hours=9999,
                max_per_category=2,
                feed_titles={"feed-a": "Feed A", "feed-b": "Feed B"},
            )

        self.assertEqual([entry.title for entry in entries], ["newer-2", "newer-1"])
        self.assertEqual([entry.feed_url for entry in entries], ["feed-b", "feed-b"])
        self.assertEqual([entry.feed_title for entry in entries], ["Feed B", "Feed B"])


class FetchOpmlTests(unittest.TestCase):
    def test_fetch_opml_metadata_preserves_feed_title(self) -> None:
        with TemporaryDirectory() as tmpdir:
            opml = Path(tmpdir) / "feeds.opml"
            opml.write_text(
                """<opml><body><outline text="Labs"><outline text="Anthropic" title="Anthropic News" xmlUrl="https://example.com/rss.xml" /></outline></body></opml>""",
                encoding="utf-8",
            )

            metadata = fetch_opml_metadata(opml)

        self.assertEqual(metadata["https://example.com/rss.xml"]["feed_title"], "Anthropic News")
        self.assertEqual(metadata["https://example.com/rss.xml"]["category"], "Labs")


class FilterEntriesTests(unittest.TestCase):
    def test_kept_entries_sort_by_score_then_newest(self) -> None:
        older = FeedEntry(
            title="Older advisory",
            url="https://example.com/older",
            summary="A" * 80,
            category="security",
            published=datetime(2026, 4, 22, 1, tzinfo=timezone.utc),
        )
        newer = FeedEntry(
            title="Newer advisory",
            url="https://example.com/newer",
            summary="B" * 80,
            category="security",
            published=datetime(2026, 4, 22, 2, tzinfo=timezone.utc),
        )

        kept, _stats = filter_and_dedup([older, newer])

        self.assertEqual([entry.title for entry in kept], ["Newer advisory", "Older advisory"])

    def test_filter_preserves_feed_metadata(self) -> None:
        entry = FeedEntry(
            title="CVE-2026-1234 exploited in product",
            url="https://example.com/advisory",
            summary="A" * 80,
            category="security",
            published=datetime(2026, 4, 22, 1, tzinfo=timezone.utc),
            feed_url="https://feeds.example.com/rss",
            feed_title="Example Feed",
        )

        kept, _stats = filter_and_dedup([entry])

        self.assertEqual(kept[0].feed_url, "https://feeds.example.com/rss")
        self.assertEqual(kept[0].feed_title, "Example Feed")


class SiteBuilderTests(unittest.TestCase):
    def test_template_does_not_render_feed_items_with_inner_html(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertNotIn("card.innerHTML", template)
        self.assertIn("safeUrl", template)
        self.assertIn("textContent", template)

    def test_cli_lookback_overrides_config(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            templates = root / "templates"
            docs = root / "docs"
            templates.mkdir()
            templates.joinpath("index.html.j2").write_text("{{ title }}", encoding="utf-8")

            with ExitStack() as stack:
                stack.enter_context(patch("site_builder.DOCS_DIR", docs))
                stack.enter_context(patch("site_builder.TEMPLATE_DIR", templates))
                stack.enter_context(patch("site_builder.yaml.safe_load", return_value={"boards": {}, "site": {"lookback_days": 7}}))
                stack.enter_context(patch("site_builder.Path.read_text", return_value="site: {}"))
                mock_today = stack.enter_context(patch("site_builder.digest_today"))
                mock_feed = stack.enter_context(patch("site_builder._build_feed_for_date", return_value=None))
                mock_today.return_value = date(2026, 4, 22)

                build(lookback_days=2)

        checked_dates = [call.args[1] for call in mock_feed.call_args_list]
        self.assertEqual(len(checked_dates), 2)

    def test_daily_workflow_supports_single_board_dispatch(self) -> None:
        workflow = Path(".github/workflows/daily.yml").read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("board:", workflow)
        self.assertIn("BOARD_SELECTION", workflow)
        self.assertIn("security ai finance", workflow)

    def test_daily_workflow_uses_pinned_requirements(self) -> None:
        workflow = Path(".github/workflows/daily.yml").read_text(encoding="utf-8")

        self.assertIn('cache: "pip"', workflow)
        self.assertIn("pip install -r requirements.txt", workflow)
        self.assertTrue(Path("requirements.txt").exists())


class FetchAndSaveTests(unittest.TestCase):
    def test_board_output_includes_full_utc_batch_timestamp(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            output_dir = root / "output"
            config = root / "config.yaml"
            config.write_text(
                "\n".join(
                    [
                        "boards:",
                        "  test:",
                        "    display_name: Test",
                        "    opml: feeds/test.opml",
                        "    fetch_hours: 24",
                    ]
                ),
                encoding="utf-8",
            )
            filtered = FilteredEntry(
                title="测试新闻",
                url="https://example.com/news",
                summary="摘要",
                category="Labs",
                published="2026-04-28T00:00:00Z",
                fetch_status="rss_only",
                cve_ids=[],
                related_urls=[],
                quality_score=5,
                feed_url="feed-a",
                feed_title="Feed A",
            )

            async def fake_fetch_all_entries(*_args, **_kwargs):
                return (
                    [
                        FeedEntry(
                            title="测试新闻",
                            url="https://example.com/news",
                            summary="摘要",
                            category="Labs",
                            published=datetime(2026, 4, 28, tzinfo=timezone.utc),
                            feed_url="feed-a",
                            feed_title="Feed A",
                        )
                    ],
                    {},
                )

            with ExitStack() as stack:
                stack.enter_context(patch.object(sys, "argv", ["fetch_and_save.py", "--board", "test"]))
                stack.enter_context(patch("fetch_and_save.PROJECT_DIR", root))
                stack.enter_context(patch("fetch_and_save.CONFIG_PATH", config))
                stack.enter_context(patch("fetch_and_save.OUTPUT_DIR", output_dir))
                stack.enter_context(patch("fetch_and_save.digest_today", return_value=date(2026, 4, 28)))
                stack.enter_context(patch("fetch_and_save._utc_now_iso", return_value="2026-04-28T02:03:04Z"))
                stack.enter_context(patch("fetch_and_save.fetch_opml", return_value={"Labs": ["feed-a"]}))
                stack.enter_context(
                    patch(
                        "fetch_and_save.fetch_opml_metadata",
                        return_value={"feed-a": {"feed_title": "Feed A", "category": "Labs"}},
                    )
                )
                stack.enter_context(patch("fetch_and_save.load_seen_urls", return_value=set()))
                stack.enter_context(patch("fetch_and_save.fetch_all_entries", side_effect=fake_fetch_all_entries))
                stack.enter_context(patch("fetch_and_save.filter_and_dedup", return_value=([filtered], {"input": 1, "output": 1})))
                stack.enter_context(patch("fetch_and_save.curate_entries", return_value=([filtered], {})))

                fetch_and_save.main()

            payload = json.loads(output_dir.joinpath("test_latest.json").read_text(encoding="utf-8"))

        self.assertEqual(payload["fetched_at"], "2026-04-28")
        self.assertEqual(payload["fetched_at_utc"], "2026-04-28T02:03:04Z")


class CurationTests(unittest.TestCase):
    def test_source_caps_limit_dominant_publishers(self) -> None:
        entries = [
            FeedEntry("A1", "https://pymnts.com/a1", "summary text", "Payments", datetime.now(timezone.utc)),
            FeedEntry("A2", "https://pymnts.com/a2", "summary text", "Payments", datetime.now(timezone.utc)),
            FeedEntry("A3", "https://pymnts.com/a3", "summary text", "Payments", datetime.now(timezone.utc)),
            FeedEntry("B1", "https://bankingdive.com/b1", "summary text", "Payments", datetime.now(timezone.utc)),
        ]

        curated, stats = curate_entries(entries, {"source_caps": {"pymnts.com": 2}})

        self.assertEqual([entry.title for entry in curated], ["A1", "A2", "B1"])
        self.assertEqual(stats["dropped_source_cap"], 1)

    def test_max_entries_trims_after_source_caps(self) -> None:
        entries = [
            FeedEntry(
                f"A{i}",
                f"https://source-{i}.example/a",
                "summary text",
                "Media",
                datetime.now(timezone.utc),
            )
            for i in range(5)
        ]

        curated, stats = curate_entries(entries, {"max_entries": 3})

        self.assertEqual([entry.title for entry in curated], ["A0", "A1", "A2"])
        self.assertEqual(stats["dropped_max_entries"], 2)


class SummaryLengthTests(unittest.TestCase):
    def test_summary_length_checks_use_chinese_characters(self) -> None:
        short_cn = "这是一个很短的摘要。"
        enough_cn = "汉" * 150
        too_long_cn = "汉" * 220
        english_heavy = "A" * 260

        self.assertTrue(summary_needs_repair(short_cn))
        self.assertFalse(summary_needs_repair(enough_cn))
        self.assertTrue(summary_needs_repair(too_long_cn))
        self.assertTrue(summary_needs_repair(english_heavy))
        self.assertEqual(count_chinese_chars(enough_cn), 150)


class SourcePolicyTests(unittest.TestCase):
    def test_source_profile_classifies_google_news_and_wechat(self) -> None:
        google = source_profile(
            {
                "title": "OpenAI news",
                "url": "https://news.google.com/rss/articles/abc",
                "feed_url": "https://news.google.com/rss/search?q=OpenAI",
            }
        )
        wechat = source_profile(
            {
                "title": "中文安全研究",
                "url": "https://example.com/article",
                "feed_url": "https://wechat2rss.xlab.app/feed/hash.xml",
            }
        )

        self.assertTrue(google.is_google_news)
        self.assertTrue(google.is_aggregator)
        self.assertFalse(google.is_direct)
        self.assertTrue(wechat.is_wechat)
        self.assertTrue(wechat.is_chinese)
        self.assertTrue(wechat.is_direct)

    def test_selection_policy_caps_google_news_and_reserves_chinese(self) -> None:
        candidates = [
            ({"title": "Google 1", "url": "https://news.google.com/rss/articles/1"}, 10),
            ({"title": "Google 2", "url": "https://news.google.com/rss/articles/2"}, 9),
            ({"title": "Direct 1", "url": "https://openai.com/news/a"}, 8),
            ({"title": "Direct 2", "url": "https://anthropic.com/news/b"}, 7),
            (
                {
                    "title": "中文源",
                    "url": "https://example.com/cn",
                    "feed_url": "https://wechat2rss.xlab.app/feed/x.xml",
                },
                6,
            ),
            ({"title": "Direct 3", "url": "https://deepmind.google/blog/c"}, 5),
        ]

        selected = select_with_source_policy(
            candidates,
            top_n=4,
            policy={"max_google_news": 1, "max_aggregator": 1, "min_chinese": 1, "max_per_source": 2},
        )
        urls = [entry["url"] for entry, _score in selected]

        self.assertEqual(sum(1 for url in urls if "news.google.com" in url), 1)
        self.assertIn("https://example.com/cn", urls)
        self.assertEqual(len(urls), 4)

    def test_selection_policy_reserves_direct_source(self) -> None:
        candidates = [
            ({"title": "Google 1", "url": "https://news.google.com/rss/articles/1"}, 10),
            ({"title": "Google 2", "url": "https://news.google.com/rss/articles/2"}, 9),
            ({"title": "Direct", "url": "https://openai.com/news/direct"}, 4),
        ]

        selected = select_with_source_policy(
            candidates,
            top_n=2,
            policy={"min_direct": 1, "max_google_news": 2, "max_aggregator": 2},
        )
        urls = [entry["url"] for entry, _score in selected]

        self.assertIn("https://openai.com/news/direct", urls)


class GeminiPipelineTests(unittest.TestCase):
    def test_selection_reason_falls_back_to_empty_string(self) -> None:
        self.assertEqual(_selection_reason({}), "")
        self.assertEqual(_selection_reason({"selection_reason": "值得关注的官方发布，影响企业部署策略"}), "值得关注的官方发布，影响企业部署策略")

    def test_is_chinese_entry_detects_via_title_or_host(self) -> None:
        self.assertTrue(_is_chinese_entry({"title": "绿盟披露漏洞", "url": "https://example.com/x"}))
        self.assertTrue(_is_chinese_entry({"title_orig": "支付宝发布AI支付能力", "url": "https://example.com/x"}))
        self.assertTrue(_is_chinese_entry({"title": "English title", "url": "https://mp.weixin.qq.com/s/abc"}))
        self.assertTrue(_is_chinese_entry({"title": "English title", "url": "https://example.cn"}))
        self.assertTrue(_is_chinese_entry({"title": "English title", "feed_url": "https://wechat2rss.xlab.app/feed/x.xml"}))
        self.assertFalse(_is_chinese_entry({"title": "English title", "url": "https://thehackernews.com/x"}))
        self.assertFalse(_is_chinese_entry({"title": "English title", "url": "https://example.com/cn/article"}))

    def test_score_prompts_include_language_fairness(self) -> None:
        for prompt in BOARD_SCORE_SYSTEM.values():
            self.assertIn("评分只看新闻价值", prompt)
            self.assertIn("不因语言", prompt)

    def test_source_policy_reserves_top_chinese_slots(self) -> None:
        # deduped sorted by score desc; CN at idx 0 (sc=9), 4 (sc=5); rest English
        deduped = [
            ({"title": "中文 A", "url": "u/cn1"}, 9),
            ({"title": "EN A", "url": "u/en1"}, 8),
            ({"title": "EN B", "url": "u/en2"}, 7),
            ({"title": "EN C", "url": "u/en3"}, 6),
            ({"title": "中文 B", "url": "u/cn2"}, 5),
            ({"title": "EN D", "url": "u/en4"}, 4),
        ]
        result = select_with_source_policy(deduped, top_n=4, policy={"min_chinese": 2})
        urls = [e["url"] for e, _ in result]
        # Expect: top 4 by score, but CN B (sc=5) bumps EN C (sc=6) since min_cn=2
        self.assertIn("u/cn1", urls)
        self.assertIn("u/cn2", urls)
        self.assertEqual(len(urls), 4)
        # Score order preserved within selection
        scores = [sc for _, sc in result]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_source_policy_no_op_when_no_chinese_candidates(self) -> None:
        deduped = [
            ({"title": "EN A", "url": "u/en1"}, 8),
            ({"title": "EN B", "url": "u/en2"}, 7),
        ]
        result = select_with_source_policy(deduped, top_n=2, policy={"min_chinese": 3})
        self.assertEqual([e["url"] for e, _ in result], ["u/en1", "u/en2"])

    def test_finalize_digest_item_fills_required_fields(self) -> None:
        entry = {
            "title": "OpenAI and Anthropic discuss cybersecurity models",
            "summary": "OpenAI and Anthropic discussed cybersecurity models with lawmakers.",
            "url": "https://news.google.com/rss/articles/abc",
            "category": "Media",
            "published": "2026-04-29T00:00:00Z",
        }
        item = {
            "title_zh": "OpenAI and Anthropic discuss cybersecurity models",
            "summary": "短摘要",
            "tags": [],
            "selection_reason": "",
        }

        finalized = _finalize_digest_item(entry, item)

        self.assertGreaterEqual(count_chinese_chars(finalized["summary"]), 120)
        self.assertLessEqual(count_chinese_chars(finalized["summary"]), 180)
        self.assertTrue(finalized["tags"])
        self.assertTrue(finalized["selection_reason"])
        self.assertGreater(count_chinese_chars(finalized["title_zh"]), 0)

    def test_candidate_pool_uses_fill_floor_to_backfill_below_threshold(self) -> None:
        scored = [
            ({"title": "A", "url": "https://a.example"}, 8),
            ({"title": "B", "url": "https://b.example"}, 6),
            ({"title": "C", "url": "https://c.example"}, 5),
            ({"title": "D", "url": "https://d.example"}, 4),
        ]

        pool = _candidate_pool(scored, top_n=4, fill_score_floor=5)

        self.assertEqual([entry["title"] for entry, _score in pool], ["A", "B", "C"])


class SourceReportTests(unittest.TestCase):
    def test_source_report_summarizes_scores_and_dedupe_counts(self) -> None:
        feed_stats = {
            "feed-a": {"feed_title": "Feed A", "category": "Labs", "attempted": 1, "succeeded": 1, "raw_count": 3},
            "feed-b": {"feed_title": "Feed B", "category": "Media", "attempted": 1, "succeeded": 0, "raw_count": 0},
        }
        entries = [
            {"url": "https://a/1", "feed_url": "feed-a", "feed_title": "Feed A"},
            {"url": "https://a/2", "feed_url": "feed-a", "feed_title": "Feed A"},
            {"url": "https://a/3", "feed_url": "feed-a", "feed_title": "Feed A"},
        ]

        markdown = render_source_report(
            board="ai",
            display_name="AI 前沿",
            report_date=date(2026, 4, 24),
            feed_stats=feed_stats,
            entries=entries,
            score_by_url={"https://a/1": 9, "https://a/2": 5, "https://a/3": 2},
            selected_urls={"https://a/1"},
            merged_urls=["https://a/3"],
            selection_reason_by_url={"https://a/1": "官方发布影响企业部署"},
        )

        self.assertIn("| Feed A | 1/1 | 3 -> 3 | 5.3 · 5 | 33% | 1 | 1 |", markdown)
        self.assertNotIn("| Feed B |", markdown)
        self.assertIn("另有 1 个源今日 0 条目（0/1 抓取成功）。", markdown)
        self.assertIn("- **Feed A**：*为什么入选：官方发布影响企业部署*", markdown)

    def test_latest_report_combines_board_reports(self) -> None:
        with TemporaryDirectory() as tmpdir:
            reports = Path(tmpdir)
            reports.joinpath("ai_2026-04-24.md").write_text("# AI\n", encoding="utf-8")
            reports.joinpath("security_2026-04-24.md").write_text("# Security\n", encoding="utf-8")

            latest = refresh_latest_report(
                date(2026, 4, 24),
                ["security", "ai", "finance"],
                reports_dir=reports,
            )

            body = latest.read_text(encoding="utf-8")

        self.assertLess(body.index("# Security"), body.index("# AI"))
        self.assertIn("finance", body)
        self.assertIn("未生成报表", body)

    def test_weekly_report_aggregates_recent_board_reports(self) -> None:
        with TemporaryDirectory() as tmpdir:
            reports = Path(tmpdir)
            reports.joinpath("ai_2026-04-23.md").write_text(
                "\n".join(
                    [
                        "# AI 前沿 源质量报表 2026-04-23",
                        "",
                        "| Feed | 抓取 | 条目 | LLM 均分 | 低分占比 | 入选 | 去重被合并 |",
                        "|---|---:|---:|---:|---:|---:|---:|",
                        "| Feed A | 1/1 | 4 -> 3 | 6.0 · 6 | 0% | 2 | 1 |",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            reports.joinpath("ai_2026-04-24.md").write_text(
                "\n".join(
                    [
                        "# AI 前沿 源质量报表 2026-04-24",
                        "",
                        "| Feed | 抓取 | 条目 | LLM 均分 | 低分占比 | 入选 | 去重被合并 |",
                        "|---|---:|---:|---:|---:|---:|---:|",
                        "| Feed A | 1/1 | 2 -> 1 | 8.0 · 8 | 0% | 1 | 0 |",
                        "| Feed B | 1/1 | 1 -> 1 | 4.0 · 4 | 100% | 0 | 0 |",
                        "| Empty Feed | 1/1 | 0 -> 0 | - | - | 0 | 0 |",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            weekly = refresh_weekly_report(
                date(2026, 4, 24),
                ["ai"],
                reports_dir=reports,
            )

            body = weekly.read_text(encoding="utf-8")

        self.assertIn("# 7 日源质量汇总 2026-04-18 至 2026-04-24", body)
        self.assertIn("| Feed A | 2/2 | 6 | 6.5 | 3 | 1 |", body)
        self.assertIn("| Feed B | 1/1 | 1 | 4.0 | 0 | 0 |", body)
        self.assertNotIn("Empty Feed", body)


class DigestClockTests(unittest.TestCase):
    def test_digest_today_honors_env_override(self) -> None:
        with patch.dict("os.environ", {"DIGEST_DATE": "2026-04-25"}):
            self.assertEqual(digest_today(), date(2026, 4, 25))


if __name__ == "__main__":
    unittest.main()
