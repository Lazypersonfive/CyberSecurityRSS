# Source Registry Audit

- generated_for: 2026-09-07
- dates: 2026-09-07, 2026-09-03, 2026-08-31, 2026-08-30, 2026-08-29, 2026-08-28, 2026-08-27

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 102 | 13 | 20 | 66 | 3 | 11 | 13 | 38 | 13 |
| ai_security | 46 | 9 | 2 | 33 | 2 | 4 | 9 | 5 | 13 |
| finance | 70 | 5 | 1 | 64 | 0 | 16 | 5 | 1 | 0 |
| security | 105 | 8 | 0 | 90 | 7 | 0 | 7 | 2 | 45 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `machinelearning.apple.com` | 3 | ai | [苹果提出REFACTOR-VLA框架：通过无监督库学习构建分层类型化运动程序](https://machinelearning.apple.com/research/refactor-vla-motor-programs) |
| `aws.amazon.com` | 2 | ai_security, security | [使用 Strands Agents SDK 将 Amazon Bedrock Guardrails 扩展至工具交互环节](https://aws.amazon.com/blogs/security/extend-amazon-bedrock-guardrails-to-tool-interactions-using-the-strands-agents-sdk/) |
| `paddo.dev` | 2 | ai_security, security | [GitSpawn漏洞致多款AI代码 Agent打开恶意项目文件夹即可执行代码](https://paddo.dev/blog/gitspawn-opening-the-folder/) |
| `cxsecurity.com` | 1 | security | [ProFTPD mod_sql 认证后 SQL 注入导致远程代码执行漏洞细节及 PoC 分析](https://cxsecurity.com/issue/WLB-2026090006) |
| `guidepointsecurity.com` | 1 | security | [企业内网权限提升风险：利用 Active Directory 证书服务数据库进行威胁狩猎与检测](https://www.guidepointsecurity.com/blog/detecting-privilege-escalaction-through-adcs/) |
| `micahflee.com` | 1 | security | [利用隔离沙箱环境构建安全的 AI 编程智能体开发流程](https://micahflee.com/sandboxing-coding-agents/) |
| `solidot.org` | 1 | security | [Pixel 11 手机取消硬件 MTE 安全特性支持致使 GrapheneOS 无法完成适配](https://www.solidot.org/story?sid=85233) |
| `xeiaso.net` | 1 | security | [GNU gzip 曝出内存安全漏洞 CVE-2026-41992，LZH 解码器存在越界读取风险](https://xeiaso.net/shitposts/no-way-to-prevent-this/memory-safety/CVE-2026-41992/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
