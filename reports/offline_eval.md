# Offline Strategy Eval

- generated_for: 2026-08-26
- dates: 2026-08-26, 2026-08-25, 2026-08-24, 2026-08-23, 2026-08-22, 2026-08-21, 2026-08-20

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 47 条。
- [finance] 1/7 天未满额，累计缺口约 2 条。
- [ai_security] 中文目标 0/7 天达成。
- [security] 入选 unknown source 10 条，需登记或降权。
- [ai] 入选 unknown source 2 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.9 | 5 | 5 | 7/7 | 0.7 | 3 | 2 | 8.4 | 16 |
| ai_security | AI 安全 | 7 | 3.3 | 10 | 0/7 | 0.0 | 2 | 0 | 0/7 | 1.3 | 2 | 0 | 7.8 | 1 |
| finance | 金融科技 | 7 | 9.7 | 10 | 6/7 | 1.9 | 1 | 1 | 7/7 | 2.0 | 4 | 0 | 7.4 | 1 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.0 | 6 | 6 | 7/7 | 0.0 | 1 | 10 | 8.8 | 8 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 16 | 16 | 71 | 2 | 16 | 37 | 5 | 26 | 1 |
| ai_security | 2 | 0 | 21 | 0 | 2 | 1 | 9 | 0 | 0 |
| finance | 7 | 0 | 61 | 0 | 7 | 0 | 14 | 0 | 0 |
| security | 7 | 0 | 88 | 10 | 5 | 1 | 0 | 44 | 8 |

## Target Misses

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
- 2026-08-20 ai_security：selected 6/10，中文 0/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
