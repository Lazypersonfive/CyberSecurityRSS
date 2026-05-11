import json
import sys
import unittest
from contextlib import ExitStack
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from digest_clock import digest_today
from digest_postprocess import count_chinese_chars, summary_needs_repair
from aihot_compare import compare_aihot_items, render_aihot_compare
from llm_backends.base import backend_name_from_env, get_backend
from eval_strategy import build_offline_eval, render_offline_eval
from digest_pipeline_gemini import (
    BOARD_SCORE_SYSTEM,
    _candidate_pool,
    _finalize_digest_item,
    _is_chinese_entry,
    _selection_reason,
)
import fetch_and_save
import fetch_feeds
from fetch_feeds import FeedEntry, archive_urls, fetch_all_entries, load_seen_urls
from fetch_opml import fetch_opml, fetch_opml_metadata
from filter_entries import FilteredEntry, filter_and_dedup
from rss_curation import curate_entries
from source_policy import select_with_source_policy, source_mix_stats, source_profile
from security_editorial import adjust_security_score
from source_audit import build_source_audit, render_source_audit
from source_reports import refresh_latest_report, refresh_weekly_report, render_source_report
from site_builder import _build_feed_for_date, build


class FetchFeedsTests(unittest.IsolatedAsyncioTestCase):
    def test_load_seen_urls_reads_utf8_archive(self) -> None:
        with TemporaryDirectory() as tmpdir:
            archive = Path(tmpdir)
            archive.joinpath("2026-04-28.json").write_text(
                json.dumps({"urls": ["https://example.com/安全"]}, ensure_ascii=False),
                encoding="utf-8",
            )

            with patch("fetch_feeds.ARCHIVE_DIR", archive):
                seen = load_seen_urls("2026-04-28", lookback_days=1)

        self.assertEqual(seen, {"https://example.com/安全"})

    def test_load_seen_urls_merges_recent_days(self) -> None:
        with TemporaryDirectory() as tmpdir:
            archive = Path(tmpdir)
            archive.joinpath("2026-04-27.json").write_text(
                json.dumps({"urls": ["https://example.com/old"]}), encoding="utf-8"
            )
            archive.joinpath("2026-04-29.json").write_text(
                json.dumps({"urls": ["https://example.com/new"]}), encoding="utf-8"
            )

            with patch("fetch_feeds.ARCHIVE_DIR", archive):
                merged = load_seen_urls("2026-04-29", lookback_days=3)
                only_today = load_seen_urls("2026-04-29", lookback_days=1)
                previous_days = load_seen_urls("2026-04-29", lookback_days=3, include_today=False)

        self.assertEqual(merged, {"https://example.com/old", "https://example.com/new"})
        self.assertEqual(only_today, {"https://example.com/new"})
        self.assertEqual(previous_days, {"https://example.com/old"})

    def test_load_seen_urls_allows_zero_lookback_for_quality_first_boards(self) -> None:
        with TemporaryDirectory() as tmpdir:
            archive = Path(tmpdir)
            archive.joinpath("2026-04-27.json").write_text(
                json.dumps({"urls": ["https://example.com/old"]}), encoding="utf-8"
            )

            with patch("fetch_feeds.ARCHIVE_DIR", archive):
                seen = load_seen_urls("2026-04-29", lookback_days=0, include_today=False)

        self.assertEqual(seen, set())

    def test_archive_urls_merges_with_existing(self) -> None:
        with TemporaryDirectory() as tmpdir:
            archive = Path(tmpdir)
            archive.joinpath("2026-04-29.json").write_text(
                json.dumps({"urls": ["https://example.com/a"]}), encoding="utf-8"
            )

            with patch("fetch_feeds.ARCHIVE_DIR", archive):
                archive_urls("2026-04-29", ["https://example.com/b", "https://example.com/a", ""])

            payload = json.loads(archive.joinpath("2026-04-29.json").read_text(encoding="utf-8"))

        self.assertEqual(payload["urls"], ["https://example.com/a", "https://example.com/b"])

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

    def test_security_opml_includes_domestic_vulnerability_sources(self) -> None:
        body = Path("feeds/security.opml").read_text(encoding="utf-8")

        for name in ("奇安信CERT", "绿盟科技CERT", "安全客", "先知社区"):
            self.assertIn(name, body)

    def test_security_opml_has_no_duplicate_wechat_feed_urls(self) -> None:
        import xml.etree.ElementTree as ET

        root = ET.parse("feeds/security.opml").getroot()
        urls = [
            node.get("xmlUrl")
            for node in root.findall(".//outline")
            if "wechat2rss.xlab.app" in (node.get("xmlUrl") or "")
        ]

        self.assertEqual(len(urls), len(set(urls)))

    def test_opml_includes_rsshub_x_signal_feeds(self) -> None:
        ai_feeds = fetch_opml("feeds/ai.opml")
        ai_security_feeds = fetch_opml("feeds/ai_security.opml")
        security_feeds = fetch_opml("feeds/security.opml")

        self.assertIn("XSignals", ai_feeds)
        self.assertIn("https://rsshub.app/twitter/user/OpenAI", ai_feeds["XSignals"])
        self.assertIn("https://rsshub.app/twitter/user/OpenAIDevs", ai_feeds["XSignals"])
        self.assertIn("https://rsshub.app/twitter/user/ClaudeDevs", ai_feeds["XSignals"])
        self.assertIn("https://rsshub.app/twitter/user/claudeai", ai_feeds["XSignals"])
        self.assertIn("https://rsshub.app/twitter/user/ChatGPTapp", ai_feeds["XSignals"])
        self.assertIn("https://rsshub.app/twitter/user/AnthropicAI", ai_feeds["XSignals"])
        self.assertIn("https://rsshub.app/twitter/user/dotey", ai_feeds["XSignals"])
        self.assertIn("https://rsshub.app/twitter/user/trq212", ai_feeds["XSignals"])
        self.assertIn("https://rsshub.app/twitter/user/bcherny", ai_feeds["XSignals"])
        self.assertIn("XSignals", ai_security_feeds)
        self.assertIn(
            "https://rsshub.app/twitter/user/EmbraceTheRed",
            ai_security_feeds["XSignals"],
        )
        self.assertIn("XSignals", security_feeds)
        self.assertIn("https://rsshub.app/twitter/user/IntCyberDigest", security_feeds["XSignals"])
        self.assertIn("https://rsshub.app/twitter/user/thsottiaux", security_feeds["XSignals"])

    def test_rsshub_base_url_can_be_overridden_for_private_instance(self) -> None:
        with patch.dict("os.environ", {"RSSHUB_BASE_URL": "https://rsshub.example.com/"}):
            feeds = fetch_opml("feeds/ai.opml")

        self.assertIn(
            "https://rsshub.example.com/twitter/user/OpenAI",
            feeds["XSignals"],
        )


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

    def test_template_searches_across_all_available_dates(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("allFeeds", template)
        self.assertIn("loadAllFeeds", template)
        self.assertIn("itemsForBoard", template)
        self.assertIn("searchQuery ? DATES : [currentDate]", template)

    def test_template_uses_distinctive_editorial_visual_direction(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("oai-shell", template)
        self.assertIn("oai-search", template)
        self.assertIn("Docs / Daily intelligence", template)
        self.assertIn("--surface", template)
        self.assertIn("OpenAI-inspired interface", template)
        self.assertNotIn("lg:text-8xl", template)
        self.assertNotIn("sm:text-7xl", template)
        self.assertIn("grid lg:grid-cols-[220px_minmax(0,1fr)]", template)
        self.assertNotIn("font-sans", template)


    def test_template_renders_source_tier_badge(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("sourceBadge", template)
        self.assertIn("source_tier", template)
        self.assertIn("source_kind", template)
        self.assertIn("source_label", template)


    def test_template_summarizes_source_mix_in_sidebar_meta(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("sourceMixLine", template)
        self.assertIn("tier_t1", template)
        self.assertIn("tier_unknown", template)

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

    def test_feed_json_preserves_digest_selection_stats(self) -> None:
        with TemporaryDirectory() as tmpdir:
            digest_dir = Path(tmpdir)
            digest_dir.joinpath("security_2026-04-30.json").write_text(
                json.dumps(
                    {
                        "board": "security",
                        "display_name": "安全",
                        "date": "2026-04-30",
                        "raw_count": 70,
                        "selected_count": 20,
                        "selection_stats": {
                            "total": 20,
                            "direct": 20,
                            "chinese": 2,
                            "above_threshold": 8,
                        },
                        "generated_at": "2026-04-30T00:00:00Z",
                        "items": [{"title_zh": "测试", "url": "https://example.com"}],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            with patch("site_builder.DIGEST_DIR", digest_dir):
                feed = _build_feed_for_date({"security": {"display_name": "安全"}}, date(2026, 4, 30))

        block = feed["boards"]["security"]
        self.assertEqual(block["selected_count"], 20)
        self.assertEqual(block["selection_stats"]["above_threshold"], 8)
        self.assertNotIn("chinese", block["selection_stats"])


    def test_feed_json_backfills_source_registry_metadata(self) -> None:
        with TemporaryDirectory() as tmpdir:
            digest_dir = Path(tmpdir)
            digest_dir.joinpath("security_2026-04-30.json").write_text(
                json.dumps(
                    {
                        "board": "security",
                        "display_name": "安全",
                        "date": "2026-04-30",
                        "raw_count": 1,
                        "selected_count": 1,
                        "generated_at": "2026-04-30T00:00:00Z",
                        "items": [{"title_zh": "CISA 通告", "url": "https://cisa.gov/news-events/alerts/x"}],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            with patch("site_builder.DIGEST_DIR", digest_dir):
                feed = _build_feed_for_date({"security": {"display_name": "安全"}}, date(2026, 4, 30))

        item = feed["boards"]["security"]["items"][0]
        self.assertEqual(item["source_tier"], "t1")
        self.assertEqual(item["source_kind"], "official")
        self.assertEqual(item["source_label"], "官方通告")


    def test_feed_json_recomputes_unknown_source_metadata_from_registry(self) -> None:
        with TemporaryDirectory() as tmpdir:
            digest_dir = Path(tmpdir)
            digest_dir.joinpath("security_2026-04-30.json").write_text(
                json.dumps(
                    {
                        "board": "security",
                        "display_name": "安全",
                        "date": "2026-04-30",
                        "raw_count": 1,
                        "selected_count": 1,
                        "selection_stats": {"total": 1, "tier_unknown": 1, "kind_media": 1},
                        "generated_at": "2026-04-30T00:00:00Z",
                        "items": [
                            {
                                "title_zh": "先知社区技术文章",
                                "url": "https://xz.aliyun.com/news/1",
                                "source_tier": "unknown",
                                "source_kind": "media",
                                "source_label": "未登记源",
                            }
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            with patch("site_builder.DIGEST_DIR", digest_dir):
                feed = _build_feed_for_date({"security": {"display_name": "安全"}}, date(2026, 4, 30))

        block = feed["boards"]["security"]
        item = block["items"][0]
        self.assertEqual(item["source_tier"], "t2")
        self.assertEqual(item["source_kind"], "cn_expert")
        self.assertEqual(item["source_label"], "中文安全")
        self.assertEqual(block["selection_stats"]["tier_t2"], 1)
        self.assertEqual(block["selection_stats"]["kind_cn_expert"], 1)
        self.assertNotIn("tier_unknown", block["selection_stats"])
        self.assertNotIn("kind_media", block["selection_stats"])

    def test_daily_workflow_supports_single_board_dispatch(self) -> None:
        workflow = Path(".github/workflows/daily.yml").read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("board:", workflow)
        self.assertIn("BOARD_SELECTION", workflow)
        self.assertIn("security ai_security ai finance", workflow)

    def test_daily_workflow_uses_pinned_requirements(self) -> None:
        workflow = Path(".github/workflows/daily.yml").read_text(encoding="utf-8")

        self.assertIn('cache: "pip"', workflow)
        self.assertIn("pip install -r requirements.txt", workflow)
        self.assertTrue(Path("requirements.txt").exists())

    def test_daily_workflow_can_start_ephemeral_rsshub(self) -> None:
        workflow = Path(".github/workflows/daily.yml").read_text(encoding="utf-8")

        self.assertIn("Start RSSHub for X signals", workflow)
        self.assertIn("TWITTER_AUTH_TOKEN", workflow)
        self.assertIn("diygod/rsshub:chromium-bundled", workflow)
        self.assertIn("RSSHUB_BASE_URL=http://127.0.0.1:1200", workflow)


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
                        "    dedup_lookback_days: 0",
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
                seen_mock = stack.enter_context(patch("fetch_and_save.load_seen_urls", return_value=set()))
                stack.enter_context(patch("fetch_and_save.archive_urls", return_value=root / "archive" / "stub.json"))
                stack.enter_context(patch("fetch_and_save.fetch_all_entries", side_effect=fake_fetch_all_entries))
                stack.enter_context(patch("fetch_and_save.filter_and_dedup", return_value=([filtered], {"input": 1, "output": 1})))
                stack.enter_context(patch("fetch_and_save.curate_entries", return_value=([filtered], {})))

                fetch_and_save.main()

            payload = json.loads(output_dir.joinpath("test_latest.json").read_text(encoding="utf-8"))

        self.assertEqual(payload["fetched_at"], "2026-04-28")
        self.assertEqual(payload["fetched_at_utc"], "2026-04-28T02:03:04Z")
        seen_mock.assert_called_once_with("2026-04-28", lookback_days=0, include_today=False)


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

    def test_source_profile_classifies_rsshub_x_signal_as_aggregator(self) -> None:
        profile = source_profile(
            {
                "title": "OpenAI ships a model update",
                "url": "https://x.com/OpenAI/status/123",
                "feed_url": "https://rsshub.app/twitter/user/OpenAI",
                "feed_title": "X / OpenAI",
                "category": "XSignals",
            }
        )

        self.assertTrue(profile.is_aggregator)
        self.assertFalse(profile.is_google_news)
        self.assertFalse(profile.is_direct)

    def test_source_profile_ignores_generated_chinese_summary_for_language_mix(self) -> None:
        profile = source_profile(
            {
                "title_zh": "OpenAI 发布模型更新",
                "title_orig": "OpenAI ships a model update",
                "summary": "这是一段由系统生成的中文摘要，不代表原始信源是中文。",
                "url": "https://openai.com/news/model-update",
                "source": "openai.com",
            }
        )

        self.assertFalse(profile.is_chinese)


    def test_source_profile_uses_registry_for_official_domain(self) -> None:
        profile = source_profile({"title": "OpenAI update", "url": "https://openai.com/news/update"})

        self.assertEqual(profile.source_tier, "t1")
        self.assertEqual(profile.source_kind, "official")
        self.assertEqual(profile.source_label, "官网")

    def test_source_profile_uses_registry_for_rsshub_x_handle(self) -> None:
        profile = source_profile(
            {
                "title": "OpenAI ships a model update",
                "url": "https://x.com/OpenAIDevs/status/123",
                "feed_url": "https://rsshub.app/twitter/user/OpenAIDevs",
                "feed_title": "X / OpenAIDevs",
                "category": "XSignals",
            }
        )

        self.assertEqual(profile.source_tier, "t1_5")
        self.assertEqual(profile.source_kind, "official_x")
        self.assertEqual(profile.source_label, "官方 X")

    def test_wechat_source_key_uses_feed_url_not_shared_host(self) -> None:
        first = source_profile(
            {
                "title": "漏洞分析",
                "url": "https://mp.weixin.qq.com/s/a",
                "feed_url": "https://wechat2rss.xlab.app/feed/source-a.xml",
            }
        )
        second = source_profile(
            {
                "title": "安全通告",
                "url": "https://mp.weixin.qq.com/s/b",
                "feed_url": "https://wechat2rss.xlab.app/feed/source-b.xml",
            }
        )

        self.assertNotEqual(first.source_key, second.source_key)
        self.assertIn("source-a", first.source_key)


    def test_source_mix_stats_includes_registry_distribution(self) -> None:
        stats = source_mix_stats([
            {"title": "OpenAI", "url": "https://openai.com/news/a"},
            {"title": "中文安全", "url": "https://xz.aliyun.com/news/1"},
            {"title": "Google", "url": "https://news.google.com/rss/articles/1"},
        ])

        self.assertEqual(stats["tier_t1"], 1)
        self.assertEqual(stats["tier_t2"], 2)
        self.assertEqual(stats["kind_official"], 1)
        self.assertEqual(stats["kind_cn_expert"], 1)
        self.assertEqual(stats["kind_google_news"], 1)

    def test_selection_policy_caps_google_news_and_reserves_chinese(self) -> None:
        candidates = [
            ({"title": "Google 1", "url": "https://news.google.com/rss/articles/1"}, 10),
            ({"title": "Google 2", "url": "https://news.google.com/rss/articles/2"}, 9),
            ({"title": "Direct 1", "url": "https://openai.com/news/a"}, 8),
            ({"title": "Direct 2", "url": "https://labs.example.com/news/b"}, 7),
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


    def test_digest_item_includes_source_registry_metadata(self) -> None:
        item = _finalize_digest_item(
            {
                "title": "OpenAI releases important model update",
                "summary": "OpenAI releases important model update for developers.",
                "url": "https://openai.com/news/update",
                "category": "Labs",
                "published": "2026-05-09T00:00:00Z",
            },
            {
                "title_zh": "OpenAI发布重要模型更新",
                "summary": "OpenAI发布重要模型更新，面向开发者提供新的能力和使用方式。这条资讯来自官方来源，适合关注模型能力、产品节奏和生态变化的读者继续查看原文。",
                "tags": ["模型发布"],
                "url": "https://openai.com/news/update",
                "selection_reason": "官方发布",
            },
        )

        self.assertEqual(item["source_tier"], "t1")
        self.assertEqual(item["source_kind"], "official")
        self.assertEqual(item["source_label"], "官网")

    def test_score_prompts_include_language_fairness(self) -> None:
        for prompt in BOARD_SCORE_SYSTEM.values():
            self.assertRegex(prompt, r"评分只看(新闻|技术)价值")
            self.assertIn("不因语言", prompt)

    def test_security_prompt_prioritizes_cn_vuln_mechanics_and_deprioritizes_geo_attribution(self) -> None:
        prompt = BOARD_SCORE_SYSTEM["security"]

        self.assertIn("中文漏洞分析", prompt)
        self.assertIn("漏洞原理", prompt)
        self.assertIn("地缘归因", prompt)
        self.assertIn("上限 4", prompt)

    def test_security_editorial_caps_geopolitical_attribution(self) -> None:
        entry = {
            "title": "New Wave of DPRK Attacks Uses AI-Inserted npm Malware",
            "summary": "North Korea hackers used AI-generated packages in a campaign.",
        }

        self.assertEqual(adjust_security_score(entry, 9), 4)

    def test_security_config_targets_chinese_technical_sources(self) -> None:
        import yaml

        security = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))["boards"]["security"]

        self.assertEqual(security["top_n"], 15)
        self.assertGreaterEqual(security["fetch_hours"], 36)
        self.assertGreaterEqual(security["llm_max_entries"], 100)
        self.assertEqual(security["source_policy"]["min_chinese"], 6)
        self.assertEqual(security["source_policy"]["min_direct"], 12)
        self.assertLessEqual(security["source_policy"]["max_google_news"], 1)
        self.assertEqual(security["source_policy"]["max_aggregator"], 7)
        self.assertNotIn("mp.weixin.qq.com", security.get("source_caps") or {})

    def test_ai_security_board_is_cost_bounded_and_direct_source_first(self) -> None:
        import yaml

        boards = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))["boards"]
        board = boards["ai_security"]

        self.assertEqual(board["top_n"], 10)
        self.assertLessEqual(board["llm_max_entries"], 60)
        self.assertLessEqual(board["source_policy"]["max_google_news"], 2)
        self.assertGreaterEqual(board["source_policy"]["min_direct"], 4)
        self.assertEqual(board["source_policy"]["max_aggregator"], 5)
        self.assertTrue(Path(board["opml"]).exists())

    def test_board_output_targets_match_current_editorial_policy(self) -> None:
        import yaml

        boards = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))["boards"]

        self.assertEqual(boards["security"]["top_n"], 15)
        self.assertEqual(boards["security"]["source_policy"]["min_chinese"], 6)
        self.assertEqual(boards["ai_security"]["top_n"], 10)
        self.assertEqual(boards["ai"]["top_n"], 15)
        self.assertEqual(boards["ai"]["source_policy"]["min_chinese"], 5)
        self.assertEqual(boards["finance"]["top_n"], 10)
        self.assertEqual(boards["ai"]["source_policy"]["max_aggregator"], 7)

    def test_gemini_prompts_encode_current_board_targets(self) -> None:
        self.assertIn("每日 15 条", BOARD_SCORE_SYSTEM["security"])
        self.assertIn("至少 6 条", BOARD_SCORE_SYSTEM["security"])
        self.assertIn("每日 10 条", BOARD_SCORE_SYSTEM["ai_security"])
        self.assertIn("每日 15 条", BOARD_SCORE_SYSTEM["ai"])
        self.assertIn("至少 5 条中文", BOARD_SCORE_SYSTEM["ai"])
        self.assertIn("每日 10 条", BOARD_SCORE_SYSTEM["finance"])
        self.assertIn("Google News 只做补充", BOARD_SCORE_SYSTEM["security"])
        self.assertIn("优先于 Google News", BOARD_SCORE_SYSTEM["ai"])
        self.assertIn("顶级开发者 X 动态", BOARD_SCORE_SYSTEM["ai"])
        self.assertIn("顶级安全研究者 X 动态", BOARD_SCORE_SYSTEM["ai_security"])

    def test_digest_pipeline_accepts_dynamic_board_names(self) -> None:
        body = Path("digest_pipeline_gemini.py").read_text(encoding="utf-8")
        self.assertNotIn('choices=["security", "ai", "finance"]', body)
        self.assertIn('parser.add_argument("--board", required=True)', body)

    def test_legacy_digest_entrypoint_delegates_to_current_pipeline(self) -> None:
        body = Path("digest_pipeline.py").read_text(encoding="utf-8")
        self.assertIn("from digest_pipeline_gemini import main, run", body)
        self.assertNotIn("ANTHROPIC" + "_API_KEY", body)
        self.assertNotIn("".join(["ant", "hropic"]), body.lower())

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

    def test_finalize_digest_item_does_not_truncate_complete_chinese_title(self) -> None:
        title = "GitHub Copilot将根据用户实际AI使用量调整计费方式"
        entry = {
            "title": "GitHub will start charging Copilot users based on their actual AI usage",
            "summary": "GitHub will start charging Copilot users based on their actual AI usage.",
            "url": "https://example.com/copilot",
            "category": "Labs",
            "published": "2026-04-30T00:00:00Z",
        }
        item = {
            "title_zh": title,
            "summary": "GitHub宣布将根据Copilot用户的实际AI使用量调整计费方式，这意味着相关服务的成本将更直接地与调用规模挂钩。该变化值得企业和开发团队关注，因为它可能影响日常开发工具预算、团队席位管理和AI辅助编码的使用策略。",
            "tags": ["开发工具"],
            "selection_reason": "计费变化影响开发者",
        }

        finalized = _finalize_digest_item(entry, item)

        self.assertEqual(finalized["title_zh"], title)

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

    def test_weekly_review_flags_silent_and_low_quality_feeds(self) -> None:
        with TemporaryDirectory() as tmpdir:
            reports = Path(tmpdir)
            base = date(2026, 4, 24)
            for offset in range(7):
                day = (base - timedelta(days=offset)).isoformat()
                reports.joinpath(f"ai_{day}.md").write_text(
                    f"# AI 前沿 源质量报表 {day}\n", encoding="utf-8"
                )
                payload = {
                    "board": "ai",
                    "date": day,
                    "feeds": {
                        "https://feeds.example.com/silent": {
                            "feed_title": "Silent Feed",
                            "category": "Chinese",
                            "attempted": 1,
                            "succeeded": 1,
                            "raw_count": 0,
                            "filtered_count": 0,
                            "avg_score": None,
                            "selected": 0,
                        },
                        "https://feeds.example.com/junk": {
                            "feed_title": "Noisy Junk",
                            "category": "Media",
                            "attempted": 1,
                            "succeeded": 1,
                            "raw_count": 4,
                            "filtered_count": 4,
                            "avg_score": 2.0,
                            "selected": 0,
                        },
                        "https://feeds.example.com/good": {
                            "feed_title": "Good Source",
                            "category": "Labs",
                            "attempted": 1,
                            "succeeded": 1,
                            "raw_count": 2,
                            "filtered_count": 2,
                            "avg_score": 8.0,
                            "selected": 2,
                        },
                    },
                }
                reports.joinpath(f"ai_{day}.json").write_text(
                    json.dumps(payload, ensure_ascii=False), encoding="utf-8"
                )

            refresh_weekly_report(base, ["ai"], reports_dir=reports)
            body = (reports / "weekly.md").read_text(encoding="utf-8")

        self.assertIn("⚠️ 建议人工 review", body)
        self.assertIn("Silent Feed", body)
        self.assertIn("Noisy Junk", body)
        self.assertNotIn("Good Source", body.split("⚠️")[1])

    def test_workflow_no_longer_exposes_removed_llm_channel(self) -> None:
        body = Path(".github/workflows/daily.yml").read_text(encoding="utf-8")

        self.assertNotIn("ANTHROPIC" + "_API_KEY", body)
        self.assertNotIn('LLM_BACKEND" = "' + "".join(["ant", "hropic"]) + '"', body)
        self.assertIn("DEEPSEEK_API_KEY", body)
        self.assertIn("deepseek-v4-flash", body)


class LLMBackendTests(unittest.TestCase):
    def test_default_backend_name_is_gemini(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(backend_name_from_env(), "gemini")

    def test_deepseek_backend_requires_key_when_explicitly_enabled(self) -> None:
        with patch.dict("os.environ", {"LLM_BACKEND": "deepseek"}, clear=True):
            with self.assertRaises(SystemExit) as cm:
                get_backend()

        self.assertIn("DEEPSEEK_API_KEY", str(cm.exception))

    def test_deepseek_backend_uses_non_deprecated_default_model(self) -> None:
        from llm_backends.deepseek import DEPRECATED_MODELS, DeepSeekBackend

        with patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-key"}, clear=True):
            backend = DeepSeekBackend.from_env()

        self.assertEqual(backend.score_model, "deepseek-v4-flash")
        self.assertNotIn(backend.score_model, DEPRECATED_MODELS)

    def test_deepseek_backend_rejects_deprecated_model_names(self) -> None:
        from llm_backends.deepseek import DeepSeekBackend

        with patch.dict(
            "os.environ",
            {"DEEPSEEK_API_KEY": "test-key", "DEEPSEEK_MODEL": "deepseek-chat"},
            clear=True,
        ):
            with self.assertRaises(SystemExit) as cm:
                DeepSeekBackend.from_env()

        self.assertIn("deprecated", str(cm.exception))

    def test_deepseek_backend_generate_json_uses_openai_compatible_endpoint(self) -> None:
        from llm_backends.deepseek import DeepSeekBackend

        calls = []

        class FakeResponse:
            def raise_for_status(self) -> None:
                return None

            def json(self) -> dict:
                return {"choices": [{"message": {"content": "[{\"idx\":0,\"score\":8}]"}}]}

        class FakeClient:
            def __init__(self, timeout: int) -> None:
                self.timeout = timeout

            def __enter__(self) -> "FakeClient":
                return self

            def __exit__(self, *_exc: object) -> None:
                return None

            def post(self, url: str, *, headers: dict, json: dict) -> FakeResponse:
                calls.append((url, headers, json))
                return FakeResponse()

        backend = DeepSeekBackend(api_key="test-key", base_url="https://deepseek.example")
        with patch("llm_backends.deepseek.httpx.Client", FakeClient):
            text = backend.generate_json("deepseek-v4-flash", "system", "user", 128)

        self.assertEqual(text, '[{"idx":0,"score":8}]')
        url, headers, payload = calls[0]
        self.assertEqual(url, "https://deepseek.example/chat/completions")
        self.assertEqual(headers["Authorization"], "Bearer test-key")
        self.assertEqual(payload["model"], "deepseek-v4-flash")
        self.assertEqual(payload["messages"][0]["role"], "system")


class SourceAuditTests(unittest.TestCase):
    def test_source_audit_summarizes_coverage_and_unknown_sources(self) -> None:
        feed = {
            "date": "2026-05-11",
            "boards": {
                "security": {
                    "items": [
                        {
                            "title_zh": "官方漏洞通告",
                            "url": "https://cisa.gov/news",
                            "source": "cisa.gov",
                            "source_tier": "t1",
                            "source_kind": "official",
                            "source_label": "官方通告",
                        },
                        {
                            "title_zh": "未登记安全文章",
                            "url": "https://unknown.example/post",
                            "source": "unknown.example",
                            "source_tier": "unknown",
                            "source_kind": "media",
                            "source_label": "未登记源",
                        },
                    ]
                },
                "ai": {
                    "items": [
                        {
                            "title_zh": "开发者 X 动态",
                            "url": "https://x.com/OpenAIDevs/status/1",
                            "source": "OpenAIDevs / X",
                            "source_tier": "t1_5",
                            "source_kind": "official_x",
                            "source_label": "官方 X",
                        }
                    ]
                },
            },
        }

        markdown = render_source_audit([feed])

        self.assertIn("| ai | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |", markdown)
        self.assertIn("| security | 2 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 |", markdown)
        self.assertIn("| `unknown.example` | 1 | security |", markdown)
        self.assertIn("[未登记安全文章](https://unknown.example/post)", markdown)

    def test_build_source_audit_writes_recent_feed_report(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            reports = root / "reports"
            docs.mkdir()
            docs.joinpath("feed_2026-05-10.json").write_text(
                json.dumps(
                    {
                        "date": "2026-05-10",
                        "boards": {
                            "finance": {
                                "items": [
                                    {
                                        "title_zh": "支付网络公告",
                                        "url": "https://visa.com/a",
                                        "source": "visa.com",
                                        "source_tier": "t1",
                                        "source_kind": "official",
                                        "source_label": "官网",
                                    }
                                ]
                            }
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            out = build_source_audit(docs_dir=docs, reports_dir=reports, lookback_days=7)
            body = out.read_text(encoding="utf-8")

        self.assertEqual(out, reports / "source_audit.md")
        self.assertIn("| finance | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |", body)
        self.assertIn("No unknown selected sources", body)


class OfflineEvalTests(unittest.TestCase):
    def test_offline_eval_reports_board_targets_and_misses(self) -> None:
        feeds = [
            {
                "date": "2026-05-11",
                "boards": {
                    "security": {
                        "items": [
                            {
                                "title_zh": "中文安全漏洞",
                                "url": "https://xz.aliyun.com/a",
                                "source_tier": "t2",
                                "source_kind": "cn_expert",
                            },
                            {
                                "title_zh": "Google 转述",
                                "url": "https://news.google.com/rss/articles/1",
                                "source_tier": "t2",
                                "source_kind": "google_news",
                            },
                            {
                                "title_zh": "未登记源",
                                "url": "https://unknown.example/a",
                                "source_tier": "unknown",
                                "source_kind": "media",
                            },
                        ],
                        "selection_stats": {
                            "total": 3,
                            "chinese": 1,
                            "google_news": 1,
                            "tier_unknown": 1,
                            "tier_t2": 2,
                            "kind_cn_expert": 1,
                            "kind_google_news": 1,
                        },
                    }
                },
            }
        ]
        cfg = {
            "boards": {
                "security": {
                    "display_name": "安全",
                    "top_n": 15,
                    "source_policy": {"min_chinese": 6, "max_google_news": 1},
                }
            }
        }

        markdown = render_offline_eval(feeds, cfg)

        self.assertIn("| security | 安全 | 1 | 3.0 | 15 | 0/1 | 1.0 | 6 | 0/1 | 1.0 | 1 | 1 |", markdown)
        self.assertIn("2026-05-11 security：selected 3/15，中文 1/6，unknown 1", markdown)

    def test_build_offline_eval_writes_report_from_docs_feeds(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            reports = root / "reports"
            docs.mkdir()
            docs.joinpath("feed_2026-05-11.json").write_text(
                json.dumps(
                    {
                        "date": "2026-05-11",
                        "boards": {
                            "ai": {
                                "items": [
                                    {
                                        "title_zh": "OpenAI 发布",
                                        "url": "https://openai.com/news/a",
                                        "source_tier": "t1",
                                        "source_kind": "official",
                                    }
                                ],
                                "selection_stats": {
                                    "total": 1,
                                    "tier_t1": 1,
                                    "kind_official": 1,
                                },
                            }
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            cfg_path = root / "config.yaml"
            cfg_path.write_text(
                "boards:\n  ai:\n    display_name: AI 前沿\n    top_n: 15\n    source_policy:\n      min_chinese: 5\n",
                encoding="utf-8",
            )

            out = build_offline_eval(
                docs_dir=docs,
                reports_dir=reports,
                config_path=cfg_path,
                lookback_days=7,
            )
            body = out.read_text(encoding="utf-8")

        self.assertEqual(out, reports / "offline_eval.md")
        self.assertIn("| ai | AI 前沿 | 1 | 1.0 | 15 | 0/1 |", body)


class AIHotCompareTests(unittest.TestCase):
    def test_aihot_compare_matches_by_url_and_lists_missing_items(self) -> None:
        aihot_items = [
            {
                "title": "OpenAI 发布新模型",
                "url": "https://openai.com/news/model",
                "source": "OpenAI",
                "summary": "OpenAI 发布新模型。",
                "publishedAt": "2026-05-11T00:00:00Z",
            },
            {
                "title": "Cerebras IPO 获超额认购",
                "url": "https://example.com/cerebras",
                "source": "IT之家",
                "summary": "AI 芯片企业 IPO。",
                "publishedAt": "2026-05-11T01:00:00Z",
            },
        ]
        ours_feed = {
            "date": "2026-05-11",
            "boards": {
                "ai": {
                    "items": [
                        {
                            "title_zh": "OpenAI 发布新模型",
                            "url": "https://openai.com/news/model",
                            "source": "openai.com",
                        }
                    ]
                },
                "ai_security": {"items": []},
            },
        }

        comparison = compare_aihot_items(aihot_items, ours_feed)

        self.assertEqual(comparison["aihot_count"], 2)
        self.assertEqual(comparison["ours_count"], 1)
        self.assertEqual(len(comparison["matched"]), 1)
        self.assertEqual(comparison["aihot_only"][0]["title"], "Cerebras IPO 获超额认购")

    def test_aihot_compare_does_not_match_unrelated_chinese_ai_items(self) -> None:
        aihot_items = [
            {
                "title": "Cerebras IPO 获超额认购",
                "url": "https://example.com/cerebras",
                "source": "IT之家",
                "summary": "AI 芯片企业 IPO。",
            }
        ]
        ours_feed = {
            "date": "2026-05-11",
            "boards": {
                "ai": {
                    "items": [
                        {
                            "title_zh": "xAI 与 Cursor 达成 100 亿美元合作协议",
                            "url": "https://news.google.com/rss/articles/cursor",
                            "source": "news.google.com",
                            "summary": "AI 编程工具合作。",
                        }
                    ]
                },
                "ai_security": {"items": []},
            },
        }

        comparison = compare_aihot_items(aihot_items, ours_feed)

        self.assertEqual(comparison["matched"], [])
        self.assertEqual(len(comparison["aihot_only"]), 1)
        self.assertEqual(len(comparison["ours_only"]), 1)

    def test_aihot_compare_requires_more_than_shared_product_name(self) -> None:
        comparison = compare_aihot_items(
            [
                {
                    "title": "Claude Code实践：HTML输出格式的卓越效果",
                    "url": "https://example.com/claude-code-html",
                    "summary": "Claude Code 在 HTML 输出上效果很好。",
                }
            ],
            {
                "date": "2026-05-11",
                "boards": {
                    "ai": {
                        "items": [
                            {
                                "title_zh": "Claude Code 负责人称 AI 智能体正开启印刷术时刻",
                                "url": "https://example.com/claude-code-lead",
                                "summary": "Claude Code 负责人讨论编程普及。",
                            }
                        ]
                    },
                    "ai_security": {"items": []},
                },
            },
        )

        self.assertEqual(comparison["matched"], [])

    def test_render_aihot_compare_outputs_markdown_summary(self) -> None:
        markdown = render_aihot_compare(
            {
                "date": "2026-05-11",
                "aihot_count": 1,
                "ours_count": 1,
                "matched": [{"title": "OpenAI 发布新模型", "ours_title": "OpenAI 发布新模型"}],
                "aihot_only": [
                    {
                        "title": "Cerebras IPO 获超额认购",
                        "source": "IT之家",
                        "url": "https://example.com/cerebras",
                        "summary": "AI 芯片企业 IPO。",
                    }
                ],
                "ours_only": [],
            }
        )

        self.assertIn("# AIHOT External Benchmark", markdown)
        self.assertIn("Overlap: 1", markdown)
        self.assertIn("Cerebras IPO 获超额认购", markdown)


class DigestClockTests(unittest.TestCase):
    def test_digest_today_honors_env_override(self) -> None:
        with patch.dict("os.environ", {"DIGEST_DATE": "2026-04-25"}):
            self.assertEqual(digest_today(), date(2026, 4, 25))


if __name__ == "__main__":
    unittest.main()
