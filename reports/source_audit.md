# Source Registry Audit

- generated_for: 2026-10-08
- dates: 2026-10-08, 2026-10-05, 2026-10-01, 2026-09-28, 2026-09-21, 2026-09-17, 2026-09-14

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 12 | 21 | 70 | 2 | 8 | 12 | 41 | 9 |
| ai_security | 66 | 8 | 6 | 51 | 1 | 0 | 7 | 11 | 28 |
| finance | 70 | 18 | 2 | 50 | 0 | 9 | 18 | 2 | 0 |
| security | 105 | 16 | 0 | 83 | 6 | 0 | 13 | 3 | 43 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `expku.com` | 3 | security | [Ecava IntegraXor IGX 16.0.701.10版本存在远程代码执行漏洞](http://www.expku.com/remote/56544.html) |
| `govuln.com` | 2 | security | [OpenCode开源项目中发现远程代码执行漏洞（GHSA-632h-h47v-g4x4）及其利用分析](https://govuln.com/news/url/n9NW) |
| `machinelearning.apple.com` | 2 | ai | [苹果推出RLTL;DR研究：通过内化自生成反馈实现AI模型的自我提升](https://machinelearning.apple.com/research/rltl-dr-self-improvement) |
| `aws.amazon.com` | 1 | ai_security | [配置AI漏洞处置测试套件第二部分：转向文件的设计与实践](https://aws.amazon.com/blogs/security/configuring-your-ai-vulnerability-harness-part-2-the-steering-file/) |
| `paddo.dev` | 1 | security | [Vite安全漏洞CVE-2026-39364被用于针对云端与容器开发环境的路径穿越攻击](https://paddo.dev/blog/dev-server-left-the-laptop/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
