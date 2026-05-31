# Source Registry Audit

- generated_for: 2026-06-01
- dates: 2026-06-01, 2026-05-31, 2026-05-30, 2026-05-29, 2026-05-28, 2026-05-27, 2026-05-26

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 101 | 11 | 20 | 70 | 0 | 6 | 11 | 43 | 0 |
| ai_security | 66 | 7 | 5 | 54 | 0 | 7 | 7 | 11 | 6 |
| finance | 70 | 3 | 0 | 67 | 0 | 9 | 3 | 0 | 0 |
| security | 105 | 17 | 0 | 80 | 8 | 0 | 17 | 6 | 26 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blog.huli.tw` | 3 | security | [深入分析 npm 供应链攻击：从 antv 与 axios 遭植毒事件看前端生态安全防御](https://blog.huli.tw/2026/05/25/dive-into-npm-supply-chain-attack/) |
| `intigriti.com` | 2 | security | [Intigriti Bug Bytes 第 236 期：Google Cloud 远程代码执行漏洞与 Chrome 净化器 API 绕过](https://www.intigriti.com/researchers/blog/bug-bytes/intigriti-bug-bytes-236-may-2026) |
| `rastamouse.me` | 2 | security | [Module Stomping PIC 技术：利用合法 DLL 内存覆盖实现恶意代码隐匿](https://rastamouse.me/module-stomping-pic/) |
| `securityonline.info` | 1 | security | [WordPress 插件 WP Maps Pro 关键漏洞正遭受野外利用，攻击者可接管站点](https://securityonline.info/wp-maps-pro-vulnerability-exploited/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
