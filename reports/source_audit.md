# Source Registry Audit

- generated_for: 2026-11-13
- dates: 2026-11-13, 2026-11-12, 2026-11-09, 2026-11-05, 2026-11-02, 2026-10-29, 2026-10-26

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 102 | 14 | 18 | 69 | 1 | 12 | 14 | 37 | 2 |
| ai_security | 70 | 15 | 1 | 51 | 3 | 1 | 12 | 7 | 23 |
| finance | 70 | 15 | 2 | 52 | 1 | 4 | 15 | 2 | 0 |
| security | 105 | 24 | 0 | 77 | 4 | 0 | 20 | 5 | 49 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `threatninja.net` | 2 | security | [SSHole漏洞分析：Alpine Linux系统OpenSSH密码认证绕过](https://threatninja.net/sshole-alpine-ssh-password-authentication-bypass/) |
| `bestwing.me` | 1 | ai_security | [ZeroMDASH：基于领域自适应的Agent-Native通用漏洞挖掘工程实践](https://bestwing.me/zeromdash-agent-native-vulnerability-mining.html) |
| `blog.nsfocus.net` | 1 | security | [Linux内核IPv4 TCP模块存在释放后重用高危漏洞CVE-2026-98432](https://blog.nsfocus.net/linux%e5%86%85%e6%a0%b8ipv4-tcp%e9%87%8a%e6%94%be%e5%90%8e%e9%87%8d%e7%94%a8%e6%bc%8f%e6%b4%9e%ef%bc%88cve-2026-98432%ef%bc%89%e9%80%9a%e5%91%8a/) |
| `guidepointsecurity.com` | 1 | ai_security | [AI代理无需利用漏洞即可产生风险，安全防护需超出终端范围扩展至权限管理](https://www.guidepointsecurity.com/blog/ai-agent-security-beyond-the-endpoint/) |
| `ir.americanexpress.com` | 1 | finance | [美国运通发布2026年第三季度财务业绩报告](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Reports-Third-Quarter-2026-Financial-Results/default.aspx) |
| `machinelearning.apple.com` | 1 | ai | [研究探讨语言模型对齐的理论极限及强化学习等常见方法](https://machinelearning.apple.com/research/theoretical-limits-alignment) |
| `paddo.dev` | 1 | ai_security | [AI推动漏洞挖掘成本降低：CVE数量由1月的4302个飙升至10月的17052个](https://paddo.dev/blog/the-haystack-tripled/) |
| `shubs.io` | 1 | security | [研究人员发现某知名汽车品牌遥控解锁机制漏洞，可导致全球多款车型被远程任意解锁](https://shubs.io/unlocking-any-car-from-x-brand-in-most-of-the-world/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
