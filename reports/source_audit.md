# Source Registry Audit

- generated_for: 2026-06-30
- dates: 2026-06-30, 2026-06-29, 2026-06-28, 2026-06-27, 2026-06-26, 2026-06-25, 2026-06-24

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 20 | 19 | 65 | 1 | 1 | 20 | 47 | 16 |
| ai_security | 67 | 9 | 4 | 54 | 0 | 8 | 9 | 7 | 23 |
| finance | 70 | 1 | 0 | 68 | 1 | 16 | 1 | 0 | 0 |
| security | 105 | 9 | 0 | 67 | 29 | 0 | 9 | 0 | 54 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `0.0.0.0:8080` | 10 | security | [Lantronix 串口转以太网转换器漏洞 CVE-2025-67038 遭在野攻击利用](http://0.0.0.0:8080/post/64390) |
| `defend.network` | 5 | security | [Linux 内核 RCE 漏洞与 AWS Q 凭据窃取漏洞风险预警](https://defend.network/briefings/signal-phishing-linux-kernel-aws-credential-theft-2026-06-27.html) |
| `securityweek.com` | 5 | security | [Linux 内核 DirtyClone 漏洞曝光：本地普通用户可利用页面缓存操作获取 Root 权限](https://www.securityweek.com/dirtyclone-linux-kernel-vulnerability-leads-to-root-access/) |
| `cyberkendra.com` | 3 | security | [Nebula Security 演示 Android 17 首个全链漏洞 IonStack：单链接获取 Root 权限](https://www.cyberkendra.com/2026/06/one-malicious-link-full-root-access.html) |
| `infosecurity-magazine.com` | 2 | security | [美国联邦保险监管机构证实因 Oracle PeopleSoft 零日漏洞导致敏感数据泄露](https://www.infosecurity-magazine.com/news/us-insurance-regulator-confirms/) |
| `sandflysecurity.com` | 2 | security | [Linux Scales eBPF Rootkit 检测分析：针对 Arch 供应链的隐蔽攻击](https://sandflysecurity.com/blog/linux-scales-ebpf-rootkit-detection-and-analysis) |
| `cxsecurity.com` | 1 | security | [思源笔记 SiYuan 3.5.9 及以下版本存在恶意集市包远程代码执行漏洞](https://cxsecurity.com/issue/WLB-2026060014) |
| `ir.americanexpress.com` | 1 | finance | [美国运通发布2026年多德-弗兰克法案压力测试结果，披露公司在假设经济衰退情景下的财务韧性](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Releases-2026-Dodd-Frank-Act-Stress-Test-Results/default.aspx) |
| `machinelearning.apple.com` | 1 | ai | [苹果研究揭示 LLM 评审团存在相关性误差，九名评委的实际投票效力仅相当于两票](https://machinelearning.apple.com/research/correlated-llm-evaluation-panels) |
| `thedfirreport.com` | 1 | security | [从 Bing 搜索到勒索软件：Bumblebee 与 AdaptixC2 协同投递 Akira 勒索病毒](https://thedfirreport.com/2026/06/29/from-bing-search-to-ransomware-bumblebee-and-adaptixc2-deliver-akira-3/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
