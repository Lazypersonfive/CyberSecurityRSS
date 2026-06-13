# Source Registry Audit

- generated_for: 2026-06-13
- dates: 2026-06-13, 2026-06-12, 2026-06-11, 2026-06-10, 2026-06-09, 2026-06-08, 2026-06-07

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 94 | 15 | 16 | 63 | 0 | 8 | 15 | 35 | 0 |
| ai_security | 69 | 12 | 0 | 57 | 0 | 8 | 12 | 11 | 12 |
| finance | 70 | 4 | 0 | 66 | 0 | 14 | 4 | 0 | 0 |
| security | 105 | 18 | 0 | 80 | 7 | 0 | 18 | 4 | 32 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cyberkendra.com` | 4 | security | [研究员发布 Windows Defender 提权 0-day 漏洞 RoguePlanet 及其 PoC](https://www.cyberkendra.com/2026/06/microsoft-defender-zero-day-poc-gives.html) |
| `0.0.0.0:8080` | 2 | security | [微软正式修补已被积极利用的 Exchange Server 零日漏洞 CVE-2026-42897](http://0.0.0.0:8080/post/64333) |
| `securityweek.com` | 1 | security | [Windows Defender零日漏洞RoguePlanet被披露可实现本地提权](https://www.securityweek.com/new-windows-zero-day-exploit-rogueplanet-released/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
