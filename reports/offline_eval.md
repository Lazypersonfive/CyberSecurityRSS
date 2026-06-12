# Offline Strategy Eval

- generated_for: 2026-06-12
- dates: 2026-06-12, 2026-06-11, 2026-06-10, 2026-06-09, 2026-06-08, 2026-06-07, 2026-06-06

## Top Issues

- [ai] 4/7 天未满额，累计缺口约 11 条。
- [ai_security] 1/7 天未满额，累计缺口约 1 条。
- [ai] 中文目标 1/7 天达成。
- [security] 中文目标 3/7 天达成。
- [ai_security] 中文目标 3/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 13.4 | 15 | 3/7 | 2.9 | 5 | 1/7 | 0.9 | 3 | 0 | 7.9 | 65 |
| ai_security | AI 安全 | 7 | 9.9 | 10 | 6/7 | 2.0 | 2 | 3/7 | 1.1 | 2 | 0 | 7.2 | 10 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.3 | 1 | 6/7 | 2.1 | 4 | 0 | 7.9 | 10 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 5.0 | 6 | 3/7 | 0.0 | 1 | 6 | 8.5 | 23 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 16 | 64 | 0 | 14 | 37 | 6 | 0 | 0 |
| ai_security | 12 | 0 | 57 | 0 | 12 | 9 | 8 | 14 | 0 |
| finance | 3 | 0 | 67 | 0 | 3 | 0 | 15 | 0 | 0 |
| security | 17 | 0 | 82 | 6 | 17 | 2 | 0 | 33 | 14 |

## Target Misses

- 2026-06-12 security：selected 15/15，中文 6/6，unknown 4
- 2026-06-12 ai_security：selected 10/10，中文 1/2
- 2026-06-12 ai：selected 13/15，中文 2/5
- 2026-06-12 finance：selected 10/10，中文 0/1
- 2026-06-11 security：selected 15/15，中文 8/6，unknown 2
- 2026-06-11 ai_security：selected 10/10，中文 1/2
- 2026-06-11 ai：selected 10/15，中文 3/5
- 2026-06-10 security：selected 15/15，中文 1/6
- 2026-06-10 ai_security：selected 10/10，中文 1/2
- 2026-06-10 ai：selected 14/15，中文 2/5
- 2026-06-09 security：selected 15/15，中文 4/6
- 2026-06-09 ai_security：selected 9/10，中文 1/2
- 2026-06-09 ai：selected 15/15，中文 1/5
- 2026-06-08 security：selected 15/15，中文 5/6
- 2026-06-08 ai：selected 12/15，中文 3/5
- 2026-06-07 security：selected 15/15，中文 5/6
- 2026-06-07 ai：selected 15/15，中文 4/5

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
