---
date: 2026-10-05
categories:
  - EVAS
slug: language-scs-input-expansion
---

# EVAS 0.13.0 / IR17：语言展开、事件日程、联合连续动态与 .scs 测试台输入

10 月 4–5 日合入 main 的 3 个 PR 扩展了前端语言、事件日程和联合连续动态，并新增 `simulate tb.scs` 电压测试台入口。六份原 benchmark 参考 VA 中，ZOOM 首次可直接编译，并在 EVAS 与 Spectre 上通过两组完整时序检查（1,400 个边沿、2,100 个电压样本）；其余五份仍各有首个阻塞。

<!-- more -->

## 做了什么

- **#61（0.13.0 / IR17）**：
    - 前端展开：纯 real 函数、静态 genvar 循环、一维静态数组、静态模块层次和受限预处理，不同写法进入同一 IR。
    - 事件日程：状态改变后重定位 cross；cross/timer 混合 OR；timer 参数可由保持状态控制。
    - 历史输入：固定参数的 absdelay/slew 可读取内部仿射电压。
    - 联合动态：proper 滤波进入无事件 index-one 多项式 DAE，冷启动联合求解原关系、积分初值和滤波 DC 条件。
    - 合并前审查修复：一个有效的非对称历史盒以 `1e-7 V` 预算接受了约 `7.49e-5 V` 的残差；同一文件重复 include 时调用点身份冲突；fuzz 种子仍为 IR16。
- **#69（#63、#64、#65 的第一批）**：参数 `from`/`exclude` 范围与 integer 精确 32 位检查；静态 electrical 向量按声明顺序展开；纯初始化 OR；带 `diagnostic_version=1` 的诊断分类；`simulate tb.scs` 支持 `ahdl_include`、DC/PWL/受限 pulse 源、stop/maxstep、save 和 reltol/vabstol，复用现有编译器与内核。
- **#71**：事件改变积分轨迹后撤销旧根、重建未来日程；timer 支持缺省 period/time_tol/enable（EVAS 默认 time_tol 为 1 ps）；静态 genvar 循环里的 timer/cross/OR 在编译期展开。va07 作为候选原型保留，不加入原六题或原 31 条件分母。

## 结果与证据

- #61：643 项 Python 通过；Rust workspace 145 项通过；有界 fuzz 46 秒 735,778 次无崩溃；原 31 条件两档重新执行各 31/31；既有冻结七案例确认集 14/14（不是新增未见确认条件）。合并前 GitHub CI 三项任务通过。
- #69：最终提交 CI 中 Python 670 项、Rust 145 项通过（1 项忽略）；ngspice 对照 11 项中 6 项通过，5 项因对照转换器缺独立参考模型标为 unsupported，不计通过也不表示 EVAS 失败。`.scs` 示例 9 个观察点符合独立答案 `out = 2*u - 0.125 V`。
- #71：全量 Python 688 项中仅一项旧测试仍要求拒绝 `timer(1n)`，改为仍不支持的 `timer(V(u))` 后所属 26 项补跑通过。ZOOM 原 VA、原参数、原 checker 不变，EVAS 与 课题组服务器上的 Spectre 21.1.0.509.isr12 均通过，外部判据 15 mV 与 90 ps；timer 缺省参数六个同源案例通过两端独立检查。
- 共同外部判据不代表内部容差相同（ZOOM 网表请求 reltol=1e-5，Spectre conservative 实际用 1e-6）；没有同配置速度或一般连续时间精度结论。正式 DVS 资格仍为 I。

## 遗留与下一步

- 其余五份原 benchmark VA 的首个阻塞：AND2 的比较/逻辑/三元表达式；SAR 的 `initial_step` 与 cross 混合；校准模型事件体内的 for；VCO 的连续 real 临时变量与事件状态初始化；运放的 `I()` 电流贡献（基础电流/KCL/RC 由 [#68](https://github.com/BucketSran/vaEVAS/issues/68) 跟踪）。只记录首个阻塞，不代表后面都已支持。
- [Issue #70](https://github.com/BucketSran/vaEVAS/issues/70) 的双向自换向 cross 仍拒绝；同刻跳变闭包、隐式非线性 guard、DAE 与事件/复位/ddt 组合、运行时循环仍未补齐。
- #63–#65 本批不关闭；非恒定 pulse 拐点不能精确表示为 binary64 时仍拒绝。

## 相关链接

- [PR #61 feat(evas): 扩展受限语言、事件日程与联合连续动态](https://github.com/BucketSran/vaEVAS/pull/61)
- [PR #69 EVAS：补齐首批参数、向量、诊断和 .scs 输入](https://github.com/BucketSran/vaEVAS/pull/69)
- [PR #71 EVAS：补齐历史事件重定位、timer 缺省参数与 ZOOM 循环事件](https://github.com/BucketSran/vaEVAS/pull/71)
- 相关 Issue：[#62](https://github.com/BucketSran/vaEVAS/issues/62)、[#63](https://github.com/BucketSran/vaEVAS/issues/63)、[#64](https://github.com/BucketSran/vaEVAS/issues/64)、[#65](https://github.com/BucketSran/vaEVAS/issues/65)
- 当前入口：[语言契约](repo:evas/validation/ANALOG_CONDITIONS_CONTRACT.md)、[事件数学](repo:evas/docs/math/events.md)、[能力表](repo:evas/docs/CAPABILITIES.md)、[能力补齐证据](repo:experiments/runs/capability-completion/README.md)
