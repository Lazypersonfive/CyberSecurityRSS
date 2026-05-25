# Source Registry Audit

- generated_for: 2026-05-26
- dates: 2026-05-26, 2026-05-25, 2026-05-24, 2026-05-23, 2026-05-22, 2026-05-21, 2026-05-20

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 97 | 13 | 19 | 65 | 0 | 12 | 13 | 39 | 0 |
| ai_security | 56 | 7 | 3 | 46 | 0 | 14 | 7 | 10 | 15 |
| finance | 70 | 3 | 0 | 67 | 0 | 12 | 3 | 0 | 0 |
| security | 105 | 16 | 0 | 88 | 1 | 0 | 16 | 8 | 41 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blog.huli.tw` | 1 | security | [npm 供應鏈攻擊深度解析：從 antv 與 axios 案例看前端生態安全防禦](https://blog.huli.tw/2026/05/25/dive-into-npm-supply-chain-attack/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
