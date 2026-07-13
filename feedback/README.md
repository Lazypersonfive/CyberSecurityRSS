# Human Feedback

人工反馈先作为可回放数据进入 offline eval，不自动修改 prompt、权重或源配置。

## Schema

每行一个 JSON 对象，路径为 `feedback/YYYY-MM-DD.jsonl`：

```json
{"date":"2026-05-18","board":"security","url":"https://example.com/a","action":"upvote","reason":"漏洞原理清楚，应该靠前","source":"example.com","title_zh":"示例标题","created_at":"2026-05-18T01:00:00Z"}
```

`action` 取值：`upvote`、`downvote`、`must_include`、`bad_summary`、`bad_source`。

## CLI

```bash
python feedback_cli.py add --board security --url URL --action upvote --reason "原因"
python feedback_cli.py import --file ~/Downloads/feedback_2026-07-13.jsonl
python feedback_eval.py --days 14
```

站点卡片提供“有用 / 不想看 / 摘要有问题”按钮，反馈只保存在浏览器本地；点击侧栏“导出反馈”后，用上述 `import` 命令导入仓库。每日 workflow 会刷新 `reports/feedback_eval.md`，并把最近 14 天汇总写入 `reports/weekly.md`。

规则：反馈只生成评估建议，任何生产策略变化仍走人工 review + git diff。
