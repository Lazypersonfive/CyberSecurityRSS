# Source Registry Audit

- generated_for: 2026-06-12
- dates: 2026-06-12, 2026-06-11, 2026-06-10, 2026-06-09, 2026-06-08, 2026-06-07, 2026-06-06

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 94 | 14 | 16 | 64 | 0 | 6 | 14 | 37 | 0 |
| ai_security | 69 | 12 | 0 | 57 | 0 | 8 | 12 | 9 | 14 |
| finance | 70 | 3 | 0 | 67 | 0 | 15 | 3 | 0 | 0 |
| security | 105 | 17 | 0 | 82 | 6 | 0 | 17 | 2 | 33 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cyberkendra.com` | 4 | security | [研究员发布 Windows Defender 提权 0-day 漏洞 RoguePlanet 及其 PoC](https://www.cyberkendra.com/2026/06/microsoft-defender-zero-day-poc-gives.html) |
| `0.0.0.0:8080` | 1 | security | [AI 开发平台 Langflow 路径遍历漏洞 CVE-2026-5027 遭积极利用](http://0.0.0.0:8080/post/64328) |
| `securityweek.com` | 1 | security | [Windows Defender零日漏洞RoguePlanet被披露可实现本地提权](https://www.securityweek.com/new-windows-zero-day-exploit-rogueplanet-released/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
