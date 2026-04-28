import unittest
from contextlib import ExitStack
from datetime import date, datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from digest_clock import digest_today
from digest_postprocess import count_chinese_chars, summary_needs_repair
from digest_pipeline_gemini import _apply_language_quota, _is_chinese_entry, _selection_reason
from fetch_feeds import FeedEntry, fetch_all_entries
from fetch_opml import fetch_opml_metadata
from filter_entries import filter_and_dedup
from rss_curation import curate_entries
from source_reports import refresh_latest_report, refresh_weekly_report, render_source_report
from site_builder import build


class FetchFeedsTests(unittest.IsolatedAsyncioTestCase):
    async def test_max_per_category_applies_after_recency_sort(self) -> None:
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


class SummaryLengthTests(unittest.TestCase):
    def test_summary_length_checks_use_chinese_characters(self) -> None:
        short_cn = "这是一个很短的摘要。"
        enough_cn = "汉" * 220
        english_heavy = "A" * 260

        self.assertTrue(summary_needs_repair(short_cn))
        self.assertFalse(summary_needs_repair(enough_cn))
        self.assertTrue(summary_needs_repair(english_heavy))
        self.assertEqual(count_chinese_chars(enough_cn), 220)


class GeminiPipelineTests(unittest.TestCase):
    def test_selection_reason_falls_back_to_empty_string(self) -> None:
        self.assertEqual(_selection_reason({}), "")
        self.assertEqual(_selection_reason({"selection_reason": "值得关注的官方发布，影响企业部署策略"}), "值得关注的官方发布，影响企业部署策略")

    def test_is_chinese_entry_detects_via_title_or_host(self) -> None:
        self.assertTrue(_is_chinese_entry({"title": "绿盟披露漏洞", "url": "https://example.com/x"}))
        self.assertTrue(_is_chinese_entry({"title": "English title", "url": "https://mp.weixin.qq.com/s/abc"}))
        self.assertTrue(_is_chinese_entry({"title": "English title", "feed_url": "https://wechat2rss.xlab.app/feed/x.xml"}))
        self.assertFalse(_is_chinese_entry({"title": "English title", "url": "https://thehackernews.com/x"}))

    def test_language_quota_reserves_top_chinese_slots(self) -> None:
        # deduped sorted by score desc; CN at idx 0 (sc=9), 4 (sc=5); rest English
        deduped = [
            ({"title": "中文 A", "url": "u/cn1"}, 9),
            ({"title": "EN A", "url": "u/en1"}, 8),
            ({"title": "EN B", "url": "u/en2"}, 7),
            ({"title": "EN C", "url": "u/en3"}, 6),
            ({"title": "中文 B", "url": "u/cn2"}, 5),
            ({"title": "EN D", "url": "u/en4"}, 4),
        ]
        result = _apply_language_quota(deduped, top_n=4, min_chinese=2)
        urls = [e["url"] for e, _ in result]
        # Expect: top 4 by score, but CN B (sc=5) bumps EN C (sc=6) since min_cn=2
        self.assertIn("u/cn1", urls)
        self.assertIn("u/cn2", urls)
        self.assertEqual(len(urls), 4)
        # Score order preserved within selection
        scores = [sc for _, sc in result]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_language_quota_no_op_when_no_chinese_candidates(self) -> None:
        deduped = [
            ({"title": "EN A", "url": "u/en1"}, 8),
            ({"title": "EN B", "url": "u/en2"}, 7),
        ]
        result = _apply_language_quota(deduped, top_n=2, min_chinese=3)
        self.assertEqual([e["url"] for e, _ in result], ["u/en1", "u/en2"])


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
