# Source Registry Audit

- generated_for: 2026-07-15
- dates: 2026-07-15, 2026-07-14, 2026-07-13, 2026-07-12, 2026-07-11, 2026-07-10, 2026-07-09

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 97 | 12 | 20 | 64 | 1 | 6 | 12 | 39 | 16 |
| ai_security | 53 | 1 | 0 | 52 | 0 | 6 | 1 | 5 | 23 |
| finance | 70 | 15 | 0 | 55 | 0 | 12 | 15 | 0 | 0 |
| security | 105 | 10 | 0 | 94 | 1 | 0 | 10 | 1 | 53 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `machinelearning.apple.com` | 1 | ai | [苹果发布主动型智能体研究环境 PARE：通过模拟活跃用户评估 AI 助手](https://machinelearning.apple.com/research/proactive-agent-research-environment) |
| `vipread.com` | 1 | security | [WgpSec发布Alkaid智能体框架，探索AI在全自主攻防场景中的工程化落地](https://vipread.com/library/topic/4153) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
