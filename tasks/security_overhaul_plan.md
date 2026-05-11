# Security 板块 Overhaul 计划

> 写作时间：2026-04-30
> 触发：用户反馈「Ghost Bits Java 没看到 / 朝鲜黑客这种政治稿别再写了 / 漏洞要写原理 / 缺 CTF 和国内官方动向」
> 归档状态：2026-05-11 已被 `tasks/week_2026-05-11.md` 接管；本文保留为 security 板块质量问题的历史设计稿。

## 2026-05-11 收尾状态

本文中的核心问题已经进入 Phase 3 执行线：

- 已落地：中文源配额策略、低质 security 源清理、source registry 分类、deterministic `final_score`、CVE/URL/标题实体聚类、digest item 的 `story_id` / `related_urls` 可观测字段。
- 已落地：security prompt/rubric 调整，降低缺少技术细节的地缘归因新闻权重，漏洞摘要更强调漏洞类型、触发条件、利用难度和影响范围。
- 暂缓：arXiv cs.CR / 会议论文源不作为当前重点，用户后来明确要求先保证中文安全媒体和国内技术源。
- 暂缓：公众号 AI 安全源需要可用 RSS 或 RSSHub 路由后再接入，不能只靠公众号名称硬写进 OPML。
- 后续入口：以 `tasks/week_2026-05-11.md` 为当前执行清单，以 `reports/source_audit.md`、`reports/offline_eval.md` 和 `reports/independent_review.md` 作为验证依据。

---

## 一、问题诊断（结合今日数据）

### 🔴 问题 1：错过最新最火的 CVE 和漏洞研究

**用户说**：Ghost Bits Java（Black Hat Asia 2026 / 4.23 议题）和 700+ 字符通杀 Linux 内核的漏洞都没看到。

**根因**：
- **OPML 缺会议研究类信源**。我们 OPML 里全是新闻媒体（HackerNews/BleepingComputer/Vulners）+ 通用博客。Black Hat / DEF CON / USENIX 议题在 mainstream news 里大概要等 1-2 周才被报道。
- **Twitter/X 通道缺失**。@vxunderground / @malwrhunterteam / @taviso 这种第一手研究员账号是漏洞首发地，但我们没接 Nitter/RSSHub。
- **国内技术公众号供给不稳**。看雪 / 安全客深度文章经常是首发地，但今天活跃源里 安全客 3 条、先知 5 条 — 都没进 top 20（被英文头部源高分挤压）。

### 🟠 问题 2：政治归因新闻仍占比过高

**今日 20 条里 3-4 条是政治稿/合规公告**：
- #2 CISA KEV 加入清单（合规通告）
- #3 朝鲜黑客利用 AI 生成 npm 包（地缘归因）⚠️ 用户点名
- #17 CISA 零信任 OT 指南（政策文件）

**根因**：当前 score rubric 写着 "9-10: ... **重大 APT 活动**、大规模供应链攻击"——这个 prompt 直接鼓励 LLM 给"朝鲜/中国/俄罗斯黑客做了 X"打高分。

### 🟠 问题 3：漏洞类摘要写"影响"不写"原理"

**今日 LiteLLM CVE-2026-42208 的摘要**：
> "BerriAI 的 LiteLLM 软件包被发现存在 SQL 注入漏洞，CVSS 9.3，允许攻击者修改底层数据库。该漏洞在公开 36 小时内即遭主动利用..."

**问题**：完全没说**注入点在哪个 endpoint** / **是 boolean blind 还是 union-based** / **触发条件**。这是营销式重述，不是技术读者需要的信息。

**根因**：通用 SUMMARIZE_SYSTEM 只要求"先讲发生了什么，再讲为什么值得关注"。对漏洞类新闻这个目标太弱。

### 🟡 问题 4：CTF / 国内官方动向 / 厂商动作缺席

**用户期望但今天没看到的**：
- 国内 CTF 竞赛（强网杯/RealWorld/Tianfu Cup/GeekGame/KCTF）
- 国内官方通告（CNVD/CNNVD 漏洞预警、工信部）
- 国内安全厂商技术动态（奇安信/绿盟/深信服技术博客）

**根因**：
- OPML 里有 `奇安信CERT` `绿盟CERT` 但每天 0-1 条，且 wechat2rss feed ID 可能已过期
- CNVD 通过 wechat2rss 接入，但今日只 `CNCERT风险评估` 1 条
- CTF 完全没有信源覆盖

---

## 二、设计原则

- **不是问 LLM 更努力**，而是从源头给 LLM 它能用的素材
- **不要再加规则**（已被打脸过两次）。改 prompt + 加源，让 LLM 在更好的数据上做选择
- **score rubric 是"指南针"**，rubric 怎么写决定 LLM 怎么排
- **可单独验证**：每个改动可以独立 ship + 通过明天的 cron 验证

---

## 三、Phase 3-Sec 计划

### P3S.1 评分 rubric 重写（5 min，立即影响明天）

**`digest_pipeline_gemini.py` + `digest_pipeline.py` 的 BOARD_SCORE_SYSTEM["security"]`**：

旧：
```
9-10: 在野利用 0day、重大 APT 活动、大规模供应链攻击
7-8: 新型攻击技术、高危 CVE 详解、红蓝工具发布、关键威胁情报
5-6: 安全研究、技术博客、可观察性分析
0-4: 招聘、营销软文、职业规划、入门求助帖
```

新：
```
你是技术向的安全研究员，关心漏洞机制、攻击技术、防御架构，不关心地缘归因和合规通告。
评分标准：
- 9-10: 含技术细节的在野 0day（漏洞类型/触发条件/利用链）、新颖漏洞研究（含原理）、
        重大学术议题（Black Hat/DEF CON/USENIX/CCS/NDSS/Phrack）、CTF 解题深度复盘
- 7-8:  高危 CVE 深度分析（含 PoC 思路）、红蓝工具发布（带源码或技术说明）、
        独立研究者技术博客、漏洞预警通告（含影响面分析）
- 5-6:  常规安全资讯、技术普及类文章、CTF 比赛进度
- 3-4:  仅做地缘归因（"朝鲜黑客"/"中国 APT"/"俄罗斯"）但缺乏技术细节的新闻、
        合规政策公告（CISA/NIST 框架文件、零信任指南类）、纯防御产品营销
- 0-2:  招聘、培训广告、入门求助、职业规划、纯炒作

评分只看技术价值，不因语言或来源篇幅打折扣；中文一线媒体或官方源首发权重等同英文。
```

**关键变化**：
1. 删掉 "重大 APT 活动" 这个含糊词
2. 明确 "仅做地缘归因 ... 缺乏技术细节" → 上限 4 分（关键，专门治朝鲜黑客类稿）
3. 显式列 Black Hat/DEF CON/USENIX/CCS/NDSS/Phrack 作为 9-10 关键词
4. CTF 解题进入 9-10 区间

**预期效果**：今天的 #3 朝鲜黑客 npm 应该掉到 4 分，#17 零信任指南掉到 3-4 分。Ghost Bits 类议题如果在源里就能进 9-10。

---

### P3S.2 漏洞类摘要写原理（10 min，立即影响明天）

**`SUMMARIZE_SYSTEM`** 加一段：

```
对于 CVE / 漏洞 / 0day 类新闻，summary 必须围绕漏洞机制展开：
- 漏洞类型（SQL注入 / UAF / 整数溢出 / 越权 / 反序列化 / 路径穿越 / 等）
- 触发条件（哪个端点、什么参数、什么前置）
- 利用难度（PoC 是否公开、是否需要认证、是否需要本地访问）
- 影响范围（具体版本、产品形态）
不要写"该漏洞造成 X 影响"这种空话；如果原文提供了上述要素，至少写出其中 2-3 项。
对于研究/工具/CTF 类新闻，summary 围绕技术做法（用了什么 trick / 解了什么 chal / 工具核心机制）。
```

**风险**：原文 RSS 摘要本来就只有 200-400 字，可能不含上述细节。后果：LLM 会幻觉 / 或留白。

**缓解**：在 P3S.5 里我们会试 WebFetch 抓原文（非阻塞）；当前 prompt 加一句"如果原文未提供漏洞机制，明确说明'原文未披露技术细节'，不要编造"。

---

### P3S.3 OPML 源扩展（30-60 min，需逐个验证 RSS 可达）

#### A. 国际研究类（优先级最高）

| 源 | URL | 状态 |
|---|---|---|
| Project Zero | https://googleprojectzero.blogspot.com/feeds/posts/default | 验证 |
| Trail of Bits | https://blog.trailofbits.com/feed/ | 已在 |
| GreyNoise Labs | https://www.greynoise.io/blog/rss.xml | 验证 |
| watchTowr Labs | https://labs.watchtowr.com/rss/ | 验证 |
| Praetorian | https://www.praetorian.com/feed/ | 验证 |
| ProjectDiscovery | https://blog.projectdiscovery.io/rss/ | 验证 |
| Specter Ops | https://posts.specterops.io/feed | 验证 |
| Bishop Fox | https://bishopfox.com/feed.xml | 验证 |

#### B. 学术 / 会议类

| 源 | 备注 |
|---|---|
| arxiv cs.CR | https://export.arxiv.org/rss/cs.CR — 至关重要！ai 板块有 cs.AI 但 security 没接 cs.CR |
| Phrack | https://phrack.org/atom.xml — 一年几期但全是干货 |
| Black Hat 公告 | 暂无稳定 RSS，议题列表年度更新 |

#### C. 国内技术深度公众号（wechat2rss）

需要去 wechat2rss.xlab.app/list/all.html 找当前活跃 hash：

| 公众号 | 期望覆盖 |
|---|---|
| 看雪学院 | 二进制 / 逆向 / CTF |
| FreeBuf | 综合安全资讯 |
| 知道创宇 | 1day / 工具研究 |
| 默安玄甲实验室 | 已在 OPML，但需验证 hash |
| 长亭安全研究 | Web 安全 / 红队 |
| 长亭 tianyabaixiang | 同上 |
| Tencent 玄武实验室 | 已在 OPML，验证 hash |
| 阿里云 ASRC | 已在，验证 hash |

#### D. CTF 类（之前完全缺）

| 源 | URL |
|---|---|
| CTFtime upcoming | https://ctftime.org/event/list/upcoming/rss/ |
| Nu1L Team | https://nu1l.com/feed |
| 看雪 KCTF | 看雪官网 RSS |

#### E. 国内官方通告

| 源 | 状态 |
|---|---|
| CNVD 漏洞 | 找 wechat2rss 或 https://www.cnvd.org.cn/webinfo/list?type=8 抓取 |
| CNNVD 通告 | 同上 |
| CNCERT 月报 | 已在 OPML（CNCERT风险评估） |
| 中国信息安全 | 已在 OPML |
| 工信部信息通信发展司 | 找 wechat2rss |

**实施方法**：
- 每条逐个 `httpx.get()` 验证 200 + 含 `<item>` 节点
- 测试通过的写入 `feeds/security.opml` 在合适分类下
- 失效的留 TODO，下批补

#### F. 安全工具发布跟踪

```
github.com/<owner>/<repo>/releases.atom 形式
- nuclei (ProjectDiscovery)
- ffuf
- volatility
- ghidra
- frida
- BloodHound
```

每个 ~5 分钟接入。

---

### P3S.4 板块内细分子类（10-15 min）

**思路**：站点的 security tab 内部，按子类视觉分组，让 CTF/研究/通告/CVE 可一眼区分。

`config.yaml` 加 `subboards`：

```yaml
security:
  subboards:
    research: ["新型攻击", "0day 分析", "学术议题", "Black Hat/DEF CON"]
    cve: ["CVE 详解", "漏洞预警", "PoC"]
    redblue: ["红队工具", "蓝队检测", "CTF/竞赛"]
    advisory: ["官方通告", "厂商响应"]
```

**实施轻量版**：
- summarize prompt 末尾让 LLM 给 `subcategory: "research" | "cve" | "redblue" | "advisory"`
- 站点端按 subcategory 显示分组锚点（不是新 tab，是 anchor links）

---

### P3S.5（可选，5-10h）：WebFetch 增强漏洞摘要

**设想**：CVE/漏洞类条目在摘要前，先 WebFetch 抓原文 1500 字，传给 Gemini 摘要。

**好处**：解决问题 3 的根本——RSS summary 只有 200 字，写不出原理。

**风险**：
- 部分站点 403（已知 openai.com / 部分国内站）
- WebFetch 慢，每条 +2-3s，security 20 条 +40-60s，但 CI 总预算还远未触及 timeout
- 失败容错要好

**实施判断**：先做 P3S.1-3，看 P3S.2 的 prompt 调整能不能让现有 RSS summary 撑得住。撑不住再做 P3S.5。

---

## 四、实施顺序

| 步骤 | 工作量 | 依赖 | 验证手段 |
|------|--------|------|---------|
| **P3S.1** rubric 重写 | 5 min | 无 | 明天 cron 跑完看 #3 朝鲜黑客类条目是否消失 |
| **P3S.2** 漏洞摘要 prompt | 10 min | 无 | 明天看 CVE 条目摘要是否含漏洞类型/触发条件 |
| **P3S.3.A** 国际研究源 | 60 min | 需手动 verify URL | RSS feed 应在 24-48h 内开始有 entry 进 raw_count |
| **P3S.3.B** arxiv cs.CR | 5 min | 无（URL 已知） | 明天看是否有论文进 top 20 |
| **P3S.3.C** 国内 wechat2rss | 30-60 min | 需查 wechat2rss 当前 hash | 明天看活跃源里是否新增 |
| **P3S.3.D** CTF 源 | 30 min | 验证 RSS | 比赛公告类条目应进 |
| **P3S.3.E** 国内官方 | 30-60 min | 同 C | CNVD 通告应进 |
| **P3S.4** 子类标签 | 30 min | 依赖 P3S.1/2 | 站点端可见分组 |
| **P3S.5** WebFetch（可选） | 5-10h | 看 P3S.2 效果 | CVE 摘要质量明显提升 |

**最小可见改动**：P3S.1 + P3S.2 + P3S.3.B 合计 20 分钟，明天 cron 立刻见效（rubric + 摘要重写 + arxiv cs.CR 接入）。

**完整一轮**：P3S.1-4 约 3-4 小时，分两次 commit。

---

## 五、验收标准

### 明天（cron 自动跑完后）

- [ ] 朝鲜黑客 / 国家级归因类条目从 top 20 消失或降到末位
- [ ] CVE 类条目摘要中至少有一项：漏洞类型 / 触发条件 / 利用难度
- [ ] 至少 1 条来自 arxiv cs.CR 的论文进入 top 20

### 一周后

- [ ] 至少 5 条来自新增国际研究源（Project Zero / watchTowr / Trail of Bits 等）
- [ ] 至少 3 条来自国内技术公众号（看雪 / 长亭 / 玄武）
- [ ] 出现 ≥1 条 CTF 类内容（题解或比赛预告）
- [ ] 出现 ≥1 条国内官方通告（CNVD/CNNVD）

### 一月后

- [ ] 用户主观感受：今天的 security top 20 里至少一半"我看了有学到东西"
- [ ] 用户认为可以拿来发公众号或转给同事的内容比例 > 30%

---

## 六、风险登记

| 风险 | 缓解 |
|------|------|
| 新源 RSS 不稳定（403/挂掉） | 加入前逐个 httpx.get 验证；失败的下批补 |
| arxiv cs.CR 论文太学术，进 top 20 后摘要难写好 | LLM 应能处理；如果失败，加论文专属 prompt |
| Score rubric 改写后中文媒体反而被压（之前提过的"语言公平"被覆盖） | rubric 末尾保留"中文一线媒体权重等同英文"那句话 |
| 国内 wechat2rss feed hash 仍在轮换 | 把 hash 列表加到 monthly health check 清单（roadmap.md 里已有） |
| WebFetch 启用后 CI 超时 | 设 per-request 5s timeout，失败 fall back 到 RSS summary |

---

## 七、和 roadmap.md 的关系

Phase 2 完成度高，但 **Phase 1 在 security 板块还没真的完工**——这点诊断对。

这个 plan 严格属于 **Phase 1 收尾**（让现有日报形态 in security 板块达到产品级）。**不是 Phase 3**（roadmap 里 Phase 3 是周报/RSS/事实校验等扩展层）。

完成 P3S.1-3 之后，再回头看 roadmap 的 Bet B 选择就更稳——你需要先确定日报值得读，才能进周报。

---

## 八、决策点

请明确：

1. **是否同意 P3S.1（rubric 重写）当前措辞？** 特别是"地缘归因 缺乏技术细节 → 上限 4 分"——CISA KEV 类合规通告会被压低，但这个权衡你接受吗？
2. **P3S.3 优先级**：先做 A（国际研究）+ B（arxiv），还是先做 C（国内公众号）+ E（国内官方）？我建议 **B + A**（cs.CR 立刻见效，国际研究覆盖面广），但你可能更想要中文。
3. **P3S.5 WebFetch 是否启用**？如果 P3S.2 的 prompt 改写后 CVE 摘要质量仍弱，再启用？
