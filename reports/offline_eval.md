# Offline Strategy Eval

- generated_for: 2026-08-27
- dates: 2026-08-27, 2026-08-26, 2026-08-25, 2026-08-24, 2026-08-23, 2026-08-22, 2026-08-21

## Top Issues

- [ai_security] 6/7 天未满额，累计缺口约 43 条。
- [finance] 1/7 天未满额，累计缺口约 2 条。
- [ai_security] 中文目标 1/7 天达成。
- [ai] 中文目标 6/7 天达成。
- [security] 入选 unknown source 10 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.7 | 5 | 4 | 6/7 | 1.1 | 3 | 2 | 8.4 | 18 |
| ai_security | AI 安全 | 7 | 3.9 | 10 | 1/7 | 0.3 | 2 | 0 | 1/7 | 1.1 | 2 | 0 | 7.8 | 2 |
| finance | 金融科技 | 7 | 9.7 | 10 | 6/7 | 2.1 | 1 | 1 | 7/7 | 2.1 | 4 | 0 | 7.5 | 1 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.7 | 6 | 6 | 7/7 | 0.0 | 1 | 10 | 8.8 | 12 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 19 | 70 | 2 | 14 | 35 | 8 | 25 | 1 |
| ai_security | 1 | 1 | 25 | 0 | 1 | 2 | 8 | 2 | 0 |
| finance | 6 | 0 | 62 | 0 | 6 | 0 | 15 | 0 | 0 |
| security | 6 | 0 | 89 | 10 | 5 | 1 | 0 | 43 | 10 |

## Target Misses

- 2026-08-27 ai：selected 15/15，中文 4/5
- 2026-08-26 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-26 ai_security：selected 3/10，中文 0/2
- 2026-08-25 security：selected 15/15，中文 8/6，unknown 1
- 2026-08-25 ai_security：selected 4/10，中文 0/2
- 2026-08-25 ai：selected 15/15，中文 5/5，unknown 1
- 2026-08-24 security：selected 15/15，中文 9/6，unknown 3
- 2026-08-24 ai_security：selected 1/10，中文 0/2
- 2026-08-24 finance：selected 8/10，中文 2/1
- 2026-08-23 security：selected 15/15，中文 6/6，unknown 3
- 2026-08-23 ai_security：selected 2/10，中文 0/2
- 2026-08-22 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-22 ai_security：selected 2/10，中文 0/2
- 2026-08-21 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-21 ai_security：selected 5/10，中文 0/2
- 2026-08-21 ai：selected 15/15，中文 5/5，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
