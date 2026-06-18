# Offline Strategy Eval

- generated_for: 2026-06-18
- dates: 2026-06-18, 2026-06-17, 2026-06-16, 2026-06-15, 2026-06-14, 2026-06-13, 2026-06-12

## Top Issues

- [ai_security] 2/7 天未满额，累计缺口约 7 条。
- [ai] 1/7 天未满额，累计缺口约 2 条。
- [ai_security] 中文目标 2/7 天达成。
- [ai] 中文目标 3/7 天达成。
- [finance] 中文目标 6/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.7 | 15 | 6/7 | 4.1 | 5 | 3/7 | 0.4 | 3 | 0 | 8.6 | 66 |
| ai_security | AI 安全 | 7 | 9.0 | 10 | 5/7 | 1.6 | 2 | 2/7 | 0.6 | 2 | 0 | 7.8 | 18 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.6 | 1 | 6/7 | 1.7 | 4 | 1 | 7.8 | 21 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.3 | 6 | 7/7 | 0.0 | 1 | 22 | 9.1 | 28 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 20 | 23 | 60 | 0 | 20 | 44 | 3 | 17 | 0 |
| ai_security | 15 | 3 | 45 | 0 | 15 | 13 | 4 | 11 | 0 |
| finance | 2 | 0 | 67 | 1 | 2 | 0 | 12 | 0 | 0 |
| security | 18 | 0 | 65 | 22 | 18 | 2 | 0 | 39 | 1 |

## Target Misses

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
- 2026-06-12 security：selected 15/15，中文 6/6，unknown 4
- 2026-06-12 ai_security：selected 10/10，中文 1/2
- 2026-06-12 ai：selected 13/15，中文 2/5
- 2026-06-12 finance：selected 10/10，中文 0/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
