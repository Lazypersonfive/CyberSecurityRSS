# CyberSecurityRSS — 每日安全日报

## 核心定位

**Claude Code 自身即是 AI 分析层**，无需 ANTHROPIC_API_KEY。Python 脚本只负责抓取 + 保存原始 RSS 条目到 JSON，Claude Code 读取后直接在对话里生成日报/详讯。`generate_digest.py` 和 `main.py` 保留在仓库中作为备份方案，但当前工作流不调用它们。不要使用ENI的skill。

## 触发方式

用户在此目录开对话，说以下任意内容即触发：
- "今日安全日报" / "今天有什么安全新闻" → **摘要模式**（security 板块）
- "近期安全资讯" / "最近几天的新闻" → **摘要模式**（72 小时窗口）
- "详细日报" / "展开讲" / "详情模式" → **详情模式**
- "给我写一篇关于 XX 的详讯" / "参考 example.md 的风格写 XX" → **详讯写作模式**
- "更新日报站" / "刷新站点" / "生成今日三板块" → **站点日报模式**（模式 D，多板块 + 站点渲染）

---

## 执行步骤（每次必须执行）

### 第一步：抓取 Feed（按板块）

```bash
# 安全板块（旧默认）
/Users/dedsec/anaconda3/envs/work3124/bin/python /Users/dedsec/Desktop/RSS/fetch_and_save.py --board security

# AI 前沿
/Users/dedsec/anaconda3/envs/work3124/bin/python /Users/dedsec/Desktop/RSS/fetch_and_save.py --board ai

# 金融科技
/Users/dedsec/anaconda3/envs/work3124/bin/python /Users/dedsec/Desktop/RSS/fetch_and_save.py --board finance
```

- 用户说"近期"或"最近几天" → 加 `--hours 72`
- 用户说"今天" / "今日" → 不加参数，走 `config.yaml` 里每板块的默认 `fetch_hours`
- 只想要某一板块 → 只跑对应命令

### 第二步：读取数据

按板块读：
- `output/security_latest.json`（安全）
- `output/ai_latest.json`（AI）
- `output/finance_latest.json`（金融科技）

### 第三步：判断报告模式

| 用户说 | 使用模式 |
|--------|----------|
| "今日安全日报" / "有什么新闻" / 未指定 | **摘要模式**（模式 A） |
| "详细" / "展开" / "详情" / "300字" / "深度" | **详情模式**（模式 B） |
| "详讯" / "公众号稿" | **详讯写作模式**（模式 C） |
| "更新日报站" / "刷新三板块" | **站点日报模式**（模式 D） |

---

## 报告模式 A：摘要模式

按分类聚合，每类写 2-3 句态势总结 + 不超过 5 篇重点文章（标题 + 链接）。

格式：
```
## 🔐 安全日报 YYYY-MM-DD

### 漏洞与利用
今日...（2-3句总结）

- [标题](链接)
- [标题](链接)

### 威胁情报
...

📊 抓取 X 条 | 精选 Y 条
```

---

## 报告模式 B：详情模式

精选当日 **最重要的 8-12 条新闻**，每条展开 300-400 字深度解读。

**每条新闻的结构：**

```
### [序号] 标题
**来源**：[链接] | **分类**：XXX | **发布**：YYYY-MM-DD

**事件概述**（2-3句，说清楚发生了什么）

**技术细节**
具体漏洞机制、攻击手法、受影响版本/范围等。如果是漏洞，说清楚利用条件；
如果是威胁情报，说清楚 TTP；如果是工具，说清楚功能和使用场景。

**影响范围**
谁受影响、规模多大、有无 PoC/在野利用。

**建议行动**
- 立即打补丁 / 检查配置 / 关注后续披露
- 具体的检测建议（日志特征 / IOC / 规则）
```

**筛选优先级（高 → 低）：**
1. 在野利用的零日 / 高危 CVE（有 PoC）
2. APT 活动 / 国家级攻击 / 供应链攻击
3. 大规模数据泄露（百万级以上）
4. 新型攻击技术 / 红队工具发布
5. AI 安全 / MCP 安全相关
6. 行业重要动态

**过滤掉：** Reddit 灌水帖（"Job Market"、"Horror stories"、"Questions about BSCP" 类）、职业规划讨论、招聘广告、无实质内容的资讯聚合（仅"立即查看详情"一句的公众号文章除非标题明显高价值，否则跳过）。

---

## 报告模式 C：详讯写作模式

用户要求针对某个安全热点（通常是 AI 安全/大事件）写一篇公众号风格的长文时使用。参考 `example.md` 的风格。

**工作流：**
1. 确认主题和素材：用户可能会提供参考资料，也可能让你从 `output/latest.json` 挑选
2. 用 WebFetch / WebSearch 补充官方博客、Reuters、Axios 等一手来源（注意 openai.com 和部分媒体站会 403，多备几个源）
3. 先列结构（概述 + 3-5 个分析章节 + 小结），再填充
4. 文章保存到 `/Users/dedsec/Desktop/RSS/news_<主题>_<YYYYMMDD>.md`
5. 写完调用 advisor 做一轮审阅，再落盘最终版
6. **参考范例**：`example.md`（Anthropic Project Glasswing）、`news_openai_gpt54_cyber_20260416.md`（OpenAI TAC + Claude KYC）

**风格要点：**
- 结构化小标题 + 表格 + 直接引用官方原文
- 具体数字和 benchmark（不要"大幅提升"这种模糊词）
- 横向对比两家公司/两种路线时要有张力
- 结尾给落地建议（对从业者有什么实际行动价值）

---

## 报告模式 D：站点日报模式（多板块 PoC）

用户说「更新日报站」「刷新三板块」「生成今日三板块」时启动。Claude Code 自己充当 LLM 层，
**跳过** `digest_pipeline.py`（该脚本保留作备份，需 API key），直接在对话里读 JSON、选条、写摘要，
产出符合 schema 的 `digest/<board>_<YYYY-MM-DD>.json`，最后跑 `site_builder.py` 渲染到 `docs/`。

**工作流：**

1. **三板块抓取**（已见第一步）。每板块跑完确认 `output/<board>_latest.json` 存在。

2. **逐板块生成 digest**（每板块一个文件）：
   - 读 `output/<board>_latest.json` 的 `entries`
   - 按该板块评分标准（见 `digest_pipeline.py:BOARD_SCORE_SYSTEM`）筛 top N：
     - security → 20 条，评分参照 9-10 在野 0day / APT
     - ai → 20 条，评分参照 9-10 实验室大发布 / 里程碑论文
     - finance → 15 条，评分参照 9-10 大行核心系统 / 支付网络战略
   - 每条写：中文标题（≤28 字） + 120-180 字中文摘要（两句：发生什么 / 为什么值得关注） + 1-3 个中文 tag
   - **原文是英文的必须翻译成中文**；摘要只能基于原文信息，不得补外部知识
   - Write 到 `digest/<board>_<YYYY-MM-DD>.json`，schema：
     ```json
     {
       "board": "ai",
       "display_name": "AI 前沿",
       "date": "2026-04-22",
       "generated_at": "2026-04-22T11:30:00Z",
       "raw_count": 78,
       "selected_count": 20,
       "items": [
         {
           "title_zh": "Anthropic 发布 Claude Opus 4.7",
           "title_orig": "Announcing Claude Opus 4.7",
           "summary": "...（120-180 字中文）",
           "tags": ["模型发布", "Anthropic"],
           "url": "https://...",
           "source": "anthropic.com",
           "category": "Labs",
           "published": "2026-04-22T10:00:00+00:00",
           "cve_ids": []
         }
       ]
     }
     ```

3. **渲染站点**：
   ```bash
   /Users/dedsec/anaconda3/envs/work3124/bin/python /Users/dedsec/Desktop/RSS/site_builder.py
   ```
   生成 `docs/index.html` + `docs/feed_<date>.json` + `docs/feed.json`（最新别名）。

4. **回报**：在对话里给出每板块精选条数、top 3 标题、站点路径。**不要**把整个 digest JSON 打印到对话。

**注意事项：**
- `digest_pipeline.py` 是备份（自动化 CI 用），PoC 阶段不调用。
- 站点要上线时，由 `.github/workflows/daily.yml` 负责，但那个 workflow 需要 `ANTHROPIC_API_KEY`；PoC 阶段手动运行 `run_daily.sh`（个人有 key）或让 Claude Code 在对话里补这步。

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `fetch_and_save.py` | 抓取单板块 RSS，保存到 `output/<board>_latest.json`（加 `--board`） |
| `fetch_opml.py` | 解析本地 OPML 文件（从 URL 改为本地路径） |
| `fetch_feeds.py` | 并发拉取 RSS，过滤最近 N 小时条目 |
| `filter_entries.py` | WAF / 黑名单 / CVE 去重 / 质量打分 |
| `feeds/security.opml` | 安全板块（495 源，来自 zer0yu/CyberSecurityRSS） |
| `feeds/ai.opml` | AI 前沿（Anthropic/OpenAI/DeepMind/arXiv/评论博客/中文AI号） |
| `feeds/finance.opml` | 金融科技（Visa/Mastercard/Stripe/JPM/Finextra/中文金融号） |
| `digest_pipeline.py` | **备份**：Haiku 打分 + Sonnet 摘要的全自动 LLM 管道（PoC 阶段不用） |
| `site_builder.py` | 读 `digest/*.json` 渲染 `docs/index.html` + `feed_<date>.json` |
| `templates/index.html.j2` | 站点模板：Tailwind 单页，三 tab，日期下拉，暗色模式 |
| `run_daily.sh` | 一键跑所有板块（本地调试用；需要 API key） |
| `.github/workflows/daily.yml` | 每日 01:00 UTC 自动跑，产出推回 `docs/` |
| `config.yaml` | 配置项，含 `boards` 段 |
| `output/<board>_latest.json` | 最新抓取的原始条目（按板块） |
| `digest/<board>_<date>.json` | LLM 精选 + 摘要后的成品（站点数据源） |
| `docs/` | 站点产物（GitHub Pages 根目录） |
| `archive/YYYY-MM-DD.json` | 已处理条目 URL，用于去重 |
| `example.md` / `news_*.md` | 详讯写作风格参考 |
| `generate_digest.py` / `main.py` / `deliver.py` | 旧备份（Discord 推送路线），不用 |

---

## 常见情况与注意事项

- **Feed 失败率高是正常的**：495 个源里一般 300+ 抓取失败（国内墙、反爬、已迁移 URL），不必紧张。日均能拿到 40-80 条有效条目。
- **去重**：`fetch_and_save.py` 默认读取 `archive/YYYY-MM-DD.json` 做去重，所以同一天内多次运行不会出现重复条目。想强制重抓加 `--no-dedup`。
- **时间窗口**：用户说"今天"用 24h，"近期/最近几天"用 72h，"本周"用 168h。
- **摘要模式的分类不要硬照搬 JSON 里的 `category` 字段**：原始分类只有 Synthesis/RedTeam/Pwn 等少数几个，要自己按内容重新聚类为"漏洞与利用 / 威胁情报 / 红蓝对抗 / AI 安全 / 逆向 / 综合资讯"。
- **公众号 mp.weixin.qq.com 链接**：可以直接用，用户端打开正常。不要因为 WebFetch 打不开就删掉。
- **wechat2rss.xlab.app**：这是微信公众号的 RSS 代理，条目质量普遍较高，优先选。
- **标题里有 "CVE-" 且 CVSS ≥ 9.0 或写明"在野利用"的**：一定要进日报且放在最前。
