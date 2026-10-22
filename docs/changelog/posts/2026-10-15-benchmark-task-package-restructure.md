---
date: 2026-10-15T14:33:00
categories:
  - Benchmark
slug: benchmark-task-package-restructure
---

# Benchmark 整理材料：R01 采样电路资产入库，确定题包规范，草稿批次与历史分开存放

10-12 至 10-15，main 上直接推送了 11 个 benchmark 提交，没有对应的 PR。这批提交只整理材料、规范和静态检查工具，没有新增计分题，没有做模型实验，也没有做新的仿真校准。整理后，正式题目录在题包审核前保持为空；56 道已建设任务和 R01 合同草稿按批次存放，41 个早期题包归档。

<!-- more -->

## 做了什么

- `31f594e5`（10-12）：加入 R01"采样与多通道读出"功能族资产，包括 3 个采样模块、5 个组合系统和 1 个表征仪器的 VA 与台架。README 写明，这九组资产不是九道新增计分题，现有 56 题的合同和数量不变。
- `a64c2ad0`（10-12）：benchmark 顶层固定为 tasks、checkers、workbench、reference 四个目录。作者文档和历史批次说明移入 workbench，题目输入和归档证据不变。
- `34923516`（10-14）：确定单文件题包的目标规范，采用 analog-design-bench 的原位编辑方式：`environment/starter/circuit.va` 进入环境后成为 `/app/circuit.va`，求解者直接编辑这个文件，最后也收集它。英文题面以 `Spec` 和 `Deliverable` 两段组织，参考解和终评材料放在求解环境之外。英文起草模板同步更新。
- `e2581ef6`（10-14）：修正入口说明。上一提交曾写"R01 的 20 道英文题包已完成公开 Spectre 仿真……"，现在改为：这 20 道草稿仍在本地工作区，尚未进入 main，也不计入 56 题。
- `32ac8c79`（10-14）：盘点 main 的材料和工作分支，写入 `DISCUSSION.md`。main 中有 37 个 v2 题包和 19 个 v3 题包；本地有 31 个工作区和 155 个本地分支，其中 31 个分支的名称与 benchmark 相关。
- `8a9367a4`（10-14）：新增 `tasks.json` 任务登记，由 `benchmark_workbench.py` 生成索引。R01 已确认的方向和交付伪代码整合进功能族 README。20 道旧格式草稿保存为本地恢复快照，不作为正式题包进入 main。
- `42690eab`、`9f1b8663`（10-14）：两处小修正。一是更正五组"中断与恢复修复"材料的归档状态；二是规定合同审核时先说明公开与隐藏条件的边界，合同确认后再实现 checker 和校准样本。
- `fae1bac2`（10-15）：在题包审核前，正式题目录保持为空。56 道保留任务和 R01 合同草稿按批次放进 `benchmark/material/draftbench/batches/`，41 个早期题包归档，来源和历史 manifest 通过显式路径解析保留。
- `75bc7205`（10-15）：规定多文件题的交付方式：沿用 Harbor 题包布局，原位编辑工程文件；默认逐个声明文件，只在需要时开放目录。同时写明修改范围、制品收集、参考解布局，以及 verifier 怎样独立重建。
- `35aeb7cb`（10-15）：新增 `scripts/benchmark_package.py`，按建设阶段（contract / implementation / calibration / accepted）静态检查题包，并接入 `benchmark_workbench.py --check`。benchmark 下的规范文档和模板改动也会触发 benchmark CI 检查。

## 结果与证据

- 提交说明写明：`fae1bac2` 没有修改任务合同，没有做模型实验或新的模拟器校准；`75bc7205` 没有修改题包、checker 或运行时。
- `35aeb7cb` 新增了对应测试 `scripts/tests/test_benchmark_package.py`。按文档说明，阶段检查不执行仿真、Dockerfile 或脚本，也不判断工程价值。静态检查通过不能代替作者校准或人工录取。
- 在 GitHub 上查不到这些提交关联的 PR，提交说明里也没有审查或 CI 结果记录，CI 结果未核实。

## 遗留与下一步

- `DISCUSSION.md` 列出的待办：确定旧 56 题迁移到新规范的边界；按新规范转换 R01 题包、生成器和格式检查；完成代表题的合同和验收方案审核。
- 已有题包继续沿用各自原来的运行合同。旧格式检查通过，不能算作已与 analogbench 规范统一的证据。
- 电路功能与场景审核仍以 [#159](https://github.com/BucketSran/vaEVAS/issues/159) 为入口。

## 相关链接

- 提交：[31f594e5](https://github.com/BucketSran/vaEVAS/commit/31f594e5)、[a64c2ad0](https://github.com/BucketSran/vaEVAS/commit/a64c2ad0)、[34923516](https://github.com/BucketSran/vaEVAS/commit/34923516)、[e2581ef6](https://github.com/BucketSran/vaEVAS/commit/e2581ef6)、[32ac8c79](https://github.com/BucketSran/vaEVAS/commit/32ac8c79)、[8a9367a4](https://github.com/BucketSran/vaEVAS/commit/8a9367a4)、[42690eab](https://github.com/BucketSran/vaEVAS/commit/42690eab)、[9f1b8663](https://github.com/BucketSran/vaEVAS/commit/9f1b8663)、[fae1bac2](https://github.com/BucketSran/vaEVAS/commit/fae1bac2)、[75bc7205](https://github.com/BucketSran/vaEVAS/commit/75bc7205)、[35aeb7cb](https://github.com/BucketSran/vaEVAS/commit/35aeb7cb)
- 当前入口（路径为 main 最新位置）：[benchmark 入口](repo:benchmark/README.md)、[草稿区总览](repo:benchmark/material/draftbench/README.md)、[批次目录](repo:benchmark/material/draftbench/batches/README.md)、[题包约定](repo:benchmark/material/draftbench/docs/task-package.md)、[评测与静态检查](repo:benchmark/material/draftbench/docs/evaluation.md)、[R01 功能族](repo:benchmark/material/draftbench/circuits/r01-sampling/README.md)、[历史题包](repo:benchmark/material/historyref/tasks/README.md)、[benchmark_package.py](repo:scripts/benchmark_package.py)
- Issue：[#159](https://github.com/BucketSran/vaEVAS/issues/159)
