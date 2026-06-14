# Source Registry Audit

- generated_for: 2026-06-15
- dates: 2026-06-15, 2026-06-14, 2026-06-13, 2026-06-12, 2026-06-11, 2026-06-10, 2026-06-09

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 97 | 14 | 22 | 61 | 0 | 5 | 14 | 41 | 12 |
| ai_security | 62 | 12 | 0 | 50 | 0 | 7 | 12 | 16 | 6 |
| finance | 70 | 3 | 0 | 67 | 0 | 14 | 3 | 0 | 0 |
| security | 105 | 19 | 0 | 73 | 13 | 0 | 19 | 3 | 35 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `0.0.0.0:8080` | 4 | security | [微软修复正在被积极利用的 Exchange Server 零日漏洞 CVE-2026-42897](http://0.0.0.0:8080/post/64333) |
| `cyberkendra.com` | 4 | security | [研究员发布 Windows Defender 提权 0-day 漏洞 RoguePlanet 及其 PoC](https://www.cyberkendra.com/2026/06/microsoft-defender-zero-day-poc-gives.html) |
| `securityweek.com` | 3 | security | [Ivanti Sentry 关键 OS 命令注入漏洞遭到在野利用，蜜罐捕获到针对该漏洞的攻击尝试](https://www.securityweek.com/ivanti-sentry-exploitation-attempts-hitting-honeypots/) |
| `defend.network` | 1 | security | [Arch Linux 软件仓库遭遇供应链蠕虫攻击，数百个软件包被植入 eBPF 后门](https://defend.network/briefings/arch-linux-supply-chain-velvet-ant-linux-backdoor-2026-06-13.html) |
| `solidot.org` | 1 | security | [本田思域车载系统被曝存在“邪恶女佣”漏洞，攻击者可通过 USB 接口刷入任意固件](https://www.solidot.org/story?sid=84576) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
