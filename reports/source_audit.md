# Source Registry Audit

- generated_for: 2026-10-19
- dates: 2026-10-19, 2026-10-15, 2026-10-12, 2026-10-08, 2026-10-05, 2026-10-01, 2026-09-28

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 11 | 15 | 77 | 2 | 6 | 11 | 43 | 6 |
| ai_security | 66 | 10 | 5 | 48 | 3 | 0 | 9 | 12 | 24 |
| finance | 70 | 18 | 1 | 51 | 0 | 7 | 18 | 1 | 0 |
| security | 105 | 13 | 0 | 87 | 5 | 0 | 12 | 4 | 46 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `expku.com` | 3 | security | [Ecava IntegraXor IGX 16.0.701.10版本存在远程代码执行漏洞](http://www.expku.com/remote/56544.html) |
| `aws.amazon.com` | 2 | ai_security | [AWS Security Agent在真实CVE测试中自主成功利用37个漏洞中的33个](https://aws.amazon.com/blogs/security/aws-security-agent-now-part-of-aws-continuum-exploited-33-of-37-new-real-world-cves/) |
| `govuln.com` | 2 | security | [OpenCode开源项目中发现远程代码执行漏洞（GHSA-632h-h47v-g4x4）及其利用分析](https://govuln.com/news/url/n9NW) |
| `machinelearning.apple.com` | 2 | ai | [苹果开源框架MLX支持Mac Studio通过RDMA实现本地与分布式大模型推理](https://machinelearning.apple.com/research/mlx-distributed-inference) |
| `pentestpartners.com` | 1 | ai_security | [分析生成式AI中的提示词注入威胁及其安全防护界限](https://www.pentestpartners.com/security-blog/your-ai-can-access-it-can-an-attacker/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
