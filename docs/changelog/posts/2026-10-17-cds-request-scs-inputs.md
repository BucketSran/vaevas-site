---
date: 2026-10-17T04:47:00
categories:
  - EVAS
slug: cds-request-scs-inputs
---

# EVAS 在原预算内跑完 R01 原 CDS 请求，并放宽三处 SCS/端口输入限制

四个 PR 已合入 main：R01 原 CDS0/1/2 请求在原 120 秒内核预算内完成，原 checker 与 Spectre 有限配对各 3/3；另外支持 `save time`、ANSI 逐端口声明和省略 delay 的 pulse。这些只移除了原请求的首个阻塞点，不是正式 benchmark 或新增 Q 成绩。

<!-- more -->

## 做了什么

- PR199（原 CDS 请求）：R01 原 CDS 请求在 `main@8c3ef9ee` 下会耗尽 120 秒内核预算。本次减少稀疏投影、状态恒等投影、精确源证明和只读模型复制中的重复工作，并修复同刻重入时根与完整窗口的配对、有限哨兵重置和 `min/max` 中时间来源的传递。原输入、输出网格、精度和超时都不改。
- PR203（SCS 保存）：`save time y u` 以前把 `time` 当成未知电压节点而拒绝整份网表。现在非节点的 `time` 使用已有时间轴，电压列保持请求顺序；真实存在的同名电气节点仍按电压保存。内核与 IR 未改。
- PR204（ANSI 端口）：模块头里逐端口写 `input/output/inout` 的 ANSI 写法以前在第一个方向词处被拒绝。现在归一化为已有端口元数据，复用原有绑定和 Rust 路径；重复声明、混合裸端口和范围外类型仍拒绝。
- PR206（pulse 缺省 delay）：线性 pulse 省略 `delay` 时以前在 SCS 准入阶段被拒绝。现在缺省 delay 取 0 s，其他六项仍须显式提供。

## 结果与证据

- CDS 三例（内核 / CLI 秒，内核上限 120 秒）：CDS0 104.39 / 114.10，CDS1 113.21 / 122.86，CDS2 115.38 / 125.73；原 checker 均通过，Spectre 有限配对 325、334、337 点通过。原六槽索引里三条 MUX 仍为 NOT_RUN，adapter 仍返回 1，不算全批通过。150 个构建源中 3 个与原验收字节有差异，已显式记录，没有在新字节上重跑原三例。
- `save time`：7 项回归；7 个 Spectre 正例共 21 个时间完全相同的原生配对点通过 10 nV 门槛。原 20 个请求均移除首阻塞，其中 269 完成并通过冻结旧 checker，19 项后续拒绝保留。
- ANSI 端口：5 个 Spectre 正例、2 个拒绝控制；25 个原生时间点电压差为 0。原 26 个请求中 001、047、089 完成并通过冻结旧 checker，23 项后续拒绝保留。
- pulse delay：22 个原生时间点电压差为 0；原 22 个请求的缺 delay 首阻塞均移除，但 18 项源不确定性组合、4 项编译/语法拒绝仍在，旧 checker 未运行。PR206 的 CI 中完整 Python 回归 1831 项，失败/错误/跳过均为 0。
- PR206 还补记一项收据限制：ANSI 26 项与 pulse 22 项本地回放的 worker 均返回 0 且未超时，但进程组清理遇到 PermissionError，收据标为 `cleanup_incomplete`。
- 四个 PR 的必需 CI 均通过；三个输入类 PR 都有新上下文的 Standards/Spec 独立审查，未留发现。原始输出与审查记录保留在本地 `current/runs/` 下，不作为公开数据集。

## 遗留与下一步

- PR199 关联 #65（控制流、结构与分析事件语义），不关闭其余语言缺口；MUX 及更广的语言组合仍开放。
- PR199 只证明原有限契约，没有新增 Q 等级或稳定加速倍数；CDS2 的 LTE 放宽告警保留。
- 三个输入类 PR 留下的后续拒绝（源不确定性组合、编译/语法拒绝等）需各自处理；F30、#131 保持原边界。

## 相关链接

- [PR #199 fix(evas): 完成原 CDS 请求并保留验收证据](https://github.com/BucketSran/vaEVAS/pull/199)
- [PR #203 fix(evas): preserve time axis and node voltages in SCS saves](https://github.com/BucketSran/vaEVAS/pull/203)
- [PR #204 feat(evas): accept explicit ANSI electrical ports](https://github.com/BucketSran/vaEVAS/pull/204)
- [PR #206 Default omitted SCS pulse delay to zero](https://github.com/BucketSran/vaEVAS/pull/206)
- [Issue #65](https://github.com/BucketSran/vaEVAS/issues/65)
- [CDS 验收说明](repo:experiments/backends/support/event-runtime-control/README.md)、[CDS 证据身份](repo:experiments/backends/support/event-runtime-control/cds-original-acceptance.json)
- [save time 合同与对照](repo:experiments/backends/support/scs-save-time/README.md)、[ANSI 端口合同](repo:experiments/backends/support/ansi-ports/README.md)、[pulse delay 合同](repo:experiments/backends/support/pulse-delay/README.md)
