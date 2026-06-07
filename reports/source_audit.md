# Source Registry Audit

- generated_for: 2026-06-08
- dates: 2026-06-08, 2026-06-07, 2026-06-06, 2026-06-05, 2026-06-04, 2026-06-03, 2026-06-02

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 102 | 12 | 20 | 70 | 0 | 10 | 12 | 35 | 0 |
| ai_security | 69 | 11 | 0 | 58 | 0 | 7 | 11 | 3 | 12 |
| finance | 70 | 3 | 0 | 67 | 0 | 16 | 3 | 0 | 0 |
| security | 105 | 15 | 0 | 87 | 3 | 0 | 15 | 3 | 30 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `praetorian.com` | 2 | security | [安全研究人员推出 WasmForge 工具，将 Sliver 远控木马编译为 WebAssembly 规避检测](https://www.praetorian.com/blog/wasmforge-sliver-webassembly/) |
| `blog.nviso.eu` | 1 | security | [安全研究揭示攻击者如何利用合法 QEMU 虚拟机工具进行隐蔽内网渗透](https://blog.nviso.eu/2026/06/04/the-detection-response-chronicles-covert-operations-through-qemu/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
