import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from digest_postprocess import count_chinese_chars, summary_needs_repair
from fetch_feeds import FeedEntry, fetch_all_entries
from filter_entries import filter_and_dedup
from rss_curation import curate_entries
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
            entries, _health = await fetch_all_entries(feeds, hours=9999, max_per_category=2)

        self.assertEqual([entry.title for entry in entries], ["newer-2", "newer-1"])


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


class SiteBuilderTests(unittest.TestCase):
    def test_cli_lookback_overrides_config(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            templates = root / "templates"
            docs = root / "docs"
            templates.mkdir()
            templates.joinpath("index.html.j2").write_text("{{ title }}", encoding="utf-8")

            with patch("site_builder.DOCS_DIR", docs):
                with patch("site_builder.TEMPLATE_DIR", templates):
                    with patch("site_builder.yaml.safe_load", return_value={"boards": {}, "site": {"lookback_days": 7}}):
                        with patch("site_builder.Path.read_text", return_value="site: {}"):
                            with patch("site_builder.date") as mock_date:
                                with patch("site_builder._build_feed_for_date", return_value=None) as mock_feed:
                                    mock_date.today.return_value = date(2026, 4, 22)
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


if __name__ == "__main__":
    unittest.main()
