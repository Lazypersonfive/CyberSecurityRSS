# Source Registry Audit

- generated_for: 2026-05-25
- dates: 2026-05-25, 2026-05-24, 2026-05-23, 2026-05-22, 2026-05-21, 2026-05-20, 2026-05-19

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 100 | 15 | 20 | 65 | 0 | 13 | 15 | 39 | 0 |
| ai_security | 50 | 7 | 2 | 41 | 0 | 14 | 7 | 8 | 15 |
| finance | 70 | 3 | 0 | 67 | 0 | 13 | 3 | 0 | 0 |
| security | 105 | 18 | 0 | 87 | 0 | 0 | 18 | 6 | 42 |

## Unknown Selected Sources

No unknown selected sources in the audited window.

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
