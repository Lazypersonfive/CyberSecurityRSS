# Current State Review - 2026-06-11

## Purpose

本文档汇总当前日报系统已经发现的问题、已经完成的改动，以及下一阶段希望优化的方向。它不是替代 `tasks/roadmap.md` 的长期路线图，而是截至 2026-06-11 的项目状态基线，便于后续周回顾和任务拆分。

## Current Product Goal

当前项目目标不是做“RSS 汇总页”，而是做一个面向个人决策的信息精选系统：

1. 先保证每天能稳定产出四个板块的精选日报。
2. 再保证信源结构健康：官方、一手、专家、中文源和 X 信号各自发挥作用。
3. LLM 负责理解和结构化判断，最终分数、配额、来源权重和事件主条选择由代码控制。
4. 站点展示要简洁、可搜索、可跨日期回看，后续再扩展 RSS/API/Skill。

当前生产 backend 是 Gemini，DeepSeek 作为可替换 backend 预留；Anthropic 通道已下线。

## Board Targets

| Board | Daily target | Source target | Editorial focus |
|---|---:|---|---|
| `security` | 15 | 至少 6 条中文，候选不足时需在报表中体现 | 高危漏洞、在野利用、官方通告、供应链攻击、攻防技术、国内安全动态 |
| `ai_security` | 10 | 至少 2 条中文，宁缺毋滥 | Prompt injection、agent 安全、模型投毒、AI coding 风险、AI 供应链与防护机制 |
| `ai` | 15 | 约三分之一中文；arXiv 最多 2 条 | 海外前沿、一手官方、顶级开发者 X、重要产品/模型/生态变化 |
| `finance` | 10 | 至少 1 条中文；优先 direct | 金融科技、支付网络、银行科技、监管与机构一手信息 |

## Latest Observed Metrics

最新 7 日窗口：2026-06-05 至 2026-06-11。

| Board | Selected avg/min | Chinese avg/min | Main observation |
|---|---:|---:|---|
| `security` | 15 / 15 | 4.43 / 1 | 条数稳定，但中文目标仍不稳定，且存在 selected unknown sources |
| `ai_security` | 9.86 / 9 | 2.00 / 1 | 基本满额，但仍有泛 AI 或非安全内容混入风险 |
| `ai` | 14.43 / 12 | 3.00 / 1 | X 信号有效，论文 cap 生效，但中文占比不稳定 |
| `finance` | 10 / 10 | 1.57 / 1 | 当前最稳定，Google News 仍是补覆盖来源之一 |

来源结构观察：

- `security`: Google News 为 0，说明安全板块已经基本摆脱 Google News 聚合；但 `Unknown` selected 仍有 11 条。
- `ai_security`: Google News 7 条，X 6 条，中文专家 14 条；数量尚可，关键是分类准确性。
- `ai`: X 33 条，Google News 10 条，arXiv 10 条；XSignals 已成为 AI 前沿的重要信号源。
- `finance`: Google News 17 条，官方源只有 4 条；金融板块长期仍需要更多 direct/official 来源。

## Problems Found

### P0 - Source Supply And Source Quality

1. **安全中文源比例仍不稳定**
   - 目标是 `security` 每日 15 条中至少 6 条中文。
   - 最新 7 日均值只有 4.43，最低 1。
   - 主要原因不是选择策略完全失效，而是大量中文安全 RSS 7 天 0 raw，尤其是公众号代理源和部分厂商/社区源。

2. **AI 前沿中文比例不稳定**
   - AI 前沿本质上以海外和 X 为主，这是合理的。
   - 但中文目标仍希望约三分之一；当前最新 7 日均值 3.00，最低 1。
   - 需要区分“中文补覆盖”和“为了配额牺牲高价值海外一手消息”。后者不应发生。

3. **部分入选源仍未登记到 source registry**
   - `security` 当前 selected unknown 包括 `praetorian.com`、`zgao.top`、`pwndefend.com`、`404media.co`、`blog.nviso.eu`、`yanglong.pro`。
   - 其中部分应登记为专家/媒体源，部分应降权或排除。
   - AIHOT 方法论要求信源分层由代码和人工维护，不能交给 LLM 临时判断。

4. **大量中文安全源已长时间 0 raw**
   - 周报已经能列出 7 天 0 条目源。
   - 但当前还没有形成“重要源失效后替换 RSS”的闭环。
   - 长亭、绿盟、腾讯玄武、看雪、安全客等源如果长期 0 raw，会直接影响中文技术内容覆盖。

### P1 - Editorial Fit

5. **AI 安全仍可能混入泛 AI 内容**
   - 典型问题：普通 agent 工具、WebAssembly 工具、泛供应链或地缘供应链新闻进入 AI 安全。
   - AI 安全应该聚焦明确的安全机制：攻击、利用、防护、风险、漏洞、投毒、越权、泄露、供应链攻击等。
   - 没有明确安全机制的 AI 新闻，应留在 `ai`，不要进入 `ai_security`。

6. **安全板块尾部偶尔出现低相关技术资料**
   - 例如 PHPDoc 语法整理这类内容有技术价值，但不适合安全日报 top15。
   - 原因通常是 fill 阶段在高质量候选不足时，为了凑满数量而拉入边界内容。
   - 安全板块宁可把低相关条目放低，也不应把“开发资料”当安全热点。

7. **漏洞摘要的原理描述仍不够稳定**
   - 目前摘要能说明事件和影响，但并非每条漏洞都稳定覆盖：漏洞类型、触发条件、影响版本、利用条件、修复状态。
   - 对安全板块来说，“漏洞原理和利用条件”比泛泛影响更重要。

8. **金融板块 official/direct 仍偏少**
   - Finance 虽然最稳定，但高度依赖 Finextra、PYMNTS、PaymentsDive 和 Google News。
   - Visa/Mastercard/Stripe/JPM/监管机构等 direct 来源需要继续增强。

### P2 - Product And Evaluation

9. **反馈机制已有雏形，但还没进入稳定周流程**
   - 已有 `feedback_cli.py` / `feedback_eval.py` 的方向。
   - 但每天人工反馈“好/坏/漏选”的数据还没有稳定积累，也没有进入 source audit 的固定回路。

10. **AIHOT 对比还只是参考，不是常规评估项**
    - AIHOT 的价值在于方法论：精选信源、多维评分、代码重算 final_score、事件聚类、日报只是视图。
    - 当前我们已经吸收部分架构，但还没有把 AIHOT selected feed 变成固定外部 benchmark。

11. **站点仍是展示层，缺少更多质量信号**
    - 当前站点支持跨日期搜索、日期回看、按 final_score 展示。
    - 但还没有面向用户展示 source tier、related count、source mix、为什么入选等质量信号。

12. **成本暂时不是首要瓶颈，但需要保留约束意识**
    - 当前已切到 `gemini-3.5-flash`，价格约为旧 `gemini-3-flash-preview` 的 3 倍。
    - 以历史日均消耗估算仍在每月 10 USD 目标内，但后续加 prefetch、eval、AIHOT compare 时要避免无意义重复调用。

## Changes Already Made

### Architecture And Backend

- 下线 Anthropic 通道，不再维护 Anthropic backup。
- 保留 Gemini 作为生产 backend，默认 `LLM_BACKEND=gemini`。
- 预留 DeepSeek backend，后续可通过 `LLM_BACKEND=deepseek` 和 `DEEPSEEK_API_KEY` 切换。
- 引入 `llm_backends/` adapter 思路，避免 pipeline 直接绑定单一 SDK。
- 默认 Gemini 模型已改为 `gemini-3.5-flash`。

### Scoring And Selection

- 建立 `source_registry.yaml`，引入 `tier` 与 `kind`。
- 引入多维评分和 deterministic `final_score`。
- `final_score` 由维度分、source bonus、kind bonus、freshness bonus、中文可见性 bonus 等代码规则重算。
- 站点排序优先看 `final_score`，避免完全依赖 LLM 单分。
- 引入 story clustering / dedupe，digest item 已包含 `story_id`、`related_urls`、`related_count`、`source_tier`、`source_kind`、`score_breakdown` 等字段。

### Board Configuration

- 板块调整为四个：`security`、`ai_security`、`ai`、`finance`。
- `security`: 15 条，目标至少 6 条中文；Google News cap 压到 1，实际最近安全板块 Google News 为 0。
- `ai_security`: 10 条，宁缺毋滥；Google News 与聚合源有 cap。
- `ai`: 15 条，XSignals 可占较高比例；arXiv cap 为 2。
- `finance`: 10 条，官方/机构/direct 优先；Google News 作为补覆盖来源。

### Source And Feed Work

- 接入 RSSHub/XSignals，AI 前沿和 AI 安全可使用 X 作为重要信号源。
- AI 前沿已加入多位开发者、官方账号和高价值 X 源。
- AI 安全已加入 Seebug Paper、Seebug 漏洞社区、娜璋 AI 安全之家等中文/安全源。
- 移除或降权部分低质、错板块或长期噪声源。
- 周报已能列出 7 天 0 raw 源和持续低质源。

### Digest Quality

- 修复标题硬截断问题，保留完整标题并通过 `_limit_title()` 控制极端长度。
- 修复摘要尾部重复标题和过长卡片问题。
- Prompt 已从“短标题”调整为“完整中文标题，不得半句截断”。
- 漏洞和安全摘要 prompt 已向技术细节靠拢，但仍需继续加强。

### Frontend And Site

- 前端改为更接近 OpenAI docs / Codex guides 的克制风格。
- 降低大标题视觉重量，优化移动端展示。
- 搜索从“今天”扩展为跨日期窗口搜索。
- tag 可点击筛选。
- 站点按更值得关注的条目优先展示，而不是原始顺序。

### Reports And Evaluation

- 增加 source report sidecar JSON。
- `reports/weekly.md` 聚合 7 日源质量。
- `reports/source_audit.md` 展示 selected unknown source。
- `reports/offline_eval.md` 用于离线评估策略变化。
- 增加 AIHOT 对齐文档，明确 AIHOT 是外部 benchmark，不是主数据源。
- 增加人工反馈机制设计，原则是先收集和评估，不自动调权。

## Desired Optimization Direction

### Direction 1 - Fix Source Foundation First

优先级最高的是源，而不是继续堆 prompt。

Actions:

1. 对 7 天 0 raw 的中文安全源做分组：删除死源、保留重要但失效源、寻找替代 RSS。
2. 补充稳定中文安全源，优先漏洞分析、厂商 CERT、攻防技术、CTF/竞赛、国内官方通告。
3. 持续补全 `source_registry.yaml`，让 selected unknown 接近 0。
4. 对低质但高产源加 source cap 或移出对应板块。

Success criteria:

- `security` 中文平均接近或超过 6，且不是靠低质中文内容凑数。
- selected unknown source 每周清零或接近清零。
- 每周 7 天 0 raw 的重要源都有处理结论。

### Direction 2 - Tighten AI Security Editorial Boundary

AI 安全不能变成“AI + 安全两个词都沾边”。

Actions:

1. 收紧 `ai_security` rubric：无明确 AI 安全机制的泛 AI 内容最高 4 分。
2. 对 agent 工具、普通产品更新、泛 AI 行业新闻加 deterministic downrank。
3. 将“Prompt injection / data exfiltration / model poisoning / agent sandbox / AI supply chain / AI coding malware”作为强信号。
4. 宁缺毋滥：如果只有 8-9 条合格内容，可以接受，不要用泛 AI 补满。

Success criteria:

- AI 安全每周误入泛 AI 条目显著下降。
- 选入内容都能回答“安全风险或防护机制是什么”。

### Direction 3 - Make Vulnerability Summaries More Technical

安全日报的核心读者关心“原理、影响、处置”，不是泛泛新闻摘要。

Actions:

1. CVE/漏洞类摘要强制覆盖：漏洞类型、触发条件、影响版本/组件、是否有 PoC/在野利用、修复状态。
2. 对官方通告和技术分析文章分别使用不同摘要模板。
3. 如果原文没有技术细节，摘要应明确“原文未披露细节”，不要编造。

Success criteria:

- 安全 top 5 漏洞摘要至少 80% 包含漏洞类型和触发条件。
- 不再出现只写“影响重大、建议关注”的空泛摘要。

### Direction 4 - Build A Lightweight Human Feedback Loop

不要让模型自动学习；先让人工反馈进入评估闭环。

Actions:

1. 每天允许标记：好、坏、漏选、标题问题、摘要问题、错板块。
2. 反馈先进入 JSONL，不直接改 prompt 或权重。
3. 每周回顾时由脚本生成建议：该升权的源、该降权的源、该新增规则。
4. 人工确认后才修改 `source_registry.yaml`、source cap、config scoring 或 prompt。

Success criteria:

- 每周至少有一份 feedback eval 报告。
- 策略变化都有反馈或离线评估证据支持。

### Direction 5 - Use AIHOT As Benchmark, Not Main Source

AIHOT 的启发是流程，不是把它当主 RSS。

Actions:

1. 每周拉 AIHOT selected RSS/API，与我们的 AI 前沿做漏选对比。
2. 只记录明显漏掉的大事件，不直接把 AIHOT item 混入生产主源。
3. 如果未来作为生产源，必须标记为 external/aggregated 并设置严格 cap。

Success criteria:

- 每周知道我们相比 AIHOT 漏掉了哪些 AI 大事件。
- 我们的 source registry 和 XSignals 能逐步覆盖这些事件的一手来源。

### Direction 6 - Improve Distribution After Quality Stabilizes

RSS/API/Skill 有价值，但不应早于精选质量稳定。

Actions:

1. 先稳定 digest schema 和 enriched item 中间产物。
2. 再开放 RSS/API/Skill。
3. API/Skill 输出只暴露用户需要的信息，不暴露内部评分细节和基础设施参数。

Success criteria:

- 站点、RSS、API、Skill 共用同一份稳定精选数据。
- 日报视图只是 enriched items 的一个展示结果。

## Near-Term Priorities

| Priority | Task | Why now |
|---|---|---|
| P0 | 清理/替换长期 0 raw 中文安全源 | 直接决定 security 中文目标能否达成 |
| P0 | 收紧 AI 安全 rubric 和 deterministic downrank | 当前 AI 安全最容易混入泛 AI 内容 |
| P1 | 补全 selected unknown source registry | final_score 的信源分层依赖 registry 完整性 |
| P1 | 强化漏洞摘要模板 | 提升安全板块的实际阅读价值 |
| P1 | 建立每周 feedback eval 固定流程 | 把主观好坏转成可追踪策略输入 |
| P2 | AIHOT weekly compare | 作为外部漏选评估基准 |
| P2 | Finance direct/official source expansion | 降低对 Google News 和媒体转述依赖 |

## Files To Watch

| File | Purpose |
|---|---|
| `config.yaml` | 板块目标、source policy、scoring 权重 |
| `source_registry.yaml` | 信源 tier/kind 权重中心 |
| `digest_pipeline_gemini.py` | 当前生产 digest pipeline |
| `llm_backends/` | Gemini / DeepSeek backend adapter |
| `feeds/*.opml` | 各板块 RSS 源池 |
| `reports/weekly.md` | 7 日源质量汇总 |
| `reports/source_audit.md` | selected unknown source 审计 |
| `reports/offline_eval.md` | 策略离线评估 |
| `tasks/roadmap.md` | 长期 Phase 3 路线图 |
| `tasks/aihot_alignment.md` | AIHOT 方法论对齐 |
| `tasks/feedback_loop_plan.md` | 人工反馈机制设计 |

## Non-Goals For Now

- 不把 AIHOT 当主数据源。
- 不把完整 AIHOT skill 塞进生产 prompt。
- 不自动根据用户反馈修改权重或 prompt。
- 不恢复 Anthropic backend。
- 不为了满额牺牲板块相关性。
- 不优先做 RSS/API/Skill，除非精选质量稳定。

