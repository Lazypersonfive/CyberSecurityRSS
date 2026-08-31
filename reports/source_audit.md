# Source Registry Audit

- generated_for: 2026-08-31
- dates: 2026-08-31, 2026-08-30, 2026-08-29, 2026-08-28, 2026-08-27, 2026-08-26, 2026-08-25

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 13 | 27 | 62 | 3 | 8 | 13 | 38 | 22 |
| ai_security | 25 | 2 | 1 | 22 | 0 | 7 | 2 | 2 | 5 |
| finance | 70 | 5 | 0 | 65 | 0 | 20 | 5 | 0 | 0 |
| security | 105 | 7 | 0 | 91 | 7 | 0 | 6 | 3 | 48 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `machinelearning.apple.com` | 3 | ai | [苹果研究团队推出 Agent Seer：通过理解工具规范自动合成 AI 智能体测试场景](https://machinelearning.apple.com/research/agent-seer-synthesizing-scenarios) |
| `guidepointsecurity.com` | 1 | security | [企业内网权限提升风险：利用 Active Directory 证书服务数据库进行威胁狩猎与检测](https://www.guidepointsecurity.com/blog/detecting-privilege-escalaction-through-adcs/) |
| `micahflee.com` | 1 | security | [利用隔离沙箱环境构建安全的 AI 编程智能体开发流程](https://micahflee.com/sandboxing-coding-agents/) |
| `nosec.org` | 1 | security | [微软SharePoint曝出多个高危安全漏洞，企业协作平台面临内部文件泄露风险](https://nosec.org/home/detail/5975.html) |
| `paddo.dev` | 1 | security | [开源组件 LiteLLM 遭供应链投毒导致超过 2500 家组织及 43 万条构建流水线受影响](https://paddo.dev/blog/forty-minutes-five-months/) |
| `pentestpartners.com` | 1 | security | [研究人员通过单一SSID配置缺陷成功突破工业控制系统OT与IT环境的物理隔离](https://www.pentestpartners.com/security-blog/one-ssid-to-rule-them-all/) |
| `solidot.org` | 1 | security | [Google Pixel 11 取消硬件 MTE 支持引发 Android 安全加固项目担忧](https://www.solidot.org/story?sid=85233) |
| `xeiaso.net` | 1 | security | [GNU gzip 曝出内存安全漏洞 CVE-2026-41992，LZH 解码器存在越界读取风险](https://xeiaso.net/shitposts/no-way-to-prevent-this/memory-safety/CVE-2026-41992/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
