# Offline Strategy Eval

- generated_for: 2026-08-18
- dates: 2026-08-18, 2026-08-17, 2026-08-16, 2026-08-15, 2026-08-14, 2026-08-13, 2026-08-12

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 54 条。
- [finance] 1/7 天未满额，累计缺口约 2 条。
- [ai_security] 中文目标 0/7 天达成。
- [finance] Google News 超限 1 天。
- [security] 入选 unknown source 7 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.6 | 5 | 5 | 7/7 | 0.7 | 3 | 0 | 8.5 | 29 |
| ai_security | AI 安全 | 7 | 2.3 | 10 | 0/7 | 0.3 | 2 | 0 | 0/7 | 0.9 | 2 | 0 | 7.0 | 1 |
| finance | 金融科技 | 7 | 9.7 | 10 | 6/7 | 2.3 | 1 | 1 | 7/7 | 2.4 | 4 | 0 | 7.1 | 2 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.1 | 6 | 6 | 7/7 | 0.0 | 1 | 7 | 8.7 | 17 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 21 | 12 | 72 | 0 | 21 | 40 | 5 | 19 | 1 |
| ai_security | 1 | 0 | 15 | 0 | 1 | 1 | 6 | 1 | 0 |
| finance | 5 | 0 | 63 | 0 | 5 | 0 | 17 | 0 | 0 |
| security | 2 | 0 | 96 | 7 | 2 | 0 | 0 | 46 | 12 |

## Target Misses

- 2026-08-18 ai_security：selected 3/10，中文 1/2
- 2026-08-17 ai_security：selected 2/10，中文 1/2
- 2026-08-17 finance：selected 10/10，中文 5/1，Google News 5/4
- 2026-08-16 ai_security：selected 1/10，中文 0/2
- 2026-08-16 finance：selected 8/10，中文 1/1
- 2026-08-15 ai_security：selected 2/10，中文 0/2
- 2026-08-14 security：selected 15/15，中文 6/6，unknown 2
- 2026-08-14 ai_security：selected 1/10，中文 0/2
- 2026-08-13 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-13 ai_security：selected 5/10，中文 0/2
- 2026-08-12 security：selected 15/15，中文 7/6，unknown 4
- 2026-08-12 ai_security：selected 2/10，中文 0/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
