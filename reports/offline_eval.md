# Offline Strategy Eval

- generated_for: 2026-07-11
- dates: 2026-07-11, 2026-07-10, 2026-07-09, 2026-07-08, 2026-07-07, 2026-07-06, 2026-07-05

## Top Issues

- [ai] 2/7 天未满额，累计缺口约 8 条。
- [ai_security] 2/7 天未满额，累计缺口约 5 条。
- [ai] 中文目标 4/7 天达成。
- [finance] 中文目标 5/7 天达成。
- [ai_security] 中文目标 5/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 13.9 | 15 | 5/7 | 4.1 | 5 | 0 | 4/7 | 0.1 | 3 | 0 | 8.8 | 63 |
| ai_security | AI 安全 | 7 | 9.3 | 10 | 5/7 | 3.3 | 2 | 1 | 5/7 | 0.9 | 2 | 0 | 7.9 | 4 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.3 | 1 | 0 | 5/7 | 1.7 | 4 | 0 | 7.9 | 13 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 9.4 | 6 | 6 | 7/7 | 0.0 | 1 | 4 | 9.3 | 35 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 11 | 20 | 66 | 0 | 11 | 44 | 1 | 17 | 2 |
| ai_security | 1 | 0 | 64 | 0 | 1 | 3 | 6 | 22 | 0 |
| finance | 3 | 0 | 67 | 0 | 3 | 0 | 12 | 0 | 0 |
| security | 10 | 0 | 91 | 4 | 10 | 0 | 0 | 66 | 0 |

## Target Misses

- 2026-07-11 ai：selected 12/15，中文 1/5
- 2026-07-11 finance：selected 10/10，中文 0/1
- 2026-07-10 security：selected 15/15，中文 6/6，unknown 1
- 2026-07-10 ai：selected 10/15，中文 0/5
- 2026-07-10 finance：selected 10/10，中文 0/1
- 2026-07-09 ai：selected 15/15，中文 4/5
- 2026-07-07 security：selected 15/15，中文 10/6，unknown 1
- 2026-07-07 ai_security：selected 9/10，中文 1/2
- 2026-07-06 security：selected 15/15，中文 11/6，unknown 1
- 2026-07-06 ai_security：selected 6/10，中文 2/2
- 2026-07-05 security：selected 15/15，中文 11/6，unknown 1
- 2026-07-05 ai_security：selected 10/10，中文 1/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
