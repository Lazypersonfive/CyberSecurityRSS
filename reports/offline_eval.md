# Offline Strategy Eval

- generated_for: 2026-06-09
- dates: 2026-06-09, 2026-06-08, 2026-06-07, 2026-06-06, 2026-06-05, 2026-06-04, 2026-06-03

## Top Issues

- [ai] 1/7 天未满额，累计缺口约 3 条。
- [ai_security] 1/7 天未满额，累计缺口约 1 条。
- [security] 中文目标 1/7 天达成。
- [ai] 中文目标 2/7 天达成。
- [ai_security] 中文目标 3/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.6 | 15 | 6/7 | 3.1 | 5 | 2/7 | 1.3 | 3 | 0 | 7.8 | 41 |
| ai_security | AI 安全 | 7 | 9.9 | 10 | 6/7 | 1.9 | 2 | 3/7 | 1.0 | 2 | 0 | 7.1 | 10 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.6 | 1 | 7/7 | 2.6 | 4 | 0 | 7.7 | 9 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 4.4 | 6 | 1/7 | 0.0 | 1 | 6 | 8.0 | 18 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 12 | 20 | 70 | 0 | 12 | 36 | 9 | 0 | 0 |
| ai_security | 12 | 0 | 57 | 0 | 12 | 3 | 7 | 13 | 0 |
| finance | 3 | 0 | 67 | 0 | 3 | 0 | 18 | 0 | 0 |
| security | 15 | 0 | 84 | 6 | 15 | 3 | 0 | 29 | 18 |

## Target Misses

- 2026-06-09 security：selected 15/15，中文 4/6，unknown 3
- 2026-06-09 ai_security：selected 9/10，中文 1/2
- 2026-06-09 ai：selected 15/15，中文 1/5
- 2026-06-08 security：selected 15/15，中文 5/6
- 2026-06-08 ai：selected 12/15，中文 3/5
- 2026-06-07 security：selected 15/15，中文 5/6，unknown 1
- 2026-06-07 ai：selected 15/15，中文 4/5
- 2026-06-05 security：selected 15/15，中文 4/6，unknown 2
- 2026-06-05 ai_security：selected 10/10，中文 1/2
- 2026-06-05 ai：selected 15/15，中文 2/5
- 2026-06-04 security：selected 15/15，中文 4/6
- 2026-06-04 ai_security：selected 10/10，中文 1/2
- 2026-06-04 ai：selected 15/15，中文 2/5
- 2026-06-03 security：selected 15/15，中文 3/6
- 2026-06-03 ai_security：selected 10/10，中文 0/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
