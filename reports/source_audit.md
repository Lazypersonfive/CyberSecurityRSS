# Source Registry Audit

- generated_for: 2026-07-17
- dates: 2026-07-17, 2026-07-16, 2026-07-15, 2026-07-14, 2026-07-13, 2026-07-12, 2026-07-11

## Board Coverage

| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ai | 102 | 12 | 19 | 68 | 3 | 9 | 12 | 39 | 15 |
| ai_security | 45 | 4 | 0 | 41 | 0 | 8 | 4 | 6 | 14 |
| finance | 70 | 17 | 0 | 53 | 0 | 15 | 17 | 0 | 0 |
| security | 105 | 13 | 0 | 91 | 1 | 0 | 13 | 1 | 52 |

## Unknown Selected Sources

| Source | Count | Boards | Latest Example |
|---|---:|---|---|
| `machinelearning.apple.com` | 3 | ai | [苹果研究人员提出简单自蒸馏算法，无需外部教师模型即可显著提升代码生成能力](https://machinelearning.apple.com/research/simple-self-distillation) |
| `vipread.com` | 1 | security | [WgpSec发布Alkaid智能体框架，探索AI在全自主攻防场景中的工程化落地](https://vipread.com/library/topic/4153) |

## Review Rule

- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。
- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。
- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。
