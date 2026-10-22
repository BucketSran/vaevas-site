---
date: 2026-10-02
categories:
  - EVAS
slug: ir15-ir16-continuous-dynamics
---

# IR15 与 IR16：受限连续动态、非线性积分和事件截止点认证

10 月 1–2 日合入 main 的 5 个 PR 把原 31 条件两档的有限观测达标从各 24/31 提升到各 31/31（#29，IR15），此后各轮扩展复跑仍为各 31/31，最终为 EVAS 0.12.2 / IR16。这些条件已用于开发，满分不代表全时域精度，正式 DVS 资格仍为 I。

<!-- more -->

## 做了什么

- **#29 IR15**：新增普通 analog 局部顺序赋值及输入驱动条件、常量数组与一阶 `laplace_nd`、`idtmod`/受限 `sin`、无状态多项式瞬态。多项式瞬态先用 Newton 求名义解，再用根盒证明验收。
- **#30 连续网络（0.10.0 / IR16）**：积分可带仿射电压反馈和线性算子嵌套（如 `y=idt(1-y,0)`，独立答案 `1-exp(-t)`）；`laplace_nd` 支持 1–8 阶；`ddt` 支持直接 PWL 输入；cross 可由多项式或连续积分/滤波轨迹驱动，用区间方法证明唯一穿越。提供从原始 VA/manifest 重编译到 IR16 的入口。顺带修复：单位斜坡下 `ddt(u)` 套恒等滤波后 DC 初值从 0 变成 1、残差却为零的组合错误。
- **#31 非线性积分（0.11.0）**：显式多项式 ODE、事件修改的联合积分/复位、内部节点或算子输入的 `ddt`。合并前审查发现并修复两项精度问题，例如解析反例误差约 0.586 V 却被 `1e-4 V` 设置接受。
- **#32 混合动态与事件生命周期**：积分/proper 滤波混合网络、无事件的 index-one 多项式隐式 DAE、非精确事件时刻的采样/条件认证；修复 `ddt(idt(q))` 恢复瞬时依赖后被误当唯一解的问题。
- **#33 已知事件截止点**：非线性连续历史只认证到下一次已知事件。例如 `y'=q*y²` 中 q 在 0.5 处从 1 变成 −1，旧实现会因假想的未来爆炸而拒绝，新实现先算到 0.5 再续算（0.12.2 / IR16）。

## 结果与证据

| PR | Python / Rust 测试 | 原 31 条件两档 |
| --- | --- | --- |
| #29 | 372 / 83 | 62 次新执行，各 31/31 |
| #30 | 423 / 112 | 62 次新请求，各 31/31 |
| #31 | 458 / 118 | 重新执行，各 31/31 |
| #32 | 497 / 122 | 各 31/31 |
| #33 | 506 / 124 | 各 31/31 |

- 每轮都有 1 项旧性能探针 ignored；各轮 62 份 CSV 与该 PR 指定的参照快照一致，原 DUT、阈值、检查器和分母未改。
- #32 的 20 条共同生命周期新 EVAS 回放：18 条 `finite_consistent`、2 条 `classified_trigger_observation`；Spectre 复用旧 20 条执行（9 条一致、2 条分类差异、8 条不一致、1 条分析失败），没有新远端仿真。
- 本批没有新 Spectre 执行或性能测量；完整原始数据只在本地保留。

## 遗留与下一步

- 旧 IR1–15 必须从原始 VA/manifest 重新编译，不能只改版本号。
- #32、#33 列出的缺口：一般事件固定点唯一性、隐式 DAE 与事件/其他算子组合、首次非线性滤波 DC、非线性直接通路、动态 guard 的事件后重定位，以及 absdelay/slew/idtmod 的非点观察。
- 高阶网络增广维度最多 32，包围预算不足时保守拒绝。

## 相关链接

- [PR #29 feat(evas): 交付 IR15 受限能力与精度链认证](https://github.com/BucketSran/vaEVAS/pull/29)
- [PR #30 feat(evas): 补齐受限连续动态、动态 cross 与 IR16 迁移](https://github.com/BucketSran/vaEVAS/pull/30)
- [PR #31 feat(evas): certify nonlinear integrals and joint event dynamics](https://github.com/BucketSran/vaEVAS/pull/31)
- [PR #32 feat(evas): certify mixed dynamics and shared event lifecycle](https://github.com/BucketSran/vaEVAS/pull/32)
- [PR #33 按已知事件截止点认证非线性连续历史](https://github.com/BucketSran/vaEVAS/pull/33)
- 当前手册：[连续动态数学](repo:evas/docs/math/continuous.md)、[动态契约](repo:evas/validation/DYNAMICS_CONTRACTS.md)、[能力表](repo:evas/docs/CAPABILITIES.md)
