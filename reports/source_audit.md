# Source Registry Audit

- generated_for: 2026-06-04
- dates: 2026-06-04, 2026-06-03, 2026-06-02, 2026-06-01, 2026-05-31, 2026-05-30, 2026-05-29

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 15 | 20 | 70 | 0 | 10 | 15 | 39 | 0 |
| ai_security | 67 | 10 | 1 | 56 | 0 | 6 | 10 | 6 | 7 |
| finance | 70 | 2 | 0 | 68 | 0 | 12 | 2 | 0 | 0 |
| security | 105 | 14 | 0 | 91 | 0 | 0 | 14 | 5 | 30 |

## Unknown Selected Sources

No unknown selected sources in the audited window.

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
