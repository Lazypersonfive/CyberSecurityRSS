# Source Registry Audit

- generated_for: 2026-10-01
- dates: 2026-10-01, 2026-09-28, 2026-09-21, 2026-09-17, 2026-09-14, 2026-09-10, 2026-09-07

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 102 | 11 | 20 | 70 | 1 | 9 | 11 | 40 | 9 |
| ai_security | 70 | 14 | 4 | 50 | 2 | 0 | 13 | 6 | 30 |
| finance | 70 | 14 | 2 | 54 | 0 | 8 | 14 | 2 | 0 |
| security | 105 | 19 | 0 | 82 | 4 | 0 | 15 | 1 | 47 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `govuln.com` | 2 | security | [OpenCode开源项目中发现远程代码执行漏洞（GHSA-632h-h47v-g4x4）及其利用分析](https://govuln.com/news/url/n9NW) |
| `paddo.dev` | 2 | ai_security, security | [Vite安全漏洞CVE-2026-39364被用于针对云端与容器开发环境的路径穿越攻击](https://paddo.dev/blog/dev-server-left-the-laptop/) |
| `aws.amazon.com` | 1 | ai_security | [AWS发布安全领域AI应用现状评估：重点关注减少误报以建立信任](https://aws.amazon.com/blogs/security/the-state-of-ai-for-security-measuring-what-matters-most-for-building-trust/) |
| `cxsecurity.com` | 1 | security | [ProFTPD mod_sql 认证后 SQL 注入导致远程代码执行漏洞细节及 PoC 分析](https://cxsecurity.com/issue/WLB-2026090006) |
| `machinelearning.apple.com` | 1 | ai | [苹果推出动态缩放激活转向技术DSAS 以降低无谓干预对模型性能的损耗](https://machinelearning.apple.com/research/dynamically-scaled-activation-steering) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
