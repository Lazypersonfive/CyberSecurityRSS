# Source Registry Audit

- generated_for: 2026-06-10
- dates: 2026-06-10, 2026-06-09, 2026-06-08, 2026-06-07, 2026-06-06, 2026-06-05, 2026-06-04

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 101 | 13 | 18 | 70 | 0 | 10 | 13 | 33 | 0 |
| ai_security | 69 | 13 | 0 | 56 | 0 | 7 | 13 | 5 | 14 |
| finance | 70 | 3 | 0 | 67 | 0 | 17 | 3 | 0 | 0 |
| security | 105 | 18 | 0 | 79 | 8 | 0 | 18 | 3 | 26 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `praetorian.com` | 2 | security | [安全研究人员推出 WasmForge 工具，将 Sliver 远控木马编译为 WebAssembly 规避检测](https://www.praetorian.com/blog/wasmforge-sliver-webassembly/) |
| `zgao.top` | 2 | security | [针对 Kubernetes 凭证泄露后的 RBAC 持久化后门排查技术指南](https://zgao.top/k8s-kubeconfig%e6%b3%84%e9%9c%b2%e5%90%8e%e7%9a%84rbac%e6%8c%81%e4%b9%85%e5%8c%96%e5%90%8e%e9%97%a8%e6%8e%92%e6%9f%a5/) |
| `404media.co` | 1 | security | [微软紧急关闭 70 多个遭黑客入侵的 GitHub 仓库以阻止针对 AI 用户的恶意软件](https://www.404media.co/microsoft-hacked-to-deliver-malware-to-claude-and-gemini-users/) |
| `blog.nviso.eu` | 1 | security | [安全研究揭示攻击者如何利用合法 QEMU 虚拟机工具进行隐蔽内网渗透](https://blog.nviso.eu/2026/06/04/the-detection-response-chronicles-covert-operations-through-qemu/) |
| `pwndefend.com` | 1 | security | [研究人员发现 Mirai 僵尸网络正利用 CVE-2026-34910 漏洞构建](https://www.pwndefend.com/2026/06/09/cve-2026-34910-exploitation-itw-building-a-botnet-mirai/) |
| `yanglong.pro` | 1 | security | [PHPDoc 规范语法大全与常用标签结构整理指南](https://www.yanglong.pro/phpdoc-%e8%af%ad%e6%b3%95%e5%a4%a7%e5%85%a8/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
