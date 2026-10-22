---
date: 2026-09-27
categories:
  - 项目
  - EVAS
  - Benchmark
slug: prehistory-vabench-legacy-evas
---

# 前史：vaBench v1–v4、旧版 EVAS 0.8.x 与本仓库建立

本仓库建立之前，课题组已有两套成果：vaBench 题库（v1–v4，来源仓库 `Arcadia-1/behavioral-veriloga-eval`）和旧版 EVAS 仿真器（PyPI 包 `evas-sim`，最后一个标签 v0.8.7）。2026-09-27 建立 vaEVAS 仓库，重新开发 EVAS，并把历史材料作为只读参考迁入。

<!-- more -->

## 做了什么

**vaBench（旧题库）**

- 来源仓库：https://github.com/Arcadia-1/behavioral-veriloga-eval 。本地副本的 git 历史显示首个提交在 2026-03-20。
- 四个发布目录首次出现在该仓库 git 历史中的日期：v1 为 2026-05-22，v2、v3 都是 2026-06-24，v4 为 2026-07-12。
- 据该仓库 README，v2 已退役，它的 5 个候选题并入 v3，编号为 283–287。
- 迁入本仓库时用的快照是 `7b5616dc`（2026-07-28，提交说明为 "Promote r53 on EVAS 0.8.7"）。迁入日期是 2026-10-03，对应提交 6d806a04。
- v1 整包迁入：86 项 L1/L2 发布目标，其中 73 项核心、13 项辅助。v4 只迁入最新快照 r53 和全部文档，`benchmarkv4` 基线和 r45–r52 等旧快照没有迁入。v3 完整发布包没有迁入。

**旧版 EVAS（evas-sim 0.8.x）**

- 来源仓库：https://github.com/Arcadia-1/EVAS 。本地副本的首个提交在 2026-03-14。
- 几个标签的日期：v0.4.1 为 2026-03-17，v0.8.0 为 2026-07-06，v0.8.3 为 2026-07-18，v0.8.7（提交 `6cb6fa7`）为 2026-07-28。
- 它的 README 写明定位：电压域、事件驱动的 Verilog-A 行为模型仿真器，没有 ngspice，也没有 KCL/KVL 求解器。
- vaBench v4 的两次认证分别用了不同的 EVAS 版本：
    - R45 认证用 EVAS 0.8.3，gold 400/400 通过。
    - r53 把运行时绑定到 `evas-sim==0.8.7`，复用源码认证，没有重新跑完整 400 题。r53 的门禁不含 Spectre，也没有运行 Spectre。

**本仓库建立**

- 2026-09-27 17:25（北京时间）提交 `3df4abd8`（chore: initialize vaEVAS workspace），共 9 个文件，包括 README、AGENTS.md，以及 evas、experiments、tasks 等目录说明。
- 第一批 PR 在 2026-09-28 合入，见下一条。其中 PR1 的四后端基线把"旧 EVAS 0.8.7"作为四个后端之一。

## 结果与证据

- 历史包来源与迁入取舍：[historyref 说明](repo:benchmark/material/historyref/README.md)。
- [R45 认证说明](repo:benchmark/material/historyref/v4/R45_RELEASE_CERTIFICATION.md)：运行身份为 EVAS 0.8.3。
- [r53 认证说明](repo:benchmark/material/historyref/v4/R53_RELEASE_CERTIFICATION.md)与 [r53 封印](repo:benchmark/material/historyref/v4/release/benchmarkv4-r53/RELEASE_SEAL.json)：绑定 0.8.7，复用 gold 400/400 的源码认证。
- 旧仓库在本地的位置：`legacy/EVAS`、`legacy/behavioral-veriloga-eval`。上一阶段的报告论文在 `legacy/AAAI-2027`。

## 遗留与下一步

- 旧版本的评分方式、任务数量和仿真器能力只适用于当时的版本和范围，不能直接用来解释当前主线。
- 迁入的 Cadence 源码和派生参考解还没有确认对外分发许可。
- vaBench v3 完整包没有迁入，只用它的导入记录追溯模型来源。

## 相关链接

- 仓库初始化提交：https://github.com/BucketSran/vaEVAS/commit/3df4abd8
- vaBench v1/v4 历史迁入：https://github.com/BucketSran/vaEVAS/commit/6d806a04
- 旧题库来源：https://github.com/Arcadia-1/behavioral-veriloga-eval
- 旧 EVAS 来源：https://github.com/Arcadia-1/EVAS
