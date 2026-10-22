---
date: 2026-10-20
categories:
  - 项目
slug: workflow-fast-feedback
---

# 工作流减负：固定主对话与进度入口，CI 只等决定下一步的反馈

10月17日至20日的六个工作流 PR 和一个直接提交都已进入 main：审查改成短摘要，同一任务固定主对话和进度入口，开发只等能决定下一步的局部反馈，完整 CI 在后台跑。PR 都写明"不声称已测得提速"，也没有改 EVAS 行为、原 checker、精度或预算。

<!-- more -->

## 做了什么

- PR201：审查摘要限 300/800 字，工具拒绝多份、空白或超长稿件，完整发现另存；EVAS 缺口按"局部缺口 → 共享能力 → 复杂组合"排序；记录阶段耗时；写明何时安全换主对话。
- PR202：精简常驻的 AGENTS 入口；工作区、CI 选择和阶段记录默认只显示摘要、失败和证据位置，`--json` / `--report` 保留完整结果。CI 选择对调度语义修改、未知路径、共享依赖、删除和重命名等仍保留必要检查。
- PR210：同一任务保留固定主对话与进度入口，取消"按上下文压缩次数强制换窗"，压缩后先恢复已有记录；必要交接在两个对话和固定入口留双向链接。同时落地快速反馈：先做 lint 和生成表检查，草稿按最近有效增量选模块，Python 全量回归分四组，按完整身份验证后才复用成功证据。
- PR211：开发只等待局部失败与消费者反馈，固定候选的完整 CI/审查在后台跑，最终验收与合并仍要收齐结果。SCS 与 source generation 补入 12 个公开消费者模块的快速映射；满足条件的数值 Rust 模块改动可免完整安装，但另构建并检查实际 release 核。
- PR215：在现有 policy 和 CI fast-checks 中提前检查两类反例——Select 表示变化让旧消费者回退，以及新增证明漏算数组内部工作或另开预算额度。
- PR216：补齐初始化输出与非线性观察证据的快速映射；每个稳定候选指定一个完整 Python 执行方，默认由 CI 承担。
- 直接提交 85a688d1：给项目 PR skill、Issue 约定和 `CONTRIBUTING.md` 增加可选的 PR 与 Issue 交付模板（`.github/pull_request_template.md`、`.github/ISSUE_TEMPLATE/task.md`）。

## 结果与证据

- PR202：重放 #201 的 16 文件差异，CI 选择从 8 类降为 2 类；同一工作区报告从 3244 减到 904 字符，但 PR 写明本轮总输出未降低，未证明整轮提速。
- PR210：托管 CI 全部通过，四组回归汇总确认 1831/1831 项 Python 执行成功、无夹具跳过，Linux/macOS 安装验证通过。用户免除了本轮独立审查并授权合并。
- PR211：完整托管 CI 15 项检查全部通过（含 157 项维护测试），1831/1831 Python 回归实际执行；独立 Standards/Spec 审查发现的 2 项注释绕过已修复。
- PR215：维护测试 162 项通过；三组冻结的坏版/修正版重放结果符合预期（Select 匹配内核运行失败/通过，整数数组漏计拒绝/通过，初始化独立额度拒绝/通过）。
- PR216：169 项维护测试通过；固定源码复现两项旧断言失败，修正后通过；规范与需求独审无问题。
- 85a688d1：外层 README 记录为按授权直接快进推送到 `main@85a688d1`；该提交的 [main CI](https://github.com/BucketSran/vaEVAS/actions/runs/39416399529) 当前显示为 completed / success（2026-10-22 用 `gh run view` 查得）。

## 遗留与下一步

- PR201 写明工具无法证明文风、审查真实性或完整压缩次数。
- PR215 写明初始预算检查只覆盖额度分配者和耗尽后重试，不能替代聚合调用计费复核；PR216 写明预算源码缺陷仍需各自修复与验收。
- 这几轮期间 EVAS 开发暂停，PR208 保持草稿不合并（后于 2026-10-21 合入，见对应条目）。

## 相关链接

- [PR #201 chore(workflow): 精简审查并明确换窗交接](https://github.com/BucketSran/vaEVAS/pull/201)
- [PR #202 chore(workflow): slim entry and narrow safe CI routing](https://github.com/BucketSran/vaEVAS/pull/202)
- [PR #210 固定主对话与进度入口，落实快速反馈工作流](https://github.com/BucketSran/vaEVAS/pull/210)
- [PR #211 按开发依赖安排 CI 等待与证据复用](https://github.com/BucketSran/vaEVAS/pull/211)
- [PR #215 工作流：在集成前检查Select消费者与证明预算](https://github.com/BucketSran/vaEVAS/pull/215)
- [PR #216 workflow: check observation consumers before integration](https://github.com/BucketSran/vaEVAS/pull/216)
- [提交 85a688d1 docs(workflow): add optional PR and issue delivery templates](https://github.com/BucketSran/vaEVAS/commit/85a688d1)
- [快速反馈规则](repo:CONTRIBUTING.md#keep-iteration-feedback-short)、[审查摘要规则](repo:CONTRIBUTING.md#concise-review-delivery)、[换窗规则](repo:docs/contributing/workspaces.md#conversation-handoff-triggers)、[Issue 约定](repo:docs/agents/issue-tracker.md)、[PR 模板](repo:.github/pull_request_template.md)
