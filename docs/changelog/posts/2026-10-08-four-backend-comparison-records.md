---
date: 2026-10-08
categories:
  - 项目
  - EVAS
slug: four-backend-comparison-records
---

# 四后端对照工具成型：协作基线、可追溯比较记录与 CMP8 实测

2026-10-06 至 10-08 合入 5 个 PR，建立 Spectre、OpenVAF-R＋ngspice、Gnucap＋modelgen-verilog、EVAS 四后端比较的记录、身份校验和论文条件卡。CMP8 开发批次实测为 Spectre 8P、EVAS 8P、OpenVAF-R＋ngspice 4P/1F/3X、Gnucap＋modelgen 5P/3F，正式资格仍为 32I；这是既有开发集的有限证据，不是论文独立验证集。

<!-- more -->

## 做了什么

- #73：发布原只在本地 main 的五个提交，建立 benchmark/EVAS 各自验收、Spectre 对照、DAC 冻结和 current 日常入口的协作基线；同时发布 24 配置 Spectre 实测摘要。
- #84：提供四后端证据表和刷新工具 `refresh.py`，记录各后端的输入、checker、工具、收据和误差预算；固定 8 个开发条件 × 4 后端共 32 配置，刷新时生成新快照、保留父快照。
- #93：比较执行器增加实际内核身份查询、STARTED/run ID 校验和完整批次收集器；缺案例、重复身份、伪造版本或"失败改通过"都会被拒绝。
- #98：两个开源后端各跑 8 个固定配置，在受审 main `d4b41c79` 上重跑 EVAS 8 项，原 Spectre 8 项波形经固定 checker 桥重分析后复用。关闭 #95。
- #99：交付论文对照的条件卡、独立判据、输入冻结、观察适配和表格工具，从 40 条候选收敛到 12 条固定条件。

## 结果与证据

- #73 的 24 配置是七个固定候选版本的证据：原语言 5 吻合/5 未决，原数值 4 通过/1 失败/3 未决；D7 精确终点计数差异保留。
- #84 时，历史本批 EVAS8 与 Spectre8 的 16 份有限观测达到各自目标；另 16 配置因容器 overlay 缺失记为 T/unrun，没有缩小分母。48 项工具测试通过。
- #93 保留的 8 项真实 EVAS 观察属于源码 `c7baed1b`，另 24 项未运行；它不是最终 TABLE，也不是论文独立验证集。
- #98：两个开源后端实际完成 16 次编译、14 次主仿真；两个 event-OR 编译失败和一个 90 秒超时保留为 X，没有自动重试。32 项全部保留。
- #99：首轮 12 条件 × 4 后端全部尝试，结果为 I35/X13/T0，正式 P/F/U 未授予；35 项缺完整观察或误差资格，不是 35 项通过。
- 原始日志和波形为 local-only，本地报告在 `current/runs/four-backend-round-20261007/`，#99 的审查与检查日志在 `current/runs/pr-consolidation-20261008/`。

## 遗留与下一步

- #99 的 12 条件是开发知情条件，合并后也不是未接触的独立确认集；A1 行为缺口、观察误差资格和最终论文结果由 #96 继续跟踪。
- 仿真器侧的修复集中在 #108（见 10-09 条目），端点差异在 #79。
- #84 记录：新论文测评集分母 unknown，EVAS 许可证 unknown，不做耗时排名。

## 相关链接

- PR：[#73](https://github.com/BucketSran/vaEVAS/pull/73)、[#84](https://github.com/BucketSran/vaEVAS/pull/84)、[#93](https://github.com/BucketSran/vaEVAS/pull/93)、[#98](https://github.com/BucketSran/vaEVAS/pull/98)、[#99](https://github.com/BucketSran/vaEVAS/pull/99)
- Issue：[#95](https://github.com/BucketSran/vaEVAS/issues/95)、[#96](https://github.com/BucketSran/vaEVAS/issues/96)
- 仓库：[比较表](repo:experiments/backends/comparison/TABLE.md)、[比较工具说明](repo:experiments/backends/comparison/README.md)、[论文条件与判据](repo:evas/validation/paper/README.md)、[论文执行与表格](repo:experiments/backends/paper/README.md)、[24 配置执行报告](repo:experiments/backends/dvs2-spectre-validation/results/pr-alignment-20261006.md)
