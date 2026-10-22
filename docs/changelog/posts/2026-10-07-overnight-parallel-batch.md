---
date: 2026-10-07T03:58:00
categories:
  - EVAS
slug: overnight-parallel-batch
---

# 10-06 夜间并行批次：13 个 EVAS 有限切片合入 main

2026-10-06 前后，按切片并行开发的 13 个 PR 合入 main，覆盖事件体循环、`.scs` 向量端口、内核身份与结果包、平台 wheel、`laplace_np`、两级 `absdelay` 和诊断/lint。固定组合检查点 `9a214a19` 上 Python 770、Rust 149+2 通过（1 项既有忽略），这是组合证据，不是逐 PR 的新执行；各项都是有限切片，不关闭父 issue。

<!-- more -->

## 做了什么

- 语言（#65 的子切片）：#74 允许事件体内有限的静态 genvar 循环；#82 允许 `initial_step` 与 cross 共用常量初始化体；#85 支持有限无状态的比较、逻辑和 `?:` 条件表达式；#92 允许纯 real 函数内的有限 `if/else`。
- 网表输入：#75 把 `.scs` 中的标量节点按端口声明方向映射到 VA 静态向量端口（#63 的 S1 切片）。
- 算子（#66）：#80 把单个负实极点的 `laplace_np` 降为已有的 `laplace_nd`；#86 支持固定 PWL 输入上的两级 `absdelay`，一级误差包围传到二级再认证。
- 打包与身份（#67）：#76 新增 `python -m evas version --json`，不启动仿真即可报告 Python/IR 版本和显式内核哈希；#78 新增 `python -m evas.results run`，保存完整 JSON/CSV 结果包，`manifest.json` 是唯一完成标记；#89 让平台 wheel 内置经校验的 Rust 内核。
- 诊断（#64）：#83 新增只编译、不启动内核的 `python -m evas lint`；#90 给编译器资源上限和已审计的诊断来源分类；#91 统一结构化错误传递，并生成可重生成的源码观察清单。

## 结果与证据

- 组合 `9a214a19`（不含 #79/#81/#85/#77）重建内核后通过 Python 770、Rust 149+2、CMP48、维护 18、checker 88、四项数学和 clippy/fmt；16 次新 EVAS 执行配对原 Spectre 输出，得到 12 matched、4 个原 coarse inconclusive，对应 dense 四项均 matched。
- 同日 24 配置 Spectre 实测（`21.1.0.509.isr12`）覆盖七项新增行为。24 是整批执行数，不是某个 PR 的通过数，也不构成一般连续时间资格。见 [执行报告](repo:experiments/backends/dvs2-spectre-validation/results/pr-alignment-20261006.md)。
- #85 最终头 CI：Python 797/797，Rust kernel 149 + IR 2（1 项既有 ignored）。
- #89 安装 CI 在 Ubuntu 24.04 x86_64 / Python 3.10 和 macOS 14 arm64 / Python 3.12 上通过；数值 CI 815 项 Python、151 项 Rust 通过。曾有一次 macOS 产物把 thin arm64 误标为 universal2，已拒绝该产物并加检查。
- #91 清单当时有 780 条重叠观察（338 条 Python、442 条 Rust、372 条 unknown）；它不是 780 个独立错误，也不是触发覆盖率。固定头 CI 含 824 项 Python、151 项 Rust。
- #92 两例 Spectre 配对共 62 个电压观测，EVAS 与 Spectre 差值为 0；共 4 次 Spectre 执行，其中 2 次因原模型数字缺前导零编译失败，均保留。
- 各 PR 由 GPT-6-Astra 与 Claude CLI + GLM-5.3 独立审查。原始日志、波形和审查材料为 local-only。

## 遗留与下一步

- 语言：运行时循环、历史调用、嵌套事件仍拒绝；#85 未包含 #79 的精确停止事件差异和 #81 的性能工作；#92 后原 PA 模型仍受其他缺口阻挡。
- 打包：#89 不含 manylinux、universal2、Intel macOS 或 PyPI 发布。GitHub 记录 #67 在 #89 合入后关闭。
- 诊断：外部 harness/benchmark 消费、实际触发覆盖和未归类来源仍未完成，#64 当时保持开放（GitHub 记录其于 2026-10-11 关闭）。
- #65、#66 的其余需求继续开放。

## 相关链接

- PR：[#74](https://github.com/BucketSran/vaEVAS/pull/74)、[#75](https://github.com/BucketSran/vaEVAS/pull/75)、[#76](https://github.com/BucketSran/vaEVAS/pull/76)、[#78](https://github.com/BucketSran/vaEVAS/pull/78)、[#80](https://github.com/BucketSran/vaEVAS/pull/80)、[#82](https://github.com/BucketSran/vaEVAS/pull/82)、[#83](https://github.com/BucketSran/vaEVAS/pull/83)、[#85](https://github.com/BucketSran/vaEVAS/pull/85)、[#86](https://github.com/BucketSran/vaEVAS/pull/86)、[#89](https://github.com/BucketSran/vaEVAS/pull/89)、[#90](https://github.com/BucketSran/vaEVAS/pull/90)、[#91](https://github.com/BucketSran/vaEVAS/pull/91)、[#92](https://github.com/BucketSran/vaEVAS/pull/92)
- Issue：[#63](https://github.com/BucketSran/vaEVAS/issues/63)、[#64](https://github.com/BucketSran/vaEVAS/issues/64)、[#65](https://github.com/BucketSran/vaEVAS/issues/65)、[#66](https://github.com/BucketSran/vaEVAS/issues/66)、[#67](https://github.com/BucketSran/vaEVAS/issues/67)
- 仓库：[算子数学契约](repo:evas/docs/math/operators.md)、[纯函数分支对照](repo:experiments/backends/function-branches)
