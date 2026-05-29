# Source Registry Audit

- generated_for: 2026-05-30
- dates: 2026-05-30, 2026-05-29, 2026-05-28, 2026-05-27, 2026-05-26, 2026-05-25, 2026-05-24

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 101 | 13 | 18 | 70 | 0 | 11 | 13 | 42 | 0 |
| ai_security | 63 | 8 | 7 | 48 | 0 | 6 | 8 | 15 | 6 |
| finance | 70 | 3 | 0 | 67 | 0 | 9 | 3 | 0 | 0 |
| security | 105 | 19 | 0 | 80 | 6 | 0 | 19 | 6 | 27 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blog.huli.tw` | 3 | security | [深入分析 npm 供应链攻击：从 antv 与 axios 遭植毒事件看前端生态安全防御](https://blog.huli.tw/2026/05/25/dive-into-npm-supply-chain-attack/) |
| `rastamouse.me` | 2 | security | [Module Stomping PIC 技术：利用合法 DLL 内存覆盖实现恶意代码隐匿](https://rastamouse.me/module-stomping-pic/) |
| `securityonline.info` | 1 | security | [WordPress 插件 WP Maps Pro 关键漏洞正遭受野外利用，攻击者可接管站点](https://securityonline.info/wp-maps-pro-vulnerability-exploited/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
