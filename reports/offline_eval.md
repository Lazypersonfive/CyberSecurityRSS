# Offline Strategy Eval

- generated_for: 2026-07-20
- dates: 2026-07-20, 2026-07-19, 2026-07-18, 2026-07-17, 2026-07-16, 2026-07-15, 2026-07-14

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 40 条。
- [finance] 2/7 天未满额，累计缺口约 5 条。
- [ai_security] 中文目标 2/7 天达成。
- [ai] 中文目标 4/7 天达成。
- [finance] Google News 超限 1 天。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.9 | 5 | 3 | 4/7 | 1.1 | 3 | 6 | 8.2 | 38 |
| ai_security | AI 安全 | 7 | 4.3 | 10 | 0/7 | 1.1 | 2 | 0 | 2/7 | 1.1 | 2 | 0 | 7.4 | 3 |
| finance | 金融科技 | 7 | 9.3 | 10 | 5/7 | 2.9 | 1 | 1 | 7/7 | 3.0 | 4 | 0 | 7.4 | 1 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.6 | 6 | 6 | 7/7 | 0.0 | 1 | 10 | 8.4 | 21 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 12 | 18 | 69 | 6 | 12 | 41 | 8 | 14 | 0 |
| ai_security | 4 | 0 | 26 | 0 | 4 | 6 | 8 | 7 | 0 |
| finance | 10 | 0 | 55 | 0 | 10 | 0 | 21 | 0 | 0 |
| security | 8 | 0 | 87 | 10 | 8 | 3 | 0 | 42 | 10 |

## Target Misses

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
- 2026-07-16 ai_security：selected 5/10，中文 1/2
- 2026-07-16 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-15 ai_security：selected 4/10，中文 0/2
- 2026-07-15 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-14 ai_security：selected 5/10，中文 4/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
