# Offline Strategy Eval

- generated_for: 2026-08-02
- dates: 2026-08-02, 2026-08-01, 2026-07-31, 2026-07-30, 2026-07-29, 2026-07-28, 2026-07-27

## Top Issues

- [ai_security] 6/7 天未满额，累计缺口约 31 条。
- [finance] 1/7 天未满额，累计缺口约 4 条。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 5/7 天达成。
- [security] 中文目标 6/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.0 | 5 | 4 | 5/7 | 1.1 | 3 | 3 | 8.3 | 28 |
| ai_security | AI 安全 | 7 | 5.6 | 10 | 1/7 | 1.4 | 2 | 0 | 3/7 | 1.3 | 2 | 0 | 7.4 | 10 |
| finance | 金融科技 | 7 | 9.4 | 10 | 6/7 | 2.7 | 1 | 1 | 7/7 | 2.7 | 4 | 0 | 7.2 | 2 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 6.6 | 6 | 5 | 6/7 | 0.0 | 1 | 8 | 8.4 | 19 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 12 | 15 | 75 | 3 | 12 | 37 | 8 | 15 | 1 |
| ai_security | 3 | 1 | 35 | 0 | 3 | 6 | 9 | 7 | 0 |
| finance | 6 | 0 | 60 | 0 | 6 | 0 | 19 | 0 | 0 |
| security | 8 | 0 | 89 | 8 | 8 | 4 | 0 | 41 | 10 |

## Target Misses

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
- 2026-07-28 security：selected 15/15，中文 9/6，unknown 1
- 2026-07-28 ai_security：selected 3/10，中文 0/2
- 2026-07-27 security：selected 15/15，中文 8/6，unknown 2
- 2026-07-27 ai_security：selected 2/10，中文 1/2
- 2026-07-27 finance：selected 6/10，中文 4/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
