# Source Registry Audit

- generated_for: 2026-07-16
- dates: 2026-07-16, 2026-07-15, 2026-07-14, 2026-07-13, 2026-07-12, 2026-07-11, 2026-07-10

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 97 | 12 | 17 | 66 | 2 | 6 | 12 | 39 | 15 |
| ai_security | 48 | 2 | 0 | 46 | 0 | 6 | 2 | 5 | 19 |
| finance | 70 | 14 | 0 | 56 | 0 | 14 | 14 | 0 | 0 |
| security | 105 | 11 | 0 | 93 | 1 | 0 | 11 | 1 | 52 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `machinelearning.apple.com` | 2 | ai | [苹果研究团队提出 CLaRa 框架，通过连续潜空间推理解决 RAG 长上下文与优化不一致问题](https://machinelearning.apple.com/research/clara-latent-reasoning) |
| `vipread.com` | 1 | security | [WgpSec发布Alkaid智能体框架，探索AI在全自主攻防场景中的工程化落地](https://vipread.com/library/topic/4153) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
