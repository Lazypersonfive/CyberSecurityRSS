# Phase 2: 治理强化 + 站点 UX

## Summary

围绕「现有体验有摩擦」做最小集合的修复和优化，分四档：

1. **核心 bug 修复**：archive 写入缺失 + 跨日去重
2. **运维可见性**：死源标记 + CI lint
3. **用户体验**：站点搜索 + tag 筛选
4. **小清理**：AGENTS.md / 重复配置

不做：邮件推送、监控告警、source_caps vs max_per_source 重构（v3 再谈）。

## 任务清单与依赖

```
P1 (高优先 / 1 小时)
├─ 1a. 补齐 archive 写入  ← 阻塞 1b 真正生效
├─ 1b. load_seen_urls 多日回看
├─ 3.  CI lint workflow（独立 lint.yml）
└─ 5.  小清理：.gitignore AGENTS.md + 删 min_chinese 顶层

P2 (1-2 小时)
└─ 2.  weekly.md 末尾追加「建议人工 review」段落

P3 (站点 UX / 2-3 小时)
└─ 4.  站点搜索 + tag 点击筛选

可选 (按用户实际可达性决定)
└─ 6.  生成 docs/digest.rss（GH Pages 在国内可达即做）
```

---

## 1. 跨日 URL 去重（含修复 archive 写入）

### 现状诊断

- `fetch_feeds.py:load_seen_urls(date_str)` 读取 `archive/<date>.json` 的 URL 集合用于 fetch 去重
- **`fetch_and_save.py` 不写 archive**——只有废弃的 `deliver.py:_archive_urls()` 写
- 结果：`archive/` 目录在新 pipeline 下永远为空，URL 去重事实上依赖纯靠 LLM dedupe

### 改动

**`fetch_and_save.py`**：filter 完成后写 archive
```python
# After filter_and_dedup, before writing output JSON:
_archive_urls([fe.url for fe in filtered], today_str)
```

**`fetch_feeds.py`**：`load_seen_urls` 接受 lookback
```python
def load_seen_urls(date_str: str, lookback_days: int = 7) -> set[str]:
    """Merge URLs from last N days of archive/<date>.json files."""
    target = date.fromisoformat(date_str)
    seen: set[str] = set()
    for offset in range(lookback_days):
        path = ARCHIVE_DIR / f"{(target - timedelta(days=offset)).isoformat()}.json"
        if path.exists():
            seen.update(json.loads(path.read_text(encoding="utf-8")).get("urls", []))
    return seen
```

**`fetch_and_save.py` caller**：
```python
seen_urls = set() if args.no_dedup else load_seen_urls(today_str, lookback_days=7)
```

### 测试

- `test_load_seen_urls_merges_recent_days`：构造 archive/2026-04-27.json + archive/2026-04-29.json，调用 `load_seen_urls("2026-04-29", lookback_days=3)`，断言两份 URLs 都在
- `test_archive_writer_persists_urls`：跑 fetch_and_save 一次，断言 archive/<today>.json 存在且包含 URLs

### 验收

- 本地：`archive/2026-04-29.json` 在下次 fetch 后出现，含当日所有 filtered URLs
- 远端：明早 cron 跑完后 git diff 应能看到 archive/ 新增文件
- 第二天 cron：`load_seen_urls` 命中昨日 URL，今天 raw_count 应明显下降（覆盖 30h 窗口的重复部分）

### 默认 lookback_days = 7

- security/ai 用 24-30h 窗口，7 天回看绰绰有余
- finance 用 336h（14 天）窗口，**lookback 也开 14 天**？或者保留 7 天接受少量重复
- 建议 finance 也设 7：14 天 IR 公告往往是不同事件，URL 即使巧合相同概率极低

---

## 2. 死源自动标记

### 现状

- `reports/weekly.md` 已存在并按 board 列出每个 feed 的 7 日累计
- 没有「应该 review 的源」结论摘要

### 改动

`source_reports.py:refresh_weekly_report` 末尾追加段落：

```markdown
## ⚠️ 建议人工 review（不自动删）

### 7 天 0 条目源（疑似失效）
- 机器之心（wechat2rss）：连续 7 天 raw_count=0
- ...

### 持续低质源（avg_score < 3 且 raw ≥ 5）
- 黑海洋：7 天 raw=68，avg=2.4
- ...
```

### 阈值

- 0-entry：连续 7 天 raw=0
- 低质：累计 raw ≥ 5 且 avg_score < 3

阈值写代码常量，不进 config（避免 over-engineering）。

### 测试

- `test_weekly_lists_zero_entry_feeds`
- `test_weekly_lists_low_quality_feeds`

---

## 3. CI lint

### 改动

新增 `.github/workflows/lint.yml`：

```yaml
name: lint
on:
  push:
    branches: [main]
  pull_request:

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12", cache: "pip" }
      - run: pip install ruff
      - run: ruff check .
```

不加 `ruff format --check`（可能现有代码 style 不严格统一，避免一次性大量重写）。

### 不加在 daily.yml

理由：lint 失败不应阻塞每日内容生成。

### 验收

- push 后 lint workflow 触发并通过
- 故意写一个 unused import 测试能拦下

---

## 4. 站点搜索 + tag 点击筛选

### 改动

`templates/index.html.j2`：

1. **顶部搜索框**：`<input id="search" placeholder="搜索..."/>`，监听 `input` 事件
2. **过滤逻辑**：在 `renderBody()` 里加 `filterItems(items)` 函数，按 title_zh / summary / tag 子串匹配
3. **Tag 点击**：现有 tag span 加 `onclick`，点击后填充搜索框 + 触发渲染
4. **清除按钮**：搜索框右侧 ✕

约 60-80 行 vanilla JS，无外部依赖。

### 不做

- 模糊搜索 / 拼音搜索：YAGNI
- 跨日期搜索：只搜当前日期、当前 board

### 验收

- 截图对比：搜索 "Anthropic"，仅显示含该词的卡片
- 点击 #OpenAI tag，仅显示 OpenAI 相关
- 清除后恢复全部

---

## 5. 小清理

### 5a. .gitignore AGENTS.md

```
# Tooling-only, not for sync
AGENTS.md
```

### 5b. 删除 `min_chinese` 顶层配置

当前 `digest_pipeline_gemini.py:run()`：
```python
min_chinese = int(bcfg.get("min_chinese", 0))
source_policy.setdefault("min_chinese", min_chinese)
```

**改动**：
- `config.yaml`：每个 board 的顶层 `min_chinese` 删除
- `digest_pipeline_gemini.py / digest_pipeline.py`：删除 `setdefault` 那行，直接信任 `source_policy.min_chinese`
- `_apply_language_quota` shim 保留（外部测试用），但内部直接转发

### 5c. 一并清理 setdefault 注释

加注释「`min_chinese` 唯一来源是 source_policy 段；顶层不再支持」。

---

## 6. 可选：digest.rss 输出

### 现状评估

- GH Pages 在国内可达性看具体网络环境：北方电信常通，部分校园网/移动卡
- 生成成本极低（site_builder.py 加 30 行）

### 决策

**先生成不发布**：
- `site_builder.py` 渲染 `docs/digest.rss`（最近 7 天聚合）
- 站点首页加一行 "📡 [RSS](digest.rss)"
- 用户在国内能访问就用，不能访问也不影响主体

如果你确定永远用不上（不订阅 / 国内访问困难），可以从计划中删除。

---

## 验证步骤（合并提交后）

1. **本地**：`PYTHONPATH=. python -m unittest discover -s tests -q` → all pass
2. **CI**：push 触发 lint workflow 绿灯 + daily workflow 在下次 cron 跑通
3. **数据**：明早 cron 后检查
   - `archive/2026-04-30.json` 存在
   - `reports/weekly.md` 末尾有「建议 review」段
   - 站点能搜索、tag 可点击
   - URL 跨日去重生效（看日志 fetch_and_save 的 raw_entry_count 应下降）

---

## 不做（明确范围）

- 邮件推送 / 企业微信 bot（v3）
- 监控 / 告警（个人项目无需）
- source_caps / max_per_source 合并（功能 OK，重构不值）
- 跨板块搜索 / 全文检索（YAGNI）
- 移动端响应式重设（已验证可用）

---

## 估时

| 任务 | 估时 |
|------|------|
| 1. archive 写入 + 跨日去重 + 测试 | 45 min |
| 2. weekly review 段 + 测试 | 60 min |
| 3. CI lint workflow | 15 min |
| 4. 站点搜索 + tag 筛选 | 90 min |
| 5. 小清理 | 15 min |
| 6. digest.rss（如做） | 30 min |
| **合计** | **3.5-4 小时** |

建议分两次提交：
- **C1**：1 + 3 + 5（基础 + 清理）
- **C2**：2 + 4（功能新增）
- C3 可选：6
