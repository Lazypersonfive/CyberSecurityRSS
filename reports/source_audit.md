# Source Registry Audit

- generated_for: 2026-07-22
- dates: 2026-07-22, 2026-07-21, 2026-07-20, 2026-07-19, 2026-07-18, 2026-07-17, 2026-07-16

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 15 | 19 | 65 | 6 | 7 | 15 | 42 | 11 |
| ai_security | 29 | 6 | 0 | 23 | 0 | 7 | 6 | 7 | 3 |
| finance | 65 | 10 | 0 | 55 | 0 | 20 | 10 | 0 | 0 |
| security | 105 | 8 | 0 | 86 | 11 | 0 | 8 | 5 | 39 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `machinelearning.apple.com` | 5 | ai | [苹果研究人员提出无环境合成数据生成方法，旨在突破 API 调用智能体的训练瓶颈](https://machinelearning.apple.com/research/environment-free) |
| `cxsecurity.com` | 4 | security | [Linux Kernel 7.0 DRM 模块释放后使用漏洞 CVE-2026-46215 提权漏洞利用公开](https://cxsecurity.com/issue/WLB-2026070008) |
| `solidot.org` | 2 | security | [WordPress 修复两个高危漏洞并强制更新，黑客正利用漏洞远程控制未修复网站](https://www.solidot.org/story?sid=84884) |
| `govuln.com` | 1 | security | [WordPress 7.0.2 核心组件存在两个严重漏洞，可导致身份验证前远程代码执行](https://govuln.com/news/url/g80P) |
| `key08.com` | 1 | security | [大模型持久化记忆研究笔记发布，探索不依赖 RAG 的长上下文知识编写技术](https://key08.com/index.php/2026/07/19/3219.html) |
| `sandflysecurity.com` | 1 | security | [无代理Linux EDR技术原理：如何通过SSH连接远程检测系统中的Rootkit](https://sandflysecurity.com/blog/how-agentless-linux-edr-detects-rootkits-over-ssh) |
| `taosecurity.blogspot.com` | 1 | security | [FreeBSD项目在2026年6月发布的安全公告数量创历史新高，AI技术显著提升漏洞发现效率](https://taosecurity.blogspot.com/2026/07/freebsd-released-most-security.html) |
| `venturebeat.com` | 1 | ai | [企业级 AI 代理评估存在严重偏差，多数机构在自动化评估不完善的情况下仍强行上线](https://venturebeat.com/ai/the-agent-evaluation-gap-enterprise-ai-organizations-have-a-reality-alignment-problem-not-a-coverage-problem-and-most-are-shipping-to-production-anyway) |
| `xlab.tencent.com` | 1 | security | [腾讯玄武Atuin AI在CyberGym评估中表现升级：基于GLM-5.2的任务通过率达84.8%](https://xlab.tencent.com/cn/2026/07/17/xuanwu-atuin-cybergym-glm52/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
