# Offline Strategy Eval

- generated_for: 2026-07-16
- dates: 2026-07-16, 2026-07-15, 2026-07-14, 2026-07-13, 2026-07-12, 2026-07-11, 2026-07-10

## Top Issues

- [ai_security] 4/7 天未满额，累计缺口约 22 条。
- [ai] 2/7 天未满额，累计缺口约 8 条。
- [ai] 中文目标 3/7 天达成。
- [ai_security] 中文目标 4/7 天达成。
- [finance] 中文目标 5/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 13.9 | 15 | 5/7 | 3.9 | 5 | 0 | 3/7 | 0.9 | 3 | 2 | 8.6 | 72 |
| ai_security | AI 安全 | 7 | 6.9 | 10 | 3/7 | 2.7 | 2 | 0 | 4/7 | 0.9 | 2 | 0 | 7.9 | 4 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.4 | 1 | 0 | 5/7 | 2.0 | 4 | 0 | 7.8 | 8 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.6 | 6 | 6 | 7/7 | 0.0 | 1 | 1 | 8.8 | 32 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 12 | 17 | 66 | 2 | 12 | 39 | 6 | 15 | 0 |
| ai_security | 2 | 0 | 46 | 0 | 2 | 5 | 6 | 19 | 0 |
| finance | 14 | 0 | 56 | 0 | 14 | 0 | 14 | 0 | 0 |
| security | 11 | 0 | 93 | 1 | 11 | 1 | 0 | 52 | 4 |

## Target Misses

- 2026-07-16 ai_security：selected 5/10，中文 1/2
- 2026-07-16 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-15 ai_security：selected 4/10，中文 0/2
- 2026-07-15 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-14 ai_security：selected 5/10，中文 4/2
- 2026-07-13 security：selected 15/15，中文 6/6，unknown 1
- 2026-07-13 ai_security：selected 4/10，中文 1/2
- 2026-07-11 ai：selected 12/15，中文 1/5
- 2026-07-11 finance：selected 10/10，中文 0/1
- 2026-07-10 ai：selected 10/15，中文 0/5
- 2026-07-10 finance：selected 10/10，中文 0/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
