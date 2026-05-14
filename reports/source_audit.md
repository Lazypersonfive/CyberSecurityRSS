# Source Registry Audit

- generated_for: 2026-05-15
- dates: 2026-05-15, 2026-05-14, 2026-05-13, 2026-05-12, 2026-05-11, 2026-05-10, 2026-05-09

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 100 | 12 | 16 | 71 | 1 | 17 | 12 | 32 | 1 |
| ai_security | 54 | 10 | 3 | 41 | 0 | 8 | 10 | 20 | 11 |
| finance | 60 | 4 | 0 | 56 | 0 | 13 | 4 | 0 | 0 |
| security | 102 | 10 | 0 | 87 | 5 | 0 | 10 | 6 | 21 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blog.csdn.net` | 3 | security | [ARM64 架构下 this_cpu_ops 性能优化探讨与内核页表挑战](https://blog.csdn.net/21cnbao/article/details/161028912) |
| `blog.google` | 1 | ai | [谷歌金融 AI 增强版功能正式扩展至欧洲市场，提升用户投资数据分析体验](https://blog.google/products-and-platforms/products/search/ai-powered-google-finance-in-europe/) |
| `furutsuki.hatenablog.com` | 1 | security | [Daily AlpacaHack 挑战赛解题视频系列发布，通过实战演示助力初学者掌握 CTF 技巧](https://furutsuki.hatenablog.com/entry/2026/05/14/002228) |
| `k8gege.org` | 1 | security | [AI 渗透工具 Kali & HexStrike 被曝存在多个高危远程命令执行漏洞](http://k8gege.org/p/hexstrike_0day.html) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
