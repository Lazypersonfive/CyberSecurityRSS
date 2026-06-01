# Source Registry Audit

- generated_for: 2026-06-01
- dates: 2026-06-01, 2026-05-31, 2026-05-30, 2026-05-29, 2026-05-28, 2026-05-27, 2026-05-26

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 102 | 16 | 20 | 66 | 0 | 7 | 16 | 42 | 0 |
| ai_security | 65 | 7 | 5 | 53 | 0 | 7 | 7 | 12 | 6 |
| finance | 70 | 3 | 0 | 67 | 0 | 9 | 3 | 0 | 0 |
| security | 105 | 17 | 0 | 88 | 0 | 0 | 17 | 6 | 30 |

## Unknown Selected Sources

No unknown selected sources in the audited window.

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
