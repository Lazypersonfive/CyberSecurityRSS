# Source Registry Audit

- generated_for: 2026-05-14
- dates: 2026-05-14, 2026-05-13, 2026-05-12, 2026-05-11, 2026-05-10, 2026-05-09, 2026-05-08

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 100 | 15 | 15 | 69 | 1 | 16 | 15 | 32 | 1 |
| ai_security | 50 | 10 | 4 | 36 | 0 | 9 | 10 | 18 | 9 |
| finance | 60 | 7 | 0 | 53 | 0 | 12 | 7 | 0 | 0 |
| security | 102 | 9 | 0 | 90 | 3 | 0 | 9 | 6 | 20 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blog.csdn.net` | 2 | security | [针对 ARM64 架构的 this_cpu_ops 性能优化研究，通过独立页表解决 percpu 数据访问挑战](https://blog.csdn.net/21cnbao/article/details/161028912) |
| `blog.google` | 1 | ai | [谷歌金融 AI 增强版功能正式扩展至欧洲市场，提升用户投资数据分析体验](https://blog.google/products-and-platforms/products/search/ai-powered-google-finance-in-europe/) |
| `furutsuki.hatenablog.com` | 1 | security | [Daily AlpacaHack 挑战赛解题视频系列发布，通过实战演示助力初学者掌握 CTF 技巧](https://furutsuki.hatenablog.com/entry/2026/05/14/002228) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
