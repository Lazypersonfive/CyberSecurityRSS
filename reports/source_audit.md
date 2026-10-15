# Source Registry Audit

- generated_for: 2026-10-15
- dates: 2026-10-15, 2026-10-12, 2026-10-08, 2026-10-05, 2026-10-01, 2026-09-28, 2026-09-21

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 10 | 19 | 74 | 2 | 6 | 10 | 43 | 8 |
| ai_security | 66 | 10 | 6 | 48 | 2 | 0 | 9 | 12 | 26 |
| finance | 70 | 17 | 2 | 51 | 0 | 7 | 17 | 2 | 0 |
| security | 105 | 14 | 0 | 86 | 5 | 0 | 13 | 3 | 47 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `expku.com` | 3 | security | [Ecava IntegraXor IGX 16.0.701.10版本存在远程代码执行漏洞](http://www.expku.com/remote/56544.html) |
| `govuln.com` | 2 | security | [OpenCode开源项目中发现远程代码执行漏洞（GHSA-632h-h47v-g4x4）及其利用分析](https://govuln.com/news/url/n9NW) |
| `machinelearning.apple.com` | 2 | ai | [苹果推出RLTL;DR研究：通过内化自生成反馈实现AI模型的自我提升](https://machinelearning.apple.com/research/rltl-dr-self-improvement) |
| `aws.amazon.com` | 1 | ai_security | [配置AI漏洞处置测试套件第二部分：转向文件的设计与实践](https://aws.amazon.com/blogs/security/configuring-your-ai-vulnerability-harness-part-2-the-steering-file/) |
| `pentestpartners.com` | 1 | ai_security | [分析生成式AI中的提示词注入威胁及其安全防护界限](https://www.pentestpartners.com/security-blog/your-ai-can-access-it-can-an-attacker/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
