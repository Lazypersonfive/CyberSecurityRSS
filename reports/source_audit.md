# Source Registry Audit

- generated_for: 2026-08-26
- dates: 2026-08-26, 2026-08-25, 2026-08-24, 2026-08-23, 2026-08-22, 2026-08-21, 2026-08-20

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 16 | 16 | 71 | 2 | 5 | 16 | 37 | 26 |
| ai_security | 23 | 2 | 0 | 21 | 0 | 9 | 2 | 1 | 0 |
| finance | 68 | 7 | 0 | 61 | 0 | 14 | 7 | 0 | 0 |
| security | 105 | 7 | 0 | 88 | 10 | 0 | 5 | 1 | 44 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cxsecurity.com` | 4 | security | [WordPress 插件 WPZOOM Portfolio 1.4.21 反射型跨站脚本漏洞预警](https://cxsecurity.com/issue/WLB-2026080012) |
| `machinelearning.apple.com` | 2 | ai | [苹果研究内化视觉思维技术，旨在降低多模态大模型在主动视频推理中的开销](https://machinelearning.apple.com/research/internalized-visual-thinking) |
| `pentestpartners.com` | 2 | security | [研究人员通过单一SSID配置缺陷成功突破工业控制系统OT与IT环境的物理隔离](https://www.pentestpartners.com/security-blog/one-ssid-to-rule-them-all/) |
| `fidelissecurity.com` | 1 | security | [解析 WordPress REST API 安全：wp2shell 攻击链揭示的利用风险与防御](https://fidelissecurity.com/threatgeek/threat-detection-response/wordpress-rest-api-security-wp2shell-attack-chain/) |
| `key08.com` | 1 | security | [对抗 AI 自动化逆向工程：二进制文件混淆与反 AI 识别技术探索](https://key08.com/index.php/2026/08/23/3296.html) |
| `nosec.org` | 1 | security | [微软SharePoint曝出多个高危安全漏洞，企业协作平台面临内部文件泄露风险](https://nosec.org/home/detail/5975.html) |
| `solidot.org` | 1 | security | [卡巴斯基发现首例针对汽车 Android 主机的恶意程序，利用固件更新传播](https://www.solidot.org/story?sid=85168) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
