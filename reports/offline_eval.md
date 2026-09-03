# Offline Strategy Eval

- generated_for: 2026-09-03
- dates: 2026-09-03, 2026-08-31, 2026-08-30, 2026-08-29, 2026-08-28, 2026-08-27, 2026-08-26

## Top Issues

- [ai_security] 5/7 天未满额，累计缺口约 31 条。
- [ai_security] 中文目标 4/7 天达成。
- [ai] 中文目标 4/7 天达成。
- [security] 入选 unknown source 7 条，需登记或降权。
- [ai] 入选 unknown source 3 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.7 | 5 | 4 | 4/7 | 1.4 | 3 | 3 | 8.3 | 32 |
| ai_security | AI 安全 | 7 | 5.6 | 10 | 2/7 | 1.7 | 2 | 0 | 4/7 | 0.7 | 2 | 1 | 8.1 | 6 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.1 | 1 | 1 | 7/7 | 2.4 | 4 | 0 | 7.2 | 0 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.7 | 6 | 6 | 7/7 | 0.0 | 1 | 7 | 8.3 | 15 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 13 | 23 | 66 | 3 | 13 | 39 | 10 | 16 | 1 |
| ai_security | 5 | 2 | 31 | 1 | 5 | 5 | 5 | 11 | 0 |
| finance | 4 | 1 | 65 | 0 | 4 | 1 | 17 | 0 | 0 |
| security | 8 | 0 | 90 | 7 | 7 | 2 | 0 | 44 | 10 |

## Target Misses

- 2026-09-03 ai：selected 15/15，中文 4/5，unknown 1
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

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
