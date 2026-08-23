# Offline Strategy Eval

- generated_for: 2026-08-24
- dates: 2026-08-24, 2026-08-23, 2026-08-22, 2026-08-21, 2026-08-20, 2026-08-19, 2026-08-18

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 46 条。
- [finance] 1/7 天未满额，累计缺口约 2 条。
- [ai_security] 中文目标 0/7 天达成。
- [finance] 中文目标 6/7 天达成。
- [security] 入选 unknown source 9 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.9 | 5 | 5 | 7/7 | 0.6 | 3 | 1 | 8.4 | 15 |
| ai_security | AI 安全 | 7 | 3.4 | 10 | 0/7 | 0.1 | 2 | 0 | 0/7 | 0.9 | 2 | 0 | 7.7 | 0 |
| finance | 金融科技 | 7 | 9.7 | 10 | 6/7 | 1.4 | 1 | 0 | 6/7 | 1.6 | 4 | 0 | 7.4 | 2 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.1 | 6 | 6 | 7/7 | 0.0 | 1 | 9 | 8.9 | 10 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 17 | 14 | 73 | 1 | 17 | 39 | 4 | 25 | 1 |
| ai_security | 3 | 0 | 21 | 0 | 3 | 0 | 6 | 1 | 0 |
| finance | 7 | 0 | 61 | 0 | 7 | 0 | 11 | 0 | 0 |
| security | 5 | 0 | 91 | 9 | 3 | 0 | 0 | 45 | 9 |

## Target Misses

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
- 2026-08-20 ai_security：selected 6/10，中文 0/2
- 2026-08-19 security：selected 15/15，中文 8/6，unknown 1
- 2026-08-19 ai_security：selected 5/10，中文 0/2
- 2026-08-19 finance：selected 10/10，中文 0/1
- 2026-08-18 ai_security：selected 3/10，中文 1/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
