# Offline Strategy Eval

- generated_for: 2026-05-25
- dates: 2026-05-24, 2026-05-23, 2026-05-22, 2026-05-21, 2026-05-20, 2026-05-19, 2026-05-18

## Top Issues

- [ai_security] 5/7 天未满额，累计缺口约 22 条。
- [ai] 3/7 天未满额，累计缺口约 10 条。
- [finance] 1/7 天未满额，累计缺口约 1 条。
- [ai] 中文目标 1/7 天达成。
- [ai_security] 中文目标 4/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 13.6 | 15 | 4/7 | 3.3 | 5 | 1/7 | 2.3 | 3 | 3 | 7.8 | 52 |
| ai_security | AI 安全 | 7 | 6.9 | 10 | 2/7 | 2.3 | 2 | 4/7 | 2.3 | 2 | 0 | 6.3 | 5 |
| finance | 金融科技 | 7 | 9.9 | 10 | 6/7 | 2.1 | 1 | 7/7 | 2.3 | 4 | 0 | 7.7 | 8 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.0 | 6 | 5/7 | 0.0 | 1 | 3 | 9.1 | 12 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 10 | 19 | 63 | 3 | 10 | 35 | 16 | 0 | 1 |
| ai_security | 8 | 0 | 40 | 0 | 8 | 5 | 16 | 15 | 0 |
| finance | 3 | 0 | 66 | 0 | 3 | 0 | 16 | 0 | 0 |
| security | 17 | 0 | 85 | 3 | 17 | 5 | 0 | 41 | 9 |

## Target Misses

- 2026-05-24 security：selected 15/15，中文 6/6，unknown 1
- 2026-05-24 ai_security：selected 6/10，中文 3/2
- 2026-05-24 ai：selected 14/15，中文 6/5，Google News 4/3
- 2026-05-23 security：selected 15/15，中文 7/6，unknown 1
- 2026-05-23 ai_security：selected 9/10，中文 5/2
- 2026-05-23 ai：selected 15/15，中文 3/5，unknown 1
- 2026-05-22 ai：selected 15/15，中文 4/5
- 2026-05-21 ai_security：selected 10/10，中文 3/2，Google News 3/2
- 2026-05-21 ai：selected 15/15，中文 2/5
- 2026-05-20 ai_security：selected 3/10，中文 0/2，Google News 3/2
- 2026-05-20 ai：selected 11/15，中文 2/5
- 2026-05-19 security：selected 15/15，中文 5/6，unknown 1
- 2026-05-19 ai_security：selected 2/10，中文 0/2
- 2026-05-19 ai：selected 15/15，中文 3/5，unknown 2
- 2026-05-18 security：selected 15/15，中文 2/6
- 2026-05-18 ai_security：selected 8/10，中文 0/2，Google News 3/2
- 2026-05-18 ai：selected 10/15，中文 3/5，Google News 5/3
- 2026-05-18 finance：selected 9/10，中文 4/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
