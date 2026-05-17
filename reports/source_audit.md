# Source Registry Audit

- generated_for: 2026-05-18
- dates: 2026-05-18, 2026-05-17, 2026-05-16, 2026-05-15, 2026-05-14, 2026-05-13, 2026-05-12

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 100 | 12 | 13 | 75 | 0 | 15 | 12 | 33 | 1 |
| ai_security | 67 | 16 | 4 | 47 | 0 | 11 | 16 | 26 | 9 |
| finance | 69 | 3 | 0 | 66 | 0 | 17 | 3 | 0 | 0 |
| security | 103 | 13 | 0 | 82 | 8 | 0 | 13 | 6 | 15 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blog.csdn.net` | 3 | security | [ARM64 架构下 this_cpu_ops 性能优化探讨与内核页表挑战](https://blog.csdn.net/21cnbao/article/details/161028912) |
| `k8gege.org` | 3 | security | [AI 渗透工具 Kali & HexStrike 被发现存在多个 SSE 导致的 RCE 漏洞](http://k8gege.org/p/hexstrike_0day.html) |
| `furutsuki.hatenablog.com` | 2 | security | [Daily AlpacaHack：面向初学者的常设 CTF 挑战与解题分享](https://furutsuki.hatenablog.com/entry/2026/05/14/002228) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
