---
hide:
  - navigation
  - toc
---

# 项目看板

想法、设计和任务都记在 [GitHub Issues](https://github.com/BucketSran/vaEVAS/issues) 上，Issue 是唯一的记录；本页每次构建时读取 Issue 的阶段标签（`stage:*`）和领域标签（`area:*`），自动画成看板，不另存一份任务表。EVAS 各功能的详细状态、优先级和验收以[统一功能清单](https://github.com/BucketSran/vaEVAS/blob/main/evas/docs/COMPARISON.md#engineering-status)为准，标签只是粗粒度视图。

{{ board }}

## 有了新想法怎么做

1. **记下来**：点上面的“记一个想法”，或者直接对任意会话说“记个想法：……”。会话先搜已有 Issue，同一目标已有记录就在那里补评论，否则新建一个带 `stage:idea` 和领域标签的 Issue。
2. **分诊**：定期看“想法”一列，逐条决定：合并到已有 Issue、进入设计（`stage:design`）、排期（`stage:planned`），或者以“不做”关闭并写明原因。
3. **设计**：在 Issue 里写目标、完成条件和方案；定下来就改成 `stage:planned`。
4. **实施**：开分支或 PR 时引用 Issue，阶段改成 `stage:active`；卡片上会自动出现关联的 PR。暂停时改成 `stage:paused`，并在 Issue 里写明原因和恢复条件。
5. **完成**：PR 合入、Issue 关闭后，会话写一条[更新日志](changelog/index.md)并引用 `#编号`，卡片移到“最近 14 天关闭”，并链接到那条日志。

规则原文见仓库的 [Issue 约定](https://github.com/BucketSran/vaEVAS/blob/main/docs/agents/issue-tracker.md)（标签一节随 [PR #219](https://github.com/BucketSran/vaEVAS/pull/219) 加入）。会话可以直接新建想法 Issue、修改阶段和领域标签；关闭 Issue、合并 PR 仍要先问。

!!! note "提醒规则"
    - **待分诊**：开着的 Issue 没有阶段标签，或者不止一个。
    - **停滞**：进行中却超过 14 天没更新；其他未暂停的 Issue 超过 30 天没更新。卡片会加深色边框。
    - **漏记日志**：已合入、但没有任何一条更新日志提到的 PR。
    - **状态矛盾**：例如标了 `wontfix` 却还开着。
    - **状态卡落后**：首页“最新阶段”的日期早于最新一条更新日志。
