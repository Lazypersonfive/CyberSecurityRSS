# Offline Strategy Eval

- generated_for: 2026-06-01
- dates: 2026-06-01, 2026-05-31, 2026-05-30, 2026-05-29, 2026-05-28, 2026-05-27, 2026-05-26

## Top Issues

- [ai_security] 3/7 天未满额，累计缺口约 4 条。
- [ai] 2/7 天未满额，累计缺口约 4 条。
- [security] 中文目标 3/7 天达成。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 3/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.4 | 15 | 5/7 | 3.7 | 5 | 3/7 | 0.9 | 3 | 0 | 8.0 | 28 |
| ai_security | AI 安全 | 7 | 9.4 | 10 | 4/7 | 1.0 | 2 | 3/7 | 1.0 | 2 | 0 | 6.9 | 4 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 0.7 | 1 | 4/7 | 1.3 | 4 | 0 | 7.6 | 19 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 4.4 | 6 | 3/7 | 0.0 | 1 | 0 | 8.6 | 22 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 11 | 20 | 70 | 0 | 11 | 43 | 6 | 0 | 1 |
| ai_security | 7 | 5 | 54 | 0 | 7 | 11 | 7 | 6 | 0 |
| finance | 3 | 0 | 67 | 0 | 3 | 0 | 9 | 0 | 0 |
| security | 17 | 0 | 88 | 0 | 17 | 6 | 0 | 29 | 22 |

## Target Misses

- 2026-06-01 security：selected 15/15，中文 3/6
- 2026-06-01 ai_security：selected 9/10，中文 0/2
- 2026-06-01 ai：selected 14/15，中文 5/5
- 2026-06-01 finance：selected 10/10，中文 0/1
- 2026-05-31 security：selected 15/15，中文 4/6
- 2026-05-31 ai：selected 15/15，中文 4/5
- 2026-05-31 finance：selected 10/10，中文 0/1
- 2026-05-29 ai：selected 15/15，中文 2/5
- 2026-05-28 security：selected 15/15，中文 2/6
- 2026-05-28 ai_security：selected 10/10，中文 0/2
- 2026-05-28 ai：selected 15/15，中文 2/5
- 2026-05-27 security：selected 15/15，中文 4/6
- 2026-05-27 ai_security：selected 9/10，中文 0/2
- 2026-05-27 ai：selected 15/15，中文 3/5
- 2026-05-27 finance：selected 10/10，中文 0/1
- 2026-05-26 ai_security：selected 8/10，中文 0/2
- 2026-05-26 ai：selected 12/15，中文 5/5

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
