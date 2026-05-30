# Offline Strategy Eval

- generated_for: 2026-05-31
- dates: 2026-05-31, 2026-05-30, 2026-05-29, 2026-05-28, 2026-05-27, 2026-05-26, 2026-05-25

## Top Issues

- [ai_security] 2/7 天未满额，累计缺口约 3 条。
- [ai] 1/7 天未满额，累计缺口约 3 条。
- [security] 中文目标 3/7 天达成。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 3/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.6 | 15 | 6/7 | 3.7 | 5 | 3/7 | 1.0 | 3 | 0 | 7.9 | 32 |
| ai_security | AI 安全 | 7 | 9.6 | 10 | 5/7 | 1.1 | 2 | 3/7 | 0.9 | 2 | 0 | 7.1 | 5 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 0.9 | 1 | 5/7 | 1.1 | 4 | 0 | 7.7 | 16 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 4.6 | 6 | 3/7 | 0.0 | 1 | 7 | 8.5 | 19 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 13 | 19 | 70 | 0 | 13 | 42 | 7 | 0 | 1 |
| ai_security | 9 | 7 | 51 | 0 | 9 | 14 | 6 | 6 | 0 |
| finance | 3 | 0 | 67 | 0 | 3 | 0 | 8 | 0 | 0 |
| security | 18 | 0 | 80 | 7 | 18 | 6 | 0 | 25 | 22 |

## Target Misses

- 2026-05-31 security：selected 15/15，中文 4/6，unknown 1
- 2026-05-31 ai：selected 15/15，中文 4/5
- 2026-05-31 finance：selected 10/10，中文 0/1
- 2026-05-29 security：selected 15/15，中文 6/6，unknown 1
- 2026-05-29 ai：selected 15/15，中文 2/5
- 2026-05-28 security：selected 15/15，中文 2/6，unknown 2
- 2026-05-28 ai_security：selected 10/10，中文 0/2
- 2026-05-28 ai：selected 15/15，中文 2/5
- 2026-05-27 security：selected 15/15，中文 4/6，unknown 2
- 2026-05-27 ai_security：selected 9/10，中文 0/2
- 2026-05-27 ai：selected 15/15，中文 3/5
- 2026-05-27 finance：selected 10/10，中文 0/1
- 2026-05-26 security：selected 15/15，中文 6/6，unknown 1
- 2026-05-26 ai_security：selected 8/10，中文 0/2
- 2026-05-26 ai：selected 12/15，中文 5/5
- 2026-05-25 security：selected 15/15，中文 4/6
- 2026-05-25 ai_security：selected 10/10，中文 1/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
