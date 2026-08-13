# Offline Strategy Eval

- generated_for: 2026-08-14
- dates: 2026-08-14, 2026-08-13, 2026-08-12, 2026-08-11, 2026-08-10, 2026-08-09, 2026-08-08

## Top Issues

- [ai_security] 7/7 天未满额，累计缺口约 49 条。
- [finance] 1/7 天未满额，累计缺口约 2 条。
- [ai] 1/7 天未满额，累计缺口约 1 条。
- [ai_security] 中文目标 0/7 天达成。
- [ai] 中文目标 6/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.9 | 15 | 6/7 | 5.4 | 5 | 3 | 6/7 | 0.9 | 3 | 2 | 8.4 | 34 |
| ai_security | AI 安全 | 7 | 3.0 | 10 | 0/7 | 0.1 | 2 | 0 | 0/7 | 1.3 | 2 | 0 | 7.4 | 0 |
| finance | 金融科技 | 7 | 9.7 | 10 | 6/7 | 2.1 | 1 | 1 | 7/7 | 2.3 | 4 | 0 | 7.2 | 3 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.7 | 6 | 6 | 7/7 | 0.0 | 1 | 13 | 8.7 | 22 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 15 | 15 | 72 | 2 | 15 | 41 | 6 | 19 | 1 |
| ai_security | 1 | 0 | 20 | 0 | 1 | 3 | 9 | 0 | 0 |
| finance | 4 | 0 | 64 | 0 | 4 | 0 | 16 | 0 | 0 |
| security | 6 | 0 | 86 | 13 | 6 | 2 | 0 | 41 | 7 |

## Target Misses

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
- 2026-08-08 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-08 ai_security：selected 4/10，中文 0/2
- 2026-08-08 ai：selected 15/15，中文 3/5，unknown 2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
