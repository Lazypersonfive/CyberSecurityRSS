# Source Registry Audit

- generated_for: 2026-06-16
- dates: 2026-06-16, 2026-06-15, 2026-06-14, 2026-06-13, 2026-06-12, 2026-06-11, 2026-06-10

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 97 | 15 | 19 | 63 | 0 | 5 | 15 | 40 | 17 |
| ai_security | 63 | 13 | 1 | 49 | 0 | 6 | 13 | 18 | 6 |
| finance | 70 | 3 | 0 | 66 | 1 | 12 | 3 | 0 | 0 |
| security | 105 | 18 | 0 | 67 | 20 | 0 | 18 | 3 | 35 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `0.0.0.0:8080` | 5 | security | [phpBB 论坛修复潜伏十年的身份验证绕过漏洞，支持一键接管管理员账号](http://0.0.0.0:8080/post/64340) |
| `cyberkendra.com` | 4 | security | [研究员发布 Windows Defender 提权 0-day 漏洞 RoguePlanet 及其 PoC](https://www.cyberkendra.com/2026/06/microsoft-defender-zero-day-poc-gives.html) |
| `securityweek.com` | 3 | security | [Ivanti Sentry 关键 OS 命令注入漏洞遭到在野利用，蜜罐捕获到针对该漏洞的攻击尝试](https://www.securityweek.com/ivanti-sentry-exploitation-attempts-hitting-honeypots/) |
| `blog.nsfocus.net` | 2 | security | [Linux 内核 Fragnesia 权限提升漏洞 CVE-2026-46300 已被成功复现](https://blog.nsfocus.net/%e3%80%90%e5%b7%b2%e5%a4%8d%e7%8e%b0%e3%80%91linux%e5%86%85%e6%a0%b8fragnesia%e6%9d%83%e9%99%90%e6%8f%90%e5%8d%87%e6%bc%8f%e6%b4%9e%ef%bc%88cve-2026-46300%ef%bc%89-2/) |
| `cxsecurity.com` | 2 | security | [Windows Defender 竞争条件漏洞可导致本地权限提升](https://cxsecurity.com/issue/WLB-2026060013) |
| `defend.network` | 2 | security | [Arch Linux 供应链遭蠕虫攻击及 Velvet Ant 组织植入 Linux 后门](https://defend.network/briefings/arch-linux-supply-chain-velvet-ant-linux-backdoor-2026-06-13.html) |
| `infosecurity-magazine.com` | 1 | security | [WordPress 流行插件遭劫持导致 120 万个站点被植入后门](https://www.infosecurity-magazine.com/news/wordpress-plugin-supply-chain/) |
| `ir.americanexpress.com` | 1 | finance | [美国运通宣布拟收购欧洲领先的餐厅预订平台 TheFork 以扩展生活服务生态](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Announces-Proposed-Acquisition-of-TheFork-a-Leading-European-Restaurant-Booking-Platform/default.aspx) |
| `solidot.org` | 1 | security | [本田思域车载系统被曝存在“邪恶女佣”漏洞，攻击者可通过 USB 接口刷入任意固件](https://www.solidot.org/story?sid=84576) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
