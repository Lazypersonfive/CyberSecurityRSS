# Offline Strategy Eval

- generated_for: 2026-06-19
- dates: 2026-06-19, 2026-06-18, 2026-06-17, 2026-06-16, 2026-06-15, 2026-06-14, 2026-06-13

## Top Issues

- [ai_security] 2/7 天未满额，累计缺口约 7 条。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 4/7 天达成。
- [security] 入选 unknown source 19 条，需登记或降权。
- [finance] 入选 unknown source 1 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.6 | 5 | 4/7 | 0.9 | 3 | 0 | 8.6 | 59 |
| ai_security | AI 安全 | 7 | 9.0 | 10 | 5/7 | 2.3 | 2 | 3/7 | 0.6 | 2 | 0 | 8.0 | 13 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.7 | 1 | 7/7 | 1.7 | 4 | 1 | 7.8 | 24 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.6 | 6 | 7/7 | 0.0 | 1 | 19 | 9.2 | 28 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 20 | 21 | 64 | 0 | 20 | 41 | 6 | 17 | 0 |
| ai_security | 12 | 3 | 48 | 0 | 12 | 13 | 4 | 16 | 0 |
| finance | 2 | 0 | 67 | 1 | 2 | 0 | 12 | 0 | 0 |
| security | 18 | 0 | 68 | 19 | 18 | 2 | 0 | 41 | 2 |

## Target Misses

- 2026-06-19 security：selected 15/15，中文 8/6，unknown 1
- 2026-06-18 security：selected 15/15，中文 10/6，unknown 2
- 2026-06-18 ai：selected 15/15，中文 2/5
- 2026-06-17 security：selected 15/15，中文 7/6，unknown 2
- 2026-06-17 ai：selected 15/15，中文 3/5
- 2026-06-16 security：selected 15/15，中文 6/6，unknown 7
- 2026-06-16 ai_security：selected 10/10，中文 1/2
- 2026-06-16 finance：selected 10/10，中文 1/1，unknown 1
- 2026-06-15 security：selected 15/15，中文 9/6，unknown 3
- 2026-06-15 ai_security：selected 4/10，中文 0/2
- 2026-06-14 security：selected 15/15，中文 7/6，unknown 3
- 2026-06-14 ai_security：selected 9/10，中文 1/2
- 2026-06-13 security：selected 15/15，中文 6/6，unknown 1
- 2026-06-13 ai_security：selected 10/10，中文 1/2
- 2026-06-13 ai：selected 15/15，中文 4/5

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
