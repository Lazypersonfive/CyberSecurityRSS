# Source Registry Audit

- generated_for: 2026-07-10
- dates: 2026-07-10, 2026-07-09, 2026-07-08, 2026-07-07, 2026-07-06, 2026-07-05, 2026-07-04

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 100 | 14 | 16 | 69 | 1 | 2 | 14 | 43 | 17 |
| ai_security | 65 | 2 | 0 | 63 | 0 | 5 | 2 | 3 | 19 |
| finance | 70 | 3 | 0 | 66 | 1 | 14 | 3 | 0 | 0 |
| security | 105 | 8 | 0 | 90 | 7 | 0 | 8 | 0 | 65 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cxsecurity.com` | 3 | security | [7-Zip 26.02 及以下版本 RAR5 备用数据流名称冲突导致 MotW 安全标记绕过漏洞](https://cxsecurity.com/issue/WLB-2026070002) |
| `defend.network` | 3 | security | [Gitea 身份验证绕过漏洞 CVE-2026-20896 遭利用，GitHub 代理工作流泄露私有仓库数据](https://defend.network/briefings/github-gitea-google-dialogflow-android-redwing-2026-07-08.html) |
| `infosecurity-magazine.com` | 1 | security | [Opera GX 浏览器漏洞允许恶意网站通过自动安装 Mod 插件窃取用户数据](https://www.infosecurity-magazine.com/news/opera-gx-flaw-gx-mods-css/) |
| `ir.americanexpress.com` | 1 | finance | [美国运通公司正式发布 2026 年度《多德-弗兰克法案》压力测试结果](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Releases-2026-Dodd-Frank-Act-Stress-Test-Results/default.aspx) |
| `machinelearning.apple.com` | 1 | ai | [Apple 研究院提出 Conformal Thinking 框架以控制推理计算预算风险](https://machinelearning.apple.com/research/conformal-thinking-risk-control) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
