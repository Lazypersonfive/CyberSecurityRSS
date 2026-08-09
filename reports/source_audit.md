# Source Registry Audit

- generated_for: 2026-08-10
- dates: 2026-08-10, 2026-08-09, 2026-08-08, 2026-08-07, 2026-08-06, 2026-08-05, 2026-08-04

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 14 | 15 | 74 | 2 | 5 | 14 | 41 | 18 |
| ai_security | 35 | 5 | 1 | 29 | 0 | 12 | 5 | 5 | 1 |
| finance | 68 | 3 | 0 | 65 | 0 | 16 | 3 | 0 | 0 |
| security | 105 | 9 | 0 | 88 | 8 | 0 | 9 | 6 | 39 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `avleonov.com` | 2 | security | [Microsoft SharePoint 关键功能身份验证缺失漏洞 CVE-2026-56164 导致远程权限提升](https://avleonov.com/2026/08/07/i120-about-elevation-of-privilege-microsoft-sharepoint-cve202656164-vulnerability/) |
| `machinelearning.apple.com` | 2 | ai | [苹果研究团队发布分类流映射缩放技术，为离散数据生成提供连续流匹配新方案](https://machinelearning.apple.com/research/scaling-categorical-flow-maps) |
| `aws.amazon.com` | 1 | security | [亚马逊 AWS 发布 S3 存储桶过度授权访问的识别与修复指南](https://aws.amazon.com/blogs/security/securing-your-amazon-s3-buckets-identifying-and-remediating-over-permissioned-access/) |
| `forum.90sec.com` | 1 | security | [综合资产收集与指纹识别工具集发布，集成 9000 多个 PoC 联动批量漏洞利用功能](https://forum.90sec.com/t/topic/2556) |
| `hackingdream.net` | 1 | security | [模型上下文协议（MCP）渗透测试指南发布，涵盖攻击面分析与实验环境搭建](https://www.hackingdream.net/2026/08/mcp-penetration-testing-hacking-model-context-protocol.html) |
| `key08.com` | 1 | security | [基于模型注意力机制构建高效 Web CTF 自动化 Agent 技术研究](https://key08.com/index.php/2026/08/10/3275.html) |
| `pentestpartners.com` | 1 | security | [通过加强云凭据全生命周期管理，有效切断因泄露导致的攻击链条](https://www.pentestpartners.com/security-blog/breaking-the-attack-chain-created-by-exposed-cloud-secrets/) |
| `security.tencent.com` | 1 | security | [AI Agent 记忆提取攻击链路解析：Memory Heist 自动化检测技术研究](https://security.tencent.com/index.php/blog/msg/225) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
