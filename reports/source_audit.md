# Source Registry Audit

- generated_for: 2026-05-16
- dates: 2026-05-16, 2026-05-15, 2026-05-14, 2026-05-13, 2026-05-12, 2026-05-11, 2026-05-10

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 100 | 14 | 16 | 69 | 1 | 15 | 14 | 34 | 1 |
| ai_security | 59 | 13 | 4 | 42 | 0 | 6 | 13 | 24 | 11 |
| finance | 63 | 3 | 0 | 60 | 0 | 14 | 3 | 0 | 0 |
| security | 102 | 11 | 0 | 84 | 7 | 0 | 11 | 5 | 19 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blog.csdn.net` | 3 | security | [ARM64 架构下 this_cpu_ops 性能优化探讨与内核页表挑战](https://blog.csdn.net/21cnbao/article/details/161028912) |
| `furutsuki.hatenablog.com` | 2 | security | [Daily AlpacaHack：面向初学者的常设 CTF 挑战与解题分享](https://furutsuki.hatenablog.com/entry/2026/05/14/002228) |
| `k8gege.org` | 2 | security | [AI 渗透工具 HexStrike 被曝存在多个远程命令执行 0day 漏洞](http://k8gege.org/p/hexstrike_0day.html) |
| `blog.google` | 1 | ai | [谷歌金融 AI 增强版功能正式扩展至欧洲市场，提升用户投资数据分析体验](https://blog.google/products-and-platforms/products/search/ai-powered-google-finance-in-europe/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
