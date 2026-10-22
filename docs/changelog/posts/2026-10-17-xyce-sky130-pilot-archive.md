---
date: 2026-10-17T20:35:00
categories:
  - EVAS
slug: xyce-sky130-pilot-archive
---

# 存档 sky130 采样器"真实晶体管网表 + 理想 VA 开关"在 Xyce/ngspice 下的联合仿真试点

PR209 已合入 main（合并提交 `378d3d62`），关闭 issue #200：同一份连续理想开关 VA 在 Xyce 7.10 和 ngspice 46 下都零改写编译并与 sky130 网表联合求解成功。结果只覆盖 tt 单点，原始波形为 local-only，不是公开可复现数据集。

<!-- more -->

## 做了什么

- 载体是 Arcadia-1/analog-design-bench 的 `sky130-bottom-plate-sampler-pvt`，其 gold 解用真实 MOS 开关。试点把两只输入采样管换成 39 行的连续理想开关 VA（tanh 压控电导，没有事件语义），其余网表不动。
- 归档内容：原 VA、网表、四象限指标、Docker 配方与 R1–R7 收据，以及立项调研。另保留 issue #138 首轮分析，并纠正了 Rust 微基准与完整 JSON 请求的计时边界。
- 审核后撤回了初稿中"非谐波谱底"的归因：对公开的 80 点样本做独立 DFT，ngspice/Xyce gold 的最大杂散分别是三次/二次谐波。BSIM4.5/4.6.1 版本告警只作为差异线索，没有证明是原因。
- 本轮没有新跑仿真，也没有改 gold、checker、精度或 EVAS 行为源码。

## 结果与证据

- 工具差（gold，tt 点，同容差）：SFDR 差 −1.9 dB，held sample 最大差 0.705 mV；ngspice 99.004 dB，Xyce 97.119 dB。
- VA 替换差：差分增益误差约 0.40% → 0.014%，Xyce 下 SFDR 97.119 → 108.646 dB；存储共模误差反向增加约 2.5 mV，仍低于 25 mV 判据。
- 容差敏感：ngspice + OpenVAF/OSDI 在宽容差下 SFDR 只有 73.564 dB，收紧到 reltol=1e-6 后为 106.745 dB。跨工具比较必须锁定容差。
- 试点说明原文："ngspice 与 Xyce 的 gold 基线均满足 bench 判据（ngspice 全 9 个 PVT 点 6/6 通过）"。
- 六份公开频谱独立复算一致；三份 ngspice 原 raw 的指标重提取与入库数据相同。Standards/Spec 独立审查完成；合并前与合并后 main CI 均通过。
- 外部 benchmark 的上游 commit 无法从任务副本恢复，记为 unknown。共模、功率、时间网格和日志的复算仍需本地原件（`current/runs/xyce-va-pilot-20261017/`）。

## 遗留与下一步

- 只做了 tt 单点，VA 列没有做 9 点 PVT 全矩阵；没有审计 BSIM4.5 与 4.6.1 的方程级差异；Xyce 收紧容差对照（reltol=1e-6）没有跑。
- 单次墙钟包含 Docker 启动，没有交替重复，不作为工具速度比较。
- 事件语义（cross/transition）接入属于 issue #181 的协议实验，当时仍开放；事件托管模式另见 #176。
- 外层 README 记录了之后在本地做的 Xyce/ngspice 速度复测和 Spectre 同源 TT 对照，这些均未提交发布。

## 相关链接

- [PR #209 experiment: archive sky130 VA-switch joint-simulation pilot (#200)](https://github.com/BucketSran/vaEVAS/pull/209)
- [Issue #200 试点：sky130 底板采样器 gold 解 + 理想 VA 开关在 Xyce 下的联合仿真链路](https://github.com/BucketSran/vaEVAS/issues/200)
- [Issue #181 Xyce 接入](https://github.com/BucketSran/vaEVAS/issues/181)、[Issue #176 ngspice 托管事件模型模式](https://github.com/BucketSran/vaEVAS/issues/176)
- [试点说明](repo:experiments/backends/xyce-va-pilot/README.md)、[R1–R7 收据](repo:experiments/backends/xyce-va-pilot/RECEIPTS.md)、[立项调研](repo:experiments/backends/xyce-va-pilot/2026-10-17-open-source-va-scs-joint-survey.md)
