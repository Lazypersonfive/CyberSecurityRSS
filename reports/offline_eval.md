# Offline Strategy Eval

- generated_for: 2026-06-21
- dates: 2026-06-21, 2026-06-20, 2026-06-19, 2026-06-18, 2026-06-17, 2026-06-16, 2026-06-15

## Top Issues

- [ai_security] 2/7 天未满额，累计缺口约 8 条。
- [ai] 中文目标 4/7 天达成。
- [ai_security] 中文目标 5/7 天达成。
- [security] 入选 unknown source 20 条，需登记或降权。
- [finance] 入选 unknown source 1 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.7 | 5 | 4/7 | 0.6 | 3 | 0 | 8.7 | 61 |
| ai_security | AI 安全 | 7 | 8.9 | 10 | 5/7 | 2.6 | 2 | 5/7 | 0.6 | 2 | 0 | 7.9 | 9 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.3 | 1 | 7/7 | 1.4 | 4 | 1 | 7.7 | 28 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.9 | 6 | 7/7 | 0.0 | 1 | 20 | 9.2 | 28 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 21 | 16 | 68 | 0 | 21 | 39 | 4 | 19 | 0 |
| ai_security | 9 | 4 | 49 | 0 | 9 | 11 | 4 | 17 | 0 |
| finance | 2 | 0 | 67 | 1 | 2 | 0 | 10 | 0 | 0 |
| security | 15 | 0 | 70 | 20 | 15 | 0 | 0 | 41 | 2 |

## Target Misses

- 2026-06-21 security：selected 15/15，中文 8/6，unknown 3
- 2026-06-21 ai_security：selected 8/10，中文 2/2
- 2026-06-20 security：selected 15/15，中文 7/6，unknown 2
- 2026-06-20 ai：selected 15/15，中文 4/5
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

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
