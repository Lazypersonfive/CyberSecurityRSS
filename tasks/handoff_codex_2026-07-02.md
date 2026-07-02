# Codex 交接文档：P0 坏链修复收尾 + 下一阶段队列（2026-07-02）

> 背景：20 天回顾（见 `tasks/url_hygiene_2026-07-02.md`）确认 `hackernews.cc/feed` 的 RSS
> 生成器配置错误，所有 `<link>` 写成 `http://0.0.0.0:8080/post/<id>`，坏链已进入已发布的
> digest 和站点。Claude 已完成代码层修复（未提交），剩余回填、提交和后续队列交由 Codex 执行。

## 环境约定

- Python：`/Users/dedsec/anaconda3/envs/work3124/bin/python`（下文简写 `$PY`）
- 测试：`PYTHONPATH=. $PY tests/test_regressions.py`（unittest，当前 127 个全绿）
- Lint：`$PY -m ruff check .`
- 仓库根目录有用户自己的未跟踪文件 `news_claude_code_china_fingerprint_20260701.md`——**不要动、不要提交**。

## 一、已完成（工作区未提交，验证已过）

| 改动 | 文件 | 说明 |
|---|---|---|
| 新模块：URL 卫生 | `url_hygiene.py`（新） | `is_public_http_url()` 拒绝非公网 host（0.0.0.0/127.x/localhost/私网段/link-local/::1/非 http(s)）；`repair_entry_url(link, feed_url)` 把非公网 item 链接改写到 feed 的公网 host（`http://0.0.0.0:8080/post/N` + `hackernews.cc/feed` → `https://hackernews.cc/post/N`，已实测返回 200 真文章）。通用规则，不是 per-feed 硬编码 |
| fetch 层接入修复 | `fetch_feeds.py` | `_fetch_one` 解析 item 时先过 `repair_entry_url` |
| filter 层最终门 | `filter_entries.py` | `filter_and_dedup` 开头拒绝非公网 URL，计入 `dropped_nonpublic_url`，永不进入 output/digest/站点 |
| 源登记（unknown 清理第一批） | `source_registry.yaml` | `hackernews.cc`（t2/cn_expert/中文安全媒体）、`securityweek.com`（t2/media）、`cyberkendra.com`（t2/media）。`defend.network` 质量存疑，本轮不登记不拉黑，继续观察 |
| 报表口径修复 | `eval_strategy.py` | Board Health 表 `Min CN`（实为配置值，易误读）拆成 `CN Target`（配置）+ `Obs Min CN`（窗口观测最低值）；`BoardEval` 新增 `observed_min_chinese` 字段 |
| 测试 | `tests/test_regressions.py` | +4：`UrlHygieneTests`（guard 边界、repair 改写、query 保留、feed host 非公网不改写）、filter 丢弃统计、eval 新表头断言。123 → 127 全绿 |
| 需求文档 | `tasks/url_hygiene_2026-07-02.md`（新） | R1-R4 需求与验收标准 |

## 二、Codex 待执行（按顺序）

### T1（P0 收尾）：回填已发布的坏链接 —— ✅ 已由 Claude 完成（2026-07-02，未提交）

**执行记录**（Codex 无需重做，只需在 T3 提交时包含这些变更）：
- 41 个文件（digest/security_*.json + docs/feed_*.json）已 JSON 感知改写，两轮：
  1. 第一轮：`http://0.0.0.0:8080` → `https://hackernews.cc`；`url:0.0.0.0/post` → `url:hackernews.cc/post`
  2. 第二轮：裸 host 值 `"source_key": "0.0.0.0"` 等精确等值替换 → `"hackernews.cc"`
     （第一轮遗漏的形态，37 个文件补齐）
- 站点已重建（`site_builder.py`，7 dates，latest=2026-07-02）
- 已验收：`grep -rl '0\.0\.0\.0' digest/ docs/ | wc -l` = **0**；
  抽查 `https://hackernews.cc/post/64411` 返回 **200**

**给 Codex 的提醒**：如果后续发现其他 JSON 报表（reports/）也有残留，用同样两轮规则处理。

### T2（工程卫生）：pytest 依赖

- `pyproject.toml` 已有 `[tool.pytest.ini_options]` 段但依赖没声明。
  在 pyproject `[project.optional-dependencies]` 加 `dev = ["pytest", "ruff"]`（或建 `requirements-dev.txt`，二选一）。
- 验收：`$PY -m pytest -q` 在本地能收集并跑过全部测试（unittest 风格 pytest 能直接收集）。

### T3：提交与推送

- **当前工作区状态**（Claude 留下的全部未提交变更，一次提交）：
  - 修改：`eval_strategy.py`、`fetch_feeds.py`、`filter_entries.py`、`source_registry.yaml`、`tests/test_regressions.py`
  - 新增：`url_hygiene.py`、`tasks/url_hygiene_2026-07-02.md`、`tasks/handoff_codex_2026-07-02.md`
  - T1 回填产生的 `digest/*.json`、`docs/*` 变更
  - **不要提交**：`news_claude_code_china_fingerprint_20260701.md`（用户个人文件）
- 提交前先跑：`PYTHONPATH=. $PY tests/test_regressions.py`（应 127 全绿）+ `$PY -m ruff check .`
- 建议 commit message：

```
fix(security): repair non-routable feed links + registry/eval hygiene

- url_hygiene.py: is_public_http_url() guard + repair_entry_url() rewrite;
  hackernews.cc feed emits http://0.0.0.0:8080/post/<id> links (28 published
  in the last window, still entering daily) — rewrite onto the feed's public
  host (verified 200), generic so the next misconfigured feed is covered too.
- fetch_feeds: repair at parse time; filter_entries: final gate drops
  non-public URLs (dropped_nonpublic_url stat).
- Backfill: rewrite published 0.0.0.0 links across digest/ + docs/, rebuild site.
- source_registry: register hackernews.cc (cn_expert), securityweek, cyberkendra.
- eval_strategy: 'Min CN' column split into 'CN Target' + 'Obs Min CN'.
- deps: declare pytest for local runs.

Tests: 123 -> 127, ruff clean.
```

- push 后确认 lint workflow 绿。

### T4：明日 cron 验证（07-03 06:45 CST 跑完后）

- `digest/security_2026-07-03.json` 中 hackernews.cc 条目 URL 应为 `https://hackernews.cc/post/...`，不再有 `0.0.0.0`
- `reports/source_audit.md` / `offline_eval.md`：security unknown 计数应因三个域名登记明显下降（此前 7 天 33 条）
- `offline_eval.md` 表头应显示 `CN Target | Obs Min CN`
- security 中文数不应下降（hackernews.cc 是中文供给，修复是恢复而非移除）

## 三、下一阶段队列（T4 验证通过后再动，按优先级）

以下来自 2026-07-02 的 20 天回顾评估（GPT 报告 + Claude 核实），背景细节看
`tasks/url_hygiene_2026-07-02.md` 和当天对话结论。

### P1a：ai_security 源池扩充（对用户职业价值最高的板块）
- 现状：32 天窗口仅 20 天满 10 条，最低跌到 4；尾部有泛 AI 内容凑数（Ornith 发布、Visa Glasswing 等错板块条目）。
- 方向：补 AI 安全专业源（Protect AI / HiddenLayer / Lakera / PIabs 博客类 + 中文大模型安全公众号，接入前逐个 `httpx.get` 验证 RSS 可达）；**保持宁缺毋滥**——不要为满额降低边界。
- 配套：offline_eval 把「质量达标的缺口」标记为正常而非失败（区分 quality-gated shortfall 与 supply failure）。
- 验收：满额天数上升，且尾部条目全部能说明安全机制。

### P1b：ai 板块中文稳定性诊断（先诊断，勿盲目加源）
- 现状：`min_chinese: 5` 20 天仅 10 天达成。
- 第一步是归因：写个小脚本对未达成日拆解——中文候选在 pool 里有没有（供给缺，典型是周末公众号停更）vs 在 pool 里但被挤掉（配额缺陷）。两种结论对应不同修法（补稳定日更源 vs 调 pool 预留）。
- 验收：产出归因结论 + 对应修复后 7 天 ≥6 天达成。

### P2a：同账号 X 连发聚类
- 案例：xAI 三条 `@xai` 连发推（Grok Build Plugin Marketplace：Sentry/Vercel/MongoDB 各一条）占了 ai 板块 3 个位置；`Claude Tag` 也有类似重复。
- 方向：`story_clustering.py` 加确定性规则——同一 X 作者、发布时间窗口内（如 6h）、正文共享同一发布事件实体（或 summary 尾部带相同的转推上下文）→ 合并为一个 story。用历史样例写回归测试（2026-06-12 的 xAI 三连推数据在 `digest/ai_2026-06-12.json`）。
- 注意：宁可漏合并不可误合并（同账号一天发两个不同产品是常态）。

### P2b：finance official 扩源
- 现状：official 平均 0.3 条/天，主体是 Finextra/PYMNTS 转述。
- 方向：监管与机构一手源（Fed、BIS、PBOC/央行公众号、FCA），Visa/MC IR 已在。接入前验证 RSS。

### 明确不做（红线，写给 Codex）
- 不自动调权、不自动改 prompt（feedback loop 保持只读）
- 不把 AIHOT 接成生产信源
- LLM 只出预筛和多维评分；最终分、阈值、配额、主条选择必须由代码决定
- 任何源的增删先过 `httpx` 验证 + 测试，不裸改 OPML

## 四、快速验证命令汇总

```bash
PY=/Users/dedsec/anaconda3/envs/work3124/bin/python
PYTHONPATH=. $PY tests/test_regressions.py   # 127+ tests, OK
$PY -m ruff check .                           # clean
grep -rl '0\.0\.0\.0' digest/ docs/ | wc -l   # 回填后应为 0
$PY site_builder.py                           # 重建站点
```
