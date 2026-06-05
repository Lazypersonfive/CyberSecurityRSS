# Offline Strategy Eval

- generated_for: 2026-06-06
- dates: 2026-06-06, 2026-06-05, 2026-06-04, 2026-06-03, 2026-06-02, 2026-06-01, 2026-05-31

## Top Issues

- [ai_security] 2/7 天未满额，累计缺口约 3 条。
- [security] 中文目标 1/7 天达成。
- [ai_security] 中文目标 3/7 天达成。
- [ai] 中文目标 3/7 天达成。
- [finance] 中文目标 6/7 天达成。

## Board Health

| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | AI 前沿 | 7 | 15.0 | 15 | 7/7 | 3.7 | 5 | 3/7 | 1.3 | 3 | 0 | 8.1 | 41 |
| ai_security | AI 安全 | 7 | 9.6 | 10 | 5/7 | 1.6 | 2 | 3/7 | 1.0 | 2 | 0 | 6.7 | 11 |
| finance | 金融科技 | 7 | 10.0 | 10 | 7/7 | 1.1 | 1 | 6/7 | 2.0 | 4 | 0 | 7.6 | 7 |
| security | 安全 | 7 | 15.0 | 15 | 7/7 | 4.0 | 6 | 1/7 | 0.0 | 1 | 2 | 8.2 | 21 |

## Source Mix

| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 14 | 21 | 70 | 0 | 14 | 40 | 9 | 0 | 0 |
| ai_security | 11 | 0 | 56 | 0 | 11 | 5 | 7 | 7 | 0 |
| finance | 2 | 0 | 68 | 0 | 2 | 0 | 14 | 0 | 0 |
| security | 14 | 0 | 89 | 2 | 14 | 5 | 0 | 28 | 20 |

## Target Misses

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
- 2026-05-31 security：selected 15/15，中文 4/6
- 2026-05-31 ai：selected 15/15，中文 4/5
- 2026-05-31 finance：selected 10/10，中文 0/1

## Read This

- `Full Days` 低说明该板块供给或 caps 仍不足。
- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。
- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。
