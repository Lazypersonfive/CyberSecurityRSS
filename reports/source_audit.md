# Source Registry Audit

- generated_for: 2026-10-26
- dates: 2026-10-26, 2026-10-22, 2026-10-19, 2026-10-15, 2026-10-12, 2026-10-08, 2026-10-05

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 17 | 14 | 72 | 2 | 6 | 17 | 43 | 3 |
| ai_security | 66 | 13 | 4 | 46 | 3 | 0 | 8 | 12 | 24 |
| finance | 70 | 18 | 3 | 48 | 1 | 7 | 18 | 3 | 0 |
| security | 105 | 10 | 0 | 92 | 3 | 0 | 7 | 5 | 52 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `expku.com` | 3 | security | [Ecava IntegraXor IGX 16.0.701.10版本存在远程代码执行漏洞](http://www.expku.com/remote/56544.html) |
| `aws.amazon.com` | 2 | ai_security | [AWS Security Agent在真实CVE测试中自主成功利用37个漏洞中的33个](https://aws.amazon.com/blogs/security/aws-security-agent-now-part-of-aws-continuum-exploited-33-of-37-new-real-world-cves/) |
| `machinelearning.apple.com` | 2 | ai | [苹果开源框架MLX支持Mac Studio通过RDMA实现本地与分布式大模型推理](https://machinelearning.apple.com/research/mlx-distributed-inference) |
| `ir.americanexpress.com` | 1 | finance | [美国运通发布2026年第三季度财务业绩报告](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Reports-Third-Quarter-2026-Financial-Results/default.aspx) |
| `pentestpartners.com` | 1 | ai_security | [分析生成式AI中的提示词注入威胁及其安全防护界限](https://www.pentestpartners.com/security-blog/your-ai-can-access-it-can-an-attacker/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
