# Offline Strategy Eval

- generated_for: 2026-09-28
- dates: 2026-09-28, 2026-09-21, 2026-09-17, 2026-09-14, 2026-09-10, 2026-09-07, 2026-09-03

## Top Issues

- [ai] 1/7 天未满额，累计缺口约 3 条。
- [ai] 中文目标 5/7 天达成。
- [finance] 中文目标 6/7 天达成。
- [security] 入选 unknown source 3 条，需登记或降权。
- [ai_security] 入选 unknown source 2 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.6 | 15 | 6/7 | 4.7 | 5 | 4 | 5/7 | 1.3 | 3 | 2 | 7.8 | 37 |
| ai_security | AI 安全 | 7 | 10.0 | 10 | 7/7 | 4.3 | 2 | 2 | 7/7 | 0.0 | 2 | 2 | 8.4 | 8 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.1 | 2 | 1 | 6/7 | 1.1 | 3 | 0 | 7.9 | 2 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.4 | 6 | 6 | 7/7 | 0.0 | 1 | 3 | 8.8 | 9 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 12 | 19 | 69 | 2 | 12 | 40 | 9 | 7 | 0 |
| ai_security | 13 | 4 | 51 | 2 | 12 | 7 | 0 | 30 | 0 |
| finance | 12 | 2 | 56 | 0 | 12 | 2 | 8 | 0 | 0 |
| security | 17 | 0 | 85 | 3 | 13 | 0 | 0 | 50 | 1 |

## Target Misses

- 2026-09-28 security：selected 15/15，中文 6/6，unknown 1
- 2026-09-21 ai：selected 15/15，中文 5/5，unknown 1
- 2026-09-17 security：selected 15/15，中文 6/6，unknown 1
- 2026-09-10 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-09-10 ai：selected 15/15，中文 4/5
- 2026-09-07 security：selected 15/15，中文 6/6，unknown 1
- 2026-09-07 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-09-07 ai：selected 12/15，中文 5/5
- 2026-09-03 ai：selected 15/15，中文 4/5，unknown 1
- 2026-09-03 finance：selected 10/10，中文 1/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
