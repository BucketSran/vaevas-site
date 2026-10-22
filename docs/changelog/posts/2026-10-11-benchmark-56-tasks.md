---
date: 2026-10-11T16:42:00
categories:
  - Benchmark
slug: benchmark-56-tasks
---

# benchmark 新增 19 道任务并统一为 56 题总览

六个 PR 已合入 main：按五份"下一批"设计 issue 新建 19 道 Harbor 任务（CTLE/滤波/RF、DAC/ADC、OTA、LDO、分数 PLL 与持续校准），再把它们和此前 37 题合并成按工程动作和电路功能分组的 56 题总览。新 19 题只有作者校准，没有做模型解题实验，固定评分后端为 Spectre，开源同题等价未验证。

<!-- more -->

## 做了什么

- CTLE、滤波与 RF 测量（PR152，#149）：五道题，覆盖一零点两极点 CTLE、可编程低通扩展、I/Q 上下变频与动态包络、实际扫频与幅相测量。
- DAC 合同与 ADC 测量（PR153，#151）：六道题，覆盖分段/温度计/非理想位权/亚基数 DAC、实际 DAC 端点扫描、VA 中计算相干 ADC 指标（DNL/INL、SNDR、SFDR、ENOB）。
- OTA 动态与真实电路数据建模（PR154，#147）：三道题，其中 A2 用 JKU 34 MOS OTA 的六条实际源轨迹，三条训练、三条留出。
- 真实 LDO 启动与响应驱动表征（PR155，#148）：两道题，基于固定 ADB OTA5 LDO 与 SKY130 模型，记录许可证和格式适配。
- 分数 PLL 与持续校准（PR156，#150）：三道扩展与集成题，DCO 与前端固定在题目环境里，候选必须通过控制端改变实际电路响应。
- 56 题总览（PR158）：原入口仍以 18 张早期设计卡为主；新增总览按五类工程动作和 10 个电路功能组整理两批任务，37 + 19 题的类别合计为 27 / 2 / 6 / 5 / 16。题目、参考解和 checker 未修改。
- PR152–156 正文写的是"等待用户审核，不合并 main"；按 PR158 正文，这五个 PR 在 PR158 之前已合并。

## 结果与证据

- PR152：26 个作者候选、58 个实际 Spectre 条件；10 个参考/正确替代实现的 22 个条件全部通过，16 种语义错版全部在至少一个条件被检出；36 个负例条件中 32 个拒绝、4 个通过，全部保留。
- PR153：34 个作者变体、56 个最终执行位置；12 个正确实现的 34 个位置全部通过，22 个编译成功的语义错版在预登记目标条件上被拒绝。
- PR154：19 个作者变体、57 个最终条件；6 个正确实现的 18 条件全部通过，39 个负条件中 38 个拒绝；真实源电路在 ngspice/IHP PSP103 下运行。
- PR155：17 个实现、51 个最终条件全部实际编译运行；4 个正确实现的 12 条件全通过，13 个语义错版各被至少一个条件拒绝。
- PR156：22 个变体、44 个最终条件；7 个正确实现的 14 条件全部通过，15 种语义错版的 30 条件全部拒绝。复核时发现旧评分窗与公开 15 µs 期限矛盾，最终保留 15 µs 合同并另按实际事件检查期限。
- PR158：56 个唯一任务与两批实际目录、`task.toml` 分类相符；251 个本地文档路径有效。合并时 EVAS 全量 `regression` 和 `fuzz-smoke` 仍在运行，PR 正文没有把它写成通过。
- 校准入口：[滤波/RF](repo:experiments/benchmark_next/filter/README.md)、[转换器](repo:experiments/benchmark_next/converter/author-calibration.md)、[OTA](repo:experiments/benchmark_next/ota/final-calibration.json)、[LDO](repo:experiments/benchmark_next/ldo/author-calibration.md)、[PLL 与校准](repo:experiments/benchmark_next/calibration/author-calibration.json)。总览当时位于 `benchmark/workbench/TASKS.md`；目录调整后，main 上的待审题包总览见 [TASKS.md](repo:benchmark/material/draftbench/TASKS.md)。完整原始归档为 local-only。

## 遗留与下一步

- 19 道新题只具备 Spectre 扩展集资格；真实源能在 ngspice 运行，不等于 VA 任务已取得开源同题复验资格。
- 没有模型解题实验，也不宣称跑完了完整 Harbor Agent Trial。噪声、完整接收机和 CDR 不在 #149 范围内。
- 五份设计 issue 已关闭，关闭不代表 review 完成；父议题 #107、#72 保持开放，后续由用户重新组织 review，选题审核见 #159。

## 相关链接

- [PR152 CTLE、滤波与 RF 测量任务](https://github.com/BucketSran/vaEVAS/pull/152)
- [PR153 DAC 合同与 ADC 测量任务](https://github.com/BucketSran/vaEVAS/pull/153)
- [PR154 OTA 动态与真实电路数据建模任务](https://github.com/BucketSran/vaEVAS/pull/154)
- [PR155 真实 LDO 启动与响应驱动表征](https://github.com/BucketSran/vaEVAS/pull/155)
- [PR156 分数 PLL 与持续校准任务](https://github.com/BucketSran/vaEVAS/pull/156)
- [PR158 按动作和电路功能统一 56 题](https://github.com/BucketSran/vaEVAS/pull/158)
- 设计 issue：[#147](https://github.com/BucketSran/vaEVAS/issues/147)、[#148](https://github.com/BucketSran/vaEVAS/issues/148)、[#149](https://github.com/BucketSran/vaEVAS/issues/149)、[#150](https://github.com/BucketSran/vaEVAS/issues/150)、[#151](https://github.com/BucketSran/vaEVAS/issues/151)
- 后续：[#159 选题审核](https://github.com/BucketSran/vaEVAS/issues/159)、[#107](https://github.com/BucketSran/vaEVAS/issues/107)、[#72](https://github.com/BucketSran/vaEVAS/issues/72)
