import json
import sys
import unittest
from contextlib import ExitStack
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from digest_clock import digest_today
from delivered_history import DeliveredHistory, filter_delivered_candidates, load_delivered_history
from digest_postprocess import count_chinese_chars, summary_needs_repair
from aihot_compare import compare_aihot_items, parse_aihot_rss_items, render_aihot_compare
from llm_backends.base import backend_name_from_env, get_backend
from eval_strategy import build_offline_eval, render_offline_eval
from digest_pipeline_gemini import (
    BOARD_SCORE_SYSTEM,
    _attach_final_scores,
    _candidate_pool,
    _finalize_digest_item,
    _is_chinese_entry,
    _llm_dedupe,
    _score_entries,
    _score_candidates_for_selection,
    _selection_reason,
    _sanitize_vulnerability_claims,
)
import fetch_and_save
import fetch_feeds
from fetch_feeds import FeedEntry, archive_urls, fetch_all_entries, load_seen_urls
from fetch_opml import fetch_opml, fetch_opml_metadata
from filter_entries import FilteredEntry, filter_and_dedup
from feedback_cli import add_feedback, import_feedback_file
from feedback_eval import build_report, classify_feedback, sync_weekly_feedback
from rss_curation import curate_entries
from source_policy import select_with_source_policy, source_mix_stats, source_profile
from scoring_policy import compute_dimension_score, compute_final_score
from security_editorial import adjust_ai_security_score, adjust_finance_score, adjust_security_score
from story_clustering import cluster_scored_candidates, story_id_for_entry
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

    async def test_max_per_feed_prevents_firehose_crowding_out_category(self) -> None:
        if fetch_feeds.httpx is None:
            self.skipTest("httpx is not installed in this Python environment")

        # firehose posts 4 newest entries; quiet feed posted 2 older ones.
        # Without per-feed cap, category cap 4 newest-first would select only
        # firehose entries. With max_per_feed=2 the quiet feed survives.
        feeds = {"security": ["firehose", "quiet"]}
        base = datetime(2026, 4, 22, tzinfo=timezone.utc)
        results = {
            "firehose": [
                FeedEntry(f"fh-{i}", f"https://fh/{i}", "summary text long enough", "", base.replace(hour=10 + i))
                for i in range(4)
            ],
            "quiet": [
                FeedEntry("q-1", "https://q/1", "summary text long enough", "", base.replace(hour=1)),
                FeedEntry("q-2", "https://q/2", "summary text long enough", "", base.replace(hour=2)),
            ],
        }

        async def fake_fetch(_semaphore, _client, url):
            return results[url]

        with patch("fetch_feeds._fetch_one_bounded", side_effect=fake_fetch):
            entries, _health = await fetch_all_entries(
                feeds,
                hours=9999,
                max_per_category=4,
                max_per_feed=2,
            )

        titles = {entry.title for entry in entries}
        # firehose keeps its 2 newest; quiet keeps both of its entries
        self.assertEqual(titles, {"fh-3", "fh-2", "q-1", "q-2"})

    async def test_future_dated_feed_entries_are_ignored(self) -> None:
        if fetch_feeds.httpx is None:
            self.skipTest("httpx is not installed in this Python environment")

        now = datetime.now(timezone.utc)
        feeds = {"security": ["feed-a"]}
        results = {
            "feed-a": [
                FeedEntry("valid", "https://a/valid", "summary text long enough", "", now),
                FeedEntry(
                    "future",
                    "https://a/future",
                    "summary text long enough",
                    "",
                    now + timedelta(days=365),
                ),
            ],
        }

        async def fake_fetch(_semaphore, _client, url):
            return results[url]

        with patch("fetch_feeds._fetch_one_bounded", side_effect=fake_fetch):
            entries, _health = await fetch_all_entries(feeds, hours=24, max_per_category=10)

        self.assertEqual([entry.url for entry in entries], ["https://a/valid"])


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

        for name in ("奇安信CERT", "绿盟科技CERT", "安全客", "先知社区", "跳跳糖", "360 Netlab Blog"):
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

    def test_security_opml_excludes_future_dated_legacy_blog_source(self) -> None:
        body = Path("feeds/security.opml").read_text(encoding="utf-8")

        self.assertNotIn("micropoor.blogspot.com", body)
        self.assertNotIn("qbitai.com/feed", body)

    def test_opml_excludes_weekly_low_quality_sources_from_wrong_boards(self) -> None:
        security = Path("feeds/security.opml").read_text(encoding="utf-8")
        ai_security = Path("feeds/ai_security.opml").read_text(encoding="utf-8")

        for text in (
            "Kali Linux Tutorials",
            "Daring Fireball",
            "Wired",
            "The Decoder",
            "PromptLayer",
            "代码审计星球",
            "美团技术团队",
            "青衣十三楼飞花堂",
            "体验盒子",
        ):
            self.assertNotIn(text, security)
        self.assertIn("Simon Willison", ai_security)
        self.assertNotIn("X / Simon Willison", ai_security)

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

    def test_ai_security_opml_includes_extra_direct_security_sources(self) -> None:
        ai_security_feeds = fetch_opml("feeds/ai_security.opml")
        flat = {url for urls in ai_security_feeds.values() for url in urls}

        self.assertIn("https://www.hiddenlayer.com/feed", flat)
        self.assertIn("https://github.blog/security/vulnerability-research/feed/", flat)
        self.assertIn("https://www.legitsecurity.com/blog/rss.xml", flat)
        self.assertIn("https://www.endorlabs.com/learn/rss.xml", flat)
        self.assertIn("https://paper.seebug.org/rss/", flat)
        self.assertIn("https://wechat2rss.xlab.app/feed/ac86a71f04b6d10cc5a87ec9ecc8c94fff5d80d1.xml", flat)
        self.assertTrue(any("AI+supply+chain" in url for url in flat))

    def test_rsshub_base_url_can_be_overridden_for_private_instance(self) -> None:
        with patch.dict("os.environ", {"RSSHUB_BASE_URL": "https://rsshub.example.com/"}):
            feeds = fetch_opml("feeds/ai.opml")

        self.assertIn(
            "https://rsshub.example.com/twitter/user/OpenAI",
            feeds["XSignals"],
        )


class UrlHygieneTests(unittest.TestCase):
    def test_is_public_http_url_rejects_local_addresses(self) -> None:
        from url_hygiene import is_public_http_url

        bad = [
            "http://0.0.0.0:8080/post/64413",
            "http://127.0.0.1/x",
            "http://localhost:3000/a",
            "http://10.1.2.3/internal",
            "http://172.16.0.9/x",
            "http://172.31.255.1/x",
            "http://192.168.1.5/router",
            "http://100.64.0.1/cgnat",
            "http://169.254.1.1/link-local",
            "http://224.0.0.1/multicast",
            "http://[::1]/v6",
            "ftp://example.com/file",
            "",
        ]
        for url in bad:
            self.assertFalse(is_public_http_url(url), url)

        good = [
            "https://hackernews.cc/post/64413",
            "http://example.com/a?b=1",
            "https://172.32.0.1/not-private",
        ]
        for url in good:
            self.assertTrue(is_public_http_url(url), url)

    def test_repair_entry_url_rewrites_nonroutable_to_feed_host(self) -> None:
        from url_hygiene import repair_entry_url

        fixed = repair_entry_url("http://0.0.0.0:8080/post/64413", "http://hackernews.cc/feed")
        self.assertEqual(fixed, "https://hackernews.cc/post/64413")

        # Public link untouched.
        self.assertEqual(
            repair_entry_url("https://example.com/a", "http://hackernews.cc/feed"),
            "https://example.com/a",
        )
        # Feed host itself non-public: no rewrite possible.
        self.assertEqual(
            repair_entry_url("http://0.0.0.0:8080/x", "http://127.0.0.1/feed"),
            "http://0.0.0.0:8080/x",
        )
        # Query string preserved.
        self.assertEqual(
            repair_entry_url("http://0.0.0.0:8080/p?id=7", "https://hackernews.cc/feed"),
            "https://hackernews.cc/p?id=7",
        )

    def test_filter_drops_nonpublic_urls(self) -> None:
        entry = FeedEntry(
            title="CVE-2026-9999 broken link entry",
            url="http://0.0.0.0:8080/post/1",
            summary="A" * 80,
            category="security",
            published=datetime(2026, 7, 1, 1, tzinfo=timezone.utc),
        )

        kept, stats = filter_and_dedup([entry])

        self.assertEqual(kept, [])
        self.assertEqual(stats.get("dropped_nonpublic_url"), 1)


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

        self.assertIn("ic-shell", template)
        self.assertIn("ic-search", template)
        self.assertIn("--surface", template)
        self.assertNotIn("lg:text-8xl", template)
        self.assertNotIn("sm:text-7xl", template)
        self.assertIn("grid lg:grid-cols-[220px_minmax(0,1fr)]", template)
        self.assertNotIn("font-sans", template)

    def test_template_drops_borrowed_openai_identity(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertNotIn("OpenAI-inspired interface", template)
        self.assertNotIn("Docs / Daily intelligence", template)
        self.assertNotIn("oai-shell", template)
        self.assertNotIn("https://openai.com/", template)
        # Self-owned identity: inline favicon + wordmark mark.
        self.assertIn('rel="icon"', template)
        self.assertIn("ic-mark", template)

    def test_template_renders_score_driven_hierarchy(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("renderHeroCard", template)
        self.assertIn("final_score", template)
        self.assertIn("ic-hero", template)
        self.assertIn("scoreBadge", template)

    def test_template_exposes_cluster_and_reason_signals(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("related_urls", template)
        self.assertIn("related_count", template)
        self.assertIn("relatedToggle", template)
        self.assertIn("selection_reason", template)

    def test_template_supports_local_quality_feedback_export(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("feedbackButton", template)
        self.assertIn("feedback-export", template)
        self.assertIn("application/x-ndjson", template)
        self.assertIn("bad_summary", template)

    def test_template_renders_timeline_layout(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("ic-tl-time", template)
        self.assertIn("ic-tl-rail", template)
        self.assertIn("ic-tl-dot", template)
        self.assertIn("renderTimelineItem", template)
        # Non-hero items sort chronologically inside the single-date view.
        self.assertIn("sortByPublishedDesc", template)

    def test_template_tiers_scores(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("scoreTier", template)
        self.assertIn("data-tier", template)
        self.assertIn('score-chip[data-tier="high"]', template)
        self.assertIn('score-chip[data-tier="mid"]', template)

    def test_template_supports_local_star(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("starButton", template)
        self.assertIn("localStorage", template)
        self.assertIn("starredOnly", template)
        self.assertIn("starKey", template)

    def test_template_reason_uses_labeled_divider(self) -> None:
        template = Path("templates/index.html.j2").read_text(encoding="utf-8")

        self.assertIn("ic-reason-label", template)
        self.assertIn("入选理由", template)

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
                        "delivered_filter_stats": {"input": 28, "kept": 20, "filtered": 8},
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
        self.assertEqual(block["delivered_filter_stats"]["filtered"], 8)
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

    def test_feed_json_sorts_items_by_attention_score_then_source_tier(self) -> None:
        with TemporaryDirectory() as tmpdir:
            digest_dir = Path(tmpdir)
            digest_dir.joinpath("ai_2026-05-11.json").write_text(
                json.dumps(
                    {
                        "board": "ai",
                        "display_name": "AI 前沿",
                        "date": "2026-05-11",
                        "raw_count": 3,
                        "selected_count": 3,
                        "generated_at": "2026-05-11T00:00:00Z",
                        "items": [
                            {
                                "title_zh": "低分 T1",
                                "url": "https://openai.com/news/low",
                                "final_score": 6.0,
                            },
                            {
                                "title_zh": "高分 T2",
                                "url": "https://simonwillison.net/2026/high",
                                "final_score": 8.5,
                            },
                            {
                                "title_zh": "同分 T1",
                                "url": "https://deepmind.google/blog/tie",
                                "final_score": 8.5,
                            },
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            with patch("site_builder.DIGEST_DIR", digest_dir):
                feed = _build_feed_for_date({"ai": {"display_name": "AI 前沿"}}, date(2026, 5, 11))

        titles = [item["title_zh"] for item in feed["boards"]["ai"]["items"]]
        self.assertEqual(titles, ["同分 T1", "高分 T2", "低分 T1"])

    def test_feed_json_sorts_items_by_source_tier_when_scores_missing(self) -> None:
        with TemporaryDirectory() as tmpdir:
            digest_dir = Path(tmpdir)
            digest_dir.joinpath("security_2026-05-11.json").write_text(
                json.dumps(
                    {
                        "board": "security",
                        "display_name": "安全",
                        "date": "2026-05-11",
                        "raw_count": 3,
                        "selected_count": 3,
                        "generated_at": "2026-05-11T00:00:00Z",
                        "items": [
                            {"title_zh": "未登记", "url": "https://unknown.example/a"},
                            {"title_zh": "T2 媒体", "url": "https://techcrunch.com/a"},
                            {"title_zh": "T1 官方", "url": "https://cisa.gov/news-events/alerts/a"},
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            with patch("site_builder.DIGEST_DIR", digest_dir):
                feed = _build_feed_for_date({"security": {"display_name": "安全"}}, date(2026, 5, 11))

        titles = [item["title_zh"] for item in feed["boards"]["security"]["items"]]
        self.assertEqual(titles, ["T1 官方", "T2 媒体", "未登记"])

    def test_feed_json_preserves_xsignals_as_aggregator(self) -> None:
        with TemporaryDirectory() as tmpdir:
            digest_dir = Path(tmpdir)
            digest_dir.joinpath("ai_2026-05-11.json").write_text(
                json.dumps(
                    {
                        "board": "ai",
                        "display_name": "AI 前沿",
                        "date": "2026-05-11",
                        "raw_count": 1,
                        "selected_count": 1,
                        "selection_stats": {"total": 1, "aggregator": 1, "kind_expert_x": 1},
                        "generated_at": "2026-05-11T00:00:00Z",
                        "items": [
                            {
                                "title_zh": "开发者发布模型部署观察",
                                "url": "https://x.com/dotey/status/2053438255987896328",
                                "source_tier": "t2",
                                "source_kind": "expert_x",
                                "source_label": "专家 X",
                                "source_key": "x:dotey",
                            }
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            with patch("site_builder.DIGEST_DIR", digest_dir):
                feed = _build_feed_for_date({"ai": {"display_name": "AI 前沿"}}, date(2026, 5, 11))

        block = feed["boards"]["ai"]
        self.assertEqual(block["selection_stats"]["aggregator"], 1)
        self.assertEqual(block["selection_stats"].get("direct", 0), 0)
        self.assertEqual(block["selection_stats"]["kind_expert_x"], 1)

    def test_feed_json_passes_clustering_stats_to_offline_eval(self) -> None:
        with TemporaryDirectory() as tmpdir:
            digest_dir = Path(tmpdir)
            digest_dir.joinpath("security_2026-05-11.json").write_text(
                json.dumps(
                    {
                        "board": "security",
                        "display_name": "安全",
                        "date": "2026-05-11",
                        "raw_count": 2,
                        "selected_count": 1,
                        "clustering_stats": {"deterministic_merged": 1, "llm_merged": 1, "merged_total": 2},
                        "generated_at": "2026-05-11T00:00:00Z",
                        "items": [{"title_zh": "CVE 合并事件", "url": "https://cisa.gov/news-events/alerts/x"}],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            with patch("site_builder.DIGEST_DIR", digest_dir):
                feed = _build_feed_for_date({"security": {"display_name": "安全"}}, date(2026, 5, 11))

        self.assertEqual(feed["boards"]["security"]["clustering_stats"]["merged_total"], 2)

    def test_daily_workflow_supports_single_board_dispatch(self) -> None:
        workflow = Path(".github/workflows/daily.yml").read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("board:", workflow)
        self.assertIn("BOARD_SELECTION", workflow)
        self.assertIn("security ai_security ai finance", workflow)

    def test_daily_workflow_does_not_publish_partial_site_for_single_board_dispatch(self) -> None:
        workflow = Path(".github/workflows/daily.yml").read_text(encoding="utf-8")

        self.assertIn("name: Build site", workflow)
        self.assertIn("if: env.BOARD_SELECTION == 'all'", workflow)

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

    def test_source_profile_counts_registry_cn_expert_as_chinese(self) -> None:
        profile = source_profile(
            {
                "title": "npm supply chain deep dive",
                "url": "https://blog.huli.tw/2026/05/25/dive-into-npm-supply-chain-attack/",
            }
        )

        self.assertTrue(profile.is_chinese)
        self.assertEqual(profile.source_kind, "cn_expert")

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

    def test_selection_policy_enforces_minimum_final_score(self) -> None:
        candidates = [
            ({"title": "Strong", "url": "https://example.com/strong"}, 8.0),
            ({"title": "Weak", "url": "https://example.com/weak"}, 5.9),
        ]

        selected = select_with_source_policy(
            candidates,
            top_n=2,
            policy={"min_final_score": 6.0, "allow_cap_relaxation": True},
        )

        self.assertEqual([entry["title"] for entry, _score in selected], ["Strong"])

    def test_selection_policy_reserves_official_sources(self) -> None:
        candidates = [
            ({"title": "Media A", "url": "https://www.finextra.com/news/a"}, 9.0),
            ({"title": "Media B", "url": "https://www.pymnts.com/news/b"}, 8.0),
            ({"title": "Federal Reserve", "url": "https://www.federalreserve.gov/newsevents/c.htm"}, 7.0),
        ]

        selected = select_with_source_policy(
            candidates,
            top_n=2,
            policy={"min_official": 1},
        )

        self.assertIn("https://www.federalreserve.gov/newsevents/c.htm", [entry["url"] for entry, _ in selected])

    def test_cap_relaxation_can_keep_google_news_cap_hard(self) -> None:
        candidates = [
            ({"title": "Google 1", "url": "https://news.google.com/rss/articles/1"}, 10),
            ({"title": "Google 2", "url": "https://news.google.com/rss/articles/2"}, 9),
            ({"title": "Direct 1", "url": "https://openai.com/news/a"}, 8),
            ({"title": "Direct 2", "url": "https://deepmind.google/blog/b"}, 7),
        ]

        selected = select_with_source_policy(
            candidates,
            top_n=4,
            policy={
                "max_google_news": 1,
                "max_aggregator": 1,
                "allow_cap_relaxation": True,
                "relax_aggregate_caps": False,
            },
        )
        urls = [entry["url"] for entry, _score in selected]

        self.assertEqual(sum(1 for url in urls if "news.google.com" in url), 1)
        self.assertEqual(len(urls), 3)


class ScoringPolicyTests(unittest.TestCase):
    def test_dimension_score_uses_board_weights(self) -> None:
        entry = {
            "score_dimensions": {
                "relevance": 10,
                "technical_depth": 8,
                "exploitability": 6,
                "impact_scope": 4,
                "actionability": 2,
            }
        }

        self.assertAlmostEqual(compute_dimension_score("security", entry), 6.7)

    def test_dimension_score_falls_back_to_legacy_score_when_dimensions_missing(self) -> None:
        self.assertEqual(compute_dimension_score("ai", {"score": 7}), 7.0)
        self.assertEqual(compute_dimension_score("ai", {}), 5.0)

    def test_final_score_prefers_official_source_over_google_news_rewrite(self) -> None:
        now = datetime(2026, 5, 11, 12, tzinfo=timezone.utc)
        dimensions = {
            "relevance": 7,
            "novelty": 7,
            "entity_importance": 7,
            "developer_relevance": 7,
            "ecosystem_impact": 7,
        }
        official = {
            "title": "OpenAI model update",
            "url": "https://openai.com/news/model-update",
            "published": "2026-05-11T06:00:00Z",
            "score_dimensions": dimensions,
        }
        google = {
            "title": "OpenAI model update",
            "url": "https://news.google.com/rss/articles/model-update",
            "feed_url": "https://news.google.com/rss/search?q=OpenAI",
            "published": "2026-05-11T06:00:00Z",
            "score_dimensions": dimensions,
        }

        official_score = compute_final_score("ai", official, now=now)
        google_score = compute_final_score("ai", google, now=now)

        self.assertGreater(official_score["final_score"], google_score["final_score"])
        self.assertEqual(official_score["source_bonus"], 1.0)
        self.assertEqual(google_score["kind_bonus"], -1.0)

    def test_final_score_allows_board_specific_kind_bonus_override(self) -> None:
        google = {
            "title": "AI model news",
            "url": "https://news.google.com/rss/articles/model-update",
            "score": 7,
        }

        score = compute_final_score(
            "ai",
            google,
            scoring_config={"boards": {"ai": {"kind_bonus": {"google_news": -1.6}}}},
        )

        self.assertEqual(score["kind_bonus"], -1.6)

    def test_final_score_rewards_expert_sources_above_media(self) -> None:
        now = datetime(2026, 5, 11, 12, tzinfo=timezone.utc)
        expert = {
            "title": "Simon Willison analyzes agent deployment",
            "url": "https://simonwillison.net/2026/May/11/agents/",
            "score": 7,
            "published": "2026-05-11T11:00:00Z",
        }
        media = {
            "title": "TechCrunch covers agent deployment",
            "url": "https://techcrunch.com/2026/05/11/agents/",
            "score": 7,
            "published": "2026-05-11T11:00:00Z",
        }

        self.assertGreater(
            compute_final_score("ai", expert, now=now)["final_score"],
            compute_final_score("ai", media, now=now)["final_score"],
        )

    def test_final_score_gives_cn_visibility_only_to_registered_cn_sources(self) -> None:
        now = datetime(2026, 5, 11, 12, tzinfo=timezone.utc)
        registered_cn = {
            "title": "FreeBuf 发布漏洞分析",
            "url": "https://www.freebuf.com/vuls/123",
            "published": "2026-05-11T06:00:00Z",
            "score": 6,
        }
        generated_cn_translation = {
            "title_zh": "这是系统生成的中文标题",
            "title_orig": "OpenAI model update",
            "summary": "中文摘要不代表原始来源是中文。",
            "url": "https://openai.com/news/model-update",
            "published": "2026-05-11T06:00:00Z",
            "score": 6,
        }

        cn_score = compute_final_score("security", registered_cn, now=now)
        translated_score = compute_final_score("security", generated_cn_translation, now=now)

        self.assertEqual(cn_score["cn_visibility_bonus"], 0.3)
        self.assertEqual(translated_score["cn_visibility_bonus"], 0.0)

    def test_final_score_clamps_to_zero_ten_range(self) -> None:
        now = datetime(2026, 5, 11, 12, tzinfo=timezone.utc)
        high = compute_final_score(
            "ai",
            {"title": "OpenAI", "url": "https://openai.com/news/a", "score": 10, "published": "2026-05-11T11:00:00Z"},
            now=now,
        )
        low = compute_final_score(
            "ai",
            {"title": "Noise", "url": "https://news.google.com/rss/articles/noise", "score": -5},
            now=now,
        )

        self.assertEqual(high["final_score"], 10.0)
        self.assertEqual(low["final_score"], 0.0)


class StoryClusteringTests(unittest.TestCase):
    def test_story_id_prefers_cve_key(self) -> None:
        entry = {
            "title": "Exploit for CVE-2026-12345 released",
            "url": "https://example.com/post",
            "cve_ids": ["CVE-2026-12345"],
        }

        self.assertEqual(story_id_for_entry(entry), "cve:cve-2026-12345")

    def test_story_id_uses_explicit_canonical_url_key(self) -> None:
        entry = {
            "title": "OpenAI model update",
            "url": "https://www.example.com/path/?utm_source=x&b=2",
        }

        self.assertEqual(story_id_for_entry(entry), "url:example.com/path?b=2")

    def test_cluster_scored_candidates_merges_same_cve_and_keeps_authoritative_source(self) -> None:
        candidates = [
            (
                {
                    "title": "Google News: CVE-2026-12345 exploited in the wild",
                    "url": "https://news.google.com/rss/articles/cve",
                    "feed_url": "https://news.google.com/rss/search?q=CVE-2026-12345",
                    "cve_ids": ["CVE-2026-12345"],
                },
                9,
            ),
            (
                {
                    "title": "CISA adds CVE-2026-12345 to KEV",
                    "url": "https://www.cisa.gov/news-events/alerts/cve-2026-12345",
                    "cve_ids": ["CVE-2026-12345"],
                },
                8,
            ),
        ]

        clustered, merged_urls = cluster_scored_candidates(candidates)

        self.assertEqual(len(clustered), 1)
        self.assertEqual(clustered[0][0]["url"], "https://www.cisa.gov/news-events/alerts/cve-2026-12345")
        self.assertEqual(clustered[0][0]["story_id"], "cve:cve-2026-12345")
        self.assertEqual(clustered[0][0]["related_urls"], ["https://news.google.com/rss/articles/cve"])
        self.assertEqual(merged_urls, ["https://news.google.com/rss/articles/cve"])

    def test_cluster_scored_candidates_does_not_merge_weak_shared_vendor_only(self) -> None:
        candidates = [
            ({"title": "OpenAI launches a new voice model", "url": "https://openai.com/news/voice"}, 8),
            ({"title": "OpenAI updates enterprise privacy controls", "url": "https://openai.com/news/privacy"}, 8),
        ]

        clustered, merged_urls = cluster_scored_candidates(candidates)

        self.assertEqual(len(clustered), 2)
        self.assertEqual(merged_urls, [])

    def test_cluster_story_id_is_stable_for_title_cluster(self) -> None:
        candidates = [
            ({"title": "OpenAI releases model update for developers", "url": "https://z.example.com/story"}, 8),
            ({"title": "OpenAI releases model update for developers", "url": "https://a.example.com/story"}, 8),
        ]

        clustered, _merged_urls = cluster_scored_candidates(candidates)

        self.assertEqual(len(clustered), 1)
        self.assertEqual(clustered[0][0]["story_id"], "url:a.example.com/story")

    def test_cluster_prefers_expert_blog_over_generic_media_when_scores_tie(self) -> None:
        candidates = [
            (
                {
                    "title": "OpenAI agent deployment analysis for developers",
                    "url": "https://techcrunch.com/2026/05/11/openai-agent-deployment-analysis/",
                },
                7,
            ),
            (
                {
                    "title": "OpenAI agent deployment analysis for developers",
                    "url": "https://simonwillison.net/2026/May/11/openai-agent-deployment-analysis/",
                },
                7,
            ),
        ]

        clustered, _merged_urls = cluster_scored_candidates(candidates)

        self.assertEqual(len(clustered), 1)
        self.assertEqual(
            clustered[0][0]["url"],
            "https://simonwillison.net/2026/May/11/openai-agent-deployment-analysis/",
        )


class DeliveredHistoryTests(unittest.TestCase):
    def test_load_history_reads_previous_digest_items_and_related_urls(self) -> None:
        with TemporaryDirectory() as tmpdir:
            digest_dir = Path(tmpdir)
            digest_dir.joinpath("security_2026-07-12.json").write_text(
                json.dumps(
                    {
                        "items": [
                            {
                                "url": "https://example.com/primary",
                                "story_id": "cve:cve-2026-12345",
                                "related_urls": ["https://example.net/rewrite"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            history = load_delivered_history(
                "security",
                date(2026, 7, 13),
                lookback_days=7,
                digest_dir=digest_dir,
            )

        self.assertEqual(
            history.urls,
            {"https://example.com/primary", "https://example.net/rewrite"},
        )
        self.assertEqual(history.story_ids, {"cve:cve-2026-12345"})

    def test_filter_history_drops_delivered_url_and_cve_but_keeps_unselected_candidate(self) -> None:
        history = DeliveredHistory(
            urls={"https://example.com/already-shown"},
            story_ids={"cve:cve-2026-12345"},
        )
        candidates = [
            {"url": "https://example.com/already-shown", "title": "Shown yesterday"},
            {
                "url": "https://other.example/new-report",
                "title": "Fresh report for CVE-2026-12345",
                "cve_ids": ["CVE-2026-12345"],
            },
            {"url": "https://example.com/not-selected-yesterday", "title": "Still eligible"},
        ]

        kept, stats = filter_delivered_candidates(candidates, history)

        self.assertEqual([item["url"] for item in kept], ["https://example.com/not-selected-yesterday"])
        self.assertEqual(stats, {"url": 1, "story": 1, "total": 2})


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

    def test_digest_item_preserves_feed_url_for_source_mix_rebuilds(self) -> None:
        item = _finalize_digest_item(
            {
                "title": "OpenAI developer signal",
                "summary": "OpenAI developer signal.",
                "url": "https://x.com/OpenAIDevs/status/2053438255987896328",
                "feed_url": "https://rsshub.app/twitter/user/OpenAIDevs",
                "feed_title": "OpenAIDevs",
            },
            {
                "title_zh": "OpenAI开发者发布新动态",
                "summary": "OpenAI开发者账号发布新动态，涉及开发者生态和模型能力变化。这条资讯来自官方开发者渠道，适合关注 API、工具链和生态节奏的读者继续查看原文。",
                "tags": ["开发者"],
                "selection_reason": "官方开发者信号",
            },
        )

        self.assertEqual(item["feed_url"], "https://rsshub.app/twitter/user/OpenAIDevs")
        self.assertEqual(source_profile(item).source_kind, "official_x")
        self.assertTrue(source_profile(item).is_aggregator)

    def test_score_entries_attaches_multidimensional_scores(self) -> None:
        class FakeBackend:
            name = "fake"
            score_model = "fake-score"
            summarize_model = "fake-summary"

            def generate_json(self, model, system, user_prompt, max_output_tokens):
                return json.dumps(
                    [
                        {
                            "idx": 0,
                            "score": 8,
                            "score_dimensions": {
                                "relevance": 9,
                                "technical_depth": 8,
                                "exploitability": 7,
                                "impact_scope": 8,
                                "actionability": 6,
                            },
                        }
                    ]
                )

        entries = [{"title": "CVE analysis", "summary": "technical details", "url": "https://example.com/a"}]

        scores = _score_entries(FakeBackend(), "security", entries)

        self.assertEqual(scores, [8])
        self.assertEqual(entries[0]["score_dimensions"]["technical_depth"], 8)

    def test_score_prompts_include_language_fairness(self) -> None:
        for prompt in BOARD_SCORE_SYSTEM.values():
            self.assertRegex(prompt, r"评分只看(新闻|技术)价值")
            self.assertIn("不因语言", prompt)

    def test_vuln_tech_element_detection(self) -> None:
        from digest_postprocess import vuln_summary_needs_repair, vuln_tech_element_count

        vague = "该漏洞影响重大，攻击者可能利用它造成严重后果，相关用户应当保持关注并留意后续进展。"
        technical = (
            "Langflow 存在路径遍历漏洞，未经身份验证的远程攻击者可构造恶意请求读取任意文件，"
            "影响 1.0 至 1.4 版本，官方尚未发布补丁，建议临时限制网络访问。"
        )

        self.assertLess(vuln_tech_element_count(vague), 2)
        self.assertTrue(vuln_summary_needs_repair(vague))
        self.assertGreaterEqual(vuln_tech_element_count(technical), 3)
        self.assertFalse(vuln_summary_needs_repair(technical))

    def test_repair_vuln_summaries_only_accepts_improvements(self) -> None:
        from digest_pipeline_gemini import _repair_vuln_summaries

        good_rewrite = (
            "UpdraftPlus 备份插件存在反序列化漏洞，经过身份验证的攻击者可构造恶意备份文件触发远程代码执行，"
            "进而完全接管站点并窃取数据库中的敏感数据，影响 1.25 之前的全部版本，波及大量在线站点。"
            "官方已发布修复补丁并更新到插件市场，建议站长立即升级到最新版本，同时排查近期备份任务是否存在异常记录。"
        )
        worse_rewrite = (
            "该漏洞威胁很大，攻击者可能借机发起攻击，给网站运营带来不小的风险，大家务必提高警惕并小心防范，"
            "请站长和管理员持续关注官方网站的后续公告与相关说明，及时了解事件最新进展，避免遭受不必要的经济损失，"
            "同时也提醒广大互联网用户注意保护好自己的账号和个人数据安全，遇到可疑情况请及时联系平台处理。"
        )

        class FakeBackend:
            name = "fake"
            score_model = "fake-score"
            summarize_model = "fake-summary"

            def generate_json(self, model, system, user_prompt, max_output_tokens):
                return json.dumps(
                    [
                        {"idx": 0, "summary": good_rewrite},
                        {"idx": 1, "summary": worse_rewrite},
                    ],
                    ensure_ascii=False,
                )

        vague_draft = (
            "这个插件漏洞影响广泛，攻击者可能借此发起攻击，对网站运营造成风险，"
            "管理员应当持续关注官方动态并保持警惕，避免遭受不必要的损失和数据问题。"
        )
        batch = [
            {"title": "UpdraftPlus CVE-2026-1111 flaw", "summary": "deserialization detail", "cve_ids": ["CVE-2026-1111"]},
            {"title": "Plugin CVE-2026-2222 issue", "summary": "vague text", "cve_ids": ["CVE-2026-2222"]},
        ]
        summaries = {0: vague_draft, 1: vague_draft}

        repaired = _repair_vuln_summaries(FakeBackend(), batch, summaries)

        # idx 0: rewrite covers more tech elements -> accepted
        self.assertEqual(repaired[0], good_rewrite)
        # idx 1: rewrite is vaguer than draft -> rejected, draft kept
        self.assertEqual(repaired[1], vague_draft)

    def test_repair_vuln_summaries_skips_non_vuln_entries(self) -> None:
        from digest_pipeline_gemini import _repair_vuln_summaries

        calls = []

        class FakeBackend:
            name = "fake"
            score_model = "fake-score"
            summarize_model = "fake-summary"

            def generate_json(self, *args):
                calls.append(args)
                return "[]"

        batch = [{"title": "Security conference announces lineup", "summary": "talks and dates"}]
        summaries = {0: "大会公布了议程安排，多位研究者将分享议题，时间和地点已经确认，欢迎从业者关注并报名参加，议程覆盖多个方向。"}

        repaired = _repair_vuln_summaries(FakeBackend(), batch, summaries)

        self.assertEqual(repaired, summaries)
        self.assertEqual(calls, [])

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

    def test_ai_security_editorial_caps_generic_ai_news(self) -> None:
        not_ai = {
            "title": "Cisco patches critical router authentication bypass",
            "summary": "The flaw allows remote attackers to take over devices.",
        }
        generic_ai = {
            "title": "OpenAI expands ChatGPT Plus training program in Malta",
            "summary": "The company announced broader access and education programs.",
        }
        technical = {
            "title": "Prompt injection flaw leaks private agent memory",
            "summary": "Researchers describe exploit steps and mitigation guidance.",
        }
        security_analysis = {
            "title": "New zero-trust framework for LLM security risks",
            "summary": "The analysis covers defense gates and deployment tradeoffs.",
        }

        # No AI context at all -> belongs on security board, cap 3
        self.assertEqual(adjust_ai_security_score(not_ai, 8), 3)
        # AI context but no concrete security mechanism -> cap 4
        self.assertEqual(adjust_ai_security_score(generic_ai, 8), 4)
        self.assertEqual(adjust_ai_security_score(technical, 8), 8)
        # Broad but genuine AI-security analysis keeps the LLM score; only a
        # concrete mechanism can promote a low score to the floor.
        self.assertEqual(adjust_ai_security_score(security_analysis, 7), 7)
        self.assertEqual(adjust_ai_security_score(security_analysis, 4), 4)

    def test_ai_security_editorial_not_fooled_by_substring_matches(self) -> None:
        # Regression: "ai" used to match inside "supply chAIn" / "emAIl",
        # letting generic supply-chain stories flood the AI-security board
        # with a guaranteed floor-6 score.
        supply_chain = {
            "title": "Geopolitical supply chain attack tensions hit chipmakers",
            "summary": "Trade limits reshape email and domain infrastructure markets.",
        }

        self.assertEqual(adjust_ai_security_score(supply_chain, 8), 3)

    def test_security_editorial_geo_cap_requires_word_boundary(self) -> None:
        # Regression: "apt" used to match inside "adapt"/"chapter"/"laptop".
        benign = {
            "title": "Adaptive fuzzing chapter: laptop kernel exploitation deep dive",
            "summary": "A technical walkthrough of adaptive coverage-guided fuzzing.",
        }
        apt_numbered = {
            "title": "APT41 campaign targets telecom providers",
            "summary": "Attribution report on state-sponsored activity.",
        }

        self.assertEqual(adjust_security_score(benign, 9), 9)
        self.assertEqual(adjust_security_score(apt_numbered, 9), 4)

    def test_ai_security_editorial_promotes_ai_coding_security_signals(self) -> None:
        entry = {
            "title": "MCP repository hides README text and postinstall payload",
            "summary": "A Claude Code workflow can execute a supply chain attack.",
        }

        self.assertEqual(adjust_ai_security_score(entry, 4), 6)

    def test_ai_security_editorial_caps_vendor_marketing_and_lawsuits(self) -> None:
        marketing = {
            "title": "Vendor named Gartner representative for agentic application security testing",
            "summary": "The company announced recognition in a market report.",
        }
        lawsuit = {
            "title": "AI security startup sues competitor over hallucinated report",
            "summary": "The dispute concerns commercial claims between two vendors.",
        }

        self.assertEqual(adjust_ai_security_score(marketing, 8), 4)
        self.assertEqual(adjust_ai_security_score(lawsuit, 8), 4)

    def test_finance_editorial_requires_financial_context(self) -> None:
        generic_ai = {
            "title": "OpenAI security leader leaves company",
            "summary": "The research organization is restructuring its team.",
        }
        generic_regulation = {
            "title": "EU expands social media safety regulation",
            "summary": "The proposal covers consumer protection on online platforms.",
        }
        fintech = {
            "title": "Visa deploys AI fraud controls for card payments",
            "summary": "The payment network is applying models to transaction risk scoring.",
        }

        self.assertEqual(adjust_finance_score(generic_ai, 8), 3)
        self.assertEqual(adjust_finance_score(generic_regulation, 8), 3)
        self.assertEqual(adjust_finance_score(fintech, 8), 8)

    def test_security_editorial_caps_vulnerability_without_mechanism(self) -> None:
        vague = {
            "title": "Critical U-Boot vulnerability threatens millions of devices",
            "summary": "Researchers disclosed a serious issue and urged users to monitor updates.",
        }
        technical = {
            "title": "U-Boot buffer overflow vulnerability",
            "summary": "A crafted packet triggers an out-of-bounds write in the network parser.",
        }

        self.assertEqual(adjust_security_score(vague, 10), 8)
        self.assertEqual(adjust_security_score(technical, 10), 10)

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
        self.assertLessEqual(security["source_caps"]["bleepingcomputer.com"], 3)
        self.assertLessEqual(security["source_caps"]["thehackernews.com"], 3)
        self.assertNotIn("mp.weixin.qq.com", security.get("source_caps") or {})

    def test_ai_security_board_is_cost_bounded_and_direct_source_first(self) -> None:
        import yaml

        boards = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))["boards"]
        board = boards["ai_security"]

        self.assertEqual(board["top_n"], 10)
        self.assertLessEqual(board["llm_max_entries"], 90)
        self.assertLessEqual(board["source_policy"]["max_google_news"], 2)
        self.assertGreaterEqual(board["source_policy"]["min_direct"], 4)
        self.assertEqual(board["source_policy"]["max_aggregator"], 5)
        self.assertFalse(board["source_policy"]["relax_aggregate_caps"])
        self.assertEqual(board["fill_score_floor"], 5)
        self.assertEqual(board["source_policy"]["min_final_score"], 5.0)
        self.assertTrue(Path(board["opml"]).exists())

    def test_board_output_targets_match_current_editorial_policy(self) -> None:
        import yaml

        boards = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))["boards"]

        self.assertEqual(boards["security"]["top_n"], 15)
        self.assertEqual(boards["security"]["source_policy"]["min_chinese"], 6)
        self.assertEqual(boards["ai_security"]["top_n"], 10)
        self.assertEqual(boards["ai"]["top_n"], 15)
        self.assertGreaterEqual(boards["ai"]["fetch_hours"], 48)
        self.assertEqual(boards["ai"]["dedup_lookback_days"], 0)
        self.assertEqual(boards["ai"]["fill_score_floor"], 4)
        self.assertEqual(boards["ai"]["source_policy"]["min_chinese"], 5)
        self.assertEqual(boards["finance"]["top_n"], 10)
        self.assertEqual(boards["ai"]["source_policy"]["max_aggregator"], 7)
        self.assertFalse(boards["ai"]["source_policy"]["relax_aggregate_caps"])
        self.assertEqual(boards["ai"]["source_caps"]["arxiv.org"], 2)

    def test_finance_opml_has_chinese_fintech_fallback(self) -> None:
        body = Path("feeds/finance.opml").read_text(encoding="utf-8")

        self.assertIn("Google News 中文金融科技", body)
        self.assertIn("数字人民币", body)
        self.assertIn("跨境支付", body)
        self.assertIn("Finextra Headlines", body)
        self.assertIn("The Fintech Times", body)

    def test_ai_security_opml_has_dedicated_ai_security_labs(self) -> None:
        body = Path("feeds/ai_security.opml").read_text(encoding="utf-8")

        self.assertIn("Protect AI", body)
        self.assertIn("Prompt Security", body)
        self.assertIn("HiddenLayer Blog", body)
        self.assertIn("GitHub Security Lab", body)
        self.assertIn("Legit Security", body)
        self.assertIn("Endor Labs", body)
        self.assertIn("娜璋AI安全之家", body)
        self.assertIn("Seebug Paper", body)

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

    def test_digest_items_receive_deterministic_final_score_metadata(self) -> None:
        enriched = _attach_final_scores(
            "ai",
            [{"title_zh": "OpenAI 发布模型更新", "url": "https://openai.com/news/model-update"}],
            [
                (
                    {
                        "title": "OpenAI model update",
                        "url": "https://openai.com/news/model-update",
                        "published": "2026-05-11T06:00:00Z",
                        "score_dimensions": {
                            "relevance": 9,
                            "novelty": 8,
                            "entity_importance": 9,
                            "developer_relevance": 8,
                            "ecosystem_impact": 8,
                        },
                    },
                    8,
                )
            ],
            None,
        )

        item = enriched[0]
        self.assertEqual(item["score"], 8)
        self.assertGreater(item["final_score"], 8)
        self.assertIn("source_bonus", item["score_breakdown"])
        self.assertEqual(item["score_dimensions"]["novelty"], 8)

    def test_xss_summary_does_not_claim_system_level_arbitrary_code_execution(self) -> None:
        entry = {
            "title": "Critical stored XSS lets crafted email run scripts in user sessions",
            "summary": "A stored cross-site scripting flaw executes JavaScript in the victim browser.",
        }
        draft = "攻击者发送恶意邮件后可在用户浏览器会话中执行脚本，进而实现任意代码执行并窃取会话数据。"

        sanitized = _sanitize_vulnerability_claims(entry, draft)

        self.assertNotIn("任意代码执行", sanitized)
        self.assertIn("浏览器会话内脚本执行", sanitized)

    def test_selection_scoring_uses_final_score_not_raw_llm_score(self) -> None:
        final_scored = _score_candidates_for_selection(
            "ai",
            [
                (
                    {
                        "title": "OpenAI official update",
                        "url": "https://openai.com/news/model-update",
                        "published": "2026-05-11T06:00:00Z",
                    },
                    7,
                ),
                (
                    {
                        "title": "OpenAI update via Google News",
                        "url": "https://news.google.com/rss/articles/model-update",
                        "feed_url": "https://news.google.com/rss/search?q=OpenAI",
                        "published": "2026-05-11T06:00:00Z",
                    },
                    8,
                ),
            ],
            {
                "https://openai.com/news/model-update": 7,
                "https://news.google.com/rss/articles/model-update": 8,
            },
            None,
        )

        self.assertEqual(final_scored[0][0]["url"], "https://openai.com/news/model-update")
        self.assertGreater(final_scored[0][1], final_scored[1][1])

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

    def test_finalize_digest_item_strips_repeated_title_from_summary_suffix(self) -> None:
        title = "GitHub Copilot计费细节曝光"
        summary = (
            "GitHub Copilot 披露不同模型的 Token 消耗倍率，显示高性能模型在平台内会占用更多计算资源。"
            "这对企业团队有实际影响，因为模型选择将直接关系到开发工具预算、调用策略和使用治理。"
            f" {title}"
        )
        entry = {
            "title": title,
            "summary": "GitHub Copilot usage details.",
            "url": "https://example.com/copilot",
            "category": "Labs",
            "published": "2026-06-01T00:00:00Z",
        }

        finalized = _finalize_digest_item(
            entry,
            {
                "title_zh": title,
                "summary": summary,
                "tags": ["开发工具"],
                "selection_reason": "计费变化影响开发团队",
            },
        )

        self.assertFalse(finalized["summary"].endswith(title))
        self.assertLessEqual(len(finalized["summary"]), 240)

    def test_finalize_digest_item_compacts_rendered_long_summary(self) -> None:
        title = "Claude Design 推出额度共享功能"
        summary = (
            "Claude Design 现已支持额度共享并显著增加了使用频次，尽管 Token 消耗依然较高，"
            "但其作为 Agent 产品在生成效果上获得了开发者的高度评价。"
            "用户可以通过导入 Adobe Spectrum 2 等成熟设计系统的 URL，确保 AI 生成的界面在风格一致性与专业感上达到更高水准，"
            "从而有效利用 GitHub 上的开源资源来大幅提升视觉设计的开发效率。"
            f" {title}。该条来自x.com，归类于XSignals，原始信息显示其在本轮抓取、去重和打分中优先级较高。"
        )
        entry = {
            "title": title,
            "summary": "Claude Design update.",
            "url": "https://x.com/example/status/1",
            "category": "XSignals",
            "published": "2026-06-01T00:00:00Z",
        }

        finalized = _finalize_digest_item(
            entry,
            {
                "title_zh": title,
                "summary": summary,
                "tags": ["设计工具"],
                "selection_reason": "开发者工具更新",
            },
        )

        self.assertLessEqual(len(finalized["summary"]), 220)

    def test_candidate_pool_uses_fill_floor_to_backfill_below_threshold(self) -> None:
        scored = [
            ({"title": "A", "url": "https://a.example"}, 8),
            ({"title": "B", "url": "https://b.example"}, 6),
            ({"title": "C", "url": "https://c.example"}, 5),
            ({"title": "D", "url": "https://d.example"}, 4),
        ]

        pool = _candidate_pool(scored, top_n=4, fill_score_floor=5)

        self.assertEqual([entry["title"] for entry, _score in pool], ["A", "B", "C"])

    def test_candidate_pool_reserves_chinese_quota_slots(self) -> None:
        # 6 high-scored English items fill a pool of 4 (top_n=2 -> pool 4);
        # Chinese items score lower and sit outside the score cut. With
        # min_chinese=2 the pool must swap them in over the English tail.
        scored = [
            ({"title": f"EN {i}", "url": f"https://en.example/{i}"}, 9 - i)
            for i in range(4)
        ] + [
            ({"title": "中文安全分析一", "url": "https://cn.example/1"}, 5),
            ({"title": "中文安全分析二", "url": "https://cn.example/2"}, 4),
        ]

        pool = _candidate_pool(scored, top_n=2, fill_score_floor=4, min_chinese=2)

        titles = [entry["title"] for entry, _score in pool]
        self.assertIn("中文安全分析一", titles)
        self.assertIn("中文安全分析二", titles)
        # Highest-scored English items stay; only the tail was swapped.
        self.assertIn("EN 0", titles)
        self.assertIn("EN 1", titles)
        self.assertEqual(len(pool), 4)

    def test_candidate_pool_chinese_quota_noop_when_satisfied(self) -> None:
        scored = [
            ({"title": "中文头条", "url": "https://cn.example/top"}, 9),
            ({"title": "EN A", "url": "https://en.example/a"}, 8),
            ({"title": "EN B", "url": "https://en.example/b"}, 7),
        ]

        pool = _candidate_pool(scored, top_n=2, fill_score_floor=4, min_chinese=1)

        self.assertEqual([entry["title"] for entry, _score in pool], ["中文头条", "EN A", "EN B"])

    def test_llm_dedupe_preserves_related_urls_on_primary_item(self) -> None:
        class FakeBackend:
            name = "fake"
            score_model = "fake-score"
            summarize_model = "fake-summarize"

            def generate_json(self, *_args: object) -> str:
                return "[[0,1]]"

        deduped, merged_urls = _llm_dedupe(
            FakeBackend(),
            [
                ({"title": "OpenAI launches GPT-6 coding agent for developers", "url": "https://openai.com/news/a"}, 8),
                ({"title": "OpenAI launches GPT-6 coding agent for software developers", "url": "https://example.com/rewrite"}, 7),
            ],
        )

        self.assertEqual(len(deduped), 1)
        self.assertEqual(merged_urls, ["https://example.com/rewrite"])
        self.assertEqual(deduped[0][0]["related_urls"], ["https://example.com/rewrite"])
        self.assertEqual(deduped[0][0]["related_count"], 1)

    def test_llm_dedupe_rejects_unrelated_items_grouped_by_model(self) -> None:
        class FakeBackend:
            name = "fake"
            score_model = "fake-score"
            summarize_model = "fake-summarize"

            def generate_json(self, *_args: object) -> str:
                return "[[0,1,2]]"

        candidates = [
            ({"title": "OpenAI launches GPT-6 model", "url": "https://a.example/model"}, 9),
            ({"title": "OpenAI acquires a database startup", "url": "https://b.example/deal"}, 8),
            ({"title": "OpenAI changes API billing terms", "url": "https://c.example/billing"}, 7),
        ]

        deduped, merged_urls = _llm_dedupe(FakeBackend(), candidates)

        self.assertEqual(len(deduped), 3)
        self.assertEqual(merged_urls, [])

    def test_llm_dedupe_rejects_suspicious_mass_collapse(self) -> None:
        class FakeBackend:
            name = "fake"
            score_model = "fake-score"
            summarize_model = "fake-summarize"

            def generate_json(self, *_args: object) -> str:
                return json.dumps(
                    [*[list(range(idx, idx + 2)) for idx in range(0, 24, 2)],
                     *[[idx] for idx in range(24, 30)]]
                )

        candidates = []
        for pair in range(12):
            candidates.extend(
                [
                    (
                        {
                            "title": f"OpenAI launches Model{pair} coding agent for developers",
                            "url": f"https://official.example/{pair}",
                        },
                        9,
                    ),
                    (
                        {
                            "title": f"OpenAI launches Model{pair} coding agent for software developers",
                            "url": f"https://media.example/{pair}",
                        },
                        8,
                    ),
                ]
            )
        candidates.extend(
            (
                {"title": f"Independent vendor update {idx}", "url": f"https://example.com/{idx}"},
                7,
            )
            for idx in range(24, 30)
        )

        deduped, merged_urls = _llm_dedupe(FakeBackend(), candidates)

        self.assertEqual(len(deduped), 30)
        self.assertEqual(merged_urls, [])


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
        self.assertIn("GEMINI_REQUEST_TIMEOUT_SEC", body)
        self.assertIn("timeout 15m python digest_pipeline_gemini.py", body)
        self.assertIn("Fail if any board failed", body)


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

    def test_gemini_backend_honors_request_timeout_env(self) -> None:
        from llm_backends import gemini
        from llm_backends.gemini import GeminiBackend

        class FakeGenAI:
            class Client:
                def __init__(self, api_key: str, http_options: object) -> None:
                    self.api_key = api_key
                    self.http_options = http_options

        with (
            patch.object(gemini, "genai", FakeGenAI),
            patch.object(gemini, "GOOGLE_GENAI_IMPORT_ERROR", None),
            patch.dict(
                "os.environ",
                {"GEMINI_API_KEY": "test-key", "GEMINI_REQUEST_TIMEOUT_SEC": "12"},
                clear=True,
            ),
        ):
            backend = GeminiBackend.from_env()

        self.assertEqual(backend.request_timeout_sec, 12)
        self.assertEqual(backend.client.http_options.timeout, 12000)
        self.assertEqual(backend.score_model, "gemini-3-flash-preview")
        self.assertEqual(backend.summarize_model, "gemini-3-flash-preview")


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
                                "final_score": 7.8,
                            },
                            {
                                "title_zh": "Google 转述",
                                "url": "https://news.google.com/rss/articles/1",
                                "source_tier": "t2",
                                "source_kind": "google_news",
                                "final_score": 5.9,
                            },
                            {
                                "title_zh": "未登记源",
                                "url": "https://unknown.example/a",
                                "source_tier": "unknown",
                                "source_kind": "media",
                                "final_score": 4.3,
                            },
                        ],
                        "clustering_stats": {"merged_total": 2},
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

        self.assertIn("## Top Issues", markdown)
        self.assertIn("[security] 1/1 天未满额", markdown)
        # CN Target = config target (6); Obs Min CN = observed minimum (1).
        self.assertIn("CN Target | Obs Min CN", markdown)
        self.assertNotIn("| Min CN |", markdown)
        self.assertIn("| security | 安全 | 1 | 3.0 | 15 | 0/1 | 1.0 | 6 | 1 | 0/1 | 1.0 | 1 | 1 | 6.0 | 2 |", markdown)
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
    def test_parse_aihot_rss_items_normalizes_feed_entries(self) -> None:
        rss = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>AI HOT — 精选</title>
<item><title>OpenAI 发布新模型</title><link>https://openai.com/news/model</link><description>摘要内容</description><pubDate>Mon, 11 May 2026 01:22:36 GMT</pubDate><source>AIHOT</source></item>
</channel></rss>"""

        items = parse_aihot_rss_items(rss)

        self.assertEqual(items[0]["title"], "OpenAI 发布新模型")
        self.assertEqual(items[0]["url"], "https://openai.com/news/model")
        self.assertEqual(items[0]["summary"], "摘要内容")
        self.assertEqual(items[0]["publishedAt"], "Mon, 11 May 2026 01:22:36 GMT")

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
                "source": "rss",
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


class FeedbackLoopTests(unittest.TestCase):
    def test_feedback_cli_appends_jsonl_record(self) -> None:
        with TemporaryDirectory() as tmpdir:
            feedback_dir = Path(tmpdir) / "feedback"
            with patch("feedback_cli.FEEDBACK_DIR", feedback_dir):
                path = add_feedback(
                    board="security",
                    url="https://example.com/vuln",
                    action="upvote",
                    reason="漏洞原理清楚",
                    feedback_date="2026-05-18",
                    title_zh="示例漏洞分析",
                )

            record = json.loads(path.read_text(encoding="utf-8").strip())

        self.assertEqual(record["board"], "security")
        self.assertEqual(record["action"], "upvote")
        self.assertEqual(record["source"], "example.com")

    def test_feedback_eval_classifies_selected_and_fetched_items(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digest"
            output_dir = root / "output"
            digest_dir.mkdir()
            output_dir.mkdir()
            digest_dir.joinpath("security_2026-05-18.json").write_text(
                json.dumps({"items": [{"url": "https://example.com/selected"}]}),
                encoding="utf-8",
            )
            output_dir.joinpath("security_latest.json").write_text(
                json.dumps({"entries": [{"url": "https://example.com/fetched"}]}),
                encoding="utf-8",
            )
            with (
                patch("feedback_eval.DIGEST_DIR", digest_dir),
                patch("feedback_eval.OUTPUT_DIR", output_dir),
            ):
                selected = classify_feedback({"board": "security", "url": "https://example.com/selected"})
                fetched = classify_feedback({"board": "security", "url": "https://example.com/fetched"})
                missing = classify_feedback({"board": "security", "url": "https://example.com/missing"})

        self.assertEqual(selected, "selected")
        self.assertEqual(fetched, "fetched_not_selected")
        self.assertEqual(missing, "not_found_recent_artifacts")

    def test_feedback_cli_imports_site_jsonl_export(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            exported = root / "site.jsonl"
            exported.write_text(
                json.dumps(
                    {
                        "date": "2026-07-13",
                        "board": "ai_security",
                        "url": "https://example.com/agent",
                        "action": "downvote",
                        "reason": "站点快捷反馈",
                        "title_zh": "泛营销内容",
                    },
                    ensure_ascii=False,
                )
                + "\nnot-json\n",
                encoding="utf-8",
            )
            with patch("feedback_cli.FEEDBACK_DIR", root / "feedback"):
                imported, skipped = import_feedback_file(exported)
                records = (root / "feedback" / "2026-07-13.jsonl").read_text(encoding="utf-8")

        self.assertEqual((imported, skipped), (1, 1))
        self.assertIn("ai_security", records)

    def test_feedback_summary_is_written_into_weekly_report(self) -> None:
        with TemporaryDirectory() as tmpdir:
            weekly = Path(tmpdir) / "weekly.md"
            weekly.write_text("# Weekly\n", encoding="utf-8")
            records = [
                {"board": "security", "action": "upvote"},
                {"board": "ai_security", "action": "downvote"},
            ]

            sync_weekly_feedback(records, weekly)
            sync_weekly_feedback(records, weekly)
            body = weekly.read_text(encoding="utf-8")

        self.assertEqual(body.count("## 人工反馈（最近 14 天）"), 1)
        self.assertIn("upvote=1", body)
        self.assertIn("ai_security=1", body)

    def test_feedback_report_recommends_repeated_source_feedback(self) -> None:
        records = [
            {
                "date": "2026-05-18",
                "board": "security",
                "url": f"https://good.example/{idx}",
                "source": "good.example",
                "action": "upvote",
                "reason": "好",
            }
            for idx in range(3)
        ]

        markdown = build_report(records)

        self.assertIn("good.example", markdown)
        self.assertIn("收到 3 次正反馈", markdown)


class DigestClockTests(unittest.TestCase):
    def test_digest_today_honors_env_override(self) -> None:
        with patch.dict("os.environ", {"DIGEST_DATE": "2026-04-25"}):
            self.assertEqual(digest_today(), date(2026, 4, 25))


if __name__ == "__main__":
    unittest.main()
