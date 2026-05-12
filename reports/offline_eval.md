# Offline Strategy Eval

- generated_for: 2026-05-13
- dates: 2026-05-13, 2026-05-12, 2026-05-11, 2026-05-10, 2026-05-09, 2026-05-08, 2026-05-07

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.3 | 15 | 6/7 | 3.7 | 5 | 1/7 | 2.3 | 3 | 1 | 7.6 | 9 |
| ai_security | AI 安全 | 7 | 6.6 | 10 | 1/7 | 1.1 | 2 | 3/7 | 1.4 | 2 | 0 | 6.1 | 3 |
| finance | 金融科技 | 7 | 8.0 | 10 | 4/7 | 0.9 | 1 | 3/7 | 1.4 | 4 | 0 | 7.5 | 10 |
| security | 安全 | 7 | 14.6 | 15 | 5/7 | 4.1 | 6 | 2/7 | 0.0 | 1 | 1 | 8.9 | 25 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 18 | 13 | 68 | 1 | 18 | 30 | 16 | 1 | 2 |
| ai_security | 7 | 4 | 35 | 0 | 7 | 18 | 10 | 6 | 0 |
| finance | 6 | 0 | 50 | 0 | 6 | 0 | 10 | 0 | 0 |
| security | 9 | 0 | 92 | 1 | 9 | 4 | 0 | 28 | 22 |

## Target Misses

- 2026-05-13 security：selected 13/15，中文 3/6，unknown 1
- 2026-05-13 ai：selected 15/15，中文 4/5
- 2026-05-12 security：selected 15/15，中文 4/6
- 2026-05-12 ai_security：selected 9/10，中文 0/2，Google News 4/2
- 2026-05-12 ai：selected 15/15，中文 4/5
- 2026-05-11 ai_security：selected 7/10，中文 2/2
- 2026-05-11 ai：selected 15/15，中文 3/5，unknown 1
- 2026-05-10 security：selected 14/15，中文 2/6
- 2026-05-10 ai_security：selected 3/10，中文 0/2
- 2026-05-10 ai：selected 10/15，中文 3/5，Google News 4/3
- 2026-05-10 finance：selected 3/10，中文 0/1
- 2026-05-09 security：selected 15/15，中文 5/6
- 2026-05-09 ai_security：selected 5/10，中文 2/2
- 2026-05-09 ai：selected 15/15，中文 3/5
- 2026-05-09 finance：selected 7/10，中文 0/1
- 2026-05-08 security：selected 15/15，中文 0/6
- 2026-05-08 ai_security：selected 6/10，中文 0/2
- 2026-05-08 ai：selected 15/15，中文 4/5
- 2026-05-08 finance：selected 10/10，中文 0/1
- 2026-05-07 ai_security：selected 6/10，中文 1/2
- 2026-05-07 finance：selected 6/10，中文 0/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
