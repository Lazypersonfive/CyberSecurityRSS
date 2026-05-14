# Offline Strategy Eval

- generated_for: 2026-05-15
- dates: 2026-05-15, 2026-05-14, 2026-05-13, 2026-05-12, 2026-05-11, 2026-05-10, 2026-05-09

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.3 | 15 | 6/7 | 3.4 | 5 | 0/7 | 2.4 | 3 | 1 | 7.8 | 19 |
| ai_security | AI 安全 | 7 | 7.7 | 10 | 3/7 | 1.7 | 2 | 5/7 | 1.1 | 2 | 0 | 6.8 | 4 |
| finance | 金融科技 | 7 | 8.6 | 10 | 5/7 | 1.7 | 1 | 5/7 | 1.9 | 4 | 0 | 7.4 | 13 |
| security | 安全 | 7 | 14.6 | 15 | 5/7 | 3.7 | 6 | 1/7 | 0.0 | 1 | 5 | 8.9 | 27 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 12 | 16 | 71 | 1 | 12 | 32 | 17 | 1 | 2 |
| ai_security | 10 | 3 | 41 | 0 | 10 | 20 | 8 | 11 | 0 |
| finance | 4 | 0 | 56 | 0 | 4 | 0 | 13 | 0 | 0 |
| security | 10 | 0 | 87 | 5 | 10 | 6 | 0 | 21 | 19 |

## Target Misses

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
- 2026-05-10 security：selected 14/15，中文 2/6
- 2026-05-10 ai_security：selected 3/10，中文 0/2
- 2026-05-10 ai：selected 10/15，中文 3/5，Google News 4/3
- 2026-05-10 finance：selected 3/10，中文 0/1
- 2026-05-09 security：selected 15/15，中文 5/6
- 2026-05-09 ai_security：selected 5/10，中文 2/2
- 2026-05-09 ai：selected 15/15，中文 3/5
- 2026-05-09 finance：selected 7/10，中文 0/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
