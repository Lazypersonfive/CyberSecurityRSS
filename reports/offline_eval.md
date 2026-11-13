# Offline Strategy Eval

- generated_for: 2026-11-13
- dates: 2026-11-13, 2026-11-12, 2026-11-09, 2026-11-05, 2026-11-02, 2026-10-29, 2026-10-26

## Top Issues

- [ai] 2/7 天未满额，累计缺口约 3 条。
- [ai] 中文目标 4/7 天达成。
- [security] 入选 unknown source 4 条，需登记或降权。
- [ai_security] 入选 unknown source 3 条，需登记或降权。
- [finance] 入选 unknown source 1 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | CN Target | Obs Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 14.6 | 15 | 5/7 | 4.3 | 5 | 3 | 4/7 | 1.7 | 3 | 1 | 7.7 | 35 |
| ai_security | AI 安全 | 7 | 10.0 | 10 | 7/7 | 3.4 | 2 | 2 | 7/7 | 0.1 | 2 | 3 | 8.3 | 10 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 2.0 | 2 | 2 | 7/7 | 0.6 | 3 | 1 | 7.7 | 0 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 7.1 | 6 | 6 | 7/7 | 0.0 | 1 | 4 | 8.8 | 19 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 18 | 69 | 1 | 14 | 37 | 12 | 2 | 0 |
| ai_security | 15 | 1 | 51 | 3 | 12 | 7 | 1 | 23 | 1 |
| finance | 15 | 2 | 52 | 1 | 15 | 2 | 4 | 0 | 0 |
| security | 24 | 0 | 77 | 4 | 20 | 5 | 0 | 49 | 0 |

## Target Misses

- 2026-11-13 security：selected 15/15，中文 7/6，unknown 1
- 2026-11-13 ai：selected 15/15，中文 3/5，unknown 1
- 2026-11-12 ai：selected 15/15，中文 3/5
- 2026-11-09 security：selected 15/15，中文 9/6，unknown 1
- 2026-11-09 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-11-09 ai：selected 15/15，中文 4/5
- 2026-11-05 security：selected 15/15，中文 6/6，unknown 1
- 2026-11-05 ai_security：selected 10/10，中文 2/2，unknown 1
- 2026-11-05 ai：selected 13/15，中文 5/5
- 2026-11-02 security：selected 15/15，中文 6/6，unknown 1
- 2026-11-02 ai：selected 14/15，中文 5/5
- 2026-10-29 ai_security：selected 10/10，中文 3/2，unknown 1
- 2026-10-26 finance：selected 10/10，中文 2/2，unknown 1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
