# Offline Strategy Eval

- generated_for: 2026-06-15
- dates: 2026-06-15, 2026-06-14, 2026-06-13, 2026-06-12, 2026-06-11, 2026-06-10, 2026-06-09

## Top Issues

- [ai_security] 3/7 天未满额，累计缺口约 8 条。
- [ai] 3/7 天未满额，累计缺口约 8 条。
- [ai_security] 中文目标 0/7 天达成。
- [ai] 中文目标 2/7 天达成。
- [security] 中文目标 5/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 13.9 | 15 | 4/7 | 3.4 | 5 | 2/7 | 0.7 | 3 | 0 | 8.4 | 83 |
| ai_security | AI 安全 | 7 | 8.9 | 10 | 4/7 | 0.9 | 2 | 0/7 | 1.0 | 2 | 0 | 7.1 | 11 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.6 | 1 | 6/7 | 2.0 | 4 | 0 | 7.9 | 15 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 5.9 | 6 | 5/7 | 0.0 | 1 | 13 | 8.8 | 28 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 22 | 61 | 0 | 14 | 41 | 5 | 12 | 0 |
| ai_security | 12 | 0 | 50 | 0 | 12 | 16 | 7 | 6 | 0 |
| finance | 3 | 0 | 67 | 0 | 3 | 0 | 14 | 0 | 0 |
| security | 19 | 0 | 73 | 13 | 19 | 3 | 0 | 35 | 8 |

## Target Misses

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
- 2026-06-11 security：selected 15/15，中文 8/6，unknown 2
- 2026-06-11 ai_security：selected 10/10，中文 1/2
- 2026-06-11 ai：selected 10/15，中文 3/5
- 2026-06-10 security：selected 15/15，中文 1/6
- 2026-06-10 ai_security：selected 10/10，中文 1/2
- 2026-06-10 ai：selected 14/15，中文 2/5
- 2026-06-09 security：selected 15/15，中文 4/6
- 2026-06-09 ai_security：selected 9/10，中文 1/2
- 2026-06-09 ai：selected 15/15，中文 1/5

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
