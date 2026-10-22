---
date: 2026-10-03
categories:
  - 项目
slug: docs-restructure-oct03
---

# 文档与目录整理：手册分层、实验目录重组、三课教程和追溯检查

10 月 2–3 日 main 上的一组文档整理：状态校准到 EVAS 0.12.2 / IR16，实验目录和示例重新组织，并由 #35 修复整理过程中被改动的冻结文件与历史收据身份、加上可检查的测试追溯矩阵。全部是文档和目录调整，没有重跑仿真。

<!-- more -->

## 做了什么

- **状态与导航校准**（`4aab15ec`，10-02）：当前状态改为已合并的 0.12.2 / IR16，区分直接算子路径与联合动态，重复的审查叙述改为固定历史链接。
- **实验目录**（`f3440b21`，10-02）：按用途和证据分出当前、参考/历史、旧审计三类导航，并约定今后的实验命名。
- **skill 与 review 规则**（`ee0ba9c7`，10-02）：拆开 EVAS 与 benchmark 的任务约定，集中写明面向人读的 diff 审查和发布检查；新增 `benchmark/README.md` 占位。
- **项目指南**（`1527502c`，10-02）：理清 benchmark 与仿真器的分工，独立验证协议从入口页拆到 `PROTOCOL.md`；已完成的实验报告改链到已发布历史；从当前文件树移除冗余占位和已归档的旧 EVAS 迁移审计目录。
- **示例与测试分层**（`7d0398d2`，10-03）：`examples/` 只保留自带 `.va` 的示例，六个能力 smoke 输入移到 `validation/smoke/`；新增测试分层说明；`experiments/` 重组为 `runs/`、`backends/`、`archive/`。
- **三课教程**（`8de77e94`，10-03）：示例改成 01 静态增益、02 瞬态积分（idt）、03 cross 事件计数器，每课有 `dut.va`、`sim.json`、电路示意和手算期望值。
- **vaBench 历史迁入**（`6d806a04`，10-03）：v1/v4 历史发布包作为只读参考迁入，详见"前史"条目。
- **#35 手册与追溯**：数学章节移到 `evas/docs/math/`；40 个 EVAS 测试文件声明 GUARDS 标签，`scripts/traceability.py` 生成测试与能力的追溯矩阵，`--check` 只读检查标签格式、未知 ID、链接/锚点和矩阵是否过期。目录整理曾替换冻结清单和历史收据里的路径，导致身份核验失败；#35 把 v1 的三份冻结文件和 37 份历史 JSON 收据恢复到原字节。另修正教程里的 cross 参数顺序、参考方程和波形名称。

## 结果与证据

- 直接提交的自检：`4aab15ec` 检查 706 个本地链接/锚点，56 个运行时文件和 42 个测试文件哈希不变；`f3440b21` 检查 719 个链接/锚点。
- #35：生成器回归先复现原实现失败，修复后 7 个测试通过；v1 身份核验（36 个 Git 工件、4 个快照、13 项原始输入）通过；1,077 处 Markdown 引用和 50 处固定历史 Git 引用无失效。
- 本批没有重跑全量 506 项 EVAS 测试、Spectre 或原 31 条件矩阵，历史执行结果不当作本轮运行。

## 遗留与下一步

- GUARDS 标签由人审查，生成器只保证登记与生成物一致，不证明逐方法覆盖或测试执行。#35 合并时追溯检查尚未接入 CI。
- 只读 benchmark 导入和冻结文档按历史原样保留，不改写为当前导航。

## 相关链接

- [PR #35 docs: 重组 EVAS 手册、校验追溯映射并修复历史身份](https://github.com/BucketSran/vaEVAS/pull/35)
- 直接提交：[4aab15ec](https://github.com/BucketSran/vaEVAS/commit/4aab15ec)、[f3440b21](https://github.com/BucketSran/vaEVAS/commit/f3440b21)、[ee0ba9c7](https://github.com/BucketSran/vaEVAS/commit/ee0ba9c7)、[1527502c](https://github.com/BucketSran/vaEVAS/commit/1527502c)、[7d0398d2](https://github.com/BucketSran/vaEVAS/commit/7d0398d2)、[8de77e94](https://github.com/BucketSran/vaEVAS/commit/8de77e94)、[6d806a04](https://github.com/BucketSran/vaEVAS/commit/6d806a04)
- 当前入口：[数学手册](repo:evas/docs/math/README.md)、[教程](repo:evas/examples/README.md)、[测试分层](repo:evas/tests/README.md)、[验证协议](repo:evas/validation/PROTOCOL.md)、[实验索引](repo:experiments/README.md)、[追溯脚本](repo:scripts/traceability.py)
