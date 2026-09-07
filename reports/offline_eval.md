# Offline Strategy Eval

- generated_for: 2026-09-07
- dates: 2026-09-07, 2026-09-03, 2026-08-31, 2026-08-30, 2026-08-29, 2026-08-28, 2026-08-27

## Top Issues

- [ai_security] 4/7 天未满额，累计缺口约 24 条。
- [ai] 1/7 天未满额，累计缺口约 3 条。
- [finance] 中文目标 4/7 天达成。
- [ai] 中文目标 4/7 天达成。
- [ai_security] 中文目标 5/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.6 | 15 | 6/7 | 4.7 | 5 | 4 | 4/7 | 1.6 | 3 | 3 | 8.2 | 39 |
| ai_security | AI 安全 | 7 | 6.6 | 10 | 3/7 | 2.0 | 2 | 0 | 5/7 | 0.6 | 2 | 2 | 8.0 | 7 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.3 | 2 | 1 | 4/7 | 2.3 | 3 | 0 | 7.2 | 0 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.7 | 6 | 6 | 7/7 | 0.0 | 1 | 7 | 8.3 | 17 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 13 | 20 | 66 | 3 | 13 | 38 | 11 | 13 | 0 |
| ai_security | 9 | 2 | 33 | 2 | 9 | 5 | 4 | 13 | 0 |
| finance | 5 | 1 | 64 | 0 | 5 | 1 | 16 | 0 | 0 |
| security | 8 | 0 | 90 | 7 | 7 | 2 | 0 | 45 | 9 |

## Target Misses

- 2026-09-07 security：selected 15/15，中文 6/6，unknown 1
- 2026-09-07 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-09-07 ai：selected 12/15，中文 5/5
- 2026-09-03 ai：selected 15/15，中文 4/5，unknown 1
- 2026-09-03 finance：selected 10/10，中文 1/2
- 2026-08-31 security：selected 15/15，中文 6/6，unknown 2
- 2026-08-31 ai_security：selected 9/10，中文 3/2，unknown 1
- 2026-08-31 finance：selected 10/10，中文 1/2
- 2026-08-30 security：selected 15/15，中文 6/6，unknown 2
- 2026-08-30 ai_security：selected 0/10，中文 0/2
- 2026-08-30 finance：selected 10/10，中文 4/2，Google News 4/3
- 2026-08-29 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-29 ai_security：selected 3/10，中文 2/2
- 2026-08-29 ai：selected 15/15，中文 4/5，unknown 2
- 2026-08-28 security：selected 15/15，中文 9/6，unknown 1
- 2026-08-28 ai_security：selected 4/10，中文 1/2
- 2026-08-28 finance：selected 10/10，中文 1/2
- 2026-08-27 ai：selected 15/15，中文 4/5

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
