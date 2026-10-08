# Offline Strategy Eval

- generated_for: 2026-10-08
- dates: 2026-10-08, 2026-10-05, 2026-10-01, 2026-09-28, 2026-09-21, 2026-09-17, 2026-09-14

## Top Issues

- [ai_security] 1/7 天未满额，累计缺口约 4 条。
- [ai_security] 中文目标 6/7 天达成。
- [ai] 中文目标 6/7 天达成。
- [security] 入选 unknown source 6 条，需登记或降权。
- [ai] 入选 unknown source 2 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.1 | 5 | 4 | 6/7 | 1.1 | 3 | 2 | 8.0 | 30 |
| ai_security | AI 安全 | 7 | 9.4 | 10 | 6/7 | 4.0 | 2 | 0 | 6/7 | 0.0 | 2 | 1 | 8.3 | 5 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.4 | 2 | 2 | 7/7 | 1.3 | 3 | 0 | 8.1 | 5 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.0 | 6 | 6 | 7/7 | 0.0 | 1 | 6 | 8.5 | 11 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 12 | 21 | 70 | 2 | 12 | 41 | 8 | 9 | 0 |
| ai_security | 8 | 6 | 51 | 1 | 7 | 11 | 0 | 28 | 0 |
| finance | 18 | 2 | 50 | 0 | 18 | 2 | 9 | 0 | 0 |
| security | 16 | 0 | 83 | 6 | 13 | 3 | 0 | 43 | 1 |

## Target Misses

- 2026-10-08 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-10-05 security：selected 15/15，中文 6/6，unknown 3
- 2026-10-05 ai_security：selected 6/10，中文 0/2
- 2026-10-05 ai：selected 15/15，中文 4/5，unknown 1
- 2026-10-01 security：selected 15/15，中文 6/6，unknown 1
- 2026-09-28 security：selected 15/15，中文 6/6，unknown 1
- 2026-09-21 ai：selected 15/15，中文 5/5，unknown 1
- 2026-09-17 security：selected 15/15，中文 6/6，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
