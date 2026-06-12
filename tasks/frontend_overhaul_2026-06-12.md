# 前端升级需求：黑白极简「情报产品」化（2026-06-12）

> 触发：用户希望前端更好看、友好、高端。确认方向「四个都要 + 保持黑白极简做深」。
> 约束：纯静态、零构建、GitHub Pages 直服务；不引入多 MB 中文 webfont；不破坏现有搜索/日期/主题/source badge 功能。

## 设计目标（四支柱）

### 1. 信息层次（评分驱动）
- 单日浏览模式下，每个板块第一条（final_score 最高）= **hero 大卡**：更大标题、保留摘要、视觉权重最高。
- 每张卡片右上显示 `final_score`（等宽小字，克制）；hero 额外有 `TOP` 序号/强调描边。
- 其余条目用更紧凑卡片，形成"头条大、次条小"的出版物层次，而非等大卡片队列。
- 搜索模式（跨日期）不套用 hero，避免跨日头条混淆。

### 2. 事件聚类展示（差异化）
- `related_count > 0` 的条目显示可展开「▸ 本事件另有 N 篇相关报道」；展开列出 `related_urls`，每条渲染为「相关报道 · <域名>」可点链接（不暴露 Google News 长 URL 原文）。
- `selection_reason` 以克制的「入选理由：…」弱化样式呈现，体现编辑判断、不与摘要争夺注意力。

### 3. 产品身份（去掉借来的壳）
- 删除导航死链 `Docs / Guides / Boards / Archive`。
- 删除 footer 的 `OpenAI-inspired interface` 与 openai.com 外链。
- 左上角 `O` 占位符 → 自有几何 wordmark（雷达/信号母题，呼应"情报"）。
- 加 inline SVG favicon（同一母题，零外部依赖）。
- 导航替换为真实可用项：板块快捷跳转 + 关于/仓库链接。
- CSS 类前缀 `oai-` → `ic-`（intelligence console），消除"OpenAI"暗示。

### 4. 视觉精致度（黑白做深）
- source badge 去"信号灯"化：深黑白模式下以单色为主，用实心/空心点 + 标签区分 tier，仅 T1 保留极轻强调。
- 排版做深：hero 标题加大、中文字距/行高细调、字重层次拉开。
- hero 卡顶部一道极细发丝强调线。
- 卡片 hover 细化；移动端 hero 与评分不塌缩。

## 数据契约（feed_<date>.json item，已存在，无需改管线）
`final_score` `score` `selection_reason` `story_id` `related_urls` `related_count`
`source_tier` `source_kind` `source_label` `dimension_score` `score_breakdown`
`title_zh` `title_orig` `summary` `tags` `cve_ids` `url` `source` `published`

## 安全约束（不可回退）
- 继续用 `el()` + `textContent`，禁止 `innerHTML` 注入 feed 内容。
- 链接继续走 `safeUrl()`，只允许 http/https。

## 测试（先写，断言模板结构）
- `renderHeroCard` / hero 概念存在，且 `final_score` 被渲染。
- `relatedToggle` / 相关报道展开逻辑存在，引用 `related_urls` `related_count`。
- `selection_reason` 被渲染。
- 身份清理：模板不含 `OpenAI-inspired interface`、不含 `Docs / Daily intelligence`、不含 `oai-shell`；含新 wordmark 标识与 favicon。
- 保留既有安全断言：无 `card.innerHTML`、含 `safeUrl`、含 `textContent`。
- 保留搜索/source badge/sourceMix 断言（类名更新为 `ic-`）。

## 验证
- `python -m unittest tests.test_regressions`
- `ruff check .`、`py_compile`（site_builder 不变，模板非 py）
- `site_builder.py` 重建 docs，Preview 截图明/暗双主题确认层次与聚类展开。
