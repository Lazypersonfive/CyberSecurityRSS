# Offline Strategy Eval

- generated_for: 2026-08-31
- dates: 2026-08-31, 2026-08-30, 2026-08-29, 2026-08-28, 2026-08-27, 2026-08-26, 2026-08-25

## Top Issues

- [ai_security] 6/7 天未满额，累计缺口约 37 条。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 5/7 天达成。
- [security] 入选 unknown source 8 条，需登记或降权。
- [ai] 入选 unknown source 3 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.9 | 5 | 4 | 5/7 | 1.3 | 3 | 3 | 8.4 | 28 |
| ai_security | AI 安全 | 7 | 4.7 | 10 | 1/7 | 1.1 | 2 | 0 | 3/7 | 1.0 | 2 | 1 | 7.8 | 3 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.3 | 1 | 1 | 7/7 | 2.6 | 4 | 0 | 7.4 | 0 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.7 | 6 | 6 | 7/7 | 0.0 | 1 | 8 | 8.3 | 15 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 15 | 25 | 62 | 3 | 15 | 37 | 9 | 20 | 1 |
| ai_security | 4 | 1 | 27 | 1 | 4 | 3 | 7 | 7 | 0 |
| finance | 6 | 1 | 63 | 0 | 6 | 1 | 18 | 0 | 0 |
| security | 7 | 0 | 90 | 8 | 6 | 3 | 0 | 44 | 10 |

## Target Misses

- 2026-08-31 security：selected 15/15，中文 6/6，unknown 2
- 2026-08-31 ai_security：selected 9/10，中文 3/2，unknown 1
- 2026-08-30 security：selected 15/15，中文 6/6，unknown 2
- 2026-08-30 ai_security：selected 0/10，中文 0/2
- 2026-08-29 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-29 ai_security：selected 3/10，中文 2/2
- 2026-08-29 ai：selected 15/15，中文 4/5，unknown 2
- 2026-08-28 security：selected 15/15，中文 9/6，unknown 1
- 2026-08-28 ai_security：selected 4/10，中文 1/2
- 2026-08-27 ai：selected 15/15，中文 4/5
- 2026-08-26 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-26 ai_security：selected 3/10，中文 0/2
- 2026-08-25 security：selected 15/15，中文 8/6，unknown 1
- 2026-08-25 ai_security：selected 4/10，中文 0/2
- 2026-08-25 ai：selected 15/15，中文 5/5，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
