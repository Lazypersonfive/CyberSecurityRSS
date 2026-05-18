# Source Registry Audit

- generated_for: 2026-05-19
- dates: 2026-05-19, 2026-05-18, 2026-05-17, 2026-05-16, 2026-05-15, 2026-05-14, 2026-05-13

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 100 | 11 | 14 | 73 | 2 | 15 | 11 | 34 | 1 |
| ai_security | 60 | 16 | 3 | 41 | 0 | 9 | 16 | 22 | 9 |
| finance | 69 | 1 | 0 | 68 | 0 | 19 | 1 | 0 | 0 |
| security | 103 | 15 | 0 | 87 | 1 | 0 | 15 | 6 | 19 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `blogs.nvidia.com` | 2 | ai | [英伟达首款专为 AI 智能体设计的 Vera CPU 正式交付 OpenAI 与 Anthropic 等实验室](https://blogs.nvidia.com/blog/vera-cpu-delivery/) |
| `krebsonsecurity.com` | 1 | security | [CISA 承包商在 GitHub 意外泄露 AWS GovCloud 高权限密钥及内部系统凭据](https://krebsonsecurity.com/2026/05/cisa-admin-leaked-aws-govcloud-keys-on-github/) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
