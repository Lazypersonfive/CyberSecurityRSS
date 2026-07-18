# Source Registry Audit

- generated_for: 2026-07-19
- dates: 2026-07-19, 2026-07-18, 2026-07-17, 2026-07-16, 2026-07-15, 2026-07-14, 2026-07-13

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 14 | 15 | 70 | 6 | 9 | 14 | 39 | 13 |
| ai_security | 30 | 4 | 0 | 26 | 0 | 8 | 4 | 4 | 8 |
| finance | 68 | 18 | 0 | 50 | 0 | 18 | 18 | 0 | 0 |
| security | 105 | 8 | 0 | 93 | 4 | 0 | 8 | 3 | 44 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `machinelearning.apple.com` | 5 | ai | [苹果机器学习研究团队提出低影响力点遗忘技术，旨在降低模型数据删除的计算成本](https://machinelearning.apple.com/research/unlearning-free-low-influence) |
| `sandflysecurity.com` | 1 | security | [无代理Linux EDR技术原理：如何通过SSH连接远程检测系统中的Rootkit](https://sandflysecurity.com/blog/how-agentless-linux-edr-detects-rootkits-over-ssh) |
| `taosecurity.blogspot.com` | 1 | security | [FreeBSD项目在2026年6月发布的安全公告数量创历史新高，AI技术显著提升漏洞发现效率](https://taosecurity.blogspot.com/2026/07/freebsd-released-most-security.html) |
| `venturebeat.com` | 1 | ai | [企业级 AI 代理评估存在严重偏差，多数机构在自动化评估不完善的情况下仍强行上线](https://venturebeat.com/ai/the-agent-evaluation-gap-enterprise-ai-organizations-have-a-reality-alignment-problem-not-a-coverage-problem-and-most-are-shipping-to-production-anyway) |
| `vipread.com` | 1 | security | [WgpSec发布Alkaid智能体框架，探索AI在全自主攻防场景中的工程化落地](https://vipread.com/library/topic/4153) |
| `xlab.tencent.com` | 1 | security | [腾讯玄武Atuin AI在CyberGym评估中表现升级：基于GLM-5.2的任务通过率达84.8%](https://xlab.tencent.com/cn/2026/07/17/xuanwu-atuin-cybergym-glm52/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
