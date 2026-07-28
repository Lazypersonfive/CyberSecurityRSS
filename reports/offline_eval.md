# Offline Strategy Eval

- generated_for: 2026-07-29
- dates: 2026-07-29, 2026-07-28, 2026-07-27, 2026-07-26, 2026-07-25, 2026-07-24, 2026-07-23

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 43 条。
- [finance] 2/7 天未满额，累计缺口约 5 条。
- [ai_security] 中文目标 4/7 天达成。
- [ai] 中文目标 4/7 天达成。
- [finance] Google News 超限 1 天。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.6 | 5 | 3 | 4/7 | 1.3 | 3 | 1 | 8.4 | 44 |
| ai_security | AI 安全 | 7 | 3.9 | 10 | 0/7 | 1.6 | 2 | 0 | 4/7 | 1.1 | 2 | 0 | 7.6 | 9 |
| finance | 金融科技 | 7 | 9.3 | 10 | 5/7 | 3.4 | 1 | 2 | 7/7 | 3.4 | 4 | 1 | 7.2 | 3 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.0 | 6 | 6 | 7/7 | 0.0 | 1 | 6 | 8.3 | 17 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 19 | 71 | 1 | 14 | 38 | 9 | 17 | 1 |
| ai_security | 0 | 0 | 27 | 0 | 0 | 7 | 8 | 8 | 0 |
| finance | 10 | 0 | 54 | 1 | 10 | 0 | 24 | 0 | 0 |
| security | 7 | 0 | 92 | 6 | 7 | 5 | 0 | 46 | 8 |

## Target Misses

- 2026-07-29 ai_security：selected 6/10，中文 3/2
- 2026-07-28 security：selected 15/15，中文 9/6，unknown 1
- 2026-07-28 ai_security：selected 3/10，中文 0/2
- 2026-07-27 security：selected 15/15，中文 8/6，unknown 2
- 2026-07-27 ai_security：selected 2/10，中文 1/2
- 2026-07-27 finance：selected 6/10，中文 4/1
- 2026-07-26 ai_security：selected 3/10，中文 1/2
- 2026-07-26 finance：selected 10/10，中文 3/1，unknown 1
- 2026-07-25 security：selected 15/15，中文 6/6，unknown 1
- 2026-07-25 ai_security：selected 2/10，中文 2/2
- 2026-07-25 ai：selected 15/15，中文 3/5，unknown 1
- 2026-07-24 security：selected 15/15，中文 6/6，unknown 1
- 2026-07-24 ai_security：selected 7/10，中文 2/2
- 2026-07-24 ai：selected 15/15，中文 4/5
- 2026-07-24 finance：selected 10/10，中文 5/1，Google News 5/4
- 2026-07-23 security：selected 15/15，中文 8/6，unknown 1
- 2026-07-23 ai_security：selected 4/10，中文 2/2
- 2026-07-23 ai：selected 15/15，中文 4/5
- 2026-07-23 finance：selected 9/10，中文 4/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
