# Human Feedback / Reward Loop Plan

## Goal

建立一个轻量、可回放、可解释的人工反馈机制，把“这条新闻好/坏”的主观判断逐步转成稳定的源权重、评分权重和筛选策略，而不是每天继续手调 prompt。

## Non-Goals

- 不做自动强化学习，不训练模型。
- 不让 Gemini 直接读取历史反馈后自行改规则。
- 不让每日 workflow 自动修改 `config.yaml` 或 `source_registry.yaml`。
- 不把用户反馈做成不可解释的黑盒权重。

## Why This Is Feasible

当前 pipeline 已经有三个适合接反馈的确定性层：

- `source_registry.yaml`: 可以调整源的 `tier/kind/label`。
- `config.scoring`: 可以调整 `source_bonus`、`kind_bonus`、`dimension_weights`、`cn_visibility_bonus`。
- `source_policy`: 可以调整 `min_chinese`、`max_google_news`、`max_aggregator`、`source_caps`。

人工反馈不需要直接改 Gemini prompt。更好的方式是把反馈变成数据，再由 offline eval 给出“如果按这个反馈调权，会怎样改变过去 7-14 天结果”。

## Feedback Types

每日反馈建议只保留几个明确动作：

| Action | Meaning | Example Use |
|---|---|---|
| `upvote` | 这条应更靠前/以后类似内容更应选 | 高质量漏洞原理、官方重大发布、顶级开发者首发 |
| `downvote` | 这条不该入选/以后类似内容降权 | 泛政治 APT、融资 PR、弱新闻、重复转述 |
| `must_include` | 这条今天漏了，应该强制进同类结果 | 重大 CVE、Ghost Bits、重要中文首发 |
| `bad_summary` | 入选对，但标题/摘要差 | 漏洞没写原理、标题截断、摘要空泛 |
| `bad_source` | 源整体低质，需要 review | 噪声媒体、失效公众号、营销聚合 |

## Proposed Data Model

先用 append-only JSONL，避免引入数据库。

Path:

```text
feedback/YYYY-MM-DD.jsonl
```

One line per feedback:

```json
{
  "date": "2026-05-11",
  "board": "security",
  "url": "https://example.com/article",
  "action": "upvote",
  "reason": "漏洞原理清楚，属于当天重要 CVE",
  "source": "freebuf.com",
  "title_zh": "Linux Dirty Frag 本地提权漏洞",
  "created_at": "2026-05-11T08:30:00Z"
}
```

Optional fields:

```json
{
  "story_id": "cve:cve-2026-31431",
  "suggested_tag": "漏洞原理",
  "severity": "high",
  "applies_to_source": true
}
```

## Scoring Translation v1

Do not apply feedback directly in production at first. Instead generate a report:

```text
reports/feedback_eval.md
```

Suggested deterministic interpretation:

| Feedback | Offline Interpretation |
|---|---|
| `upvote` | Show how much final_score/source bonus would need to increase for similar items to rank top 5 |
| `downvote` | Show whether lowering source_kind/source/source cap would remove similar items |
| `must_include` | Mark missed item and show which stage dropped it: fetch, filter, score, dedupe, source policy, cap |
| `bad_summary` | Count by board/source; feed into prompt repair backlog, not ranking |
| `bad_source` | Add to weekly review section; require manual source_registry/source_caps change |

## Workflow

1. Daily digest runs normally.
2. User reviews site and gives feedback in chat or via future UI.
3. Codex writes feedback JSONL entries.
4. `feedback_eval.py` reads recent feedback plus `digest/`, `output/`, `docs/`.
5. Report shows concrete recommendations, for example:
   - `freebuf.com` received 6 upvotes in security; consider `source_caps.freebuf.com +2` or `kind_bonus.cn_expert +0.1`.
   - `pymnts.com` received 4 downvotes in finance; consider `source_caps.pymnts.com 4 -> 2`.
   - `ai_security` missed 3 must_include X posts because RSSHub returned no item; source problem, not scoring problem.
6. Human approves exact config diff.
7. Run offline eval before applying.

## Minimal Implementation Plan

### P1: Manual Feedback File

- Add `feedback/README.md` with schema and examples.
- Add `.gitkeep` or keep directory created by script.
- Add helper CLI:

```bash
python feedback_cli.py add --board security --url URL --action upvote --reason "..."
```

### P2: Feedback Eval Report

- Add `feedback_eval.py`.
- Output `reports/feedback_eval.md`.
- Detect dropped-stage for `must_include`:
  - not in `output/<board>_latest.json`: source/fetch issue.
  - in output but not digest: score/dedupe/source policy issue.
  - in digest but low display rank: ordering/final_score issue.

### P3: UI Integration Later

- Add small “好 / 差 / 摘要差” buttons in local/admin-only mode.
- Avoid public write endpoint because site is static GitHub Pages.
- If public feedback is needed later, use GitHub Issues, Forms, or a serverless endpoint; not part of current static architecture.

## Gemini Prompt Implications

Feedback should not be pasted wholesale into Gemini system prompt. That would make behavior unstable and token-heavy.

Safe use of feedback with Gemini:

- Keep board-level editorial rules short.
- Periodically convert repeated feedback into explicit deterministic policy.
- Use small curated examples only if a failure repeats many times, e.g. “仅有地缘归因且无技术细节的 APT 新闻上限 4 分”。

Better route:

- LLM outputs dimensions.
- Code computes final_score.
- Feedback adjusts code weights and source registry after offline eval.

## Risks

- Feedback volume too low: daily one or two votes may overfit if applied automatically.
- Recency bias: one bad day may unfairly punish a generally good source.
- Source vs story confusion: a weak article from a strong source should not always downgrade the source.
- Confirmation bias: only downvoting visible selected items ignores missed high-quality items.

Mitigations:

- Require 3-5 feedback events before recommending source-level changes.
- Separate item feedback from source feedback.
- Keep all changes reviewable as normal git diffs.
- Run 7-14 day offline eval before production config changes.

## Recommendation

Implement this, but in two steps:

1. Start with JSONL feedback + report only. No automatic tuning.
2. After 1-2 weeks of feedback, add semi-automatic recommendations that generate a patch for human review.

This matches the AIHOT lesson: use AI for judgment, but keep selection policy explicit, measurable and reversible.
