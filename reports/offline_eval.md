# Offline Strategy Eval

- generated_for: 2026-08-04
- dates: 2026-08-04, 2026-08-03, 2026-08-02, 2026-08-01, 2026-07-31, 2026-07-30, 2026-07-29

## Top Issues

- [ai_security] 6/7 天未满额，累计缺口约 29 条。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 5/7 天达成。
- [security] 中文目标 6/7 天达成。
- [finance] Google News 超限 1 天。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.1 | 5 | 4 | 5/7 | 0.9 | 3 | 3 | 8.4 | 27 |
| ai_security | AI 安全 | 7 | 5.9 | 10 | 1/7 | 1.3 | 2 | 0 | 3/7 | 1.4 | 2 | 0 | 7.3 | 9 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.4 | 1 | 1 | 7/7 | 2.4 | 4 | 0 | 7.3 | 2 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 5.9 | 6 | 5 | 6/7 | 0.0 | 1 | 10 | 8.3 | 18 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 11 | 13 | 78 | 3 | 11 | 37 | 6 | 15 | 0 |
| ai_security | 3 | 1 | 37 | 0 | 3 | 6 | 10 | 7 | 0 |
| finance | 9 | 0 | 61 | 0 | 9 | 0 | 17 | 0 | 0 |
| security | 8 | 0 | 87 | 10 | 8 | 1 | 0 | 38 | 11 |

## Target Misses

- 2026-08-04 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-04 ai_security：selected 5/10，中文 0/2
- 2026-08-03 security：selected 15/15，中文 6/6，unknown 4
- 2026-08-03 ai_security：selected 2/10，中文 0/2
- 2026-08-02 ai_security：selected 8/10，中文 1/2
- 2026-08-02 finance：selected 10/10，中文 5/1，Google News 5/4
- 2026-08-01 security：selected 15/15，中文 6/6，unknown 2
- 2026-08-01 ai：selected 15/15，中文 4/5
- 2026-07-31 security：selected 15/15，中文 5/6，unknown 2
- 2026-07-31 ai_security：selected 5/10，中文 1/2
- 2026-07-31 ai：selected 15/15，中文 5/5，unknown 2
- 2026-07-30 security：selected 15/15，中文 6/6，unknown 1
- 2026-07-30 ai_security：selected 5/10，中文 2/2
- 2026-07-30 ai：selected 15/15，中文 4/5，unknown 1
- 2026-07-29 ai_security：selected 6/10，中文 3/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
