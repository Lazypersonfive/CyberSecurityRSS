# Source Registry Audit

- generated_for: 2026-06-06
- dates: 2026-06-06, 2026-06-05, 2026-06-04, 2026-06-03, 2026-06-02, 2026-06-01, 2026-05-31

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 105 | 14 | 21 | 70 | 0 | 9 | 14 | 40 | 0 |
| ai_security | 67 | 11 | 0 | 56 | 0 | 7 | 11 | 5 | 7 |
| finance | 70 | 2 | 0 | 68 | 0 | 14 | 2 | 0 | 0 |
| security | 105 | 14 | 0 | 89 | 2 | 0 | 14 | 5 | 28 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blog.nviso.eu` | 1 | security | [安全研究揭示攻击者如何利用合法 QEMU 虚拟机工具进行隐蔽内网渗透](https://blog.nviso.eu/2026/06/04/the-detection-response-chronicles-covert-operations-through-qemu/) |
| `praetorian.com` | 1 | security | [WasmForge 工具发布：将 Sliver 远控工具编译为 WebAssembly 以规避检测](https://www.praetorian.com/blog/wasmforge-sliver-webassembly/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
