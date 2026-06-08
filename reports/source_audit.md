# Source Registry Audit

- generated_for: 2026-06-09
- dates: 2026-06-09, 2026-06-08, 2026-06-07, 2026-06-06, 2026-06-05, 2026-06-04, 2026-06-03

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 102 | 12 | 20 | 70 | 0 | 9 | 12 | 36 | 0 |
| ai_security | 69 | 12 | 0 | 57 | 0 | 7 | 12 | 3 | 13 |
| finance | 70 | 3 | 0 | 67 | 0 | 18 | 3 | 0 | 0 |
| security | 105 | 15 | 0 | 84 | 6 | 0 | 15 | 3 | 29 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `praetorian.com` | 2 | security | [安全研究人员推出 WasmForge 工具，将 Sliver 远控木马编译为 WebAssembly 规避检测](https://www.praetorian.com/blog/wasmforge-sliver-webassembly/) |
| `404media.co` | 1 | security | [微软紧急关闭 70 多个遭黑客入侵的 GitHub 仓库以阻止针对 AI 用户的恶意软件](https://www.404media.co/microsoft-hacked-to-deliver-malware-to-claude-and-gemini-users/) |
| `blog.nviso.eu` | 1 | security | [安全研究揭示攻击者如何利用合法 QEMU 虚拟机工具进行隐蔽内网渗透](https://blog.nviso.eu/2026/06/04/the-detection-response-chronicles-covert-operations-through-qemu/) |
| `yanglong.pro` | 1 | security | [PHPDoc 规范语法大全与常用标签结构整理指南](https://www.yanglong.pro/phpdoc-%e8%af%ad%e6%b3%95%e5%a4%a7%e5%85%a8/) |
| `zgao.top` | 1 | security | [黑客窃取KubeConfig远程调用ApiServer创建特权容器获取Node节点权限应急排查](https://zgao.top/k8s-kubeconfig%e6%b3%84%e9%9c%b2-%e9%bb%91%e5%ae%a2%e8%bf%9c%e7%a8%8b%e8%b0%83%e7%94%a8apiserver%e5%88%9b%e5%bb%ba%e7%89%b9%e6%9d%83%e5%ae%b9%e5%99%a8%e8%8e%b7%e5%8f%96node%e8%8a%82%e7%82%b9%e6%9d%83/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
