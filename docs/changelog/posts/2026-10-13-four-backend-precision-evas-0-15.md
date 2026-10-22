---
date: 2026-10-13
categories:
  - EVAS
slug: four-backend-precision-evas-0-15
---

# 四后端精度对照扩展到 852 个固定位置，对比表改为五层能力目录，EVAS 升到 0.15.0

10 月 11–13 日的 11 个 PR 已合入 main：先把 Q1/Q2/Q3 三档精度配置固定下来，再把四后端（EVAS、Spectre、ngspice、Gnucap）对照扩展到 20 组基础能力和 24 组工程组合、852 个固定位置，同时修了一批 EVAS 数值路径，最后整理为 EVAS 0.15.0 / IR19。这些是开发验证集，不是独立的论文留出集，也不是当前 main 的全矩阵验收。

<!-- more -->

## 做了什么

- 配置绑定（PR160）：选定条件、后端和 Q 档后，运行前生成已校准的模型、设置、观察计划和验收要求；工具或依赖变化时拒绝沿用旧配置，没有合格配置时不自动降档。
- 对比表改版（PR163、PR164、PR166）：对比表从实验批次改为五层固定能力目录（PR163 为 55 行，PR164 固定为 56 行全部必测用例），完整验收写 ✓ 和已验证精度，失败写短原因，无结论写"—"；历史成绩和原判据原样保留。PR166 把 11 个"取证不足"格拆成具体原因。
- 精度广度（PR162）：20 组基础、24 组工程组合、71 个必测变体、每后端三档 Q 配置，852 个固定位置都有实际四后端执行记录。同时修 EVAS 三处：有序自状态数组更新、PWL 斜率取原段斜率、普通相位查询失败时用更紧相位运算重试。
- 数值修复：严格滤波 deep 配置的保守拒绝（PR161，指数计算改用 Horner 嵌套）；运行时 cos、exp、ln、sqrt 和半次幂的编译与误差认证，前端与内核升为 IR19（PR165）；采样积分/局部 strobe、多项式 `ddt`、Q3 非线性滤波（PR167）；中断的 transition 驱动前馈 idt（PR170）。
- 判据与工具：新增 `root-window-v3` checker，解决旧 SH-X、EC04 触发窗把正确数学根排除在外的问题，旧判据和成绩保留（PR168）；延后分析先核对冻结输入再读回设置，增加 precheck、pilot 和阶段计时（PR169）。
- 版本：PR170 整理为 EVAS 0.15.0 / IR19。IR19 与 IR18 不兼容，回退需重编译 VA；PR165 正文说明不发布 tag 或包索引版本。

## 结果与证据

- PR160：每个 Q 档的完整配置资格为 Spectre 8/8、EVAS 7/8、ngspice 4/8、Gnucap 6/8；96 个选择中 75 个有合格配置，21 个保留失败或缺证原因。
- PR162：EVAS 213 个位置中 105 个完整通过、81 个证据不完整、27 个拒绝/超时。EC21 Q3 由旧的 89.8498 s 完成变为在 90 s 限制下 90.0165 s 超时，记为失败。
- PR165：EVAS 五张数学卡 Q1–Q3 共 15/15 通过；原 78 个横线格变为 53 格 Q3、3 格工程门槛通过、11 格实际失败、11 格取证不足。
- PR167：同一批 EVAS 原 30 个配置全部完成，27 个完整通过；Spectre 原 30 个为 6 通过 / 3 数值误差 / 21 证据不足。最终 CI 1244 项 Python、251 项 Rust 通过。
- PR168：新增 18 个实际配置，EVAS 原模型 6/6 通过，Spectre 只读回调运行 5/6 通过。
- PR170：117 个位置中旧整链 EVAS 36 完整通过，Spectre 只读源 27 通过 / 9 缺证；新积分两端 3/3 通过 Q1–Q3。最终 CI 1301 项 Python、253 项 Rust 通过。
- 入口：[对比表](repo:evas/docs/COMPARISON.md)、[评测标准](repo:evas/docs/COMPARISON-METHODOLOGY.md)、[累计清单](repo:evas/validation/paper/COVERAGE.md)、[配置使用说明](repo:evas/validation/paper/README.md)、[广度收据](repo:experiments/backends/support/20261012-breadth.json)、[能力缺口收据](repo:experiments/backends/support/20261013-capability-gaps.json)、[root-window-v3 收据](repo:experiments/backends/support/20261013-root-window-v3.json)、[117 槽收据](repo:experiments/backends/support/20261013-legacy-chain-q.json)。原始波形和完整审查为 local-only。

## 遗留与下一步

- PR162 列出的下一批：EC03/EC04 和局部 strobe 收口；ngspice F03 的 36 个分析因设置读取器不接受带引号名称而保留 `ReadbackError`。
- 阈值采样回调边界仍缺证，原 7/8 不改为 8/8；严格"没有提前触发"的 EVAS 结论仍未决。
- 导数只限于合格物理输入上的光滑多项式；多历史、复位、反馈和长期内存压力没有取得支持。
- #96、#119 保持开放；草稿 PR #131 未动。

## 相关链接

- [PR160 固定 Q1/Q2/Q3 配置绑定](https://github.com/BucketSran/vaEVAS/pull/160)
- [PR161 修复严格滤波配置的保守拒绝](https://github.com/BucketSran/vaEVAS/pull/161)
- [PR162 四后端精度广度验证与三处数值修复](https://github.com/BucketSran/vaEVAS/pull/162)
- [PR163 五层能力目录](https://github.com/BucketSran/vaEVAS/pull/163)
- [PR164 固定对比表必测范围](https://github.com/BucketSran/vaEVAS/pull/164)
- [PR165 初等函数认证与 IR19](https://github.com/BucketSran/vaEVAS/pull/165)
- [PR166 补齐 11 格对比取证](https://github.com/BucketSran/vaEVAS/pull/166)
- [PR167 导数与采样动态精度缺口](https://github.com/BucketSran/vaEVAS/pull/167)
- [PR168 root-window-v3 真根判据](https://github.com/BucketSran/vaEVAS/pull/168)
- [PR169 延后资格分析与分阶段运行](https://github.com/BucketSran/vaEVAS/pull/169)
- [PR170 EVAS 0.15.0](https://github.com/BucketSran/vaEVAS/pull/170)
- Issue：[#96](https://github.com/BucketSran/vaEVAS/issues/96)、[#119](https://github.com/BucketSran/vaEVAS/issues/119)
