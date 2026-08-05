# Offline Strategy Eval

- generated_for: 2026-08-06
- dates: 2026-08-06, 2026-08-05, 2026-08-04, 2026-08-03, 2026-08-02, 2026-08-01, 2026-07-31

## Top Issues

- [ai_security] 6/7 天未满额，累计缺口约 26 条。
- [ai_security] 中文目标 1/7 天达成。
- [security] 中文目标 5/7 天达成。
- [ai] 中文目标 6/7 天达成。
- [finance] Google News 超限 1 天。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.3 | 5 | 4 | 6/7 | 0.7 | 3 | 2 | 8.5 | 22 |
| ai_security | AI 安全 | 7 | 6.3 | 10 | 1/7 | 0.7 | 2 | 0 | 1/7 | 1.4 | 2 | 0 | 7.0 | 10 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.4 | 1 | 1 | 7/7 | 2.4 | 4 | 0 | 7.3 | 1 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 5.7 | 6 | 5 | 5/7 | 0.0 | 1 | 11 | 8.3 | 19 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 13 | 15 | 75 | 2 | 13 | 39 | 5 | 17 | 0 |
| ai_security | 5 | 0 | 39 | 0 | 5 | 6 | 10 | 3 | 0 |
| finance | 8 | 0 | 62 | 0 | 8 | 0 | 17 | 0 | 0 |
| security | 7 | 0 | 87 | 11 | 7 | 3 | 0 | 36 | 12 |

## Target Misses

- 2026-08-06 security：selected 15/15，中文 6/6，unknown 1
- 2026-08-06 ai_security：selected 7/10，中文 0/2
- 2026-08-05 security：selected 15/15，中文 5/6，unknown 1
- 2026-08-05 ai_security：selected 7/10，中文 1/2
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

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
