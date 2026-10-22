# Offline Strategy Eval

- generated_for: 2026-10-22
- dates: 2026-10-22, 2026-10-19, 2026-10-15, 2026-10-12, 2026-10-08, 2026-10-05, 2026-10-01

## Top Issues

- [ai_security] 1/7 天未满额，累计缺口约 4 条。
- [ai] 中文目标 4/7 天达成。
- [ai_security] 中文目标 6/7 天达成。
- [security] 入选 unknown source 4 条，需登记或降权。
- [ai_security] 入选 unknown source 3 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.6 | 5 | 3 | 4/7 | 0.9 | 3 | 2 | 8.1 | 37 |
| ai_security | AI 安全 | 7 | 9.4 | 10 | 6/7 | 3.3 | 2 | 0 | 6/7 | 0.0 | 2 | 3 | 8.1 | 6 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.4 | 2 | 2 | 7/7 | 1.0 | 3 | 0 | 7.8 | 3 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.4 | 6 | 6 | 7/7 | 0.0 | 1 | 4 | 8.7 | 17 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 17 | 14 | 72 | 2 | 17 | 43 | 6 | 4 | 0 |
| ai_security | 14 | 4 | 45 | 3 | 10 | 11 | 0 | 23 | 0 |
| finance | 18 | 3 | 49 | 0 | 18 | 3 | 7 | 0 | 0 |
| security | 10 | 0 | 91 | 4 | 9 | 6 | 0 | 48 | 0 |

## Target Misses

- 2026-10-22 ai：selected 15/15，中文 3/5
- 2026-10-19 ai_security：selected 10/10，中文 4/2，unknown 1
- 2026-10-19 ai：selected 15/15，中文 3/5，unknown 1
- 2026-10-12 ai_security：selected 10/10，中文 6/2，unknown 1
- 2026-10-08 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-10-05 security：selected 15/15，中文 6/6，unknown 3
- 2026-10-05 ai_security：selected 6/10，中文 0/2
- 2026-10-05 ai：selected 15/15，中文 4/5，unknown 1
- 2026-10-01 security：selected 15/15，中文 6/6，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
