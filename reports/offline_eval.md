# Offline Strategy Eval

- generated_for: 2026-08-19
- dates: 2026-08-19, 2026-08-18, 2026-08-17, 2026-08-16, 2026-08-15, 2026-08-14, 2026-08-13

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 51 条。
- [finance] 1/7 天未满额，累计缺口约 2 条。
- [ai_security] 中文目标 0/7 天达成。
- [finance] 中文目标 6/7 天达成。
- [finance] Google News 超限 1 天。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.6 | 5 | 5 | 7/7 | 0.6 | 3 | 0 | 8.7 | 25 |
| ai_security | AI 安全 | 7 | 2.7 | 10 | 0/7 | 0.3 | 2 | 0 | 0/7 | 0.9 | 2 | 0 | 7.1 | 1 |
| finance | 金融科技 | 7 | 9.7 | 10 | 6/7 | 2.1 | 1 | 0 | 6/7 | 2.1 | 4 | 0 | 7.2 | 2 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.3 | 6 | 6 | 7/7 | 0.0 | 1 | 4 | 8.7 | 13 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 20 | 14 | 71 | 0 | 20 | 41 | 4 | 21 | 1 |
| ai_security | 2 | 0 | 17 | 0 | 2 | 1 | 6 | 1 | 0 |
| finance | 5 | 0 | 63 | 0 | 5 | 0 | 15 | 0 | 0 |
| security | 2 | 0 | 99 | 4 | 2 | 0 | 0 | 49 | 13 |

## Target Misses

- 2026-08-19 security：selected 15/15，中文 8/6，unknown 1
- 2026-08-19 ai_security：selected 5/10，中文 0/2
- 2026-08-19 finance：selected 10/10，中文 0/1
- 2026-08-18 ai_security：selected 3/10，中文 1/2
- 2026-08-17 ai_security：selected 2/10，中文 1/2
- 2026-08-17 finance：selected 10/10，中文 5/1，Google News 5/4
- 2026-08-16 ai_security：selected 1/10，中文 0/2
- 2026-08-16 finance：selected 8/10，中文 1/1
- 2026-08-15 ai_security：selected 2/10，中文 0/2
- 2026-08-14 security：selected 15/15，中文 6/6，unknown 2
- 2026-08-14 ai_security：selected 1/10，中文 0/2
- 2026-08-13 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-13 ai_security：selected 5/10，中文 0/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
