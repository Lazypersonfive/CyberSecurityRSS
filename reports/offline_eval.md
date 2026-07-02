# Offline Strategy Eval

- generated_for: 2026-07-02
- dates: 2026-07-02, 2026-07-01, 2026-06-30, 2026-06-29, 2026-06-28, 2026-06-27, 2026-06-26

## Top Issues

- [ai_security] 3/7 天未满额，累计缺口约 5 条。
- [ai] 中文目标 3/7 天达成。
- [ai_security] 中文目标 5/7 天达成。
- [finance] 中文目标 6/7 天达成。
- [security] 入选 unknown source 9 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 5.4 | 5 | 4 | 3/7 | 0.4 | 3 | 0 | 8.6 | 49 |
| ai_security | AI 安全 | 7 | 9.3 | 10 | 4/7 | 3.1 | 2 | 1 | 5/7 | 1.0 | 2 | 0 | 7.8 | 5 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.7 | 1 | 0 | 6/7 | 2.1 | 4 | 1 | 7.5 | 13 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 9.9 | 6 | 8 | 7/7 | 0.0 | 1 | 9 | 9.0 | 24 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 19 | 16 | 70 | 0 | 19 | 45 | 3 | 16 | 0 |
| ai_security | 7 | 1 | 57 | 0 | 7 | 5 | 7 | 21 | 0 |
| finance | 2 | 0 | 67 | 1 | 2 | 0 | 15 | 0 | 0 |
| security | 5 | 0 | 91 | 9 | 5 | 1 | 0 | 68 | 1 |

## Target Misses

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
- 2026-06-26 security：selected 15/15，中文 10/6，unknown 1
- 2026-06-26 ai：selected 15/15，中文 4/5
- 2026-06-26 finance：selected 10/10，中文 2/1，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
