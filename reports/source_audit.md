# Source Registry Audit

- generated_for: 2026-05-23
- dates: 2026-05-23, 2026-05-22, 2026-05-21, 2026-05-20, 2026-05-19, 2026-05-18, 2026-05-17

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 96 | 12 | 18 | 63 | 3 | 14 | 12 | 33 | 1 |
| ai_security | 52 | 9 | 0 | 43 | 0 | 18 | 9 | 9 | 13 |
| finance | 69 | 3 | 0 | 66 | 0 | 16 | 3 | 0 | 0 |
| security | 105 | 16 | 0 | 87 | 2 | 0 | 16 | 5 | 39 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blogs.nvidia.com` | 2 | ai | [英伟达首款专为 AI 智能体设计的 Vera CPU 正式交付 OpenAI 与 Anthropic 等实验室](https://blogs.nvidia.com/blog/vera-cpu-delivery/) |
| `blog.google` | 1 | ai | [谷歌 I/O 2026 开发者大会 Dialogues 论坛回顾：首席执行官桑达尔·皮查伊探讨 AI 未来](https://blog.google/innovation-and-ai/technology/ai/io-2026-dialogues-recap/) |
| `brutecat.com` | 1 | security | [StubZero 漏洞研究：通过信息泄露实现 Google Cloud 生产环境远程代码执行](https://brutecat.com/articles/google-cloud-rce) |
| `krebsonsecurity.com` | 1 | security | [CISA 承包商在 GitHub 意外泄露 AWS GovCloud 高权限密钥及内部系统凭据](https://krebsonsecurity.com/2026/05/cisa-admin-leaked-aws-govcloud-keys-on-github/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
