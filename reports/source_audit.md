# Source Registry Audit

- generated_for: 2026-07-05
- dates: 2026-07-05, 2026-07-04, 2026-07-03, 2026-07-02, 2026-07-01, 2026-06-30, 2026-06-29

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 19 | 14 | 71 | 1 | 5 | 19 | 44 | 16 |
| ai_security | 65 | 6 | 0 | 59 | 0 | 7 | 6 | 5 | 11 |
| finance | 70 | 2 | 0 | 67 | 1 | 15 | 2 | 0 | 0 |
| security | 105 | 4 | 0 | 89 | 12 | 0 | 4 | 2 | 67 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `defend.network` | 6 | security | [Citrix Bleed 2 漏洞遭勒索软件利用及 Microsoft 365 OAuth 令牌窃取攻击预警](https://defend.network/briefings/netnut-citrix-bleed-toddycat-oauth-gmail-2026-07-03.html) |
| `cxsecurity.com` | 2 | security | [7-Zip 26.02 及以下版本存在 RAR5 替代数据流名称冲突导致的 MotW 绕过漏洞](https://cxsecurity.com/issue/WLB-2026070002) |
| `infosecurity-magazine.com` | 2 | security | [美国联邦保险监管机构证实因 Oracle PeopleSoft 零日漏洞导致敏感数据泄露](https://www.infosecurity-magazine.com/news/us-insurance-regulator-confirms/) |
| `cnblogs.com` | 1 | security | [结合 Trae、MCP 与 Burp Suite 实现自动化渗透测试与漏洞挖掘流程](https://www.cnblogs.com/backlion/p/20999711) |
| `ir.americanexpress.com` | 1 | finance | [美国运通公司正式发布 2026 年度《多德-弗兰克法案》压力测试结果](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Releases-2026-Dodd-Frank-Act-Stress-Test-Results/default.aspx) |
| `machinelearning.apple.com` | 1 | ai | [Apple 研究院提出 Conformal Thinking 框架以控制推理计算预算风险](https://machinelearning.apple.com/research/conformal-thinking-risk-control) |
| `thedfirreport.com` | 1 | security | [从 Bing 搜索到勒索软件：Bumblebee 与 AdaptixC2 协同投递 Akira 勒索病毒](https://thedfirreport.com/2026/06/29/from-bing-search-to-ransomware-bumblebee-and-adaptixc2-deliver-akira-3/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
