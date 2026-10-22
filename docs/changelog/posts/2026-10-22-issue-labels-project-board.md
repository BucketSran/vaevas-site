---
date: 2026-10-22T15:30:00
categories:
  - 项目
slug: issue-labels-project-board
---

# Issue 加上阶段与领域标签，网站新增项目看板

GitHub Issue 继续做唯一的任务记录，新增 5 个阶段标签和 3 个领域标签。12 个开着的 Issue 已打好第一轮标签。网站新增“项目看板”，构建时读取 Issue 自动画成看板，并列出要处理的提醒。仓库里的规则修改走 [PR #219](https://github.com/BucketSran/vaEVAS/pull/219)，尚未合并。

<!-- more -->

## 做了什么

- **GitHub 上**（用户同意后执行）：
    - 建了 8 个标签：`stage:idea`、`stage:design`、`stage:planned`、`stage:active`、`stage:paused`，以及 `area:evas`、`area:benchmark`、`area:project`。
    - 给 12 个开着的 Issue 打了第一轮标签：进行中 #214、#176；已排期 #181、#119、#96、#70、#66、#65；暂停 #138、#16；设计中 #159、#107。
- **仓库**：[PR #219](https://github.com/BucketSran/vaEVAS/pull/219) 修改 `docs/agents/issue-tracker.md`，写明标签含义、记录新想法的步骤和用户授权，并新增“想法”Issue 模板。EVAS 的 Issue 仍以统一功能清单为准，标签只是粗粒度视图。
- **网站**：
    - 新增[项目看板](../../board.md)，按阶段分列；“最近 14 天关闭”只显示 8 张卡片。卡片显示 Issue 摘要、引用它的 PR、提到它的更新日志，以及最近一次正文或评论的时间。修改标签不算作更新。
    - 页面顶部列出要处理的提醒：待分诊、缺领域标签、状态矛盾、停滞、已合入却没写进日志的 PR、状态卡落后。
    - 首页状态卡新增“进行中的工作”一行，自动读取看板。
    - Benchmark 预览页的计数和逐题表、首页的 benchmark 题数改为从 main 自动生成，构建前默认先 `git fetch`。
- **授权**：用户同意以后的会话可以直接新建想法 Issue、修改阶段标签。关闭 Issue、合并 PR 仍要先问。

## 结果与证据

- 看板读取到 54 个 Issue（开着 12 个）、153 个已合入 PR、0 个里程碑。目前提醒 1 条：#16 标了 `wontfix` 却还开着。
- 自动生成的 benchmark 计数与之前手写的一致：58 个题包（v2-01 37、v3-01 19、r01-sampling-01 2），按工程动作分为 29、2、6、5、16。
- 反向验证：删掉唯一提到 #35 的那条日志后，看板报出“#35 没写进更新日志”；把状态卡日期改旧后，报出“状态卡比最新日志旧”。
- `./site.sh build`：严格构建 0 个警告，站内链接和锚点检查 0 处问题。

## 遗留与下一步

- PR #219 等用户决定是否合并。合并前，“想法”模板不会出现在 GitHub 的新建 Issue 页面上，看板的“记一个想法”按钮只会预填 `stage:idea` 标签。
- #16 是关闭，还是去掉 `wontfix`，需要用户决定。
- 还没有里程碑。DAC 投稿冻结等阶段目标需要用户给出日期，然后在 GitHub 上建里程碑。
- 第一轮阶段标签是本会话的判断，用户可以直接在 GitHub 上改，看板下次构建时会跟着变。

## 相关链接

- PR #219：https://github.com/BucketSran/vaEVAS/pull/219
- 网站说明“项目看板”一节：`local/site/README.md`
