# Offline Strategy Eval

- generated_for: 2026-07-04
- dates: 2026-07-04, 2026-07-03, 2026-07-02, 2026-07-01, 2026-06-30, 2026-06-29, 2026-06-28

## Top Issues

- [ai_security] 3/7 天未满额，累计缺口约 5 条。
- [ai] 中文目标 3/7 天达成。
- [ai_security] 中文目标 5/7 天达成。
- [security] 入选 unknown source 12 条，需登记或降权。
- [finance] 入选 unknown source 1 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.3 | 5 | 3 | 3/7 | 0.7 | 3 | 1 | 8.5 | 50 |
| ai_security | AI 安全 | 7 | 9.3 | 10 | 4/7 | 2.3 | 2 | 1 | 5/7 | 1.1 | 2 | 0 | 7.7 | 1 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.0 | 1 | 1 | 7/7 | 2.3 | 4 | 1 | 7.6 | 14 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 10.0 | 6 | 9 | 7/7 | 0.0 | 1 | 12 | 8.9 | 29 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 20 | 13 | 71 | 1 | 20 | 43 | 5 | 17 | 0 |
| ai_security | 8 | 0 | 57 | 0 | 8 | 5 | 8 | 14 | 0 |
| finance | 1 | 0 | 68 | 1 | 1 | 0 | 16 | 0 | 0 |
| security | 3 | 0 | 90 | 12 | 3 | 2 | 0 | 69 | 1 |

## Target Misses

- 2026-07-04 security：selected 15/15，中文 9/6，unknown 3
- 2026-07-04 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-04 finance：selected 10/10，中文 3/1，unknown 1
- 2026-07-03 security：selected 15/15，中文 10/6，unknown 1
- 2026-07-03 ai：selected 15/15，中文 3/5
- 2026-07-02 security：selected 15/15，中文 9/6，unknown 1
- 2026-07-02 ai_security：selected 10/10，中文 1/2
- 2026-07-02 ai：selected 15/15，中文 4/5
- 2026-07-01 security：selected 15/15，中文 9/6，unknown 1
- 2026-07-01 ai_security：selected 7/10，中文 1/2
- 2026-07-01 ai：selected 15/15，中文 4/5
- 2026-06-30 security：selected 15/15，中文 9/6，unknown 3
- 2026-06-30 ai_security：selected 9/10，中文 2/2
- 2026-06-29 security：selected 15/15，中文 11/6，unknown 2
- 2026-06-29 ai_security：selected 9/10，中文 4/2
- 2026-06-28 security：selected 15/15，中文 13/6，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
