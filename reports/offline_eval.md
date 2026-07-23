# Offline Strategy Eval

- generated_for: 2026-07-24
- dates: 2026-07-24, 2026-07-23, 2026-07-22, 2026-07-21, 2026-07-20, 2026-07-19, 2026-07-18

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 42 条。
- [finance] 3/7 天未满额，累计缺口约 6 条。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 5/7 天达成。
- [finance] Google News 超限 2 天。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.9 | 5 | 4 | 5/7 | 1.0 | 3 | 4 | 8.3 | 26 |
| ai_security | AI 安全 | 7 | 4.0 | 10 | 0/7 | 1.0 | 2 | 0 | 3/7 | 0.9 | 2 | 0 | 7.7 | 9 |
| finance | 金融科技 | 7 | 9.1 | 10 | 4/7 | 3.4 | 1 | 2 | 7/7 | 3.6 | 4 | 0 | 7.1 | 1 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.6 | 6 | 6 | 7/7 | 0.0 | 1 | 13 | 8.5 | 30 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 18 | 21 | 62 | 4 | 18 | 42 | 7 | 14 | 0 |
| ai_security | 2 | 0 | 26 | 0 | 2 | 10 | 6 | 6 | 0 |
| finance | 10 | 0 | 54 | 0 | 10 | 0 | 25 | 0 | 0 |
| security | 4 | 0 | 88 | 13 | 4 | 6 | 0 | 40 | 11 |

## Target Misses

- 2026-07-24 security：selected 15/15，中文 6/6，unknown 1
- 2026-07-24 ai_security：selected 7/10，中文 2/2
- 2026-07-24 ai：selected 15/15，中文 4/5
- 2026-07-24 finance：selected 10/10，中文 5/1，Google News 5/4
- 2026-07-23 security：selected 15/15，中文 8/6，unknown 1
- 2026-07-23 ai_security：selected 4/10，中文 2/2
- 2026-07-23 ai：selected 15/15，中文 4/5
- 2026-07-23 finance：selected 9/10，中文 4/1
- 2026-07-22 security：selected 15/15，中文 7/6，unknown 1
- 2026-07-22 ai_security：selected 5/10，中文 0/2
- 2026-07-22 ai：selected 15/15，中文 5/5，unknown 1
- 2026-07-21 ai_security：selected 3/10，中文 0/2
- 2026-07-20 security：selected 15/15，中文 6/6，unknown 7
- 2026-07-20 ai_security：selected 4/10，中文 0/2
- 2026-07-20 finance：selected 7/10，中文 5/1，Google News 5/4
- 2026-07-19 security：selected 15/15，中文 6/6，unknown 3
- 2026-07-19 ai_security：selected 3/10，中文 1/2
- 2026-07-19 finance：selected 8/10，中文 3/1
- 2026-07-18 ai_security：selected 2/10，中文 2/2
- 2026-07-18 ai：selected 15/15，中文 5/5，unknown 3

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
