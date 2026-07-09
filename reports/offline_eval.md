# Offline Strategy Eval

- generated_for: 2026-07-10
- dates: 2026-07-10, 2026-07-09, 2026-07-08, 2026-07-07, 2026-07-06, 2026-07-05, 2026-07-04

## Top Issues

- [ai_security] 2/7 天未满额，累计缺口约 5 条。
- [ai] 1/7 天未满额，累计缺口约 5 条。
- [ai] 中文目标 4/7 天达成。
- [ai_security] 中文目标 5/7 天达成。
- [finance] 中文目标 6/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.3 | 15 | 6/7 | 4.6 | 5 | 0 | 4/7 | 0.3 | 3 | 1 | 8.7 | 50 |
| ai_security | AI 安全 | 7 | 9.3 | 10 | 5/7 | 2.9 | 2 | 1 | 5/7 | 0.7 | 2 | 0 | 7.8 | 3 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.7 | 1 | 0 | 6/7 | 2.0 | 4 | 1 | 7.9 | 12 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 9.3 | 6 | 6 | 7/7 | 0.0 | 1 | 7 | 9.3 | 32 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 16 | 69 | 1 | 14 | 43 | 2 | 17 | 2 |
| ai_security | 2 | 0 | 63 | 0 | 2 | 3 | 5 | 19 | 0 |
| finance | 3 | 0 | 66 | 1 | 3 | 0 | 14 | 0 | 0 |
| security | 8 | 0 | 90 | 7 | 8 | 0 | 0 | 65 | 0 |

## Target Misses

- 2026-07-10 security：selected 15/15，中文 6/6，unknown 1
- 2026-07-10 ai：selected 10/15，中文 0/5
- 2026-07-10 finance：selected 10/10，中文 0/1
- 2026-07-09 ai：selected 15/15，中文 4/5
- 2026-07-07 security：selected 15/15，中文 10/6，unknown 1
- 2026-07-07 ai_security：selected 9/10，中文 1/2
- 2026-07-06 security：selected 15/15，中文 11/6，unknown 1
- 2026-07-06 ai_security：selected 6/10，中文 2/2
- 2026-07-05 security：selected 15/15，中文 11/6，unknown 1
- 2026-07-05 ai_security：selected 10/10，中文 1/2
- 2026-07-04 security：selected 15/15，中文 9/6，unknown 3
- 2026-07-04 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-04 finance：selected 10/10，中文 3/1，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
