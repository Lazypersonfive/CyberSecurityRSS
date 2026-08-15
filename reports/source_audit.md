# Source Registry Audit

- generated_for: 2026-08-16
- dates: 2026-08-16, 2026-08-15, 2026-08-14, 2026-08-13, 2026-08-12, 2026-08-11, 2026-08-10

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 104 | 17 | 14 | 73 | 0 | 7 | 17 | 40 | 20 |
| ai_security | 18 | 0 | 0 | 18 | 0 | 8 | 0 | 2 | 0 |
| finance | 66 | 3 | 0 | 63 | 0 | 16 | 3 | 0 | 0 |
| security | 105 | 5 | 0 | 89 | 11 | 0 | 5 | 0 | 46 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `expku.com` | 4 | security | [Apache Gravitino 1.2.1 版本存在服务端请求伪造漏洞，攻击者可利用该漏洞发起 SSRF 攻击](http://www.expku.com/web/56497.html) |
| `avleonov.com` | 2 | security | [微软 8 月补丁日修复 401 项漏洞，Windows WinSock 提权漏洞已遭利用](https://avleonov.com/2026/08/12/i125-august-microsoft-patch-tuesday/) |
| `aws.amazon.com` | 1 | security | [亚马逊 AWS 发布 S3 存储桶过度授权访问的识别与修复指南](https://aws.amazon.com/blogs/security/securing-your-amazon-s3-buckets-identifying-and-remediating-over-permissioned-access/) |
| `cxsecurity.com` | 1 | security | [iOS 蓝牙个人局域网零成本以太网网关漏洞可利用 62078 端口进行攻击](https://cxsecurity.com/issue/WLB-2026080005) |
| `github.security.telekom.com` | 1 | security | [Red Hat 发行版 ABRTraryRoot 漏洞链：本地普通用户可提权至 Root](https://github.security.telekom.com/2026/08/ABRTraryRoot-local-privilege-escalation.html) |
| `hackingdream.net` | 1 | security | [模型上下文协议 MCP 渗透测试备忘录发布，涵盖所有可能的攻击模式与测试流程](https://www.hackingdream.net/2026/08/mcp-penetration-testing-cheatsheet-all.html) |
| `key08.com` | 1 | security | [基于模型注意力机制构建高效 Web CTF 自动化 Agent 技术研究](https://key08.com/index.php/2026/08/10/3275.html) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
