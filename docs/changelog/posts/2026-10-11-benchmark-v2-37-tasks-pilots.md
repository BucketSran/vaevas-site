---
date: 2026-10-11T11:27:00
categories:
  - Benchmark
slug: benchmark-v2-37-tasks-pilots
---

# benchmark v2：固定后端判分运行时、37 道 Harbor 任务与 148 个模型试做单元

三个 PR 已合入 main：先建好"冻结候选 → 固定 Spectre 用例 → 独立 checker"的判分运行时和模型试做入口，再交付五类 v2 spec 的 37 道任务。148 个模型试做终态单元中 Agentic 48/74、one-shot 38/74 通过；这是两个模型的 pilot 结果，全部 37 题是 Spectre 扩展集，未声称 EVAS/ngspice 同题复现。

<!-- more -->

## 做了什么

- 判分运行时（PR140）：为 spec #133–#137 加固定后端 verifier。候选 VA 原字节执行；完整的独立波形判定给 0/1，编译器、后端、缺证据和 checker 失败不计分、留作诊断。未改 EVAS。
- 公开材料冻结与试做入口（PR142）：封存公开材料与候选身份，Agentic 用 Harbor/Pi 运行，one-shot 用单次无工具请求。Agent 只拿到题面和公开目录；支持 Spectre include 与 SPICE `.include/.inc/.lib` 引用并保存网表 SHA。模型启动前的 DNS 或依赖安装失败记为环境失败，不算模型零分。
- 37 道任务（PR145）：五类 v2 spec 的 32 个 P1 来源加 5 个额外必做代表，建成 37 道 Harbor 任务。每题有公开工程材料、修改边界、参考解、其他正确实现、工程语义错版和独立 checker；所有任务权重为 1。

## 结果与证据

- PR140 作者校准（实际 Spectre `21.1.0.509.isr12`）保留全部十次参考运行：五题各条件通过，两题暴露作者行为错误，三题是不计分的作者编译失败。PR 正文说明这是运行时证据，不代表 spec 完成。
- PR142 本地验证 36 项通过；17 个公开作者探针实际 Spectre 均 rc0。公开探针只验证部署，不构成模型成绩。
- PR145 按类型的试做结果（Agentic / one-shot 通过数 / 全部）：

| 类型 | 任务数 | Agentic | one-shot |
| --- | ---: | ---: | ---: |
| 按规格建模 | 19 | 24/38 | 19/38 |
| 从数据建模 | 1 | 0/2 | 0/2 |
| 扩展与集成 | 2 | 0/4 | 0/4 |
| 诊断与修复 | 5 | 10/10 | 8/10 |
| 测试与表征 | 10 | 14/20 | 11/20 |

- 未提交、非法 VA、上下文拒绝、格式失败与原因未知保留为 null，不并入电气错误；不选 best-of。
- 作者校准覆盖 179 个登记变体、584 个条件位置：79 个正确实现通过，100 个语义错版被拒绝。正式 Harbor 参考入口完成 37 个 stock Oracle Trial 及 111 个私有条件。作者校准、参考入口和模型成绩不互相代替。
- 审查中补清十一题的公式、初态、电平或时限，相应题用新版公开材料重新试做；308 题 one-shot 因私有激励补强从旧 6/6 变为 5/6，未放宽 checker。
- 证据入口：[运行时校准收据](repo:experiments/benchmark_v2/runtime-calibration.json)、[五规格验收](repo:experiments/benchmark_v2/spec-delivery.md)、[模型试做报告](repo:experiments/benchmark_v2/model_pilots/model-pilot-results.md)、[质量分析](repo:experiments/benchmark_v2/model_pilots/model-quality.md)、[作者校准](repo:experiments/benchmark_v2/author-calibration-private-overlays.md)、[Harbor 参考入口验收](repo:experiments/benchmark_v2/harbor_reference/harbor-reference-acceptance.md)。原始波形、轨迹和部署配置留在本地。

## 遗留与下一步

- verifier 不是进程沙箱，Agent 提交依赖另行验证的 circuit-harness 隔离部署。
- Agentic 单次输出上限 16384、one-shot 为 32000，推理与早期安装历史也不同，不能解读为同等计算预算下工具的独立收益。
- 从数据建模、扩展与集成及 POR 本轮没有可评分候选，这些电路能力仍未知。
- PR145 只关闭五份实施 spec（#133–#137）；父议题 #107、#72 及 circuit-harness#5 继续开放。

## 相关链接

- [PR140 v2 固定后端判分运行时](https://github.com/BucketSran/vaEVAS/pull/140)
- [PR142 冻结公开材料与模型试做提交](https://github.com/BucketSran/vaEVAS/pull/142)
- [PR145 五份 v2 spec、37 题与 148 个模型试做](https://github.com/BucketSran/vaEVAS/pull/145)
- Spec：[#133](https://github.com/BucketSran/vaEVAS/issues/133)、[#134](https://github.com/BucketSran/vaEVAS/issues/134)、[#135](https://github.com/BucketSran/vaEVAS/issues/135)、[#136](https://github.com/BucketSran/vaEVAS/issues/136)、[#137](https://github.com/BucketSran/vaEVAS/issues/137)
- 父议题：[#107](https://github.com/BucketSran/vaEVAS/issues/107)、[#72](https://github.com/BucketSran/vaEVAS/issues/72)
