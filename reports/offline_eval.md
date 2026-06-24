# Offline Strategy Eval

- generated_for: 2026-06-25
- dates: 2026-06-25, 2026-06-24, 2026-06-23, 2026-06-22, 2026-06-21, 2026-06-20, 2026-06-19

## Top Issues

- [ai_security] 4/7 天未满额，累计缺口约 11 条。
- [ai] 中文目标 4/7 天达成。
- [finance] 中文目标 5/7 天达成。
- [security] 入选 unknown source 23 条，需登记或降权。
- [ai] 入选 unknown source 1 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.7 | 5 | 4/7 | 0.6 | 3 | 1 | 8.6 | 52 |
| ai_security | AI 安全 | 7 | 8.4 | 10 | 3/7 | 2.7 | 2 | 7/7 | 1.3 | 2 | 0 | 7.3 | 11 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 0.9 | 1 | 5/7 | 1.7 | 4 | 0 | 7.5 | 20 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.1 | 6 | 7/7 | 0.0 | 1 | 23 | 9.1 | 37 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 23 | 15 | 66 | 1 | 23 | 36 | 4 | 18 | 0 |
| ai_security | 9 | 5 | 45 | 0 | 9 | 8 | 9 | 13 | 0 |
| finance | 2 | 0 | 68 | 0 | 2 | 0 | 12 | 0 | 0 |
| security | 13 | 0 | 69 | 23 | 13 | 0 | 0 | 39 | 2 |

## Target Misses

- 2026-06-25 security：selected 15/15，中文 6/6，unknown 5
- 2026-06-25 ai_security：selected 9/10，中文 3/2
- 2026-06-25 ai：selected 15/15，中文 2/5
- 2026-06-24 security：selected 15/15，中文 7/6，unknown 7
- 2026-06-24 ai：selected 15/15，中文 4/5，unknown 1
- 2026-06-24 finance：selected 10/10，中文 0/1
- 2026-06-23 security：selected 15/15，中文 7/6，unknown 5
- 2026-06-23 ai_security：selected 6/10，中文 2/2
- 2026-06-23 finance：selected 10/10，中文 0/1
- 2026-06-22 ai_security：selected 6/10，中文 2/2
- 2026-06-21 security：selected 15/15，中文 8/6，unknown 3
- 2026-06-21 ai_security：selected 8/10，中文 2/2
- 2026-06-20 security：selected 15/15，中文 7/6，unknown 2
- 2026-06-20 ai：selected 15/15，中文 4/5
- 2026-06-19 security：selected 15/15，中文 8/6，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
