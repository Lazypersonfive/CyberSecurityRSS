# Source Registry Audit

- generated_for: 2026-06-23
- dates: 2026-06-23, 2026-06-22, 2026-06-21, 2026-06-20, 2026-06-19, 2026-06-18, 2026-06-17

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 23 | 13 | 69 | 0 | 5 | 23 | 35 | 17 |
| ai_security | 60 | 10 | 4 | 46 | 0 | 6 | 10 | 7 | 16 |
| finance | 70 | 2 | 0 | 68 | 0 | 11 | 2 | 0 | 0 |
| security | 105 | 15 | 0 | 75 | 15 | 0 | 15 | 0 | 43 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `0.0.0.0:8080` | 7 | security | [Splunk Enterprise 关键漏洞 CVE-2026-20253 披露数日后即遭野外利用](http://0.0.0.0:8080/post/64364) |
| `blog.nsfocus.net` | 2 | security | [Linux内核Fragnesia权限提升漏洞CVE-2026-46300已实现复现](https://blog.nsfocus.net/%e3%80%90%e5%b7%b2%e5%a4%8d%e7%8e%b0%e3%80%91linux%e5%86%85%e6%a0%b8fragnesia%e6%9d%83%e9%99%90%e6%8f%90%e5%8d%87%e6%bc%8f%e6%b4%9e%ef%bc%88cve-2026-46300%ef%bc%89-2/) |
| `securityweek.com` | 2 | security | [Usbliter8 漏洞利用工具发布，可绕过数百万部 iPhone 的苹果启动防御机制](https://www.securityweek.com/new-exploit-bypasses-apples-boot-defenses-affects-millions-of-iphones/) |
| `solidot.org` | 2 | security | [Linux 7.2 内核彻底移除危险函数 strncpy 以消除内存信息泄露隐患](https://www.solidot.org/story?sid=84644) |
| `cxsecurity.com` | 1 | security | [思源笔记 SiYuan 3.5.9 及以下版本存在恶意集市包远程代码执行漏洞](https://cxsecurity.com/issue/WLB-2026060014) |
| `defend.network` | 1 | security | [NGINX 修复远程代码执行漏洞：CVE-2026-42530 影响多版本组件](https://defend.network/briefings/nginx-rce-windows-clipper-salesforce-ransomware-2026-06-19.html) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
