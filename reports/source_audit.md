# Source Registry Audit

- generated_for: 2026-05-27
- dates: 2026-05-27, 2026-05-26, 2026-05-25, 2026-05-24, 2026-05-23, 2026-05-22, 2026-05-21

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 101 | 14 | 20 | 67 | 0 | 12 | 14 | 41 | 0 |
| ai_security | 62 | 7 | 5 | 50 | 0 | 12 | 7 | 14 | 15 |
| finance | 70 | 1 | 0 | 69 | 0 | 11 | 1 | 0 | 0 |
| security | 105 | 18 | 0 | 84 | 3 | 0 | 18 | 8 | 35 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blog.huli.tw` | 2 | security | [npm 生态系统供应链攻击深度解析：从 antv 与 axios 恶意版本看防御策略](https://blog.huli.tw/2026/05/25/dive-into-npm-supply-chain-attack/) |
| `rastamouse.me` | 1 | security | [Module Stomping 内存隐匿技术解析：通过覆盖合法 DLL 隐藏恶意代码](https://rastamouse.me/module-stomping-pic/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
