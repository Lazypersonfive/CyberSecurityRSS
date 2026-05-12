# Source Registry Audit

- generated_for: 2026-05-13
- dates: 2026-05-13, 2026-05-12, 2026-05-11, 2026-05-10, 2026-05-09, 2026-05-08, 2026-05-07

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 100 | 18 | 13 | 68 | 1 | 16 | 18 | 30 | 1 |
| ai_security | 46 | 7 | 4 | 35 | 0 | 10 | 7 | 18 | 6 |
| finance | 56 | 6 | 0 | 50 | 0 | 10 | 6 | 0 | 0 |
| security | 102 | 9 | 0 | 92 | 1 | 0 | 9 | 4 | 28 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blog.csdn.net` | 1 | security | [针对 ARM64 架构的 this_cpu_ops 优化研究：挑战内核页表与原子操作实现](https://blog.csdn.net/21cnbao/article/details/161028912) |
| `blog.google` | 1 | ai | [谷歌金融 AI 增强版功能正式扩展至欧洲市场，提升用户投资数据分析体验](https://blog.google/products-and-platforms/products/search/ai-powered-google-finance-in-europe/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
