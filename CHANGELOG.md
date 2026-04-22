# Changelog

## 2026-04-22

- Fixed per-category feed limiting so caps are applied after collecting and sorting entries by recency.
- Fixed digest entry ordering to sort equal-score items by newest publication time first.
- Fixed `site_builder.py --lookback` so the CLI flag overrides `config.yaml` as expected.
- Fixed the site empty-state view to clear stale metadata when a board/date has no items.
- Added regression tests covering feed capping, digest ordering, and site lookback override behavior.
- Added per-board RSS source caps so a few high-volume publishers do not dominate the daily pool.
- Updated both digest pipelines to target 200-300 Chinese characters and repair summaries that come back too short or too long.
- Tightened summary generation further to target 220-260 Chinese characters and allow repeated repair passes when models still underwrite.
