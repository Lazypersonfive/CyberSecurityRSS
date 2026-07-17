# Source Registry Audit

- generated_for: 2026-07-18
- dates: 2026-07-18, 2026-07-17, 2026-07-16, 2026-07-15, 2026-07-14, 2026-07-13, 2026-07-12

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 14 | 15 | 70 | 6 | 10 | 14 | 38 | 14 |
| ai_security | 37 | 4 | 0 | 33 | 0 | 7 | 4 | 5 | 11 |
| finance | 70 | 18 | 0 | 52 | 0 | 17 | 18 | 0 | 0 |
| security | 105 | 10 | 0 | 94 | 1 | 0 | 10 | 3 | 48 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `machinelearning.apple.com` | 5 | ai | [苹果机器学习研究团队提出低影响力点遗忘技术，旨在降低模型数据删除的计算成本](https://machinelearning.apple.com/research/unlearning-free-low-influence) |
| `venturebeat.com` | 1 | ai | [企业级 AI 代理评估存在严重偏差，多数机构在自动化评估不完善的情况下仍强行上线](https://venturebeat.com/ai/the-agent-evaluation-gap-enterprise-ai-organizations-have-a-reality-alignment-problem-not-a-coverage-problem-and-most-are-shipping-to-production-anyway) |
| `vipread.com` | 1 | security | [WgpSec发布Alkaid智能体框架，探索AI在全自主攻防场景中的工程化落地](https://vipread.com/library/topic/4153) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
