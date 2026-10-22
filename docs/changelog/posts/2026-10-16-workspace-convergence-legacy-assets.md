---
date: 2026-10-16T20:36:00
categories:
  - 项目
slug: workspace-convergence-legacy-assets
---

# 收敛工作区协作，把旧工作区里未交付的测试和文档并入 main

10-16，9 个 PR 合入 main，都不改变 EVAS 仿真行为。这一批明确了 `current` 为默认工作区、每个任务由一个主对话协调。旧夜间工作区里已审但未交付的回归、生成器、观察工具和文档并入主线。CI 收窄了历史收据检查并隔离测试 fixture，EVAS 开发者检查策略也移进本仓库。

<!-- more -->

## 做了什么

- [#190](https://github.com/BucketSran/vaEVAS/pull/190)：默认在 `current` 切换任务分支，每个任务或 benchmark 批次由一个主对话协调。通常最多三个活跃写入工作区：`current`，加 EVAS、benchmark 各一个。`check_workspaces.py --assets` 只读报告各工作区的独有提交、重复候选和处置建议。Python/Rust 开发测试和 Rust 实现改动，不再触发无关的数学与 checker 校准。
- [#191](https://github.com/BucketSran/vaEVAS/pull/191)：旧夜间工作区中的 9 项独立语义回归原样纳入主线 CI。
- [#192](https://github.com/BucketSran/vaEVAS/pull/192)：回收 timer 保持值/积分生成器、独立有理数答案、错误控制和失败缩减工具。现在运行时必须指定新的输出目录和非空、不重复的种子，原证据不会被覆盖。
- [#193](https://github.com/BucketSran/vaEVAS/pull/193)：回收观察证据工具、长序列回归和生命周期断言。观察工具区分保存值、插值和缺失记录，不输出行为通过判定。
- [#194](https://github.com/BucketSran/vaEVAS/pull/194)（文档）：补入 EVAS 0.15.0 / IR19 的 REA 边界诊断与原字节收据，登记 benchmark 候选 BC-0008，并为 CVDP 三个固定样例补写工程目标和验收缺口（仅静态分析）。
- [#195](https://github.com/BucketSran/vaEVAS/pull/195)：#194 那样的历史收据归档只做静态检查。`assess_tiers` 在一次输入快照内复用参考包络，各精度档仍分别判定。
- [#196](https://github.com/BucketSran/vaEVAS/pull/196)：CI 路由测试的临时仓库关闭提交签名，并使用空 hooks 目录。宿主机启用全局签名或 pre-commit 时，测试不再失败。
- [#197](https://github.com/BucketSran/vaEVAS/pull/197)：新增 `scripts/evas_check_policy.py`，EVAS 开发者检查策略和验证说明使用同一份来源，CI 检查生成表是否漂移。
- [#198](https://github.com/BucketSran/vaEVAS/pull/198)（文档）：更新 5 份 README 入口。IR 版本统一链接现有契约，历史矩阵与分项验收分开导航。

## 结果与证据

- #190：维护测试 114 项通过。实际资产报告核对了 33 个工作区，其中 18 个有隐藏索引标记，状态保持"未知"。
- #191：9 项原测试通过。CI [38835891556](https://github.com/BucketSran/vaEVAS/actions/runs/38835891556) 中完整 Python 1734 项通过。
- #192：21 项检查通过。最终 CI 中 Python 1755 项通过，零失败或错误。原工作区的 53 份源码和历史证据保全后，该工作区退出，分支保留。
- #193：55 项定向 Python 检查通过，新增的 1 项 Rust 生命周期测试通过。
- #195：本地同一正控路径的中位用时从 67.59 秒降到 33.05 秒。这是该路径的收益，不是模拟器或整体 CI 的加速比例。CI 中 Python 1812 项零失败。
- #196：28 项 CI 路由检查通过。最终 CI 的 10 个 job 全部成功。
- #197：与 Harness `5130584f` 中的旧策略对照，369 个路径场景下 738 个计划和 3,690 个验收状态一致。PR CI 的 10 个 job 全部通过，含 1,812 项 Python。
- 这一批没有改生产仿真代码，没有新增 Spectre 对齐或能力资格声明。

## 遗留与下一步

- #190：新的临时脚本如何接入证据防覆盖保护与校准，仍待后续决定。CI 热点优化继续暂缓。合并不会自动清理工作区。
- #192 至 #194：F30 继续冻结为未完成候选，稀疏投影等受阻成果作为保全候选保留。
- #194：REA 诊断只对应 0.15.0 / IR19，不宣称已在当前 IR23 上重验。
- #195：MCP 相关改动留给后续单独交付。
- #198：CDS/MUX 整题仍未验收。

## 相关链接

- PR：[#190](https://github.com/BucketSran/vaEVAS/pull/190)、[#191](https://github.com/BucketSran/vaEVAS/pull/191)、[#192](https://github.com/BucketSran/vaEVAS/pull/192)、[#193](https://github.com/BucketSran/vaEVAS/pull/193)、[#194](https://github.com/BucketSran/vaEVAS/pull/194)、[#195](https://github.com/BucketSran/vaEVAS/pull/195)、[#196](https://github.com/BucketSran/vaEVAS/pull/196)、[#197](https://github.com/BucketSran/vaEVAS/pull/197)、[#198](https://github.com/BucketSran/vaEVAS/pull/198)
- 仓库文件：[工作区复用与交接](repo:docs/contributing/workspaces.md)、[scripts/README.md](repo:scripts/README.md)、[check_workspaces.py](repo:scripts/check_workspaces.py)、[evas_check_policy.py](repo:scripts/evas_check_policy.py)
- 本地保全与审查记录：`current/runs/workspace-retirement-20261016/`
