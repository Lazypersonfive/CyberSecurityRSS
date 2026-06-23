# Source Registry Audit

- generated_for: 2026-06-24
- dates: 2026-06-24, 2026-06-23, 2026-06-22, 2026-06-21, 2026-06-20, 2026-06-19, 2026-06-18

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 23 | 14 | 67 | 1 | 5 | 23 | 35 | 17 |
| ai_security | 60 | 10 | 5 | 45 | 0 | 8 | 10 | 8 | 14 |
| finance | 70 | 2 | 0 | 68 | 0 | 12 | 2 | 0 | 0 |
| security | 105 | 13 | 0 | 72 | 20 | 0 | 13 | 0 | 42 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `0.0.0.0:8080` | 10 | security | [iPhone 曝出 Usbliter8 BootROM 漏洞可绕过安全启动链且无法通过软件修复](http://0.0.0.0:8080/post/64374) |
| `securityweek.com` | 3 | security | [三星 KNOX 安全框架存在长达八年的释放后使用漏洞可导致内核级攻击](https://www.securityweek.com/eight-year-old-samsung-knox-flaw-exposed-millions-of-galaxy-devices-to-kernel-attacks/) |
| `cxsecurity.com` | 2 | security | [思源笔记 SiYuan 3.5.9 及以下版本存在恶意集市包远程代码执行漏洞](https://cxsecurity.com/issue/WLB-2026060014) |
| `defend.network` | 2 | security | [微软披露 AutoJack 漏洞可劫持 AI 代理实现远程代码执行](https://defend.network/briefings/autojack-ai-exploit-socgholish-disrupted-klue-salesforc-2026-06-22.html) |
| `solidot.org` | 2 | security | [Linux 7.2 内核彻底移除危险函数 strncpy 以消除内存信息泄露隐患](https://www.solidot.org/story?sid=84644) |
| `cyberkendra.com` | 1 | security | [libssh2 开源库曝出高危漏洞 CVE-2026-55200 允许远程攻击者实现零认证代码执行](https://www.cyberkendra.com/2026/06/cve-2026-55200-critical-libssh2-flaw.html) |
| `machinelearning.apple.com` | 1 | ai | [苹果研究揭示 LLM 评审团存在相关性误差，九名评委的实际投票效力仅相当于两票](https://machinelearning.apple.com/research/correlated-llm-evaluation-panels) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
