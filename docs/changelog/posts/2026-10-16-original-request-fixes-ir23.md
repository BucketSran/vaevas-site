---
date: 2026-10-16T08:56:00
categories:
  - EVAS
slug: original-request-fixes-ir23
---

# EVAS 按原始工程请求修补同步读出、滤波、SCS 输入与观察循环（IR23）

10-15 至 10-16 上午，9 个 PR 合入 main，处理原始工程请求暴露的拒绝和超时，EVAS 源码版本升到 0.19.0 / IR23。原物理同步请求在原 120 秒限制内用时 76.13 秒、输出 9001 行，但整题原 checker 仍然失败。原 CDS/MUX 请求也仍未完成，这一批不新增 Q 成绩。

<!-- more -->

## 做了什么

- [#180](https://github.com/BucketSran/vaEVAS/pull/180)：物理同步请求的连续读出改用当前电压。显式 ODE 先尝试较低阶数，每次仍检查原误差预算，并保留高阶退路。
- [#182](https://github.com/BucketSran/vaEVAS/pull/182)：外部 PWL 仿射系数乘以单个保持状态驱动的 transition 后，可以进入一阶滤波。计算按输入折点和中断边沿分段，滤波历史连续保留。
- [#183](https://github.com/BucketSran/vaEVAS/pull/183)：SCS 保存的波形加入落在常规输出点之间的源折点，窄脉冲不再被存成平线。
- [#184](https://github.com/BucketSran/vaEVAS/pull/184)：有限线性脉冲的折点保留原始有理时间，并带着已证明的电压误差界向下游传递。同时支持 SCS 的 `strobeoutput=all` 和 `strobeonly` 两种保存策略。
- [#185](https://github.com/BucketSran/vaEVAS/pull/185)：隐式多项式 DAE 积分遵守与模型相关的 `$bound_step`，不再在构造轨迹前直接拒绝。
- [#186](https://github.com/BucketSran/vaEVAS/pull/186)：`initial_step` 读取另一实例的电压时，按依赖关系解析零时刻状态，联立认证后一次提交。
- [#187](https://github.com/BucketSran/vaEVAS/pull/187)：固定且精确的 timer 可以改变 forcing 和模型步长，积分、滤波状态和代数分支坐标保留。
- [#188](https://github.com/BucketSran/vaEVAS/pull/188)：在隔离的测量回调和 `final_step` 中，可以执行有界的状态控制循环和带检查的数组。嵌套循环共用原有的 4096 次迭代预算。Python 与 Rust 一起升到 0.19.0 / IR23。
- [#189](https://github.com/BucketSran/vaEVAS/pull/189)：接受 `transition(q-2*(q<2?0:1),0,0.25,0.25)` 这类在保持目标上做条件算术的写法。隐藏的非线性和电压反馈仍然拒绝。

## 结果与证据

- #180：四路保持电压满足原要求。与实际 Spectre 的原有限配对最大差为 29.56 µV。**整题原 checker 仍失败**：模型在 cross 回调里再次用严格大于号，EVAS 在根时刻回调，Spectre 的实际回调约晚 0.0501 fs，两边得到的状态不同。最终 CI：Python 1650 项、Rust 核心 343 项通过（1 项忽略）。
- #182：普通卡 395 点、中断卡 399 点通过数值和状态检查。滤波输出与 Spectre 的差分别为 25.68 nV 和 6.90 nV，低于原门槛 101 nV。
- #183：6 个原生时间点上，EVAS 与 Spectre 的输入和输出 binary64 值完全相同。零时刻不在这次配对范围内。
- #184：5 个保存策略对照全部通过。脉冲对照有 5 个精确原生配对，最大差 1.431 µV，门槛为 10 µV。
- #185：两个冻结案例保留全部 33 个原生点，最大配对差为 2.95 nV 和 0.735 nV，门槛为 100 nV。
- #186：三例的全部原生点和 5 个共同强制点满足原 1 nV 门槛。
- #187：9 个原生点（含 0、事件点和 stop）最大配对差为 62.41 nV，门槛为 100 nV。
- #188：Rust 360 项通过（1 项忽略），另有 2 项 IR 测试通过。3 个实际 Spectre 控制满足原 100 nV 要求。
- #189：Rust 357 项、相关 Python 112 项通过。Spectre 参考的 v3 配置在 16 个精确时刻全部保存，EVAS 在每个共同时刻一致。

## 遗留与下一步

- 原物理同步请求的整题 checker 仍失败。这一失败、valid/dout 差异和历史成绩都原样保留。
- #183、#184、#185 都写明：最终集成版本对原 70 条请求的重放仍待完成。
- #184：非零源不确定性与算子、cross、held timer 组合时仍明确不支持。Spectre 漏存了部分相邻浮点 strobe 时间，因此不声称完整导出资格。
- #187：代数约束跳参、cross、held timer、非精确窗口、reset 和 `ddt` 仍然拒绝。
- IR23 要求编译器和内核版本匹配，旧格式不会被静默迁移。0.19.0 只是源码开发版本，没有发布到 PyPI，也没有打 tag。
- 原 CDS/MUX 请求仍未完成；#189 时 MUX 的 checker 仍是 NOT_RUN。相关 issue [#65](https://github.com/BucketSran/vaEVAS/issues/65)、[#66](https://github.com/BucketSran/vaEVAS/issues/66)、[#96](https://github.com/BucketSran/vaEVAS/issues/96) 和 [#119](https://github.com/BucketSran/vaEVAS/issues/119) 没有因这批修复关闭；#183 和 #184 写明它们是 [#63](https://github.com/BucketSran/vaEVAS/issues/63) 的剩余项之一。

## 相关链接

- PR：[#180](https://github.com/BucketSran/vaEVAS/pull/180)、[#182](https://github.com/BucketSran/vaEVAS/pull/182)、[#183](https://github.com/BucketSran/vaEVAS/pull/183)、[#184](https://github.com/BucketSran/vaEVAS/pull/184)、[#185](https://github.com/BucketSran/vaEVAS/pull/185)、[#186](https://github.com/BucketSran/vaEVAS/pull/186)、[#187](https://github.com/BucketSran/vaEVAS/pull/187)、[#188](https://github.com/BucketSran/vaEVAS/pull/188)、[#189](https://github.com/BucketSran/vaEVAS/pull/189)
- 证据：[同步读出与滤波](repo:experiments/backends/support/r01-sync-readout/README.md)、[SCS 源折点保存](repo:experiments/backends/support/scs-source-observation/README.md)、[源误差与 strobe 保存](repo:experiments/backends/support/scs-source-uncertainty/README.md)、[隐式步长界](repo:experiments/backends/implicit-step-bounds/README.md)、[零时刻电压依赖](repo:experiments/backends/support/initial-node-dependencies/README.md)、[隐式状态跨 timer](repo:experiments/backends/implicit-event-restart/README.md)、[保持目标算术](repo:experiments/backends/support/held-transition-targets/README.md)
