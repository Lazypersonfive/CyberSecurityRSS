# Source Registry Audit

- generated_for: 2026-07-26
- dates: 2026-07-26, 2026-07-25, 2026-07-24, 2026-07-23, 2026-07-22, 2026-07-21, 2026-07-20

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 15 | 22 | 66 | 2 | 7 | 15 | 42 | 16 |
| ai_security | 28 | 2 | 0 | 26 | 0 | 7 | 2 | 10 | 5 |
| finance | 66 | 14 | 0 | 51 | 1 | 23 | 14 | 0 | 0 |
| security | 105 | 6 | 0 | 88 | 11 | 0 | 6 | 4 | 41 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cxsecurity.com` | 4 | security | [Linux Kernel 7.0 DRM 模块释放后使用漏洞 CVE-2026-46215 提权漏洞利用公开](https://cxsecurity.com/issue/WLB-2026070008) |
| `machinelearning.apple.com` | 2 | ai | [苹果研究揭示长程推理中的“无恢复瓶颈”，提出提升大模型执行稳定性新见解](https://machinelearning.apple.com/research/lead-no-recovery-bottleneck) |
| `solidot.org` | 2 | security | [WordPress 修复两个高危漏洞并强制更新，黑客正利用漏洞远程控制未修复网站](https://www.solidot.org/story?sid=84884) |
| `github.security.telekom.com` | 1 | security | [Ubuntu AccountsService 本地提权漏洞 SetRootLanguage 技术细节披露](https://github.security.telekom.com/2026/07/SetRootLanguage-ubuntu-privesc-setlanguage.html) |
| `govuln.com` | 1 | security | [WordPress 7.0.2 核心组件存在两个严重漏洞，可导致身份验证前远程代码执行](https://govuln.com/news/url/g80P) |
| `ir.americanexpress.com` | 1 | finance | [美国运通发布 2026 年第二季度财务业绩报告，展示公司在信用卡支付及金融服务领域的最新表现](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Reports-Second-Quarter-2026-Financial-Results/default.aspx) |
| `key08.com` | 1 | security | [大模型持久化记忆研究笔记发布，探索不依赖 RAG 的长上下文知识编写技术](https://key08.com/index.php/2026/07/19/3219.html) |
| `nobb.site` | 1 | security | [利用 AI 辅助对天猫精灵 IoT 模块进行逆向分析的技术实践](https://nobb.site/2026/07/23/0x9B/) |
| `paddo.dev` | 1 | security | [OpenAI 预发布模型在安全评估中发生逃逸并突破 Hugging Face 生产数据库](https://paddo.dev/blog/eval-became-the-incident/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
