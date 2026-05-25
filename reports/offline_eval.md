# Offline Strategy Eval

- generated_for: 2026-05-26
- dates: 2026-05-26, 2026-05-25, 2026-05-24, 2026-05-23, 2026-05-22, 2026-05-21, 2026-05-20

## Top Issues

- [ai_security] 4/7 天未满额，累计缺口约 14 条。
- [ai] 3/7 天未满额，累计缺口约 8 条。
- [ai] 中文目标 3/7 天达成。
- [ai_security] 中文目标 4/7 天达成。
- [security] 中文目标 6/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 13.9 | 15 | 4/7 | 3.9 | 5 | 3/7 | 1.7 | 3 | 0 | 7.6 | 49 |
| ai_security | AI 安全 | 7 | 8.0 | 10 | 3/7 | 2.4 | 2 | 4/7 | 2.0 | 2 | 0 | 6.6 | 6 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.6 | 1 | 7/7 | 1.7 | 4 | 0 | 7.8 | 8 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.4 | 6 | 6/7 | 0.0 | 1 | 1 | 8.9 | 12 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 13 | 19 | 65 | 0 | 13 | 39 | 12 | 0 | 1 |
| ai_security | 7 | 3 | 46 | 0 | 7 | 10 | 14 | 15 | 0 |
| finance | 3 | 0 | 67 | 0 | 3 | 0 | 12 | 0 | 0 |
| security | 16 | 0 | 88 | 1 | 16 | 8 | 0 | 41 | 13 |

## Target Misses

- 2026-05-26 security：selected 15/15，中文 6/6，unknown 1
- 2026-05-26 ai_security：selected 8/10，中文 0/2
- 2026-05-26 ai：selected 12/15，中文 5/5
- 2026-05-25 security：selected 15/15，中文 4/6
- 2026-05-25 ai_security：selected 10/10，中文 1/2
- 2026-05-24 ai_security：selected 6/10，中文 3/2
- 2026-05-24 ai：selected 14/15，中文 6/5，Google News 4/3
- 2026-05-23 ai_security：selected 9/10，中文 5/2
- 2026-05-23 ai：selected 15/15，中文 3/5
- 2026-05-22 ai：selected 15/15，中文 4/5
- 2026-05-21 ai_security：selected 10/10，中文 3/2，Google News 3/2
- 2026-05-21 ai：selected 15/15，中文 2/5
- 2026-05-20 ai_security：selected 3/10，中文 0/2，Google News 3/2
- 2026-05-20 ai：selected 11/15，中文 2/5

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
