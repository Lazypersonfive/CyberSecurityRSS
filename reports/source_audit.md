# Source Registry Audit

- generated_for: 2026-08-01
- dates: 2026-08-01, 2026-07-31, 2026-07-30, 2026-07-29, 2026-07-28, 2026-07-27, 2026-07-26

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 13 | 17 | 72 | 3 | 8 | 13 | 39 | 16 |
| ai_security | 34 | 3 | 1 | 30 | 0 | 9 | 3 | 5 | 6 |
| finance | 66 | 10 | 0 | 55 | 1 | 17 | 10 | 0 | 0 |
| security | 105 | 8 | 0 | 89 | 8 | 0 | 8 | 4 | 41 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `machinelearning.apple.com` | 3 | ai | [苹果发布 MoMo 机器人操控框架，通过时空动作标记化实现灵活的运动模式调节](https://machinelearning.apple.com/research/momo-motion-mode-manipulation) |
| `nobb.site` | 2 | security | [利用人工智能辅助对天猫精灵智能插座 IoT 模块进行逆向工程分析](https://nobb.site/2026/07/26/0x9D/) |
| `solidot.org` | 2 | security | [Arch Linux 因恶意软件投毒攻击关闭 AUR 孤儿包领养与修改功能](https://www.solidot.org/story?sid=84979) |
| `blog.nsfocus.net` | 1 | security | [企业 AI 中转站数据泄露风险分析与纵深防护安全网关方案](https://blog.nsfocus.net/%e5%bd%93%e5%91%98%e5%b7%a5%e7%94%a8ai%e4%b8%ad%e8%bd%ac%e7%ab%99%e9%a1%ba%e6%89%8b%e5%8f%91%e8%b5%b0%e5%86%85%e9%83%a8%e6%95%b0%e6%8d%ae%ef%bc%8c%e4%bc%81%e4%b8%9a%e8%be%b9%e7%95%8c/) |
| `doublepulsar.com` | 1 | security | [广告服务商 Adform 遭遇供应链攻击，其嵌入式脚本被植入加密货币窃取程序](https://doublepulsar.com/adform-compromised-to-serve-crypto-stealer-via-supply-chain-attack-2f1ec024f33e?source=rss-7db6d2df42a6------2) |
| `fidelissecurity.com` | 1 | security | [Linux 内核 Ptrace 权限校验漏洞 CVE-2026-46333 可导致本地权限提升](https://fidelissecurity.com/threatgeek/threat-detection-response/linux-kernel-ptrace-permission-validation-vulnerability/) |
| `ir.americanexpress.com` | 1 | finance | [美国运通发布 2026 年第二季度财务业绩报告，展示公司在信用卡支付及金融服务领域的最新表现](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Reports-Second-Quarter-2026-Financial-Results/default.aspx) |
| `lab.wallarm.com` | 1 | security | [OpenAI 模型逃逸沙箱并入侵 Hugging Face 基础设施事件的技术反思与教训](https://lab.wallarm.com/hugging-face-open-ai-incident/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
