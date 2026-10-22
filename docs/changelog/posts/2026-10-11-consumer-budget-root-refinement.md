---
date: 2026-10-11T04:07:00
categories:
  - EVAS
slug: consumer-budget-root-refinement
---

# EVAS 按输出精度预算细化事件根，补齐采样-边沿-滤波组合与定时 strobe

六个 PR 已合入 main：EVAS 开始从下游输出的电压预算反推事件时间需要多准，补上"采样保持 → transition → 一阶滤波"这条组合，修复固定 timer 下的 strobe 拒绝，并给 Spectre 参考结果加了精度资格检查。所有结果都是开发集的有限观测，不是全轨迹精度证明。

<!-- more -->

## 做了什么

- 采样-边沿-滤波组合（PR123）：原来拒绝的"采样保持经 transition 驱动一阶 laplace"现在可以传播历史，覆盖延迟、边沿中断、复位和双实例；事件根的时间不确定性会传到边沿和滤波。用户具名接受了 SEF-TIMER-18 的 18 条瞬时跳变侧差异，原严格 FAIL 和记录保留，不豁免其他模型。
- 按消费者预算细化输入根（PR129）：直接采样因事件时间不够准超出电压预算时，EVAS 计算需要的根宽度，达到后仍用原预算重验；误差与当前根无关时保留失败。目标试算与一次完整回退共用 256 次迭代上限。
- 定时 strobe 修复（PR130）：固定 `timer` 的时间包围过宽，导致普通查询通过而 strobe 拒绝；改为用精确时钟关系取最窄浮点包围。同时交付四后端精度检查器和 OpenVAF-R 事件诊断。
- 滤波链事件根（PR132）：单次采样经固定 `transition` 和稳定一阶滤波时，从输出预算反推事件根宽度，所有电压消费者取最紧要求。Spectre 测试台新增只记录时间的 `timer`，补齐边沿结束后的原生观测点。
- Spectre 参考精度资格（PR124）：定位非线性积分与事件续算的四组对照失败，记录可复核的参考精度流程；不改数值内核。
- 候选帧共享输入（PR141）：候选和回放帧不再反复复制同一份 `DirectInput` 波形，改为共享不可变数组；这是性能长期 issue #138 的首个切片，本阶段速度优化随之收尾。

## 结果与证据

- PR123：实际 Spectre 21.1.0.509.isr12 下四类组合 × 三档配置通过固定工程检查；52,200 个共同原生观察点和 18 条严格差异全部保留。最终提交五项 GitHub CI 通过。
- PR129：直接采样正例一次迭代把根宽从 1.83e-4 s 收到 1.98e-10 s；同源码 Spectre 对照 12/12 满足原预算，1,188 个共同点最大电压差 0.099 nV。最终头五项 CI 通过，含 1,058 项 Python、228 项 Rust。
- PR130：原 12 组 strobe 拒绝，修复后 EVAS 和 Spectre 各 12/12 通过；新增积分例 Spectre 原四档约 115.49 µV 超过 100 µV，失败保留。
- PR124：原六配置完整验收 2/6；新跑八次 Spectre，严格时刻 4/8、连续观测 5/8，旧结果未删。整合后重放 16 个 EVAS 请求，12,243 个共同点和 68 个锚点满足原预算。
- PR132：严格 `1e-10 V` 预算下根细化由 3 次减为 2 次，工程 `2.01e-6 V` 下由 3 次减为 1 次；宽预算控制由 0 次增为 1 次，不宣称端到端加速。
- PR141：合成输入（4097 拐点、8193 观察点）五轮交替复测，端到端中位耗时从 508.84 ms 降到 281.16 ms；其他六例无稳定收益或退化结论，不承诺通用提速。
- 契约与收据：[采样-边沿-滤波独立契约](repo:evas/validation/sample_edge_filter/README.md)、[实现与 Spectre 对照](repo:experiments/backends/sample-edge-filter/README.md)、[滤波预算边界](repo:experiments/backends/sample-edge-filter/BOUNDARY.md)、[strobe 收据](repo:experiments/backends/strobe/README.md)、[性能记录](repo:experiments/performance/README.md)、[事件数学手册](repo:evas/docs/math/events.md)。原始波形和审查日志为 local-only，例如 `current/runs/performance-reuse-20261011/`。

## 遗留与下一步

- 重叠事件窗口、状态/历史相关根、滤波反馈、多输入和高阶消费者仍有限制；一般历史重放、复杂事件簇、多级滤波的预算分配未实现。
- 3 项 Spectre 基础档数值失败和 SEF-TIMER-18 差异保留；近邻原子事件和保持状态 timer 的原限制仍在。
- 这些是 #119、#96 的有限切片，不关闭一般误差预算分配任务；#138 其余加速候选暂停，待功能正确性完善后再考虑。

## 相关链接

- [PR123 sample-edge-filter 历史与 timer 差异范围](https://github.com/BucketSran/vaEVAS/pull/123)
- [PR124 Spectre 精度与观测资格](https://github.com/BucketSran/vaEVAS/pull/124)
- [PR129 按消费者精度预算细化输入根](https://github.com/BucketSran/vaEVAS/pull/129)
- [PR130 修复定时采样 strobe 并补齐精度对照](https://github.com/BucketSran/vaEVAS/pull/130)
- [PR132 按滤波链输出预算细化事件根](https://github.com/BucketSran/vaEVAS/pull/132)
- [PR141 候选帧共享不可变输入](https://github.com/BucketSran/vaEVAS/pull/141)
- [Issue119 分层精度控制及 Spectre 对照](https://github.com/BucketSran/vaEVAS/issues/119)
- [Issue96 论文对比规格](https://github.com/BucketSran/vaEVAS/issues/96)
- [Issue138 长期加速候选](https://github.com/BucketSran/vaEVAS/issues/138)
