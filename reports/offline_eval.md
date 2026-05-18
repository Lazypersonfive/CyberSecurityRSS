# Offline Strategy Eval

- generated_for: 2026-05-19
- dates: 2026-05-19, 2026-05-18, 2026-05-17, 2026-05-16, 2026-05-15, 2026-05-14, 2026-05-13

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.3 | 15 | 6/7 | 3.9 | 5 | 2/7 | 2.1 | 3 | 2 | 7.8 | 37 |
| ai_security | AI 安全 | 7 | 8.6 | 10 | 5/7 | 1.3 | 2 | 3/7 | 1.3 | 2 | 0 | 6.7 | 10 |
| finance | 金融科技 | 7 | 9.9 | 10 | 6/7 | 2.6 | 1 | 7/7 | 2.7 | 4 | 0 | 7.3 | 6 |
| security | 安全 | 7 | 14.7 | 15 | 6/7 | 3.4 | 6 | 0/7 | 0.0 | 1 | 1 | 8.9 | 28 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 11 | 14 | 73 | 2 | 11 | 34 | 15 | 1 | 0 |
| ai_security | 16 | 3 | 41 | 0 | 16 | 22 | 9 | 9 | 0 |
| finance | 1 | 0 | 68 | 0 | 1 | 0 | 19 | 0 | 0 |
| security | 15 | 0 | 87 | 1 | 15 | 6 | 0 | 19 | 18 |

## Target Misses

- 2026-05-19 security：selected 15/15，中文 5/6，unknown 1
- 2026-05-19 ai_security：selected 2/10，中文 0/2
- 2026-05-19 ai：selected 15/15，中文 3/5，unknown 2
- 2026-05-18 security：selected 15/15，中文 2/6
- 2026-05-18 ai_security：selected 8/10，中文 0/2，Google News 3/2
- 2026-05-18 ai：selected 10/15，中文 3/5，Google News 5/3
- 2026-05-18 finance：selected 9/10，中文 4/1
- 2026-05-17 security：selected 15/15，中文 3/6
- 2026-05-17 ai_security：selected 10/10，中文 0/2，Google News 3/2
- 2026-05-16 security：selected 15/15，中文 5/6
- 2026-05-16 ai_security：selected 10/10，中文 1/2
- 2026-05-15 security：selected 15/15，中文 3/6
- 2026-05-15 ai：selected 15/15，中文 3/5
- 2026-05-14 security：selected 15/15，中文 3/6
- 2026-05-14 ai：selected 15/15，中文 4/5
- 2026-05-13 security：selected 13/15，中文 3/6
- 2026-05-13 ai：selected 15/15，中文 4/5

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
