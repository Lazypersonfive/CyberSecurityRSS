# Source Registry Audit

- generated_for: 2026-07-12
- dates: 2026-07-12, 2026-07-11, 2026-07-10, 2026-07-09, 2026-07-08, 2026-07-07, 2026-07-06

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 97 | 12 | 21 | 64 | 0 | 2 | 12 | 43 | 16 |
| ai_security | 65 | 1 | 0 | 64 | 0 | 7 | 1 | 4 | 24 |
| finance | 70 | 2 | 0 | 68 | 0 | 13 | 2 | 0 | 0 |
| security | 105 | 11 | 0 | 91 | 3 | 0 | 11 | 1 | 64 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cxsecurity.com` | 1 | security | [7-Zip 26.02 及以下版本 RAR5 备用数据流名称冲突导致 MotW 安全标记绕过漏洞](https://cxsecurity.com/issue/WLB-2026070002) |
| `defend.network` | 1 | security | [Gitea 身份验证绕过漏洞 CVE-2026-20896 遭利用，GitHub 代理工作流泄露私有仓库数据](https://defend.network/briefings/github-gitea-google-dialogflow-android-redwing-2026-07-08.html) |
| `infosecurity-magazine.com` | 1 | security | [Opera GX 浏览器漏洞允许恶意网站通过自动安装 Mod 插件窃取用户数据](https://www.infosecurity-magazine.com/news/opera-gx-flaw-gx-mods-css/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
