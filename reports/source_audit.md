# Source Registry Audit

- generated_for: 2026-06-11
- dates: 2026-06-11, 2026-06-10, 2026-06-09, 2026-06-08, 2026-06-07, 2026-06-06, 2026-06-05

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 99 | 13 | 14 | 72 | 0 | 9 | 13 | 34 | 0 |
| ai_security | 69 | 12 | 0 | 57 | 0 | 7 | 12 | 8 | 14 |
| finance | 70 | 4 | 0 | 66 | 0 | 16 | 4 | 0 | 0 |
| security | 105 | 18 | 0 | 86 | 1 | 0 | 18 | 2 | 31 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cyberkendra.com` | 1 | security | [研究人员发布Windows Defender本地提权零日漏洞RoguePlanet的PoC](https://www.cyberkendra.com/2026/06/microsoft-defender-zero-day-poc-gives.html) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
