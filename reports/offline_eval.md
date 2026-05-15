# Offline Strategy Eval

- generated_for: 2026-05-16
- dates: 2026-05-16, 2026-05-15, 2026-05-14, 2026-05-13, 2026-05-12, 2026-05-11, 2026-05-10

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.3 | 15 | 6/7 | 3.7 | 5 | 1/7 | 2.1 | 3 | 1 | 7.8 | 23 |
| ai_security | AI 安全 | 7 | 8.4 | 10 | 4/7 | 1.6 | 2 | 4/7 | 0.9 | 2 | 0 | 6.9 | 9 |
| finance | 金融科技 | 7 | 9.0 | 10 | 6/7 | 2.0 | 1 | 6/7 | 2.0 | 4 | 0 | 7.5 | 14 |
| security | 安全 | 7 | 14.6 | 15 | 5/7 | 3.7 | 6 | 1/7 | 0.0 | 1 | 7 | 8.9 | 29 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 16 | 69 | 1 | 14 | 34 | 15 | 1 | 2 |
| ai_security | 13 | 4 | 42 | 0 | 13 | 24 | 6 | 11 | 0 |
| finance | 3 | 0 | 60 | 0 | 3 | 0 | 14 | 0 | 0 |
| security | 11 | 0 | 84 | 7 | 11 | 5 | 0 | 19 | 16 |

## Target Misses

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
- 2026-05-10 security：selected 14/15，中文 2/6
- 2026-05-10 ai_security：selected 3/10，中文 0/2
- 2026-05-10 ai：selected 10/15，中文 3/5，Google News 4/3
- 2026-05-10 finance：selected 3/10，中文 0/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
