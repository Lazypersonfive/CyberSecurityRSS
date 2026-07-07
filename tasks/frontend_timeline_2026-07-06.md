# 前端时间线升级：借鉴 AIHOT 布局（2026-07-06）

> 触发：用户认可 https://aihot.virxact.com/ 的 UI 设计，要求参考优化我们的站。
> 分析方式：抓取其 SSR HTML 解析 DOM 结构（JS chunk 拉取受阻，未取到其 CSS 数值，
> 视觉用我们自己的黑白语言重写，不做像素级克隆）。

## AIHOT 设计语言拆解（来自 40 条 SSR 时间线条目）

```
<div class="timeline-item timeline-item-selected">
  <div class="timeline-time">17:06</div>            ← 左侧时间锚点
  <div class="timeline-rail"><span class="timeline-dot"/></div>  ← 竖轨+圆点
  <article class="timeline-card">
    head: [来源名]  ……  [精选badge] [分数 mono score-mid] [收藏星]
    <a class="timeline-title">标题</a>
    <p class="timeline-summary">摘要</p>
    <div class="timeline-tags"><a class="tag">标签(可点筛选)</a>…</div>
    <hr class="timeline-divider"/>
    <div class="timeline-reason"><span class="timeline-reason-label">推荐理由：</span>…</div>
  </article>
</div>
```

其他：icon 侧栏（side-link + tooltip）、score-high/score-mid 分档、
localStorage 收藏（timeline-star, data-track）、移动端独立紧凑行（m-row-*）。

## 采用 / 不采用

| AIHOT 元素 | 决策 | 理由 |
|---|---|---|
| 时间锚点 + 竖轨圆点 | ✅ 采用 | 这是用户看中的签名视觉；给日报"简报扫描节奏" |
| 分数分档 | ✅ 采用（黑白化） | ≥9 实心黑 chip；≥7.5 描边加粗；其余弱化。不用彩色 |
| 理由带标签+分隔线 | ✅ 对齐 | 现有 reason 块改为 分隔线 + 「入选理由：」行内标签 |
| 收藏星（localStorage） | ✅ 采用 | 零后端、真实用性；侧栏加「只看收藏」开关 |
| 标签点击筛选 | 已有 | 不动 |
| icon 侧栏 | ❌ 不采用 | 我们的板块 tab 语义更强，仅微调样式 |
| 彩色主题 | ❌ 不采用 | 保持黑白极简（2026-06-12 已确认的方向） |
| 移动端独立 DOM | ❌ 不采用 | media query 折叠 rail 即可，避免双份渲染逻辑 |

## 排序决策（关键权衡）

AIHOT 是纯时间序；我们是 final_score 序 + hero。冲突解法：
**hero（当日最高分）置顶保留，其余条目按 published 倒序进时间线**，
每条左侧显示 HH:MM 锚点。跨日搜索模式维持现状（按日期分组平铺，不套时间线）。
分数信息不丢：每卡 head 仍显示分数 chip（新增分档样式）。

## 保留不动（红线）

- `el()`/`textContent` 渲染，feed 内容零 `innerHTML`；所有链接过 `safeUrl()`
- 搜索（跨日期）、日期下拉、明暗主题、source tier/kind 徽章、related_urls 折叠、hero 卡
- 零构建：单 Jinja2 模板 + CDN Tailwind + vanilla JS

## 测试（先写，RED）

1. `test_template_renders_timeline_layout`：含 `ic-tl-time`、`ic-tl-rail`、`ic-tl-dot`、`renderTimelineItem`
2. `test_template_tiers_scores`：含 `scoreTier`、`data-tier`（high/mid 判档逻辑）
3. `test_template_supports_local_star`：含 `starButton`、`localStorage`、`starredOnly`（只看收藏开关）
4. `test_template_reason_uses_labeled_divider`：含 `ic-reason-label`、`入选理由：`
5. 既有断言全部保留通过（安全模型/搜索/hero/related/identity）

## 验收

- 127+ 测试全绿，ruff clean
- `site_builder.py` 重建后 preview 双主题截图：时间线轨/锚点/收藏星/分档分数可见
- 移动端宽度（375px）rail 折叠不破版
- 收藏交互：点星 → localStorage 持久 → 「只看收藏」过滤生效
