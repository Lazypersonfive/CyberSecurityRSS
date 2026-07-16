# Offline Strategy Eval

- generated_for: 2026-07-17
- dates: 2026-07-17, 2026-07-16, 2026-07-15, 2026-07-14, 2026-07-13, 2026-07-12, 2026-07-11

## Top Issues

- [ai_security] 5/7 天未满额，累计缺口约 25 条。
- [ai] 1/7 天未满额，累计缺口约 3 条。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 3/7 天达成。
- [finance] 中文目标 6/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.6 | 15 | 6/7 | 4.3 | 5 | 1 | 3/7 | 1.3 | 3 | 3 | 8.4 | 61 |
| ai_security | AI 安全 | 7 | 6.4 | 10 | 2/7 | 2.0 | 2 | 0 | 3/7 | 1.1 | 2 | 0 | 7.7 | 4 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.6 | 1 | 0 | 6/7 | 2.1 | 4 | 0 | 7.9 | 7 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.6 | 6 | 6 | 7/7 | 0.0 | 1 | 1 | 8.8 | 23 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 12 | 19 | 68 | 3 | 12 | 39 | 9 | 15 | 0 |
| ai_security | 4 | 0 | 41 | 0 | 4 | 6 | 8 | 14 | 0 |
| finance | 17 | 0 | 53 | 0 | 17 | 0 | 15 | 0 | 0 |
| security | 13 | 0 | 91 | 1 | 13 | 1 | 0 | 52 | 4 |

## Target Misses

- 2026-07-17 ai_security：selected 7/10，中文 0/2
- 2026-07-17 ai：selected 15/15，中文 3/5，unknown 1
- 2026-07-16 ai_security：selected 5/10，中文 1/2
- 2026-07-16 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-15 ai_security：selected 4/10，中文 0/2
- 2026-07-15 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-14 ai_security：selected 5/10，中文 4/2
- 2026-07-13 security：selected 15/15，中文 6/6，unknown 1
- 2026-07-13 ai_security：selected 4/10，中文 1/2
- 2026-07-11 ai：selected 12/15，中文 1/5
- 2026-07-11 finance：selected 10/10，中文 0/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
