# Source Registry Audit

- generated_for: 2026-07-13
- dates: 2026-07-13, 2026-07-12, 2026-07-11, 2026-07-10, 2026-07-09, 2026-07-08, 2026-07-07

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 97 | 12 | 20 | 65 | 0 | 4 | 12 | 41 | 15 |
| ai_security | 68 | 1 | 0 | 67 | 0 | 7 | 1 | 5 | 25 |
| finance | 70 | 2 | 0 | 68 | 0 | 12 | 2 | 0 | 0 |
| security | 105 | 12 | 0 | 90 | 3 | 0 | 12 | 2 | 59 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `infosecurity-magazine.com` | 2 | security | [GodDamn 勒索软件利用恶意内核驱动程序 PoisonX 强制关闭系统安全防护软件](https://www.infosecurity-magazine.com/news/ransomware-removes-cybersecurity/) |
| `defend.network` | 1 | security | [Gitea 身份验证绕过漏洞 CVE-2026-20896 遭利用，GitHub 代理工作流泄露私有仓库数据](https://defend.network/briefings/github-gitea-google-dialogflow-android-redwing-2026-07-08.html) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
