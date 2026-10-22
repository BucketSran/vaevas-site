---
date: 2026-10-09
categories:
  - EVAS
slug: precision-event-alignment-issue-closure
---

# EVAS 精度与事件历史对齐检查点合入，并收口一批语言与诊断缺口

2026-10-08 至 10-09 合入 12 个 PR。核心是 #108：用户明确选择"允许合入 #108 检查点，保留缺口"，以有限范围的开发检查点合入连续精度、事件与历史组合和 strobe 控制；其余 PR 补齐输入相关初值、scalar case、transition 默认 fall 时间等有限能力，并把开发基线整理为 EVAS 0.14.0 / IR18。

<!-- more -->

## 做了什么

- #108：交付连续精度、事件与历史组合、编译准入、观察证据、cross 可移植性提示，以及 API/manifest 的五项 strobe 控制（强制求解时刻）。固定 head `bbda9edd`。
- #118：把这五项 strobe 控制接入受限 `.scs`，并整理 EVAS 0.14.0 / IR18 开发基线。
- #117：事件批次改为"先准备完整候选、全部检查通过后一次发布"的结构，属于保持行为的重构。
- #101：`initial_step` 可按实际输入比较设置初态，两个异刻事件块可共同自增/自减计数器；Python/Rust IR 同步为 18，包版本 0.14.0（未发布 tag）。
- #109：标量 `case/default` 降为已有条件 IR；对非有限运算、状态范围拒绝和 worker 失败分类；ADR-002 记录共享状态、事件和误差契约。
- #111：区分普通 analog 局部量与持久事件状态，不再要求临时变量也用 `initial_step` 初始化。
- #112：`transition(x,delay,rise)` 省略 fall 时取 rise；#114：transition 不支持的时序边界给出明确拒绝码。
- #115：初始化事件中的静态 for 循环可初始化持久数组。
- #110：证据工具按"归档身份 → 归档文件 → 当前解压字节"只读核验，堵住空 manifest 或替换 PSF 绕过来源检查的漏洞。
- #116：论文条件和判据的既有校准加入 CI，并保存 #108 的固定候选对照；#113：把 ADR-002 未完成的实现逐项交接到 #96、#66、#70。

## 结果与证据

- #108 的 `bbda9edd` 五项 CI 全部成功；最近增量的 Spectre 21.1.0.509.isr12 四例共 12 个内部强制点满足冻结的 1 µV 预算，两处 t=0 缺失仍为 I。
- #118：四个相同 VA 模型经新 `.scs` 接口执行，12 个内部强制点对冻结 Spectre 波形满足原 1 µV 预算，最大差约 41.0 nV，没有新增远端仿真。
- #101：八例 Spectre 开发配对在预先固定的有限观测预算内符合独立答案；最终完整 Python 853 项、Rust 153 项（1 项 ignored）通过。这不是一般初始化能力保证。
- #109：五个 DC 输入下 90 个必需标量和 160 个原生网格标量与 Spectre 在 1e-8 V 预算内完全一致，只证明该有限 DC 对照。
- #111：Spectre 同源对照 67 个原生时刻、737 个电压配对满足预算；#115：原 stop=1 请求 80 行 / 720 个电压配对通过；两者的精确终点覆盖仍为 I。
- #116 保存的候选证据含 24 个 EVAS 请求与 12 份 Spectre 参考的 410,908 对观察，不是 main 支持或论文 P。
- #117：Rust 218 通过、1 忽略；251 项 Python 测试覆盖 706 个请求，输出与重构前逐字节相同。

## 遗留与下一步

- #108 未关闭：原 C1 精确观察阶段、#79 的 stop=3 计数、VCO 原 22 点、M1 参考稳定资格；论文 48 槽与 Spec B 历史结果保留原执行身份。
- `.scs` 的 strobeoutput 和局部因果闭包强制点仍不支持（#118）。
- #65 的其余语言需求、#96 等能力 issue 继续开放；#62 设计项在文档交接后关闭。
- 原始波形和审查记录为 local-only，部分在 `current/runs/issue-closure-20261008/`。

## 相关链接

- PR：[#101](https://github.com/BucketSran/vaEVAS/pull/101)、[#108](https://github.com/BucketSran/vaEVAS/pull/108)、[#109](https://github.com/BucketSran/vaEVAS/pull/109)、[#110](https://github.com/BucketSran/vaEVAS/pull/110)、[#111](https://github.com/BucketSran/vaEVAS/pull/111)、[#112](https://github.com/BucketSran/vaEVAS/pull/112)、[#113](https://github.com/BucketSran/vaEVAS/pull/113)、[#114](https://github.com/BucketSran/vaEVAS/pull/114)、[#115](https://github.com/BucketSran/vaEVAS/pull/115)、[#116](https://github.com/BucketSran/vaEVAS/pull/116)、[#117](https://github.com/BucketSran/vaEVAS/pull/117)、[#118](https://github.com/BucketSran/vaEVAS/pull/118)；未合入的 [#79](https://github.com/BucketSran/vaEVAS/pull/79)
- Issue：[#62](https://github.com/BucketSran/vaEVAS/issues/62)、[#65](https://github.com/BucketSran/vaEVAS/issues/65)、[#66](https://github.com/BucketSran/vaEVAS/issues/66)、[#70](https://github.com/BucketSran/vaEVAS/issues/70)、[#96](https://github.com/BucketSran/vaEVAS/issues/96)
- 仓库：[ADR 记录](repo:evas/docs/development/DECISIONS.md)、[strobe 参考](repo:evas/docs/reference/strobe.md)、[strobe 对照](repo:experiments/backends/strobe/README.md)、[输入初始化证据](repo:experiments/backends/input-initialization/README.md)、[case 对照](repo:experiments/backends/case-statements/README.md)、[事件验收记录](repo:experiments/backends/event-acceptance/README.md)
