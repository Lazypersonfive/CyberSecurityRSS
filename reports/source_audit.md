# Source Registry Audit

- generated_for: 2026-08-24
- dates: 2026-08-24, 2026-08-23, 2026-08-22, 2026-08-21, 2026-08-20, 2026-08-19, 2026-08-18

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 17 | 14 | 73 | 1 | 4 | 17 | 39 | 25 |
| ai_security | 24 | 3 | 0 | 21 | 0 | 6 | 3 | 0 | 1 |
| finance | 68 | 7 | 0 | 61 | 0 | 11 | 7 | 0 | 0 |
| security | 105 | 5 | 0 | 91 | 9 | 0 | 3 | 0 | 45 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cxsecurity.com` | 4 | security | [WordPress 插件 WPZOOM Portfolio 1.4.21 反射型跨站脚本漏洞预警](https://cxsecurity.com/issue/WLB-2026080012) |
| `expku.com` | 1 | security | [Nmap 7.99 版本存在扩展头整数下溢漏洞 CVE-2026-58058 可导致拒绝服务](http://www.expku.com/dos/56503.html) |
| `fidelissecurity.com` | 1 | security | [解析 WordPress REST API 安全：wp2shell 攻击链揭示的利用风险与防御](https://fidelissecurity.com/threatgeek/threat-detection-response/wordpress-rest-api-security-wp2shell-attack-chain/) |
| `key08.com` | 1 | security | [对抗 AI 自动化逆向工程：二进制文件混淆与反 AI 识别技术探索](https://key08.com/index.php/2026/08/23/3296.html) |
| `machinelearning.apple.com` | 1 | ai | [苹果发布数据受限下的混合预训练缩放定律研究：优化稀缺专业领域数据利用率](https://machinelearning.apple.com/research/scaling-laws-mixture-pretraining) |
| `pentestpartners.com` | 1 | security | [GivEnergy 家庭电池系统存在多项安全漏洞，可能导致黑客访问用户家庭网络并干扰运行](https://www.pentestpartners.com/security-blog/givenergy-enters-administration-legacy-home-batteries-still-expose-customer-networks/) |
| `solidot.org` | 1 | security | [卡巴斯基发现首例针对汽车 Android 主机的恶意程序，利用固件更新传播](https://www.solidot.org/story?sid=85168) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
