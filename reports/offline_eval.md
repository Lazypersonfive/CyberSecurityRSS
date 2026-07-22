# Offline Strategy Eval

- generated_for: 2026-07-23
- dates: 2026-07-23, 2026-07-22, 2026-07-21, 2026-07-20, 2026-07-19, 2026-07-18, 2026-07-17

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 42 条。
- [finance] 3/7 天未满额，累计缺口约 6 条。
- [ai_security] 中文目标 2/7 天达成。
- [ai] 中文目标 5/7 天达成。
- [finance] Google News 超限 1 天。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.7 | 5 | 3 | 5/7 | 1.0 | 3 | 5 | 8.3 | 29 |
| ai_security | AI 安全 | 7 | 4.0 | 10 | 0/7 | 0.7 | 2 | 0 | 2/7 | 1.0 | 2 | 0 | 7.6 | 6 |
| finance | 金融科技 | 7 | 9.1 | 10 | 4/7 | 2.9 | 1 | 1 | 7/7 | 3.0 | 4 | 0 | 7.3 | 0 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.6 | 6 | 6 | 7/7 | 0.0 | 1 | 12 | 8.6 | 29 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 16 | 23 | 61 | 5 | 16 | 42 | 7 | 14 | 0 |
| ai_security | 4 | 0 | 24 | 0 | 4 | 7 | 7 | 4 | 0 |
| finance | 10 | 0 | 54 | 0 | 10 | 0 | 21 | 0 | 0 |
| security | 6 | 0 | 87 | 12 | 6 | 5 | 0 | 41 | 10 |

## Target Misses

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
- 2026-07-17 ai_security：selected 7/10，中文 0/2
- 2026-07-17 ai：selected 15/15，中文 3/5，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
