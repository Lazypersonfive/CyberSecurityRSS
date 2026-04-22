# RSS 源说明

本项目的 RSS 抓取源分为三个板块：

- `security`：网络安全、漏洞、威胁情报、攻防研究
- `ai`：AI 实验室发布、论文、工具、产业动态
- `finance`：支付、银行科技、金融基础设施、监管与行业媒体

完整订阅源以 `feeds/*.opml` 为准：

- [security.opml](/Users/dedsec/Desktop/RSS/feeds/security.opml)
- [ai.opml](/Users/dedsec/Desktop/RSS/feeds/ai.opml)
- [finance.opml](/Users/dedsec/Desktop/RSS/feeds/finance.opml)

## 文档分工

- [RSS.md](/Users/dedsec/Desktop/RSS/RSS.md)：保留原始大表和板块结构，便于人工浏览和存档
- [RSS源说明.md](/Users/dedsec/Desktop/RSS/RSS源说明.md)：记录当前抓取策略、筛选逻辑和维护方式

## 当前抓取策略

### 通用过滤

- 标题黑名单：过滤招聘、问答、水帖、教程流量文
- 来源黑名单：过滤已知高噪声站点
- Reddit 规则：没有明确安全关键词的帖子直接丢弃
- CVE / Patch Tuesday 语义去重：同一事件尽量只保留一条主记录

### 板块级裁剪

在 [config.yaml](/Users/dedsec/Desktop/RSS/config.yaml) 中为高产源设置 `source_caps`，避免少数站点挤占整个板块：

- `security`：限制 `cisa.gov`、`blog.upx8.com`、`mp.weixin.qq.com`、`simonwillison.net`、`reddit.com`
- `ai`：限制 `arxiv.org`、`technologyreview.com`、`theverge.com`、`techcrunch.com`
- `finance`：限制 `pymnts.com`、`bankingdive.com`、`paymentsdive.com`

调整原则：

- 单源产出过多，开始淹没其他来源时，降低 cap
- 单源质量稳定但样本太多时，降低 cap
- 某板块可用源不足时，提高 cap

## 摘要策略

- 默认使用中文标题
- 摘要目标长度为 `220-260` 个汉字
- 最低兜底为 `200` 个汉字
- 若模型返回过短、过长或英文字符偏多，会自动触发修复重写

## 日常运行

全量重跑：

```bash
./run_daily.sh
```

只跑单板块：

```bash
./run_daily.sh security
./run_daily.sh ai
./run_daily.sh finance
```

手动分步执行：

```bash
/Users/dedsec/anaconda3/envs/work3124/bin/python fetch_and_save.py --board security
/Users/dedsec/anaconda3/envs/work3124/bin/python fetch_and_save.py --board ai
/Users/dedsec/anaconda3/envs/work3124/bin/python fetch_and_save.py --board finance

/Users/dedsec/anaconda3/envs/work3124/bin/python digest_pipeline_gemini.py --board security
/Users/dedsec/anaconda3/envs/work3124/bin/python digest_pipeline_gemini.py --board ai
/Users/dedsec/anaconda3/envs/work3124/bin/python digest_pipeline_gemini.py --board finance

/Users/dedsec/anaconda3/envs/work3124/bin/python site_builder.py
```

## 维护入口

优先修改：

- [config.yaml](/Users/dedsec/Desktop/RSS/config.yaml)

必要时修改：

- [filter_entries.py](/Users/dedsec/Desktop/RSS/filter_entries.py)
- [rss_curation.py](/Users/dedsec/Desktop/RSS/rss_curation.py)
- [digest_pipeline.py](/Users/dedsec/Desktop/RSS/digest_pipeline.py)
- [digest_pipeline_gemini.py](/Users/dedsec/Desktop/RSS/digest_pipeline_gemini.py)
