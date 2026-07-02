# Source Registry Audit

- generated_for: 2026-07-02
- dates: 2026-07-02, 2026-07-01, 2026-06-30, 2026-06-29, 2026-06-28, 2026-06-27, 2026-06-26

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 19 | 16 | 70 | 0 | 3 | 19 | 45 | 16 |
| ai_security | 65 | 7 | 1 | 57 | 0 | 7 | 7 | 5 | 21 |
| finance | 70 | 2 | 0 | 67 | 1 | 15 | 2 | 0 | 0 |
| security | 105 | 5 | 0 | 72 | 28 | 0 | 5 | 1 | 56 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `0.0.0.0:8080` | 12 | security | [Microsoft Defender漏洞BlueHammer被勒索软件利用实施攻击](http://0.0.0.0:8080/post/64411) |
| `securityweek.com` | 6 | security | [Citrix修复NetScaler多个漏洞，包含HTTP/2 Bomb及信息泄露风险](https://www.securityweek.com/citrix-patches-netscaler-vulnerabilities-including-new-http-2-bomb-attack/) |
| `defend.network` | 4 | security | [俄罗斯情报机构利用Signal备份恢复密钥进行钓鱼攻击及Cisco漏洞遭利用](https://defend.network/briefings/russian-phishing-signal-cisco-breach-2026-06-29.html) |
| `infosecurity-magazine.com` | 2 | security | [美国联邦保险监管机构证实因 Oracle PeopleSoft 零日漏洞导致敏感数据泄露](https://www.infosecurity-magazine.com/news/us-insurance-regulator-confirms/) |
| `cnblogs.com` | 1 | security | [结合 Trae、MCP 与 Burp Suite 实现自动化渗透测试与漏洞挖掘流程](https://www.cnblogs.com/backlion/p/20999711) |
| `cyberkendra.com` | 1 | security | [Nebula Security 演示 Android 17 首个全链漏洞 IonStack：单链接获取 Root 权限](https://www.cyberkendra.com/2026/06/one-malicious-link-full-root-access.html) |
| `ir.americanexpress.com` | 1 | finance | [美国运通发布2026年多德-弗兰克法案压力测试结果，披露公司在假设经济衰退情景下的财务韧性](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Releases-2026-Dodd-Frank-Act-Stress-Test-Results/default.aspx) |
| `sandflysecurity.com` | 1 | security | [Linux Scales eBPF Rootkit 检测分析：针对 Arch 供应链的隐蔽攻击](https://sandflysecurity.com/blog/linux-scales-ebpf-rootkit-detection-and-analysis) |
| `thedfirreport.com` | 1 | security | [从 Bing 搜索到勒索软件：Bumblebee 与 AdaptixC2 协同投递 Akira 勒索病毒](https://thedfirreport.com/2026/06/29/from-bing-search-to-ransomware-bumblebee-and-adaptixc2-deliver-akira-3/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
