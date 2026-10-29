# Offline Strategy Eval

- generated_for: 2026-10-29
- dates: 2026-10-29, 2026-10-26, 2026-10-22, 2026-10-19, 2026-10-15, 2026-10-12, 2026-10-08

## Top Issues

- [ai] 中文目标 5/7 天达成。
- [ai_security] 入选 unknown source 4 条，需登记或降权。
- [finance] 入选 unknown source 1 条，需登记或降权。
- [ai] 入选 unknown source 1 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.4 | 5 | 3 | 5/7 | 1.1 | 3 | 1 | 7.9 | 31 |
| ai_security | AI 安全 | 7 | 10.0 | 10 | 7/7 | 3.9 | 2 | 2 | 7/7 | 0.0 | 2 | 4 | 8.3 | 6 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.3 | 2 | 2 | 7/7 | 0.7 | 3 | 1 | 7.8 | 0 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.9 | 6 | 6 | 7/7 | 0.0 | 1 | 0 | 8.8 | 19 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 17 | 12 | 75 | 1 | 17 | 41 | 8 | 3 | 0 |
| ai_security | 13 | 4 | 49 | 4 | 8 | 10 | 0 | 27 | 0 |
| finance | 16 | 2 | 51 | 1 | 16 | 2 | 5 | 0 | 0 |
| security | 14 | 0 | 91 | 0 | 10 | 5 | 0 | 55 | 0 |

## Target Misses

- 2026-10-29 ai_security：selected 10/10，中文 3/2，unknown 1
- 2026-10-26 finance：selected 10/10，中文 2/2，unknown 1
- 2026-10-22 ai：selected 15/15，中文 3/5
- 2026-10-19 ai_security：selected 10/10，中文 4/2，unknown 1
- 2026-10-19 ai：selected 15/15，中文 3/5，unknown 1
- 2026-10-12 ai_security：selected 10/10，中文 6/2，unknown 1
- 2026-10-08 ai_security：selected 10/10，中文 2/2，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
