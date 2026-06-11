# Source Registry Audit

- generated_for: 2026-06-11
- dates: 2026-06-11, 2026-06-10, 2026-06-09, 2026-06-08, 2026-06-07, 2026-06-06, 2026-06-05

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 101 | 12 | 15 | 73 | 1 | 10 | 12 | 33 | 0 |
| ai_security | 69 | 14 | 0 | 55 | 0 | 7 | 14 | 6 | 14 |
| finance | 70 | 4 | 0 | 66 | 0 | 17 | 4 | 0 | 0 |
| security | 105 | 16 | 0 | 78 | 11 | 0 | 16 | 3 | 27 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `praetorian.com` | 3 | security | [Centurion：构建自定义虚拟化加载器以对抗逆向工程](https://www.praetorian.com/blog/virtualized-loader-centurion/) |
| `zgao.top` | 3 | security | [排查 Kubernetes 中 kubeconfig 泄露后的 RBAC 持久化后门技术](https://zgao.top/k8s-kubeconfig%e6%b3%84%e9%9c%b2%e5%90%8e%e7%9a%84rbac%e6%8c%81%e4%b9%85%e5%8c%96%e5%90%8e%e9%97%a8%e6%8e%92%e6%9f%a5/) |
| `pwndefend.com` | 2 | security | [漏洞 CVE-2026-34910 遭在野利用被用于构建 Mirai 僵尸网络](https://www.pwndefend.com/2026/06/09/cve-2026-34910-exploitation-itw-building-a-botnet-mirai/) |
| `404media.co` | 1 | security | [微软紧急关闭 70 多个遭黑客入侵的 GitHub 仓库以阻止针对 AI 用户的恶意软件](https://www.404media.co/microsoft-hacked-to-deliver-malware-to-claude-and-gemini-users/) |
| `blog.nviso.eu` | 1 | security | [安全研究揭示攻击者如何利用合法 QEMU 虚拟机工具进行隐蔽内网渗透](https://blog.nviso.eu/2026/06/04/the-detection-response-chronicles-covert-operations-through-qemu/) |
| `oneusefulthing.org` | 1 | ai | [AI领域迎来重大跨越，全新模型Claude Fable带来人机协作新体验](https://www.oneusefulthing.org/p/what-it-feels-like-to-work-with-mythos) |
| `yanglong.pro` | 1 | security | [PHPDoc 规范语法大全与常用标签结构整理指南](https://www.yanglong.pro/phpdoc-%e8%af%ad%e6%b3%95%e5%a4%a7%e5%85%a8/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
