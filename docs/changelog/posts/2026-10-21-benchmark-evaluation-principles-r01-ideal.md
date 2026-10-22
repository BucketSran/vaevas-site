---
date: 2026-10-21T16:29:00
categories:
  - Benchmark
slug: benchmark-evaluation-principles-r01-ideal
---

# benchmark 评测原则、agent 流程与 R01 ideal 草稿题包合入 main

PR217 已合入 main：此前只在本地工作区的评测原则、agent 建设流程、Spec 提取研究和 R01 ideal 题包，以草稿身份进入 main。没有编译或运行任何 VA，R01 ideal 仍是 `implementation` 阶段、`pending = ["grading", "runtime"]`。

<!-- more -->

## 做了什么

- 三层文档：中文人审原则 `docs/design.md`、英文 agent 流程 `docs/agent-workflow.md`、详细参考 `docs/design-reference.md` 和 R01 采样电路参考页；原长文移入参考页，旧链接保留入口。`vaevas-workflow` skill 的 benchmark 一行改为指向 agent 流程。
- 评测原则 `docs/evaluation.md`：区分公开自测、独立终评、任务计分与 checker 校准，用有限采集题举例；`templates/` 与之对齐。
- Spec 提取研究：AnalogBench 与 CVDP Heavy 1.1 各 15 题，逐题独立重建 Spec，再由另一 session 对照真实题面，结论写回建设流程。Heavy 缺官方 gold，只列 checker + baseline，不冒充 gold。
- R01 ideal 题包：窗内连续跟踪、关窗时刻采样、复位优先与复位后保持。
- 工具：`benchmark_package.py` 增加题包检查（instruction 模板标记与执行脚注、starter 类型、`circuit_route`/`pending`、三个必需小节）；修复新增题包后题包数从 98 变 99 导致的数量断言失败，原 98 项历史断言保留。

## 结果与证据

- 合并后的树上跑了 CI 对 `benchmark` 的全部选择，均通过：身份检查（61 个历史文件、6 个当前校准）、workbench 检查、题包与路径回归 67 项、first-batch 同步与各目录回归、selection 步骤的 5 组脚本检查、`git diff --check`。
- 没有做的：未编译或运行 VA，未跑仿真器、容器、作者校准或模型解题。参考与校准结果均为 null。PR 写明静态检查和 Python 测试不证明题目已通过人工审核，也不证明后端支持。
- 只涉及 `benchmark/`、`vaevas-workflow` skill 及 benchmark 的脚本和测试，不碰 EVAS 源码。

## 遗留与下一步

- 待决定（题包 README 已列出）：参数域与激励域、同实例同刻边界、电压容差与测量预算。建议值（vin/vinit 0–1.8 V、vth 0.3–1.5 V、2 mV）只是提案，未采纳；配置里 `status = pending_user_decision` 会阻止启动。
- 合入后 benchmark 后续工作在新线程里从 main 继续，本地 `runs/` 证据不入库。
- 外层 README 另记录了一份工作流展示网页（`local/presentations/vabench-workflow-20261021/`），内容固定到 PR217 的提交 `ad425227`；它是本地单文件交付，README 写明未确认线上发布，不属于 PR217 的合入内容。

## 相关链接

- [PR #217 docs(benchmark): 评测原则、agent 流程与 R01 ideal 草稿合入 main](https://github.com/BucketSran/vaEVAS/pull/217)
- [评测原则](repo:benchmark/material/draftbench/docs/evaluation.md)、[人审原则](repo:benchmark/material/draftbench/docs/design.md)、[agent 流程](repo:benchmark/material/draftbench/docs/agent-workflow.md)、[详细参考](repo:benchmark/material/draftbench/docs/design-reference.md)
- [Spec 提取研究](repo:benchmark/material/draftbench/research/spec-extraction-study.md)、[R01 采样电路参考](repo:benchmark/material/draftbench/circuits/r01-sampling/reference.md)
- [R01 ideal 题包说明](repo:benchmark/material/draftbench/batches/r01-sampling-01/tasks/r01-spec-ideal/README.md)
