# Source Registry Audit

- generated_for: 2026-08-09
- dates: 2026-08-09, 2026-08-08, 2026-08-07, 2026-08-06, 2026-08-05, 2026-08-04, 2026-08-03

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 14 | 17 | 72 | 2 | 4 | 14 | 42 | 17 |
| ai_security | 34 | 5 | 1 | 28 | 0 | 11 | 5 | 5 | 1 |
| finance | 70 | 5 | 0 | 65 | 0 | 15 | 5 | 0 | 0 |
| security | 105 | 8 | 0 | 88 | 9 | 0 | 8 | 6 | 39 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cxsecurity.com` | 3 | security | [Linux内核 7.0 至 7.0.8 版本存在释放后使用漏洞 CVE-2026-46215 且已有稳定利用脚本](https://cxsecurity.com/issue/WLB-2026080002) |
| `avleonov.com` | 2 | security | [ViPNet Client 安全组件远程代码执行漏洞 BDU:2026-09885 预警](https://avleonov.com/2026/08/05/i117-about-remote-code-execution-vipnet-client-bdu202609885-vulnerability/) |
| `machinelearning.apple.com` | 2 | ai | [苹果研究团队发布分类流映射缩放技术，为离散数据生成提供连续流匹配新方案](https://machinelearning.apple.com/research/scaling-categorical-flow-maps) |
| `forum.90sec.com` | 1 | security | [综合资产收集与指纹识别工具集发布，集成 9000 多个 PoC 联动批量漏洞利用功能](https://forum.90sec.com/t/topic/2556) |
| `hackingdream.net` | 1 | security | [模型上下文协议（MCP）渗透测试指南发布，涵盖攻击面分析与实验环境搭建](https://www.hackingdream.net/2026/08/mcp-penetration-testing-hacking-model-context-protocol.html) |
| `pentestpartners.com` | 1 | security | [通过加强云凭据全生命周期管理，有效切断因泄露导致的攻击链条](https://www.pentestpartners.com/security-blog/breaking-the-attack-chain-created-by-exposed-cloud-secrets/) |
| `security.tencent.com` | 1 | security | [AI Agent 记忆提取攻击链路解析：Memory Heist 自动化检测技术研究](https://security.tencent.com/index.php/blog/msg/225) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
