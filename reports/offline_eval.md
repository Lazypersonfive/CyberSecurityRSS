# Offline Strategy Eval

- generated_for: 2026-09-14
- dates: 2026-09-14, 2026-09-10, 2026-09-07, 2026-09-03, 2026-08-31, 2026-08-30, 2026-08-29

## Top Issues

- [ai_security] 3/7 天未满额，累计缺口约 18 条。
- [ai] 1/7 天未满额，累计缺口约 3 条。
- [ai] 中文目标 4/7 天达成。
- [finance] 中文目标 5/7 天达成。
- [ai_security] 中文目标 6/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.6 | 15 | 6/7 | 4.7 | 5 | 4 | 4/7 | 1.4 | 3 | 3 | 7.9 | 42 |
| ai_security | AI 安全 | 7 | 7.4 | 10 | 4/7 | 2.6 | 2 | 0 | 6/7 | 0.1 | 2 | 3 | 8.1 | 6 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.3 | 2 | 1 | 5/7 | 2.1 | 3 | 0 | 7.3 | 1 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.9 | 6 | 6 | 7/7 | 0.0 | 1 | 6 | 8.3 | 9 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 11 | 16 | 72 | 3 | 11 | 39 | 10 | 9 | 0 |
| ai_security | 13 | 1 | 35 | 3 | 12 | 5 | 1 | 17 | 0 |
| finance | 6 | 2 | 62 | 0 | 6 | 2 | 15 | 0 | 0 |
| security | 12 | 0 | 87 | 6 | 9 | 2 | 0 | 46 | 7 |

## Target Misses

- 2026-09-10 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-09-10 ai：selected 15/15，中文 4/5
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

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
