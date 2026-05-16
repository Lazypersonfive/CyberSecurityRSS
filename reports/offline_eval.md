# Offline Strategy Eval

- generated_for: 2026-05-17
- dates: 2026-05-17, 2026-05-16, 2026-05-15, 2026-05-14, 2026-05-13, 2026-05-12, 2026-05-11

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.0 | 5 | 2/7 | 1.9 | 3 | 1 | 7.8 | 28 |
| ai_security | AI 安全 | 7 | 9.4 | 10 | 5/7 | 1.6 | 2 | 4/7 | 1.1 | 2 | 0 | 6.8 | 11 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.1 | 1 | 7/7 | 2.3 | 4 | 0 | 7.5 | 14 |
| security | 安全 | 7 | 14.7 | 15 | 6/7 | 3.9 | 6 | 1/7 | 0.0 | 1 | 8 | 8.9 | 32 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 16 | 15 | 73 | 1 | 16 | 36 | 13 | 1 | 1 |
| ai_security | 14 | 4 | 48 | 0 | 14 | 28 | 8 | 11 | 0 |
| finance | 3 | 0 | 67 | 0 | 3 | 0 | 16 | 0 | 0 |
| security | 12 | 0 | 83 | 8 | 12 | 6 | 0 | 19 | 12 |

## Target Misses

- 2026-05-17 security：selected 15/15，中文 3/6，unknown 1
- 2026-05-17 ai_security：selected 10/10，中文 0/2，Google News 3/2
- 2026-05-16 security：selected 15/15，中文 5/6，unknown 2
- 2026-05-16 ai_security：selected 10/10，中文 1/2
- 2026-05-15 security：selected 15/15，中文 3/6，unknown 2
- 2026-05-15 ai：selected 15/15，中文 3/5
- 2026-05-14 security：selected 15/15，中文 3/6，unknown 2
- 2026-05-14 ai：selected 15/15，中文 4/5
- 2026-05-13 security：selected 13/15，中文 3/6，unknown 1
- 2026-05-13 ai：selected 15/15，中文 4/5
- 2026-05-12 security：selected 15/15，中文 4/6
- 2026-05-12 ai_security：selected 9/10，中文 0/2，Google News 4/2
- 2026-05-12 ai：selected 15/15，中文 4/5
- 2026-05-11 ai_security：selected 7/10，中文 2/2
- 2026-05-11 ai：selected 15/15，中文 3/5，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
