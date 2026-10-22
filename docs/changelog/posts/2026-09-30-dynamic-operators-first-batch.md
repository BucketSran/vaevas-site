---
date: 2026-09-30T18:58:00
categories:
  - EVAS
slug: dynamic-operators-first-batch
---

# EVAS 首批动态能力：多项式求解、cross、timer、transition、absdelay、slew、idt 与稀疏 LU

9 月 29–30 日合入 main 的 13 个 PR，把 EVAS 从只做静态求解推进到受限瞬态与事件（EVAS 0.3.2 / IR v3 → 0.9.0 / IR v11）；原 31 条件两档的有限观测达标由各 13/31（#15 四后端矩阵）升到各 21/31（#23），再到各 24/31（#26）。这些是开发证据，正式连续时间资格仍为 I。

<!-- more -->

## 做了什么

- **#6 静态多项式**：支持电压乘积和 1–32 次整数幂，用有界阻尼 Newton 求解，并复用矩阵分解（0.3.2 / IR v3）。
- **#7 / #10 cross 事件**：新增 `transient` 入口，在连续 PWL 输入、仿射电压网络上定位有方向的 cross；事件后电压和原支路残差验收通过才原子提交（0.4.5 / IR v4）。#10 补上零平台和 stop 恰为零时的到达规则（0.4.6）。
- **#12 timer**：固定参数 timer；同刻事件的状态与电压联立求解，独立前向误差认证后整批提交（0.5.3 / IR v5）。
- **#13 / #14 / #15 波形算子**：transition（固定延迟、显式上/下沿、中断，0.6.1 / IR v6）、固定 absdelay、固定限速 slew；三者的历史误差都计入电压预算，预算不够就拒绝并回退候选。
- **#18 语义回归**：贡献排列、重命名、观测方式不改变结果的回归，以及 idt 的候选数学契约；不改运行时。
- **#19 / #26 idt**：先支持 `idt(直接仿射输入, 常数初值)` 的分段解析积分（0.7.0 / IR v7），再支持三参数复位（IR v11，包版本仍为 0.9.0）。
- **#8 稀疏 LU**：未知量 n≥32 且非零项 ≤0.1mn 时走稀疏 LU，其余走稠密 LU；与事件、历史算子、idt 共用入口（0.7.1）。
- **#23 条件事件**：事件体 if/else 和扁平 `cross(...) or cross(...)`（0.9.0 / IR9）。
- **#25 多写者**：允许两个事件块在不同批次写同一状态（如迟滞模型）；同批两块写同一状态仍报 `event_conflict`。

## 结果与证据

- #15 重跑原 31 条件 × 四后端 × 两档共 248 单元：EVAS 两档各 13/31、18 条明确拒绝；Spectre 各 31/31；OpenVAF/ngspice 各 16/31；Gnucap 17/31 与 16/31。
- #15 slew 专项：EVAS 16/16、Spectre 10/16。Spectre 失败保留；只细化步长后反向追赶最大误差由 12.5 mV 降到 0.04883 mV，PR 不据此声称 Spectre 或 LRM 有错。
- #13 新执行 16 次 Spectre、16 次 EVAS，两后端均 16/16 满足有限观测判据。
- #23：每档 13→21，剩 10 条明确拒绝；同场景 Spectre 对照 EVAS 16/16、Spectre 15/16（`nearby-coarse` 两根相距 0.931 ns，粗步长下 Spectre 计 1 次，失败保留）。
- #26：124 次本地执行，两档由 22/31 升到 24/31（新增 D1 free/reset），原达标的 44 份 CSV 逐字节一致；279 项 Python、63 项 Rust 通过；无新 Spectre 执行。
- #6 性能：128 维仿射链每点 777.205 µs → 26.552 µs（29.27×），只测 Rust 库内重复求解，不是 Spectre 对比。
- 原始波形和日志只在本地或课题组服务器 保留，收据哈希不代表公开下载。

## 遗留与下一步

- #26 后剩 7 个条件明确拒绝；积分输入反馈、结构复位反馈、嵌套、积分驱动 cross 仍不支持。
- #12 遇到的 Spectre 21.1 重复赋值差异另由 [Issue #16](https://github.com/BucketSran/vaEVAS/issues/16) 跟踪，不复制为 EVAS 语义。
- 稀疏排序、填充等优化继续由 [Issue #9](https://github.com/BucketSran/vaEVAS/issues/9) 跟踪；#23 的任务与审阅顺序见 [Issue #22](https://github.com/BucketSran/vaEVAS/issues/22)。

## 相关链接

- [#6](https://github.com/BucketSran/vaEVAS/pull/6) 静态多项式 · [#7](https://github.com/BucketSran/vaEVAS/pull/7) cross 事件 · [#10](https://github.com/BucketSran/vaEVAS/pull/10) cross 零平台与 stop
- [#12](https://github.com/BucketSran/vaEVAS/pull/12) timer · [#13](https://github.com/BucketSran/vaEVAS/pull/13) transition · [#14](https://github.com/BucketSran/vaEVAS/pull/14) absdelay · [#15](https://github.com/BucketSran/vaEVAS/pull/15) slew
- [#18](https://github.com/BucketSran/vaEVAS/pull/18) 语义回归 · [#19](https://github.com/BucketSran/vaEVAS/pull/19) idt · [#26](https://github.com/BucketSran/vaEVAS/pull/26) idt 复位
- [#8](https://github.com/BucketSran/vaEVAS/pull/8) 稀疏 LU · [#23](https://github.com/BucketSran/vaEVAS/pull/23) 条件事件与 cross OR · [#25](https://github.com/BucketSran/vaEVAS/pull/25) 事件多写者
- 当前手册：[事件数学](repo:evas/docs/math/events.md)、[算子数学](repo:evas/docs/math/operators.md)、[动态契约](repo:evas/validation/DYNAMICS_CONTRACTS.md)
