# Offline Strategy Eval

- generated_for: 2026-11-05
- dates: 2026-11-05, 2026-11-02, 2026-10-29, 2026-10-26, 2026-10-22, 2026-10-19, 2026-10-15

## Top Issues

- [ai] 2/7 天未满额，累计缺口约 3 条。
- [ai] 中文目标 5/7 天达成。
- [ai_security] 入选 unknown source 3 条，需登记或降权。
- [security] 入选 unknown source 2 条，需登记或降权。
- [finance] 入选 unknown source 1 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.6 | 15 | 5/7 | 4.4 | 5 | 3 | 5/7 | 1.4 | 3 | 1 | 7.8 | 32 |
| ai_security | AI 安全 | 7 | 10.0 | 10 | 7/7 | 3.4 | 2 | 2 | 7/7 | 0.1 | 2 | 3 | 8.3 | 9 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.1 | 2 | 2 | 7/7 | 0.9 | 3 | 1 | 7.9 | 0 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.0 | 6 | 6 | 7/7 | 0.0 | 1 | 2 | 8.9 | 17 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 18 | 13 | 70 | 1 | 18 | 39 | 10 | 3 | 0 |
| ai_security | 16 | 1 | 50 | 3 | 10 | 6 | 1 | 23 | 0 |
| finance | 15 | 4 | 50 | 1 | 15 | 4 | 6 | 0 | 0 |
| security | 18 | 0 | 85 | 2 | 14 | 5 | 0 | 48 | 0 |

## Target Misses

- 2026-11-05 security：selected 15/15，中文 6/6，unknown 1
- 2026-11-05 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-11-05 ai：selected 13/15，中文 5/5
- 2026-11-02 security：selected 15/15，中文 6/6，unknown 1
- 2026-11-02 ai：selected 14/15，中文 5/5
- 2026-10-29 ai_security：selected 10/10，中文 3/2，unknown 1
- 2026-10-26 finance：selected 10/10，中文 2/2，unknown 1
- 2026-10-22 ai：selected 15/15，中文 3/5
- 2026-10-19 ai_security：selected 10/10，中文 4/2，unknown 1
- 2026-10-19 ai：selected 15/15，中文 3/5，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
