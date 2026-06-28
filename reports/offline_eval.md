# Offline Strategy Eval

- generated_for: 2026-06-29
- dates: 2026-06-29, 2026-06-28, 2026-06-27, 2026-06-26, 2026-06-25, 2026-06-24, 2026-06-23

## Top Issues

- [ai_security] 3/7 天未满额，累计缺口约 6 条。
- [ai] 中文目标 3/7 天达成。
- [finance] 中文目标 4/7 天达成。
- [security] 入选 unknown source 29 条，需登记或降权。
- [finance] 入选 unknown source 1 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.1 | 5 | 3/7 | 0.1 | 3 | 1 | 8.7 | 50 |
| ai_security | AI 安全 | 7 | 9.1 | 10 | 4/7 | 3.6 | 2 | 7/7 | 1.1 | 2 | 0 | 7.8 | 15 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.3 | 1 | 4/7 | 2.1 | 4 | 1 | 7.6 | 9 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 8.9 | 6 | 7/7 | 0.0 | 1 | 29 | 9.0 | 26 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 20 | 18 | 66 | 1 | 20 | 43 | 1 | 18 | 0 |
| ai_security | 11 | 5 | 48 | 0 | 11 | 7 | 8 | 21 | 0 |
| finance | 1 | 0 | 68 | 1 | 1 | 0 | 15 | 0 | 0 |
| security | 10 | 0 | 66 | 29 | 10 | 0 | 0 | 50 | 0 |

## Target Misses

- 2026-06-29 security：selected 15/15，中文 11/6，unknown 4
- 2026-06-29 ai_security：selected 9/10，中文 4/2
- 2026-06-28 security：selected 15/15，中文 13/6，unknown 3
- 2026-06-27 security：selected 15/15，中文 8/6，unknown 2
- 2026-06-27 ai：selected 15/15，中文 4/5
- 2026-06-27 finance：selected 10/10，中文 0/1
- 2026-06-26 security：selected 15/15，中文 10/6，unknown 3
- 2026-06-26 ai：selected 15/15，中文 4/5
- 2026-06-26 finance：selected 10/10，中文 2/1，unknown 1
- 2026-06-25 security：selected 15/15，中文 6/6，unknown 5
- 2026-06-25 ai_security：selected 9/10，中文 3/2
- 2026-06-25 ai：selected 15/15，中文 2/5
- 2026-06-24 security：selected 15/15，中文 7/6，unknown 7
- 2026-06-24 ai：selected 15/15，中文 4/5，unknown 1
- 2026-06-24 finance：selected 10/10，中文 0/1
- 2026-06-23 security：selected 15/15，中文 7/6，unknown 5
- 2026-06-23 ai_security：selected 6/10，中文 2/2
- 2026-06-23 finance：selected 10/10，中文 0/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
