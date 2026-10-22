---
date: 2026-10-11T16:29:00
categories:
  - EVAS
slug: evas-issue-followup-oct11
---

# EVAS 收口一批遗留拒绝：timer 停止边界、两级 slew、多项式滤波直通与近邻 timer strobe

五个 PR 已合入 main：原来被拒绝的四类合法写法（timer 越过 stop、两级固定 slew、外部多项式输入的滤波、近邻 timer 的 strobe）现在能跑完并通过原验收，支持表也按 main `fc7e57fd` 重填。PR157 复验时 21 个固定条件、74 个配置全部通过原判据，这些都是开发集的有限观测，不是全时域证明。

<!-- more -->

## 做了什么

- timer 停止边界（PR139）：周期采样→保持→transition→滤波链在 `stop=4e-6` 被 `event_resolution` 拒绝；现在 timer 包围跨过 stop 时精确比较 `start+k*period`，原模型完成第 4 次采样。
- 两级固定 slew（PR143）：完成 #66 的 C3 切片。第二级读取第一级完整分段历史，交点用有理数表示，输入误差传到最终电压验收。
- 多项式滤波直通（PR144）：修复 #66 原 C4 模型 `laplace_nd(pow(V(u,r),2), ...)` 被"必须严格真有理"拒绝的问题；输入非线性项只依赖外部源和常量时，保留多项式直接通路并检查原方程和输出误差。
- 近邻 timer strobe（PR146）：近邻 timer（例如 `.3` 与 `.1+.2`）原先会跨过请求的 strobe 后拒绝输出；调度器现在先在强制点完成事件与历史检查，并证明下一个事件在其后。同时补齐 #64 的非阻断 timer、额外 strobe 和 `idtmod` 源码提示，提示协议升到 v2（错误诊断仍为 v1）。
- 支持表重填（PR157）：旧表把实验版本和当前版本混在一起；现按 main `fc7e57fd` 重填精度与工程组合表，未重跑的历史结果单列，解释 0.14.0 与 IR18 的含义。只改文档与紧凑证据。

## 结果与证据

- PR139：原停止边界测试 12 个子情况中 10 个报错，修复后通过。实际 Spectre 21.1 两档 6,102 个原生时刻：基础档最大滤波误差 751 nV（原失败保留），收紧档 30.7 nV 满足原预算；EVAS 两档通过。
- PR143：实际 Spectre 21.1 共 3 模型、8 配置、185,999 个原生时刻；原 1 µV 标准下 EVAS 8P，Spectre 5P/3F，超差配置全部保留。
- PR144：实际 Spectre 21.1 共六配置、14,014 个原生时刻；原 1 µV 标准下 EVAS 6P，Spectre/配对 5P/1F，反向基础档 5.96 µV 失败保留。
- PR139/143/144 按顺序合入，最终整合头 `6cf715c3` 本地 99 项相关 Python、230 项 Rust 核心和 2 项桥接测试通过；16 个配置共 206,115 个原生观测点重新验收。三者都复用原 Spectre 记录重跑 EVAS，没有新跑远端。
- PR146：Spectre 21.1.0.509.isr12 三模型各四档，EVAS 12/12；Spectre 固定/保持时钟 8/8，连续组合 2/4。最终提交 `8d184d17` 五项 CI 通过，外部 Circuit Harness #6 同步合入。
- PR157：当前构建执行 21 个固定条件、74 个配置，从原始输出重新判分全部通过原判据；核验 648 个归档工件身份。
- 证据入口：[timer/滤波边界](repo:experiments/backends/sample-edge-filter/BOUNDARY.md)、[两级 slew 对照](repo:experiments/backends/slew-cascade/README.md)、[滤波直通对照](repo:experiments/backends/filter-direct/README.md)、[strobe 实证](repo:experiments/backends/strobe/README.md)、[诊断来源](repo:evas/docs/development/diagnostic-sources.md)、[支持复验记录](repo:experiments/backends/support/README.md)、[支持表](repo:evas/docs/COMPARISON.md)。原始数据在本地 `current/runs/evas-backlog-20261011/`、`current/runs/near-timer-strobe-20261011/`。

## 遗留与下一步

- 保持状态 timer、近邻强制点、任意近邻事件和连续局部历史的原限制仍在；不代表旧 C1、#79、VCO、Spec B 的严格差异已解决。
- slew 的第三层、动态限速、混合算子、反馈仍不支持；滤波的内部非线性反馈、事件状态和事件组合仍拒绝。#66 保持开放。
- 只解析提示 v1 的外部消费者需要更新到 v2。
- #96、#119 的其余缺口另行跟踪；草稿 PR #131（采样 transition-滤波历史上的 cross 回调）未动。

## 相关链接

- [PR139 修复固定 timer 停止边界拒绝](https://github.com/BucketSran/vaEVAS/pull/139)
- [PR143 两级固定 slew 的完整历史与 Spectre 对照](https://github.com/BucketSran/vaEVAS/pull/143)
- [PR144 外部多项式滤波直通](https://github.com/BucketSran/vaEVAS/pull/144)
- [PR146 近邻 timer strobe 与诊断验收](https://github.com/BucketSran/vaEVAS/pull/146)
- [PR157 更新当前 main 支持表与复验证据](https://github.com/BucketSran/vaEVAS/pull/157)
- Issue：[#66](https://github.com/BucketSran/vaEVAS/issues/66)、[#64](https://github.com/BucketSran/vaEVAS/issues/64)、[#96](https://github.com/BucketSran/vaEVAS/issues/96)、[#119](https://github.com/BucketSran/vaEVAS/issues/119)
- [Circuit Harness PR6](https://github.com/BucketSran/circuit-harness/pull/6)
