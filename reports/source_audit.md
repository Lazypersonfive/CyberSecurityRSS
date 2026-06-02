# Source Registry Audit

- generated_for: 2026-06-02
- dates: 2026-06-02, 2026-06-01, 2026-05-31, 2026-05-30, 2026-05-29, 2026-05-28, 2026-05-27

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 17 | 22 | 66 | 0 | 7 | 17 | 42 | 0 |
| ai_security | 66 | 7 | 4 | 55 | 0 | 7 | 7 | 11 | 6 |
| finance | 70 | 3 | 0 | 67 | 0 | 8 | 3 | 0 | 0 |
| security | 105 | 19 | 0 | 86 | 0 | 0 | 19 | 4 | 28 |

## Unknown Selected Sources

No unknown selected sources in the audited window.

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
