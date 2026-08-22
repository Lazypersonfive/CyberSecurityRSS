# Offline Strategy Eval

- generated_for: 2026-08-23
- dates: 2026-08-23, 2026-08-22, 2026-08-21, 2026-08-20, 2026-08-19, 2026-08-18, 2026-08-17

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 45 条。
- [ai_security] 中文目标 0/7 天达成。
- [finance] 中文目标 6/7 天达成。
- [finance] Google News 超限 1 天。
- [security] 入选 unknown source 6 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 6.0 | 5 | 5 | 7/7 | 0.3 | 3 | 1 | 8.5 | 20 |
| ai_security | AI 安全 | 7 | 3.6 | 10 | 0/7 | 0.3 | 2 | 0 | 0/7 | 1.0 | 2 | 0 | 7.5 | 0 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.9 | 1 | 0 | 6/7 | 2.0 | 4 | 0 | 7.3 | 2 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.0 | 6 | 6 | 7/7 | 0.0 | 1 | 6 | 8.8 | 9 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 17 | 13 | 74 | 1 | 17 | 41 | 2 | 24 | 1 |
| ai_security | 3 | 0 | 22 | 0 | 3 | 0 | 7 | 1 | 0 |
| finance | 7 | 0 | 63 | 0 | 7 | 0 | 14 | 0 | 0 |
| security | 4 | 0 | 95 | 6 | 3 | 0 | 0 | 47 | 11 |

## Target Misses

- 2026-08-23 security：selected 15/15，中文 6/6，unknown 3
- 2026-08-23 ai_security：selected 2/10，中文 0/2
- 2026-08-22 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-22 ai_security：selected 2/10，中文 0/2
- 2026-08-21 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-21 ai_security：selected 5/10，中文 0/2
- 2026-08-21 ai：selected 15/15，中文 5/5，unknown 1
- 2026-08-20 ai_security：selected 6/10，中文 0/2
- 2026-08-19 security：selected 15/15，中文 8/6，unknown 1
- 2026-08-19 ai_security：selected 5/10，中文 0/2
- 2026-08-19 finance：selected 10/10，中文 0/1
- 2026-08-18 ai_security：selected 3/10，中文 1/2
- 2026-08-17 ai_security：selected 2/10，中文 1/2
- 2026-08-17 finance：selected 10/10，中文 5/1，Google News 5/4

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
