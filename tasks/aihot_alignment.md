# AIHOT Methodology Alignment

## What AIHOT Teaches Us
AIHOT 的关键不是“有一个好 prompt”，而是把信息处理拆成稳定流水线：精选信源、低成本预筛、多维评分、代码重算最终分、事件聚类、再生成日报视图。

对应到本项目，Phase 3 必须避免继续把所有判断交给 Gemini/DeepSeek 单次输出。LLM 只提供结构化判断材料；最终精选、配额、信源优先级、Google News 降权、XSignals 权重、中文源可见性都必须由代码控制。

## Strict Comparison Against Current Roadmap

| AIHOT 原则 | 当前 roadmap 覆盖情况 | 需要补强 |
|---|---|---|
| 信源比信息重要 | 已有 `source_registry.yaml` 计划 | 需要明确 T1/T1.5/T2 先人工精选，不靠自动发现大批量加源 |
| 宁缺毋滥、一手优先 | 已有 source tier / kind | 需要写入 selection 公式：官网 > 官方 X > 专家 X > 媒体 > 聚合 |
| 便宜模型先预筛 | backend 已预留 DeepSeek | 需要 Phase 3.2 增加 relevance prefilter，过滤泛科技/泛政策/低质转述 |
| LLM 不直接决定最终分 | 已有多维评分 + final_score | 必须禁止“LLM 返回最终 selected=true”这类设计 |
| 代码重算质量分 | 已有 deterministic `final_score` | 需要把权重放配置，方便回测和快速调参 |
| 事件聚类 | 已有 story clustering | 需要先做 deterministic，再做 LLM fallback，避免 embedding 成本和误合并失控 |
| 日报只是视图 | roadmap 已提 distribution layer | 当前 digest 生成仍偏“一次性成品”，后续应把 enriched items 作为中间产物保存 |
| UI 打标和分数可见 | reports 有计划 | 站点可以展示 source tier / final_score / related_count，但不要暴露内部 API 参数 |
| 用历史样本回测 | roadmap 未明确 | 增加 offline eval：用最近 7-14 天产物比较旧/新策略 |
| Skill/API/RSS 接入 | distribution layer 延后 | 保持延后，先把精选质量做稳 |

## AIHOT Skill Usage Decision
不把完整 `aihot/SKILL.md` 塞进生产 system prompt。

原因：
- Skill 是给 Agent 的路由/调用说明，不是我们的新闻评分 rubric。
- 全量塞进 prompt 会浪费 token，并把端点、限流、cursor 等基础设施细节污染摘要任务。
- 生产 pipeline 需要可测试、可回放、可降级的代码路径，而不是依赖模型“记住怎么调 API”。

正确用法：
1. **作为外部评测基准**：定期拉 AIHOT selected items，对比我们的 AI / AI Security 是否漏掉明显大事件。
2. **作为可选外部信源**：如果启用，只进 AI 前沿，不进 security/finance；标记 `source_kind=external_selected`，不自动高于官方源。
3. **作为 Agent 手动查询能力**：在 AGENTS 中记录最小调用规则，用户要求“对比 AIHOT / 看 AIHOT 今天选了什么”时，Codex 用公开 API 拉取。
4. **不作为主数据源**：不能让 AIHOT 覆盖我们自己的 source registry，否则项目会退化成二次聚合。

## Minimal AIHOT API Contract For Agents
- Base URL: `https://aihot.virxact.com`
- 调 `/api/public/*` 必须带浏览器 User-Agent。
- 默认宽问题走 selected items，不走 daily。
- 只有用户明确说“日报”才走 daily。
- 只有用户明确说“全部/完整/所有/全量”才走 `mode=all`。
- 输出给用户时只展示人话时间、标题、摘要、来源和原文 URL；不要暴露 endpoint、cursor、cache、rate limit。

## Phase 3 Additions From This Review
1. 在 `source_registry` 前先做 `source_audit.md`：列出每个板块 T1/T1.5/T2 候选，人工确认后再进 YAML。
2. 在多维评分前加 `prefilter`：DeepSeek/Gemini backend 都实现同一 schema，过滤无关条目，但保留 filtered report。
3. `final_score` 权重必须配置化，禁止散落在 prompt 或代码常量里不可见。
4. 新增 `eval_strategy.py`：用最近 7-14 天 archive/output/digest 回放，比较旧策略和新策略的入选差异。
5. AIHOT API 先做 eval/compare，不进入每日生产 selected，除非后续显式打开 `AIHOT_AS_SOURCE=true`。
