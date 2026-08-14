# Offline Strategy Eval

- generated_for: 2026-08-15
- dates: 2026-08-15, 2026-08-14, 2026-08-13, 2026-08-12, 2026-08-11, 2026-08-10, 2026-08-09

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 51 条。
- [finance] 1/7 天未满额，累计缺口约 2 条。
- [ai] 1/7 天未满额，累计缺口约 1 条。
- [ai_security] 中文目标 0/7 天达成。
- [security] 入选 unknown source 12 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.9 | 15 | 6/7 | 5.7 | 5 | 5 | 7/7 | 1.0 | 3 | 0 | 8.5 | 31 |
| ai_security | AI 安全 | 7 | 2.7 | 10 | 0/7 | 0.1 | 2 | 0 | 0/7 | 1.1 | 2 | 0 | 7.1 | 1 |
| finance | 金融科技 | 7 | 9.7 | 10 | 6/7 | 2.4 | 1 | 1 | 7/7 | 2.6 | 4 | 0 | 7.1 | 3 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.7 | 6 | 6 | 7/7 | 0.0 | 1 | 12 | 8.7 | 20 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 18 | 15 | 71 | 0 | 18 | 40 | 7 | 21 | 1 |
| ai_security | 0 | 0 | 19 | 0 | 0 | 2 | 8 | 0 | 0 |
| finance | 3 | 0 | 65 | 0 | 3 | 0 | 18 | 0 | 0 |
| security | 4 | 0 | 89 | 12 | 4 | 0 | 0 | 42 | 10 |

## Target Misses

- 2026-08-15 ai_security：selected 2/10，中文 0/2
- 2026-08-14 security：selected 15/15，中文 6/6，unknown 2
- 2026-08-14 ai_security：selected 1/10，中文 0/2
- 2026-08-13 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-13 ai_security：selected 5/10，中文 0/2
- 2026-08-12 security：selected 15/15，中文 7/6，unknown 4
- 2026-08-12 ai_security：selected 2/10，中文 0/2
- 2026-08-11 security：selected 15/15，中文 9/6，unknown 1
- 2026-08-11 ai_security：selected 4/10，中文 0/2
- 2026-08-11 ai：selected 14/15，中文 7/5
- 2026-08-10 security：selected 15/15，中文 7/6，unknown 3
- 2026-08-10 ai_security：selected 3/10，中文 1/2
- 2026-08-10 finance：selected 8/10，中文 4/1
- 2026-08-09 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-09 ai_security：selected 2/10，中文 0/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
