# Source Registry Audit

- generated_for: 2026-09-21
- dates: 2026-09-21, 2026-09-17, 2026-09-14, 2026-09-10, 2026-09-07, 2026-09-03, 2026-08-31

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 102 | 14 | 16 | 70 | 2 | 11 | 14 | 38 | 7 |
| ai_security | 69 | 13 | 3 | 50 | 3 | 0 | 12 | 7 | 29 |
| finance | 70 | 10 | 3 | 57 | 0 | 9 | 10 | 3 | 0 |
| security | 105 | 13 | 0 | 88 | 4 | 0 | 10 | 1 | 50 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `aws.amazon.com` | 3 | ai_security, security | [AWS发布安全领域AI应用现状评估：重点关注减少误报以建立信任](https://aws.amazon.com/blogs/security/the-state-of-ai-for-security-measuring-what-matters-most-for-building-trust/) |
| `machinelearning.apple.com` | 2 | ai | [苹果推出动态缩放激活转向技术DSAS 以降低无谓干预对模型性能的损耗](https://machinelearning.apple.com/research/dynamically-scaled-activation-steering) |
| `paddo.dev` | 2 | ai_security, security | [Vite安全漏洞CVE-2026-39364被用于针对云端与容器开发环境的路径穿越攻击](https://paddo.dev/blog/dev-server-left-the-laptop/) |
| `cxsecurity.com` | 1 | security | [ProFTPD mod_sql 认证后 SQL 注入导致远程代码执行漏洞细节及 PoC 分析](https://cxsecurity.com/issue/WLB-2026090006) |
| `solidot.org` | 1 | security | [Pixel 11 手机取消硬件 MTE 安全特性支持致使 GrapheneOS 无法完成适配](https://www.solidot.org/story?sid=85233) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
