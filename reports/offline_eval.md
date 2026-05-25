# Offline Strategy Eval

- generated_for: 2026-05-25
- dates: 2026-05-25, 2026-05-24, 2026-05-23, 2026-05-22, 2026-05-21, 2026-05-20, 2026-05-19

## Top Issues

- [ai_security] 5/7 天未满额，累计缺口约 25 条。
- [ai] 3/7 天未满额，累计缺口约 7 条。
- [ai] 中文目标 2/7 天达成。
- [ai_security] 中文目标 4/7 天达成。
- [security] 中文目标 5/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.0 | 15 | 4/7 | 3.6 | 5 | 2/7 | 2.0 | 3 | 0 | 7.9 | 50 |
| ai_security | AI 安全 | 7 | 6.4 | 10 | 2/7 | 2.4 | 2 | 4/7 | 2.3 | 2 | 0 | 6.3 | 4 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.9 | 1 | 7/7 | 2.0 | 4 | 0 | 7.9 | 7 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.4 | 6 | 5/7 | 0.0 | 1 | 1 | 9.0 | 13 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 15 | 20 | 63 | 0 | 15 | 38 | 14 | 0 | 1 |
| ai_security | 5 | 0 | 40 | 0 | 5 | 5 | 16 | 15 | 0 |
| finance | 3 | 0 | 67 | 0 | 3 | 0 | 14 | 0 | 0 |
| security | 18 | 0 | 86 | 1 | 18 | 6 | 0 | 42 | 11 |

## Target Misses

- 2026-05-25 security：selected 15/15，中文 5/6，unknown 1
- 2026-05-25 ai_security：selected 5/10，中文 1/2，Google News 3/2
- 2026-05-25 ai：selected 13/15，中文 5/5
- 2026-05-24 ai_security：selected 6/10，中文 3/2
- 2026-05-24 ai：selected 14/15，中文 6/5，Google News 4/3
- 2026-05-23 ai_security：selected 9/10，中文 5/2
- 2026-05-23 ai：selected 15/15，中文 3/5
- 2026-05-22 ai：selected 15/15，中文 4/5
- 2026-05-21 ai_security：selected 10/10，中文 3/2，Google News 3/2
- 2026-05-21 ai：selected 15/15，中文 2/5
- 2026-05-20 ai_security：selected 3/10，中文 0/2，Google News 3/2
- 2026-05-20 ai：selected 11/15，中文 2/5
- 2026-05-19 security：selected 15/15，中文 5/6
- 2026-05-19 ai_security：selected 2/10，中文 0/2
- 2026-05-19 ai：selected 15/15，中文 3/5

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
