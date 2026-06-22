# Source Registry Audit

- generated_for: 2026-06-22
- dates: 2026-06-22, 2026-06-21, 2026-06-20, 2026-06-19, 2026-06-18, 2026-06-17, 2026-06-16

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 22 | 14 | 69 | 0 | 5 | 22 | 38 | 18 |
| ai_security | 64 | 10 | 4 | 50 | 0 | 5 | 10 | 9 | 17 |
| finance | 70 | 2 | 0 | 67 | 1 | 10 | 2 | 0 | 0 |
| security | 105 | 15 | 0 | 73 | 17 | 0 | 15 | 0 | 41 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `0.0.0.0:8080` | 7 | security | [CISA 警告 Joomla JCE 扩展存在满分漏洞 CVE-2026-48907，已被用于执行 PHP 代码](http://0.0.0.0:8080/post/64361) |
| `blog.nsfocus.net` | 4 | security | [Linux内核Fragnesia权限提升漏洞CVE-2026-46300已实现复现](https://blog.nsfocus.net/%e3%80%90%e5%b7%b2%e5%a4%8d%e7%8e%b0%e3%80%91linux%e5%86%85%e6%a0%b8fragnesia%e6%9d%83%e9%99%90%e6%8f%90%e5%8d%87%e6%bc%8f%e6%b4%9e%ef%bc%88cve-2026-46300%ef%bc%89-2/) |
| `cxsecurity.com` | 2 | security | [Windows Defender 竞争条件漏洞可导致本地权限提升](https://cxsecurity.com/issue/WLB-2026060013) |
| `defend.network` | 2 | security | [NGINX 修复远程代码执行漏洞：CVE-2026-42530 影响多版本组件](https://defend.network/briefings/nginx-rce-windows-clipper-salesforce-ransomware-2026-06-19.html) |
| `infosecurity-magazine.com` | 1 | security | [WordPress 流行插件遭劫持导致 120 万个站点被植入后门](https://www.infosecurity-magazine.com/news/wordpress-plugin-supply-chain/) |
| `ir.americanexpress.com` | 1 | finance | [美国运通宣布拟收购欧洲领先的餐厅预订平台 TheFork 以扩展生活服务生态](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Announces-Proposed-Acquisition-of-TheFork-a-Leading-European-Restaurant-Booking-Platform/default.aspx) |
| `solidot.org` | 1 | security | [Steam 创意工坊恶意墙纸针对中俄用户传播，利用 Wallpaper Engine 植入后门](https://www.solidot.org/story?sid=84609) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
