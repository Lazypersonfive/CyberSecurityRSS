# Offline Strategy Eval

- generated_for: 2026-07-18
- dates: 2026-07-18, 2026-07-17, 2026-07-16, 2026-07-15, 2026-07-14, 2026-07-13, 2026-07-12

## Top Issues

- [ai_security] 6/7 天未满额，累计缺口约 33 条。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 4/7 天达成。
- [ai] 入选 unknown source 6 条，需登记或降权。
- [security] 入选 unknown source 1 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 4.9 | 5 | 3 | 4/7 | 1.4 | 3 | 6 | 8.3 | 46 |
| ai_security | AI 安全 | 7 | 5.3 | 10 | 1/7 | 1.6 | 2 | 0 | 3/7 | 1.0 | 2 | 0 | 7.7 | 3 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.0 | 1 | 1 | 7/7 | 2.4 | 4 | 0 | 7.8 | 3 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.0 | 6 | 6 | 7/7 | 0.0 | 1 | 1 | 8.7 | 19 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 15 | 70 | 6 | 14 | 38 | 10 | 14 | 0 |
| ai_security | 4 | 0 | 33 | 0 | 4 | 5 | 7 | 11 | 0 |
| finance | 18 | 0 | 52 | 0 | 18 | 0 | 17 | 0 | 0 |
| security | 10 | 0 | 94 | 1 | 10 | 3 | 0 | 48 | 6 |

## Target Misses

- 2026-07-18 ai_security：selected 2/10，中文 2/2
- 2026-07-18 ai：selected 15/15，中文 5/5，unknown 3
- 2026-07-17 ai_security：selected 7/10，中文 0/2
- 2026-07-17 ai：selected 15/15，中文 3/5，unknown 1
- 2026-07-16 ai_security：selected 5/10，中文 1/2
- 2026-07-16 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-15 ai_security：selected 4/10，中文 0/2
- 2026-07-15 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-14 ai_security：selected 5/10，中文 4/2
- 2026-07-13 security：selected 15/15，中文 6/6，unknown 1
- 2026-07-13 ai_security：selected 4/10，中文 1/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
