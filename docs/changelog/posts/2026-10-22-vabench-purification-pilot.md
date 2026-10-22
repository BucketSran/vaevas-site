---
date: 2026-10-22T03:15:00
categories:
  - Benchmark
slug: vabench-purification-pilot
---

# vaBench 历史题纯化 pilot：14 个电路家族交给 5 个模型独立审查

试着从 vaBench 历史题里挑出值得保留的题，标准分两种：practicalwork 看 gold DUT 有没有真实来源，theorywork 看任务定义或任务价值是否清楚。第一轮 pilot 用 14 个电路家族（含 1 个对照项），每个交给 5 个模型独立审查，共 70 次会话。结果是：来源分级在各模型之间一致性好，theory 的评分标准还不能用，各模型的宽严差异大。

<!-- more -->

## 做了什么

- 按电路家族组织审查。每个家族打一个只读材料包，包括：
    - 求解者能看到的题面和 checker 性质列表；
    - gold DUT；
    - 脚本预选的候选来源文件，以及这些候选在 `SOURCES.md` 里的来源记录；
    - 文本重叠等预匹配提示。
- 审查者只能读文件。他们可以到已恢复的源码库 `benchmark/material/historyref/veriloga/` 自行检索。
- 来源分四级：P3 逐字、P2 改编、P1 存疑、P0 无证据。
    - 判 P2 必须点名一个具体文件，并列出至少 3 个共同结构。同主题、同名或常见写法不算证据。
    - P0 的意思是"没找到外部来源证据"，不等于"证明是原创"。
- 通过规则由脚本按每位审查者自己的回答推出，不做多数表决：
    - 来源通过 = P3 或 P2；
    - 任务通过 = "定义充分"为 yes，或"场景"和"工程价值"都为 yes。
    - 有分歧的项留给人判断。
- 样本：v4 的 11 个家族和 v1 的 3 个家族。对照项是 v4 的 128 号安全分压器，它对应 Cadence 库的 `divider.va`。
- 审查模型：DeepSeek v4.1 flash、Opus 5.5、Sonnet 5.5、GLM 5.3、Kimi K3。
- 运行规模：14 × 5 = 70 次会话，8 路并行。157、249 两题重跑过，初次结果保留在 `reviews-superseded/`。

## 结果与证据

- 报告汇总：来源 no 7、split 1、yes 6；任务 split 5、yes 9。
- 来源分级一致：
    - 多数家族五位审查者给出同一等级，例如 131、171、141、146、197 全票 P2，对照项 128 全票 P3。
    - 只有 3 个家族各有 1 位给出不同等级：249、001、v1 的一阶低通。
- 任务判定分歧大：
    - 5 个家族出现分歧，包括 157、197、141、v1 的可编程激励序列器。
    - 连来源全票 P3 的对照项 128，任务判定也是 2:3。
    - 197 号的情况：DeepSeek、Opus、Sonnet 判未过，GLM、Kimi 判通过。
- 证据（本地，未提交）：`current/runs/historical-purification-20261022/` 下的 `pilot-report.html`（逐题理由与证据）、`pilot.json`、`pilot-run.log`、`reviews/`、`tools/`（材料打包、审查提示词与报告脚本）。

## 遗留与下一步

- theory 评分标准需要重写，现在不能直接用来筛题。
- 第二轮已在本地启动，截至本条仍在运行，还没有结果：
    - 题目按电路功能合并成跨版本单元，`evidence/units.json` 共列出 619 个；
    - 选出 practical 10 个单元、theory 19 个单元，每个单元仍交给 5 个模型；
    - theory 一侧改用课题组导入 SOP 里的四道门槛（有用场景、合理任务、完整测试、公平评测）；
    - 结果写在 `reviews2/`。
- 这项工作没有改动题库、没有提交，也没有 PR。

## 相关链接

- 历史资料与来源记录：[historyref 说明](repo:benchmark/material/historyref/README.md)、[SOURCES.md](repo:benchmark/material/historyref/veriloga/SOURCES.md)
- 本地报告：`current/runs/historical-purification-20261022/pilot-report.html`
