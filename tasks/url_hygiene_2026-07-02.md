# P0：坏链接修复 + 源登记 + 报表口径（2026-07-02）

> 触发：20 天回顾发现 `hackernews.cc/feed` 的 `<link>` 全部写成 `http://0.0.0.0:8080/post/<id>`，
> 过去窗口 28 条坏链入选并发布到站点（今日仍在进入）。同时 security unknown 33 条/7 天、
> offline_eval 的 `Min CN` 列实为配置目标而非观测值。

## 需求

### R1 坏链接（三层，缺一不可）
1. **恢复**：fetch 阶段引入 `url_hygiene.repair_entry_url(link, feed_url)`——
   当 item 链接的 host 非公网（0.0.0.0/127.x/localhost/私网段/link-local/::1）且 feed host 为公网时，
   用 `https://<feed_host><原 path?query>` 重写。已实测 `https://hackernews.cc/post/64413` 返回 200 真文章。
   通用规则而非 per-feed 硬编码：防的是下一个配错 RSS 生成器的源。
2. **防线**：filter 阶段最终门——`is_public_http_url()` 不通过的 URL 直接丢弃，
   计入 `dropped_nonpublic_url`。修复失败的坏链永不进入 output/digest/站点。
3. **回填**：已发布 digest 与 docs feed JSON 中的 `0.0.0.0:8080` 链接就地改写为
   `https://hackernews.cc/...`，重建站点。历史归档一并修复（都还在 GH Pages lookback 内或搜索可达）。

### R2 unknown 源登记
`source_registry.yaml` 补三个高频 unknown：
- `hackernews.cc` → t2 / cn_expert / 中文安全媒体（回填后它会继续供给中文条目）
- `securityweek.com` → t2 / media
- `cyberkendra.com` → t2 / media
（`defend.network` 质量存疑，本轮不登记不拉黑，继续观察。）

### R3 报表口径
`offline_eval.md` Board Health 表：`Min CN` 更名 `CN Target`，新增 `Obs Min CN`（窗口内观测最低中文数）。

### R4 工程卫生
- `requirements-dev.txt`（或 requirements.txt dev 段）声明 pytest；CLAUDE.md 已认 unittest 为准，两者都能跑。

## 测试（先写）
- `is_public_http_url`：拒绝 0.0.0.0 / 127.0.0.1 / localhost / 10.x / 172.16-31.x / 192.168.x / 169.254.x / [::1] / 非 http(s)；放行正常公网 URL。
- `repair_entry_url`：`http://0.0.0.0:8080/post/64413` + feed `http://hackernews.cc/feed` → `https://hackernews.cc/post/64413`；公网链接原样返回；feed host 也非公网时不重写。
- `filter_and_dedup`：非公网 URL 条目被丢弃且 stats 含 `dropped_nonpublic_url`。
- `render_offline_eval`：表头含 `CN Target` 和 `Obs Min CN`，不含旧 `Min CN |` 单列。

## 验收
- 全部测试绿 + ruff clean。
- 回填后 `digest/`、`docs/` 中 `0.0.0.0` 计数为 0；站点重建成功。
- 明日 cron：hackernews.cc 条目以 `https://hackernews.cc/post/...` 入选（中文供给不掉），unknown 计数因登记下降。
