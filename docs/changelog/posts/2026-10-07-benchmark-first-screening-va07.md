---
date: 2026-10-07T04:41:00
categories:
  - Benchmark
slug: benchmark-first-screening-va07
---

# benchmark 首批资产入库：六题初筛、VA07 判分修正与重放、ADC DNL/INL 新题

2026-10-04 至 10-07 合入 4 个 PR：六题内部初筛资产与冻结证据进入 main（首轮 Codex 6/6 任务、13/13 条件，GLM 3/6 任务、7/13 条件，只是一次生成的内部初筛结论）；VA07 区分行为零分与坏波形，并能在 EVAS 上按原八例条件重放；新增 ADC DNL/INL 测量任务。

<!-- more -->

## 做了什么

- #56：此前 main 只有 benchmark 占位说明。本 PR 把六个 Harbor 格式的内部初筛任务、共享评分源码和原始来源索引保存到 main，保留原 60 文件 manifest 和来源快照，补齐六题正校准与六个错误版本的紧凑证据，新增身份工具和 CI 身份/汇总检查。同时修复汇总工具漏算普通 Codex job 的问题。关闭 #51–#54。
- #87：VA07 的完整负例波形原先因计数检查抛错而丢失摘要，Harness 把应有的零分当成未分类失败。现在"完整波形 + 行为错误"记为 graded、reward=0；"缺失/损坏/不完整波形"记为 checker_error、reward=null。原八例、参考解、容差和分母不变。
- #88：保存候选此前只能走 VA07 单例开发 adapter。本 PR 增加完整八例映射、独立采样判分、固定包 builder 和离线镜像配方，接入 Harness 的 saved-candidate replay。
- #94：新增 ADC DNL/INL 测量任务：候选用 Verilog-A 驱动 8 位 ADC 完成 4096 次读取，交付内部 254 码的 DNL/INL 和逐次 `samples.csv`；checker 核对激励、时钟、完成信号、原始 ADC 总线和全部读取记录。

## 结果与证据

- #56：用维护后的汇总工具重分析归档，12 份提交、成绩、渠道故障和人工诊断与原最终报告一致；没有新增模型调用或 Spectre 仿真，也没有修改 EVAS。
- #87：新 checker 的真实 Spectre 21.1 八配置终评，参考解 score=1，原 wrong-speed 候选 score=0。
- #88：最终实现 `9f13fc6d` 重跑三个候选：参考解 8/8、GLM 保存候选 8/8，wrong-speed 有 6 项判错、2 项端点不可评，整题未评分。汇总为 extension 集 3 个候选：2 match、1 unevaluable；不可评样本没有删除或折算为零分。使用的是固定旧版 EVAS `d06581f9`，不代表当时 main 的全部支持范围。
- #94：四个参考场景真实运行通过，六个错误版本被拒绝；Harbor 0.23 oracle Trial 四场景 reward=1。两次 instruction-only 模型尝试中，Codex 候选缺 served-model 身份未评分，GLM 得 0 分；这不证明模型端到端能力或题目难度。见 [校准报告](repo:experiments/adc_linearity/CALIBRATION-20261007.md)。
- 原始模型输出、波形和审查材料为 local-only。

## 遗留与下一步

- #56 的材料只支持六题、一次生成的内部初筛结论；历史报告的 Spectre 版本字段为空；第三方源码及派生任务的外发许可尚未确认。
- #88：合法的近边界候选也可能未决；已知端点求解失败归 EVAS #70 / PR #79 跟踪。
- #94：后续真实 Agent 流程与任务效果由 #72 管理。

## 相关链接

- PR：[#56](https://github.com/BucketSran/vaEVAS/pull/56)、[#87](https://github.com/BucketSran/vaEVAS/pull/87)、[#88](https://github.com/BucketSran/vaEVAS/pull/88)、[#94](https://github.com/BucketSran/vaEVAS/pull/94)
- Issue：[#51](https://github.com/BucketSran/vaEVAS/issues/51)、[#52](https://github.com/BucketSran/vaEVAS/issues/52)、[#53](https://github.com/BucketSran/vaEVAS/issues/53)、[#54](https://github.com/BucketSran/vaEVAS/issues/54)、[#70](https://github.com/BucketSran/vaEVAS/issues/70)、[#72](https://github.com/BucketSran/vaEVAS/issues/72)；Harness [#4](https://github.com/BucketSran/AlphaApollo-Chips/issues/4)、[#7](https://github.com/BucketSran/AlphaApollo-Chips/issues/7)
- 仓库：[六题初筛工具](repo:experiments/va_screen)、[ADC 线性度校准](repo:experiments/adc_linearity/CALIBRATION-20261007.md)
