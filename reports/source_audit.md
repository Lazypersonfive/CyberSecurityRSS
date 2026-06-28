# Source Registry Audit

- generated_for: 2026-06-29
- dates: 2026-06-29, 2026-06-28, 2026-06-27, 2026-06-26, 2026-06-25, 2026-06-24, 2026-06-23

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 20 | 18 | 66 | 1 | 1 | 20 | 43 | 18 |
| ai_security | 64 | 11 | 5 | 48 | 0 | 8 | 11 | 7 | 21 |
| finance | 70 | 1 | 0 | 68 | 1 | 15 | 1 | 0 | 0 |
| security | 105 | 10 | 0 | 66 | 29 | 0 | 10 | 0 | 50 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `0.0.0.0:8080` | 11 | security | [Lantronix 串口转以太网转换器漏洞 CVE-2025-67038 遭在野攻击利用](http://0.0.0.0:8080/post/64390) |
| `defend.network` | 5 | security | [Linux 内核 RCE 漏洞与 AWS Q 凭据窃取漏洞风险预警](https://defend.network/briefings/signal-phishing-linux-kernel-aws-credential-theft-2026-06-27.html) |
| `securityweek.com` | 5 | security | [Amazon Q 存在安全漏洞可导致攻击者通过恶意存储库窃取云端凭据](https://www.securityweek.com/amazon-q-flaw-enabled-cloud-credential-theft-via-malicious-repositories/) |
| `cyberkendra.com` | 3 | security | [Nebula Security 演示 Android 17 首个全链漏洞 IonStack：单链接获取 Root 权限](https://www.cyberkendra.com/2026/06/one-malicious-link-full-root-access.html) |
| `cxsecurity.com` | 2 | security | [思源笔记 SiYuan 3.5.9 及以下版本存在恶意集市包远程代码执行漏洞](https://cxsecurity.com/issue/WLB-2026060014) |
| `sandflysecurity.com` | 2 | security | [Linux Scales eBPF Rootkit 检测分析：针对 Arch 供应链的隐蔽攻击](https://sandflysecurity.com/blog/linux-scales-ebpf-rootkit-detection-and-analysis) |
| `ir.americanexpress.com` | 1 | finance | [美国运通发布2026年多德-弗兰克法案压力测试结果，披露公司在假设经济衰退情景下的财务韧性](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Releases-2026-Dodd-Frank-Act-Stress-Test-Results/default.aspx) |
| `machinelearning.apple.com` | 1 | ai | [苹果研究揭示 LLM 评审团存在相关性误差，九名评委的实际投票效力仅相当于两票](https://machinelearning.apple.com/research/correlated-llm-evaluation-panels) |
| `solidot.org` | 1 | security | [Linux 7.2 内核彻底移除危险函数 strncpy 以消除内存信息泄露隐患](https://www.solidot.org/story?sid=84644) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
