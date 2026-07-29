# Offline Strategy Eval

- generated_for: 2026-07-30
- dates: 2026-07-30, 2026-07-29, 2026-07-28, 2026-07-27, 2026-07-26, 2026-07-25, 2026-07-24

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 42 条。
- [finance] 1/7 天未满额，累计缺口约 4 条。
- [ai_security] 中文目标 4/7 天达成。
- [ai] 中文目标 4/7 天达成。
- [finance] Google News 超限 1 天。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.6 | 5 | 3 | 4/7 | 1.6 | 3 | 2 | 8.3 | 40 |
| ai_security | AI 安全 | 7 | 4.0 | 10 | 0/7 | 1.6 | 2 | 0 | 4/7 | 1.4 | 2 | 0 | 7.6 | 8 |
| finance | 金融科技 | 7 | 9.4 | 10 | 6/7 | 3.0 | 1 | 1 | 7/7 | 3.0 | 4 | 1 | 7.3 | 3 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.7 | 6 | 6 | 7/7 | 0.0 | 1 | 6 | 8.3 | 16 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 12 | 17 | 74 | 2 | 12 | 36 | 11 | 14 | 1 |
| ai_security | 0 | 1 | 27 | 0 | 0 | 8 | 10 | 7 | 0 |
| finance | 10 | 0 | 55 | 1 | 10 | 0 | 21 | 0 | 0 |
| security | 8 | 0 | 91 | 6 | 8 | 5 | 0 | 44 | 8 |

## Target Misses

- 2026-07-30 security：selected 15/15，中文 6/6，unknown 1
- 2026-07-30 ai_security：selected 5/10，中文 2/2
- 2026-07-30 ai：selected 15/15，中文 4/5，unknown 1
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

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
