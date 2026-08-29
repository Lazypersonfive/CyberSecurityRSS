# Source Registry Audit

- generated_for: 2026-08-29
- dates: 2026-08-29, 2026-08-28, 2026-08-27, 2026-08-26, 2026-08-25, 2026-08-24, 2026-08-23

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 12 | 22 | 68 | 3 | 8 | 12 | 35 | 25 |
| ai_security | 27 | 2 | 1 | 24 | 0 | 9 | 2 | 2 | 4 |
| finance | 68 | 5 | 0 | 63 | 0 | 18 | 5 | 0 | 0 |
| security | 105 | 6 | 0 | 89 | 10 | 0 | 4 | 1 | 45 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cxsecurity.com` | 3 | security | [WordPress 插件 WPZOOM Portfolio 1.4.21 反射型跨站脚本漏洞预警](https://cxsecurity.com/issue/WLB-2026080012) |
| `machinelearning.apple.com` | 3 | ai | [苹果研究团队推出 Agent Seer：通过理解工具规范自动合成 AI 智能体测试场景](https://machinelearning.apple.com/research/agent-seer-synthesizing-scenarios) |
| `pentestpartners.com` | 2 | security | [研究人员通过单一SSID配置缺陷成功突破工业控制系统OT与IT环境的物理隔离](https://www.pentestpartners.com/security-blog/one-ssid-to-rule-them-all/) |
| `guidepointsecurity.com` | 1 | security | [企业内网权限提升风险：利用 Active Directory 证书服务数据库进行威胁狩猎与检测](https://www.guidepointsecurity.com/blog/detecting-privilege-escalaction-through-adcs/) |
| `key08.com` | 1 | security | [对抗 AI 自动化逆向工程：二进制文件混淆与反 AI 识别技术探索](https://key08.com/index.php/2026/08/23/3296.html) |
| `nosec.org` | 1 | security | [微软SharePoint曝出多个高危安全漏洞，企业协作平台面临内部文件泄露风险](https://nosec.org/home/detail/5975.html) |
| `solidot.org` | 1 | security | [卡巴斯基发现首例针对汽车 Android 主机的恶意程序，利用固件更新传播](https://www.solidot.org/story?sid=85168) |
| `xeiaso.net` | 1 | security | [GNU gzip 曝出内存安全漏洞 CVE-2026-41992，LZH 解码器存在越界读取风险](https://xeiaso.net/shitposts/no-way-to-prevent-this/memory-safety/CVE-2026-41992/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
