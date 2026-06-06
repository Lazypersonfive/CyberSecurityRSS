# Offline Strategy Eval

- generated_for: 2026-06-07
- dates: 2026-06-07, 2026-06-06, 2026-06-05, 2026-06-04, 2026-06-03, 2026-06-02, 2026-06-01

## Top Issues

- [ai_security] 2/7 天未满额，累计缺口约 3 条。
- [security] 中文目标 1/7 天达成。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 3/7 天达成。
- [security] 入选 unknown source 3 条，需登记或降权。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 3.7 | 5 | 3/7 | 1.3 | 3 | 0 | 8.1 | 40 |
| ai_security | AI 安全 | 7 | 9.6 | 10 | 5/7 | 1.6 | 2 | 3/7 | 1.0 | 2 | 0 | 6.8 | 12 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.3 | 1 | 7/7 | 2.1 | 4 | 0 | 7.6 | 9 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 4.1 | 6 | 1/7 | 0.0 | 1 | 3 | 8.2 | 15 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 16 | 22 | 67 | 0 | 16 | 40 | 9 | 0 | 0 |
| ai_security | 10 | 0 | 57 | 0 | 10 | 5 | 7 | 8 | 0 |
| finance | 3 | 0 | 67 | 0 | 3 | 0 | 15 | 0 | 0 |
| security | 15 | 0 | 87 | 3 | 15 | 5 | 0 | 29 | 18 |

## Target Misses

- 2026-06-07 security：selected 15/15，中文 5/6，unknown 1
- 2026-06-07 ai：selected 15/15，中文 4/5
- 2026-06-05 security：selected 15/15，中文 4/6，unknown 2
- 2026-06-05 ai_security：selected 10/10，中文 1/2
- 2026-06-05 ai：selected 15/15，中文 2/5
- 2026-06-04 security：selected 15/15，中文 4/6
- 2026-06-04 ai_security：selected 10/10，中文 1/2
- 2026-06-04 ai：selected 15/15，中文 2/5
- 2026-06-03 security：selected 15/15，中文 3/6
- 2026-06-03 ai_security：selected 10/10，中文 0/2
- 2026-06-02 security：selected 15/15，中文 3/6
- 2026-06-02 ai_security：selected 9/10，中文 1/2
- 2026-06-02 ai：selected 15/15，中文 3/5
- 2026-06-01 security：selected 15/15，中文 4/6
- 2026-06-01 ai_security：selected 8/10，中文 2/2

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
