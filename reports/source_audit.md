# Source Registry Audit

- generated_for: 2026-08-22
- dates: 2026-08-22, 2026-08-21, 2026-08-20, 2026-08-19, 2026-08-18, 2026-08-17, 2026-08-16

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 17 | 13 | 74 | 1 | 2 | 17 | 44 | 20 |
| ai_security | 24 | 3 | 0 | 21 | 0 | 7 | 3 | 0 | 1 |
| finance | 68 | 7 | 0 | 61 | 0 | 11 | 7 | 0 | 0 |
| security | 105 | 5 | 0 | 97 | 3 | 0 | 4 | 0 | 51 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `cxsecurity.com` | 1 | security | [JSONata 表达式注入漏洞 CVE-2026-77415 可导致远程任意代码执行](https://cxsecurity.com/issue/WLB-2026080011) |
| `expku.com` | 1 | security | [Nmap 7.99 版本存在扩展头整数下溢漏洞 CVE-2026-58058 可导致拒绝服务](http://www.expku.com/dos/56503.html) |
| `fidelissecurity.com` | 1 | security | [解析 WordPress REST API 安全：wp2shell 攻击链揭示的利用风险与防御](https://fidelissecurity.com/threatgeek/threat-detection-response/wordpress-rest-api-security-wp2shell-attack-chain/) |
| `machinelearning.apple.com` | 1 | ai | [苹果发布数据受限下的混合预训练缩放定律研究：优化稀缺专业领域数据利用率](https://machinelearning.apple.com/research/scaling-laws-mixture-pretraining) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
