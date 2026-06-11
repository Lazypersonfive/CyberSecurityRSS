# Source Registry Audit

- generated_for: 2026-06-11
- dates: 2026-06-11, 2026-06-10, 2026-06-09, 2026-06-08, 2026-06-07, 2026-06-06, 2026-06-05

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 96 | 12 | 16 | 68 | 0 | 8 | 12 | 35 | 0 |
| ai_security | 69 | 11 | 0 | 58 | 0 | 8 | 11 | 8 | 14 |
| finance | 70 | 4 | 0 | 66 | 0 | 16 | 4 | 0 | 0 |
| security | 105 | 17 | 0 | 86 | 2 | 0 | 17 | 2 | 32 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cyberkendra.com` | 1 | security | [Windows Defender零日漏洞PoC发布可在已打补丁系统获取SYSTEM权限](https://www.cyberkendra.com/2026/06/microsoft-defender-zero-day-poc-gives.html) |
| `securityweek.com` | 1 | security | [Windows Defender零日漏洞RoguePlanet被披露可实现本地提权](https://www.securityweek.com/new-windows-zero-day-exploit-rogueplanet-released/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
