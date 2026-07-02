# Offline Strategy Eval

- generated_for: 2026-07-03
- dates: 2026-07-03, 2026-07-02, 2026-07-01, 2026-06-30, 2026-06-29, 2026-06-28, 2026-06-27

## Top Issues

- [ai_security] 3/7 天未满额，累计缺口约 5 条。
- [ai] 中文目标 3/7 天达成。
- [ai_security] 中文目标 5/7 天达成。
- [finance] 中文目标 6/7 天达成。
- [security] 入选 unknown source 9 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.3 | 5 | 3 | 3/7 | 0.6 | 3 | 0 | 8.5 | 54 |
| ai_security | AI 安全 | 7 | 9.3 | 10 | 4/7 | 2.7 | 2 | 1 | 5/7 | 1.1 | 2 | 0 | 7.8 | 2 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.6 | 1 | 0 | 6/7 | 2.0 | 4 | 0 | 7.5 | 14 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 9.9 | 6 | 8 | 7/7 | 0.0 | 1 | 9 | 8.9 | 29 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 18 | 16 | 71 | 0 | 18 | 44 | 4 | 17 | 0 |
| ai_security | 8 | 1 | 56 | 0 | 8 | 5 | 8 | 17 | 0 |
| finance | 2 | 0 | 68 | 0 | 2 | 0 | 14 | 0 | 0 |
| security | 4 | 0 | 92 | 9 | 4 | 2 | 0 | 68 | 1 |

## Target Misses

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
- 2026-06-27 ai：selected 15/15，中文 4/5
- 2026-06-27 finance：selected 10/10，中文 0/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
