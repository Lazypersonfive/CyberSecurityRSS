# Source Registry Audit

- generated_for: 2026-05-24
- dates: 2026-05-24, 2026-05-23, 2026-05-22, 2026-05-21, 2026-05-20, 2026-05-19, 2026-05-18

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 95 | 10 | 19 | 63 | 3 | 16 | 10 | 35 | 0 |
| ai_security | 48 | 8 | 0 | 40 | 0 | 16 | 8 | 5 | 15 |
| finance | 69 | 3 | 0 | 66 | 0 | 16 | 3 | 0 | 0 |
| security | 105 | 17 | 0 | 85 | 3 | 0 | 17 | 5 | 41 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blogs.nvidia.com` | 2 | ai | [英伟达首款专为 AI 智能体设计的 Vera CPU 正式交付 OpenAI 与 Anthropic 等实验室](https://blogs.nvidia.com/blog/vera-cpu-delivery/) |
| `blog.google` | 1 | ai | [谷歌 I/O 2026 开发者大会 Dialogues 论坛回顾：首席执行官桑达尔·皮查伊探讨 AI 未来](https://blog.google/innovation-and-ai/technology/ai/io-2026-dialogues-recap/) |
| `brutecat.com` | 1 | security | [StubZero 漏洞研究：通过信息泄露实现 Google Cloud 生产环境远程代码执行](https://brutecat.com/articles/google-cloud-rce) |
| `guage.cool` | 1 | security | [Linux 环境下 ELF Shellcode 生成技术与无文件攻击实战指南](https://guage.cool/linux-shellcode.html) |
| `krebsonsecurity.com` | 1 | security | [CISA 承包商在 GitHub 意外泄露 AWS GovCloud 高权限密钥及内部系统凭据](https://krebsonsecurity.com/2026/05/cisa-admin-leaked-aws-govcloud-keys-on-github/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
