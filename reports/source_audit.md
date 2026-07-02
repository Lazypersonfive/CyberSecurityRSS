# Source Registry Audit

- generated_for: 2026-07-03
- dates: 2026-07-03, 2026-07-02, 2026-07-01, 2026-06-30, 2026-06-29, 2026-06-28, 2026-06-27

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 18 | 16 | 71 | 0 | 4 | 18 | 44 | 17 |
| ai_security | 65 | 8 | 1 | 56 | 0 | 8 | 8 | 5 | 17 |
| finance | 70 | 2 | 0 | 68 | 0 | 14 | 2 | 0 | 0 |
| security | 105 | 4 | 0 | 92 | 9 | 0 | 4 | 2 | 68 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `defend.network` | 5 | security | [Argo CD 未修复 RCE 漏洞可导致 Kubernetes 集群被接管](https://defend.network/briefings/argo-cd-kubernetes-chocopoc-github-scattered-spider-2026-07-02.html) |
| `infosecurity-magazine.com` | 2 | security | [美国联邦保险监管机构证实因 Oracle PeopleSoft 零日漏洞导致敏感数据泄露](https://www.infosecurity-magazine.com/news/us-insurance-regulator-confirms/) |
| `cnblogs.com` | 1 | security | [结合 Trae、MCP 与 Burp Suite 实现自动化渗透测试与漏洞挖掘流程](https://www.cnblogs.com/backlion/p/20999711) |
| `thedfirreport.com` | 1 | security | [从 Bing 搜索到勒索软件：Bumblebee 与 AdaptixC2 协同投递 Akira 勒索病毒](https://thedfirreport.com/2026/06/29/from-bing-search-to-ransomware-bumblebee-and-adaptixc2-deliver-akira-3/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
