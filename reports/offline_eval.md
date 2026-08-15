# Offline Strategy Eval

- generated_for: 2026-08-16
- dates: 2026-08-16, 2026-08-15, 2026-08-14, 2026-08-13, 2026-08-12, 2026-08-11, 2026-08-10

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 52 条。
- [finance] 2/7 天未满额，累计缺口约 4 条。
- [ai] 1/7 天未满额，累计缺口约 1 条。
- [ai_security] 中文目标 0/7 天达成。
- [security] 入选 unknown source 11 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.9 | 15 | 6/7 | 5.6 | 5 | 5 | 7/7 | 1.0 | 3 | 0 | 8.5 | 32 |
| ai_security | AI 安全 | 7 | 2.6 | 10 | 0/7 | 0.1 | 2 | 0 | 0/7 | 1.1 | 2 | 0 | 6.9 | 1 |
| finance | 金融科技 | 7 | 9.4 | 10 | 5/7 | 2.1 | 1 | 1 | 7/7 | 2.3 | 4 | 0 | 7.1 | 3 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.3 | 6 | 6 | 7/7 | 0.0 | 1 | 11 | 8.7 | 19 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 17 | 14 | 73 | 0 | 17 | 40 | 7 | 20 | 1 |
| ai_security | 0 | 0 | 18 | 0 | 0 | 2 | 8 | 0 | 0 |
| finance | 3 | 0 | 63 | 0 | 3 | 0 | 16 | 0 | 0 |
| security | 5 | 0 | 89 | 11 | 5 | 0 | 0 | 46 | 11 |

## Target Misses

- 2026-08-16 ai_security：selected 1/10，中文 0/2
- 2026-08-16 finance：selected 8/10，中文 1/1
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

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
