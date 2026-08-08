# Offline Strategy Eval

- generated_for: 2026-08-09
- dates: 2026-08-09, 2026-08-08, 2026-08-07, 2026-08-06, 2026-08-05, 2026-08-04, 2026-08-03

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 36 条。
- [ai_security] 中文目标 0/7 天达成。
- [ai] 中文目标 5/7 天达成。
- [security] 中文目标 6/7 天达成。
- [security] 入选 unknown source 9 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.0 | 5 | 3 | 5/7 | 0.6 | 3 | 2 | 8.5 | 26 |
| ai_security | AI 安全 | 7 | 4.9 | 10 | 0/7 | 0.3 | 2 | 0 | 0/7 | 1.6 | 2 | 0 | 7.3 | 6 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.1 | 1 | 1 | 7/7 | 2.1 | 4 | 0 | 7.3 | 0 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 5.9 | 6 | 5 | 6/7 | 0.0 | 1 | 9 | 8.4 | 19 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 17 | 72 | 2 | 14 | 42 | 4 | 17 | 0 |
| ai_security | 5 | 1 | 28 | 0 | 5 | 5 | 11 | 1 | 0 |
| finance | 5 | 0 | 65 | 0 | 5 | 0 | 15 | 0 | 0 |
| security | 8 | 0 | 88 | 9 | 8 | 6 | 0 | 39 | 5 |

## Target Misses

- 2026-08-09 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-09 ai_security：selected 2/10，中文 0/2
- 2026-08-08 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-08 ai_security：selected 4/10，中文 0/2
- 2026-08-08 ai：selected 15/15，中文 3/5，unknown 2
- 2026-08-07 ai_security：selected 7/10，中文 1/2
- 2026-08-07 ai：selected 15/15，中文 4/5
- 2026-08-06 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-06 ai_security：selected 7/10，中文 0/2
- 2026-08-05 security：selected 15/15，中文 5/6，unknown 1
- 2026-08-05 ai_security：selected 7/10，中文 1/2
- 2026-08-04 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-04 ai_security：selected 5/10，中文 0/2
- 2026-08-03 security：selected 15/15，中文 6/6，unknown 4
- 2026-08-03 ai_security：selected 2/10，中文 0/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
