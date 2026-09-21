# Offline Strategy Eval

- generated_for: 2026-09-21
- dates: 2026-09-21, 2026-09-17, 2026-09-14, 2026-09-10, 2026-09-07, 2026-09-03, 2026-08-31

## Top Issues

- [ai] 1/7 天未满额，累计缺口约 3 条。
- [ai_security] 1/7 天未满额，累计缺口约 1 条。
- [finance] 中文目标 5/7 天达成。
- [ai] 中文目标 5/7 天达成。
- [security] 入选 unknown source 4 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.6 | 15 | 6/7 | 4.7 | 5 | 4 | 5/7 | 1.6 | 3 | 2 | 7.7 | 35 |
| ai_security | AI 安全 | 7 | 9.9 | 10 | 6/7 | 4.1 | 2 | 2 | 7/7 | 0.0 | 2 | 3 | 8.4 | 9 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.0 | 2 | 1 | 5/7 | 1.3 | 3 | 0 | 7.7 | 2 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.4 | 6 | 6 | 7/7 | 0.0 | 1 | 4 | 8.5 | 10 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 16 | 70 | 2 | 14 | 38 | 11 | 7 | 0 |
| ai_security | 13 | 3 | 50 | 3 | 12 | 7 | 0 | 29 | 0 |
| finance | 10 | 3 | 57 | 0 | 10 | 3 | 9 | 0 | 0 |
| security | 13 | 0 | 88 | 4 | 10 | 1 | 0 | 50 | 2 |

## Target Misses

- 2026-09-21 ai：selected 15/15，中文 5/5，unknown 1
- 2026-09-17 security：selected 15/15，中文 6/6，unknown 1
- 2026-09-10 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-09-10 ai：selected 15/15，中文 4/5
- 2026-09-07 security：selected 15/15，中文 6/6，unknown 1
- 2026-09-07 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-09-07 ai：selected 12/15，中文 5/5
- 2026-09-03 ai：selected 15/15，中文 4/5，unknown 1
- 2026-09-03 finance：selected 10/10，中文 1/2
- 2026-08-31 security：selected 15/15，中文 6/6，unknown 2
- 2026-08-31 ai_security：selected 9/10，中文 3/2，unknown 1
- 2026-08-31 finance：selected 10/10，中文 1/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
