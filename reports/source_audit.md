# Source Registry Audit

- generated_for: 2026-08-18
- dates: 2026-08-18, 2026-08-17, 2026-08-16, 2026-08-15, 2026-08-14, 2026-08-13, 2026-08-12

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 21 | 12 | 72 | 0 | 5 | 21 | 40 | 19 |
| ai_security | 16 | 1 | 0 | 15 | 0 | 6 | 1 | 1 | 1 |
| finance | 68 | 5 | 0 | 63 | 0 | 17 | 5 | 0 | 0 |
| security | 105 | 2 | 0 | 96 | 7 | 0 | 2 | 0 | 46 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `expku.com` | 4 | security | [Apache Gravitino 1.2.1 版本存在服务端请求伪造漏洞，攻击者可利用该漏洞发起 SSRF 攻击](http://www.expku.com/web/56497.html) |
| `avleonov.com` | 1 | security | [微软 8 月补丁日修复 401 项漏洞，Windows WinSock 提权漏洞已遭利用](https://avleonov.com/2026/08/12/i125-august-microsoft-patch-tuesday/) |
| `cxsecurity.com` | 1 | security | [iOS 蓝牙个人局域网零成本以太网网关漏洞可利用 62078 端口进行攻击](https://cxsecurity.com/issue/WLB-2026080005) |
| `hackingdream.net` | 1 | security | [模型上下文协议 MCP 渗透测试备忘录发布，涵盖所有可能的攻击模式与测试流程](https://www.hackingdream.net/2026/08/mcp-penetration-testing-cheatsheet-all.html) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
