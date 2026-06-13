# Source Registry Audit

- generated_for: 2026-06-14
- dates: 2026-06-14, 2026-06-13, 2026-06-12, 2026-06-11, 2026-06-10, 2026-06-09, 2026-06-08

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 94 | 15 | 18 | 61 | 0 | 8 | 15 | 35 | 5 |
| ai_security | 68 | 13 | 0 | 55 | 0 | 8 | 13 | 14 | 10 |
| finance | 70 | 3 | 0 | 67 | 0 | 16 | 3 | 0 | 0 |
| security | 105 | 20 | 0 | 75 | 10 | 0 | 20 | 3 | 33 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cyberkendra.com` | 4 | security | [研究员发布 Windows Defender 提权 0-day 漏洞 RoguePlanet 及其 PoC](https://www.cyberkendra.com/2026/06/microsoft-defender-zero-day-poc-gives.html) |
| `0.0.0.0:8080` | 3 | security | [微软修复正在被积极利用的 Exchange Server 零日漏洞 CVE-2026-42897](http://0.0.0.0:8080/post/64333) |
| `securityweek.com` | 2 | security | [Ivanti Sentry 关键 OS 命令注入漏洞遭到野外探测，攻击者试图获取 Root 权限](https://www.securityweek.com/ivanti-sentry-exploitation-attempts-hitting-honeypots/) |
| `defend.network` | 1 | security | [Arch Linux 软件仓库遭遇供应链蠕虫攻击，数百个软件包被植入 eBPF 后门](https://defend.network/briefings/arch-linux-supply-chain-velvet-ant-linux-backdoor-2026-06-13.html) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
