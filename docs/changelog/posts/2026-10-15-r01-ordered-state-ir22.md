---
date: 2026-10-15T04:16:00
categories:
  - EVAS
slug: r01-ordered-state-ir22
---

# EVAS 补齐 R01 采样请求所需的有序状态、事件数组与增益统计（IR21–IR22）

10-14 至 10-15 凌晨，8 个 PR 合入 main。合入后，R01 的原 `timing-0` 请求和三条 gain 测量请求能在原 120 秒限制内跑完，并通过原 checker。按 #178 的记录，main `efd17ed6` 的工程重放有 23/70 条通过原 checker，此前为 12/70。这是开发重放，不新增论文 Q 成绩。

<!-- more -->

## 做了什么

- [#171](https://github.com/BucketSran/vaEVAS/pull/171)：修复两处错误接受。零次循环里引用未声明节点，以前会被接受，现在编译时拒绝。动态 timer 被改到当前时刻时，以前会漏掉回调却仍报告成功，现在明确返回 `event_resolution`。
- [#172](https://github.com/BucketSran/vaEVAS/pull/172)：显式包含 `constants.vams` 后，可以使用 14 个 VAMS 数学常量。只声明、从未引用的私有 electrical 节点不再导致奇异电压系统。
- [#173](https://github.com/BucketSran/vaEVAS/pull/173)：固定 `timer(0)` 改变保持量时，transition 等历史改用零时刻事件之后的最终状态初始化，不再产生本不应有的初始边沿。
- [#174](https://github.com/BucketSran/vaEVAS/pull/174)：发布 EVAS 0.17.0 / IR21，加入有序初始化、有界整数循环、`$display` / `final_step` 等共用机制。试算状态、历史和输出记录在认证通过后一起提交。
- [#175](https://github.com/BucketSran/vaEVAS/pull/175)：有界的事件数组下标和由参数选择的分支可以编译。结构上隔离的测量回调，在同一认证时刻的物理结算之后执行。
- [#177](https://github.com/BucketSran/vaEVAS/pull/177)：原 `r01-measure-interleaved-time/timing-0` 请求在原 120 秒限制内用时 111.99 秒，输出 9001 行。冻结的原 checker 通过。
- [#178](https://github.com/BucketSran/vaEVAS/pull/178)（文档）：在对比表现有各层补充工程程序中缺的能力要求，行顺序和成绩不变。
- [#179](https://github.com/BucketSran/vaEVAS/pull/179)：源码版本升至 0.18.0 / IR22。隔离的观察事件可以执行乘积、变量除法和 sqrt/abs/min/max，三条原 gain 请求能完整运行。

## 结果与证据

- #171：选定的 Python 回归 212 项和 Rust 全量 257 项通过（另有 1 项原本就忽略的测试）。5 个实际 Spectre 对照保留了同源输入和查询值。
- #173：三份同源模型共 42 个原生配对值满足原 `1e-8 V` 门槛，与 Spectre 的最大差为 `3.11e-15 V`。
- #174：Python 1486 项通过，Rust 291 项通过（1 项忽略）。实际 Spectre 对照中，基础控制 7/7、初始化控制 3/3 通过。重跑受影响的 16 条原请求：12 条完整运行并通过原 checker，4 条仍按联合非仿射拒绝；新增完成 0 条，丢失 0 条。
- #175：17/17 个有限控制在原 1e-9 V 门槛内与 Spectre 原生采样一致。16 条受影响原请求仍为 12 条完整运行。
- #177：291 个原有限配对点的最大电压差为 19.90 µV，低于原门槛 2 mV。完整 opt1 Python 1606 项通过，Rust 322 项通过（1 项忽略）。
- #178：main `efd17ed6` 的工程重放有 23/70 条通过原 checker，保住原来的 12 条，新增 11 条。按原 2 mV 判据，这个结果不授予新的 Q 等级，也不保证全域正确。
- #179：Python 1628 项和 Rust 325 项通过。原有限配对的最大差为 24.56 µV。重跑原 timing 三个条件，原 checker 3/3 通过。
- 各 PR 都写明：不证明全时域一致，不增加 Q 成绩；原 VA、刺激、精度预算和 checker 不变。

## 遗留与下一步

- #174 仍不支持动态数组下标、运行时循环和一般事件数学。70 条中另外 54 条当时没有在最终版本上重跑。
- #177 中 deadline 末点和 passive 邻位仍缺原生取证，完整资格分别为 0/6 和 0/2。#179 的 timing-1 输入配对未达标。
- #172 和 #173 的原请求仍分别被 ANSI 端口、`iabstol` 和 `&&` 等前端准入拦住。
- IR21、IR22 都要求从原 VA 重新编译，旧 IR 不会自动迁移。
- #171 至 #173 的 GLM 复核未完成。用户已取消把它作为合并门槛，PR 正文没有把它记为通过。
- 相关的长期需求 [#65](https://github.com/BucketSran/vaEVAS/issues/65)、[#66](https://github.com/BucketSran/vaEVAS/issues/66) 和 [#96](https://github.com/BucketSran/vaEVAS/issues/96) 保持开放。

## 相关链接

- PR：[#171](https://github.com/BucketSran/vaEVAS/pull/171)、[#172](https://github.com/BucketSran/vaEVAS/pull/172)、[#173](https://github.com/BucketSran/vaEVAS/pull/173)、[#174](https://github.com/BucketSran/vaEVAS/pull/174)、[#175](https://github.com/BucketSran/vaEVAS/pull/175)、[#177](https://github.com/BucketSran/vaEVAS/pull/177)、[#178](https://github.com/BucketSran/vaEVAS/pull/178)、[#179](https://github.com/BucketSran/vaEVAS/pull/179)
- 证据：[保留的安全对照](repo:experiments/backends/support/retained-safety/README.md)、[前端保留项对照](repo:experiments/backends/support/frontend-retained/README.md)、[初始 transition 种子收据](repo:experiments/backends/support/20261014-initial-transition-seed.json)、[R01 基础控制](repo:experiments/backends/support/r01-root-windows/final-controls/README.md)、[测量回调对照](repo:experiments/backends/support/r01-timing-observers/README.md)、[因果时序对照](repo:experiments/backends/support/r01-causal-timing/README.md)、[增益统计收据](repo:experiments/backends/support/r01-event-statistics-summary.json)
- 前端准入契约：[frontend-admission.md](repo:evas/docs/reference/frontend-admission.md)
- 本地决策记录：`current/runs/evas-night-20261014/decisions.tsv`
