# Source Registry Audit

- generated_for: 2026-08-23
- dates: 2026-08-23, 2026-08-22, 2026-08-21, 2026-08-20, 2026-08-19, 2026-08-18, 2026-08-17

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 17 | 13 | 74 | 1 | 2 | 17 | 41 | 24 |
| ai_security | 25 | 3 | 0 | 22 | 0 | 7 | 3 | 0 | 1 |
| finance | 70 | 7 | 0 | 63 | 0 | 14 | 7 | 0 | 0 |
| security | 105 | 4 | 0 | 95 | 6 | 0 | 3 | 0 | 47 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cxsecurity.com` | 3 | security | [Laravel Socialite 5.29.0 之前版本存在 Facebook OIDC Nonce 重放身份验证绕过漏洞](https://cxsecurity.com/issue/WLB-2026080013) |
| `expku.com` | 1 | security | [Nmap 7.99 版本存在扩展头整数下溢漏洞 CVE-2026-58058 可导致拒绝服务](http://www.expku.com/dos/56503.html) |
| `fidelissecurity.com` | 1 | security | [解析 WordPress REST API 安全：wp2shell 攻击链揭示的利用风险与防御](https://fidelissecurity.com/threatgeek/threat-detection-response/wordpress-rest-api-security-wp2shell-attack-chain/) |
| `machinelearning.apple.com` | 1 | ai | [苹果发布数据受限下的混合预训练缩放定律研究：优化稀缺专业领域数据利用率](https://machinelearning.apple.com/research/scaling-laws-mixture-pretraining) |
| `pentestpartners.com` | 1 | security | [GivEnergy 家庭电池系统存在多项安全漏洞，可能导致黑客访问用户家庭网络并干扰运行](https://www.pentestpartners.com/security-blog/givenergy-enters-administration-legacy-home-batteries-still-expose-customer-networks/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
