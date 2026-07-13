# AIHOT-Inspired Phase 3 Roadmap

## Goal
把日报从“LLM 单分筛选”升级为“信源分层 + LLM 多维评分 + 代码重算 final_score + 事件聚类 + 日报视图”。当前生产继续使用 Gemini；Anthropic 通道下线；DeepSeek 作为可替换 backend 预留。

## Current Backend Policy
- 默认：`LLM_BACKEND=gemini`，需要 `GEMINI_API_KEY` 或 `GOOGLE_API_KEY`。
- 预备：`LLM_BACKEND=deepseek`，需要 `DEEPSEEK_API_KEY`，默认模型 `deepseek-v4-flash`。
- 不再维护第二套旧 LLM pipeline；`digest_pipeline.py` 仅为兼容入口，实际转到当前 pluggable pipeline。
- DeepSeek 后续目标是替代 Gemini，而不是只做预筛工具。

## Phase 3 Sequence
1. **Backend cleanup**
   - 下线 Anthropic 通道和旧 secret。
   - 抽象 `llm_backends/`，让 pipeline 只依赖 backend interface。
   - 预留 DeepSeek backend，mock 测试先跑通 schema。

2. **Source registry**
   - 新增 `source_registry.yaml` 作为信源权重中心。
   - `tier`: `t1` 官网/官方博客，`t1_5` 官方 X，`t2` 专家/KOL/媒体，`unknown` 默认。
   - `kind`: `official`、`official_x`、`expert_x`、`cn_official`、`cn_expert`、`media`、`aggregator`、`community`、`google_news`。
   - Google News、RSSHub XSignals、中文安全源由代码识别并覆盖默认值。

3. **Multidimensional scoring**
   - 保留旧 `score`，新增 `score_dimensions`。
   - `security`: `relevance`、`technical_depth`、`exploitability`、`impact_scope`、`actionability`。
   - `ai_security`: `security_relevance`、`technical_depth`、`practical_risk`、`agent_model_relevance`、`actionability`。
   - `ai`: `relevance`、`novelty`、`entity_importance`、`developer_relevance`、`ecosystem_impact`。
   - `finance`: `relevance`、`institution_importance`、`technology_depth`、`market_or_regulatory_impact`、`actionability`。

4. **Deterministic final_score**
   - `dimension_score` 由板块维度加权平均。
   - `source_bonus`: `t1 +1.0`、`t1_5 +0.5`、`t2 +0.0`、`unknown -0.3`。
   - `kind_bonus`: `official +0.5`、`official_x +0.3`、`expert_x +0.2`、`cn_official +0.5`、`cn_expert +0.3`、`google_news -1.0`、`community -0.5`。
   - `freshness_bonus`: 12 小时内 `+0.3`，24 小时内 `+0.1`。
   - `cn_visibility_bonus` 只给登记过的高质量中文源。
   - `final_score` clamp 到 `0-10`，精选优先看 `final_score`，旧 `score` 只作兼容和报表对照。

5. **Story clustering**
   - 先用 CVE、规范化 URL、官方 release slug、标题实体重叠做确定性聚类。
   - 保留现有 LLM dedupe 作为兜底。
   - 每个事件只选一个 `primary_item`。
   - 主条优先级：`official > official_x > expert_x > cn_official/cn_expert > media > google_news/community`。
   - digest item 新增 `story_id`、`final_score`、`score_dimensions`、`source_tier`、`source_kind`、`related_urls`。

6. **Distribution layer**
   - RSS/API/Skill 延后到质量架构稳定后。
   - 先保证静态站、搜索、日期窗口和 reports 的质量信号完整。

7. **Human feedback loop**
   - 先收集人工反馈，不直接让模型自我学习或自动改 prompt。
   - 反馈对象包括：入选条目、未入选但用户认为应入选条目、低质误入选条目、标题/摘要质量问题。
   - 反馈先落到仓库内结构化文件，进入 offline eval 和 source audit；人工确认后再调 `source_registry.yaml`、`config.scoring`、source caps 或 prompt。
   - 详细设计见 `tasks/feedback_loop_plan.md`。

## Board Targets
- `security`: 每日 15 条，候选足够时至少 6 条中文；漏洞摘要优先写原理、触发条件、影响范围和修复状态。
- `ai_security`: 每日 10 条，宁缺毋滥，聚焦 AI 安全技术。
- `ai`: 每日 15 条，约三分之一中文；arXiv 最多 2 条；XSignals 可占重要比例，但由 `final_score + source kind` 控制。
- `finance`: 每日 10 条，优先官网、监管和机构源，Google News 只补覆盖；当前中文 fallback 已接入，长期需要中文直采源。

## Current Production Status (2026-07-13)
- Backend: Gemini 主生产；DeepSeek 预留；Anthropic 已下线。
- Source registry/final score/story clustering: v1 已上线。
- Site search: 支持跨日期搜索。
- Site ordering: 站点卡片按 `final_score` 优先展示，`source_tier/source_kind` 作为兜底排序。
- GitHub Actions RSSHub: workflow 可启动临时 RSSHub 容器使用 `TWITTER_AUTH_TOKEN`，XSignals 以 Actions 结果为准。
- 过去 7 天 daily workflow 全成功，产出 `archive/`、`digest/`、`docs/feed_*.json` 和 `reports/`。
- 2026-07-07 至 2026-07-13 的 daily workflow 全部成功，四板块产出均值分别为 `15/15`、`9.7/10`、`13.9/15`、`10/10`。
- `security` 中文均值 `8.4`，连续 `7/7` 天达到至少 6 条；但一周内重复 URL 槽位占 `30.5%`，已新增按板块回看已发布 URL/CVE/story_id 的跨日过滤。
- `ai_security` 一周内重复 URL 槽位占 `45.6%`，且有厂商排名、诉讼和泛安全内容填充；已设 `min_final_score=6.0`并加入确定性低价值上限。
- `ai` 中文均值 `4.1`，有 `4/7` 天达到 5 条；已为 LLM dedupe 增加保守事件校验和大幅折叠拒绝逻辑。
- `finance` 条数稳定，但 Finextra + PYMNTS 占一周入选的约 `66%`；已限制两源每日各 3 条，增加 Fed/ECB/BIS/Stripe 直采源，并预留至少 2 条官方条目。
- 漏洞摘要将技术要素要求从 2 项提高到 3 项，拒绝把 stored XSS 夸大为主机任意代码执行；修复 pass 输出结构化拒绝原因。
- 后续 digest 持久化 `score_dimensions` 和 `delivered_filter_stats`，便于周报直接审计模型评分与跨日拦截效果。
- Feedback loop P1 从 CLI 扩展到站点卡片：可标记“有用/不想看/摘要有问题”、导出 JSONL，导入后由 daily workflow 写入周报；仍不自动调权。


## AIHOT Methodology Constraints
- 不把完整 AIHOT skill 塞进生产 system prompt；skill 是 Agent 调用说明，不是日报评分规则。
- AIHOT 公开 API 先作为外部评测基准和手动对比工具，不作为主数据源。
- 如果后续启用 AIHOT 作为信源，只允许进入 AI 前沿板块，标记为 `external_selected`，且不自动高于官网/官方 X。
- Phase 3 的实现顺序增加两个门槛：先做人审 source audit，再做 offline eval；不允许直接靠 prompt 调参上线。
- LLM 只能输出预筛结果和多维评分；最终分、阈值、配额、主条选择必须由代码决定。

## AIHOT Skill/API Policy
- Base URL: `https://aihot.virxact.com`。
- 调 `/api/public/*` 必须带浏览器 User-Agent。
- 宽问题默认拉 `items?mode=selected&since=<time-window>`；明确“日报”才拉 daily；明确“全部/完整/所有/全量”才拉 `mode=all`。
- 对用户输出只展示标题、摘要、来源、发布时间和原文 URL；不要暴露 endpoint、cursor、cache、rate limit 等基础设施细节。
- 详细对照见 `tasks/aihot_alignment.md`。

## Acceptance Tests
- 官方域名、官方 X、专家 X、中文安全源、Google News、RSSHub XSignals 能正确识别 tier/kind。
- 多维评分缺字段时 fallback 到旧 `score=5`，不导致 daily 失败。
- 同一事件的官网内容应高于 Google News 转述；顶级开发者 X 可高于普通媒体，但不自动高于官网。
- 同一 OpenAI/DeepSeek 发布的官网、官方 X、KOL、Google News 只输出一个主条。
- CVE 相同的多源报道聚为同一事件；不确定时倾向不合并。
- `tests/test_regressions.py`、`ruff check .`、`py_compile` 全通过。
- dry-run 四板块仍生成 digest，站点 feed JSON 向后兼容。
- reports 新增 `avg_final_score`、`source_tier/kind` 分布、事件聚类合并数量。
- 人工反馈机制上线前必须只影响 reports/offline eval；任何自动调权都需要可回滚 diff 和 7-14 天回测。
