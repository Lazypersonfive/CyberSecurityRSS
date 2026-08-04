# Source Registry Audit

- generated_for: 2026-08-05
- dates: 2026-08-05, 2026-08-04, 2026-08-03, 2026-08-02, 2026-08-01, 2026-07-31, 2026-07-30

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 13 | 14 | 75 | 3 | 6 | 13 | 38 | 15 |
| ai_security | 42 | 4 | 1 | 37 | 0 | 10 | 4 | 6 | 4 |
| finance | 70 | 9 | 0 | 61 | 0 | 16 | 9 | 0 | 0 |
| security | 105 | 7 | 0 | 87 | 11 | 0 | 7 | 2 | 36 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cxsecurity.com` | 3 | security | [Linux内核 7.0 至 7.0.8 版本存在释放后使用漏洞 CVE-2026-46215 且已有稳定利用脚本](https://cxsecurity.com/issue/WLB-2026080002) |
| `machinelearning.apple.com` | 3 | ai | [苹果发布 MoMo 机器人操控框架，通过时空动作标记化实现灵活的运动模式调节](https://machinelearning.apple.com/research/momo-motion-mode-manipulation) |
| `solidot.org` | 2 | security | [Arch Linux 因恶意软件投毒攻击关闭 AUR 孤儿包领养与修改功能](https://www.solidot.org/story?sid=84979) |
| `avleonov.com` | 1 | security | [2026年7月 Linux 补丁日修复超两千个漏洞，Linux 内核与 Chromium 占比最高](https://avleonov.com/2026/07/31/i114-ijulskij-linux-patch-wednesday/) |
| `blog.nsfocus.net` | 1 | security | [企业 AI 中转站数据泄露风险分析与纵深防护安全网关方案](https://blog.nsfocus.net/%e5%bd%93%e5%91%98%e5%b7%a5%e7%94%a8ai%e4%b8%ad%e8%bd%ac%e7%ab%99%e9%a1%ba%e6%89%8b%e5%8f%91%e8%b5%b0%e5%86%85%e9%83%a8%e6%95%b0%e6%8d%ae%ef%bc%8c%e4%bc%81%e4%b8%9a%e8%be%b9%e7%95%8c/) |
| `doublepulsar.com` | 1 | security | [广告服务商 Adform 遭遇供应链攻击，其嵌入式脚本被植入加密货币窃取程序](https://doublepulsar.com/adform-compromised-to-serve-crypto-stealer-via-supply-chain-attack-2f1ec024f33e?source=rss-7db6d2df42a6------2) |
| `fidelissecurity.com` | 1 | security | [Linux 内核 Ptrace 权限校验漏洞 CVE-2026-46333 可导致本地权限提升](https://fidelissecurity.com/threatgeek/threat-detection-response/linux-kernel-ptrace-permission-validation-vulnerability/) |
| `hackingdream.net` | 1 | security | [模型上下文协议（MCP）渗透测试指南发布，涵盖攻击面分析与实验环境搭建](https://www.hackingdream.net/2026/08/mcp-penetration-testing-hacking-model-context-protocol.html) |
| `security.tencent.com` | 1 | security | [AI Agent 记忆提取攻击链路解析：Memory Heist 自动化检测技术研究](https://security.tencent.com/index.php/blog/msg/225) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
