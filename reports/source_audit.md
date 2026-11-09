# Source Registry Audit

- generated_for: 2026-11-09
- dates: 2026-11-09, 2026-11-05, 2026-11-02, 2026-10-29, 2026-10-26, 2026-10-22, 2026-10-19

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 102 | 20 | 14 | 67 | 1 | 11 | 20 | 38 | 2 |
| ai_security | 70 | 17 | 1 | 48 | 4 | 1 | 11 | 5 | 21 |
| finance | 70 | 16 | 4 | 49 | 1 | 5 | 16 | 4 | 0 |
| security | 105 | 15 | 0 | 87 | 3 | 0 | 11 | 7 | 51 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `aws.amazon.com` | 1 | ai_security | [AWS Security Agent在真实CVE测试中自主成功利用37个漏洞中的33个](https://aws.amazon.com/blogs/security/aws-security-agent-now-part-of-aws-continuum-exploited-33-of-37-new-real-world-cves/) |
| `bestwing.me` | 1 | ai_security | [ZeroMDASH：基于领域自适应的Agent-Native通用漏洞挖掘工程实践](https://bestwing.me/zeromdash-agent-native-vulnerability-mining.html) |
| `blog.nsfocus.net` | 1 | security | [Linux内核IPv4 TCP模块存在释放后重用高危漏洞CVE-2026-98432](https://blog.nsfocus.net/linux%e5%86%85%e6%a0%b8ipv4-tcp%e9%87%8a%e6%94%be%e5%90%8e%e9%87%8d%e7%94%a8%e6%bc%8f%e6%b4%9e%ef%bc%88cve-2026-98432%ef%bc%89%e9%80%9a%e5%91%8a/) |
| `guidepointsecurity.com` | 1 | ai_security | [AI代理无需利用漏洞即可产生风险，安全防护需超出终端范围扩展至权限管理](https://www.guidepointsecurity.com/blog/ai-agent-security-beyond-the-endpoint/) |
| `ir.americanexpress.com` | 1 | finance | [美国运通发布2026年第三季度财务业绩报告](https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2026/American-Express-Reports-Third-Quarter-2026-Financial-Results/default.aspx) |
| `machinelearning.apple.com` | 1 | ai | [苹果开源框架MLX支持Mac Studio通过RDMA实现本地与分布式大模型推理](https://machinelearning.apple.com/research/mlx-distributed-inference) |
| `paddo.dev` | 1 | ai_security | [AI推动漏洞挖掘成本降低：CVE数量由1月的4302个飙升至10月的17052个](https://paddo.dev/blog/the-haystack-tripled/) |
| `shubs.io` | 1 | security | [研究人员发现某知名汽车品牌遥控解锁机制漏洞，可导致全球多款车型被远程任意解锁](https://shubs.io/unlocking-any-car-from-x-brand-in-most-of-the-world/) |
| `threatninja.net` | 1 | security | [针对 PHP 8.4 会话上传进度处理与内存损坏漏洞（CVE-2026-109618 等）的技术分析](https://threatninja.net/dark-embargo-technical-analysis-of-a-php-8-4-vulnerability/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
