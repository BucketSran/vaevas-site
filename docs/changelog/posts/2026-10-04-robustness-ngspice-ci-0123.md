---
date: 2026-10-04
categories:
  - EVAS
slug: robustness-ngspice-ci-0123
---

# EVAS 稳健性审查收口：调用边界、ngspice 差分、有界求解恢复与完整 CI

10 月 3–4 日合入 main 的 5 个 PR，处理了 10-03 新建的一批审查 Issue（#36–#47 等），版本为 EVAS 0.12.3 / IR16。在 main `a7a42e17` 上重跑原 31 条件，两档仍各 31/31（开发证据，正式 DVS 资格仍为 I）；CI 首次纳入完整 Python/Rust 回归。

<!-- more -->

## 做了什么

- **#48 调用与编译边界**（关闭 #36–#39）：内核调用加墙钟超时（默认 300 秒）；`compile_sources` 从 334 行拆到 60 行；统一算子登记；语法、表达式、参数链、IR 深度和展开大小分别设预算；畸形 manifest、非有限 JSON 数值等给出明确诊断。资源上限可能拒绝部分合法大模型。
- **#49 外部对照与随机测试**（关闭 #40–#42、#46）：ngspice 共同子集差分对照、区间运算的性质测试（proptest）、cargo-fuzz 有界模糊测试、积分误差链审计。ADR-001 保留电压域目标，不把 MNA/电流语义混进 IR16。
- **#50 有界求解恢复**（关闭 #43–#45）：仿射残差失败时最多做两次迭代精化；小型方阵 Newton 失败后可尝试有次数上限的连续化初猜，最后仍用原方程、原容差验收。新增 `EVAS_STATIC_THREADS` 静态样本并行（默认 1）和库内性能基准。
- **#55 CI 门禁**（关闭 #22）：CI 加入完整回归、Clippy、格式、追溯矩阵、冻结身份、独立数学与检查器校准；保留 ngspice 和 fuzz 作业。
- **#60 诊断与求解复用**（关闭 #9、#24、#34、#47）：IR 类型拆到 `evas-ir`；新增有界诊断、编译后模型查询和只读的单会话 stdio MCP（查询不求解模型）；稀疏系数一次查找更新；只有节点顺序和全部系数逐位相同时才复用仿射 LU。

## 结果与证据

- ngspice 对照（#49、#50）：15 个静态样本、33 个瞬态观察在默认电压预算内，最大归一化差异约 0.00645；另 5 个含状态/算子的 smoke 因翻译器不支持而单列，不计为通过。
- fuzz（#49）：两个目标分别执行 2,277,535 次和 733,678 次，均无崩溃；有限轮次不证明任意输入安全。
- #55：540 项 Python、129 项 Rust 通过（1 项 ignored）；原 31 条件两档各 31/31，62 份 CSV 哈希与 #33 一致。CI 不自动跑原 31×2 矩阵或 Spectre。
- #50 性能（Apple M5，五轮中位数）：4096 样本四线程相对单线程约 1.26–2.74 倍；1024 节点首解 2.686 s，复用分解后每个右端项 0.257 ms。
- #60：首轮 PR CI 552 项 Python 通过；原 31 条件两档各 31/31。26 个固定负载、520 个独立进程的配对测量中，Random-1024 完整请求中位时间 1.67 s → 0.33 s；积分 4097 个观测点的分解次数 16,385 → 1，但总时间只小幅改善。
- 本批没有新 Spectre 执行；#50 的连续化是初猜启发式，不证明全局收敛。

## 遗留与下一步

- 稀疏填充/存储、已认证历史和 guard 的成本、长结果流式协议，由 #60 转到 [#57](https://github.com/BucketSran/vaEVAS/issues/57)、[#58](https://github.com/BucketSran/vaEVAS/issues/58)、[#59](https://github.com/BucketSran/vaEVAS/issues/59) 跟踪。
- [Issue #16](https://github.com/BucketSran/vaEVAS/issues/16) 保持打开：课题组服务器当时只有 Spectre 21.1.0.509.isr12。
- JSON 仍是完整结果协议；流式输出需要另行定义成功、失败和取消语义。

## 相关链接

- [PR #48 fix(evas): 修复 Python 编译与内核调用边界](https://github.com/BucketSran/vaEVAS/pull/48)
- [PR #49 test(evas): add ngspice differential checks, properties and fuzzing](https://github.com/BucketSran/vaEVAS/pull/49)
- [PR #50 fix(evas): 有界求解恢复、静态批量并行与性能基准](https://github.com/BucketSran/vaEVAS/pull/50)
- [PR #55 ci(evas): 补齐完整回归与 0.12.3 矩阵证据](https://github.com/BucketSran/vaEVAS/pull/55)
- [PR #60 feat(evas): add bounded diagnostics and measured solver reuse](https://github.com/BucketSran/vaEVAS/pull/60)
- 关闭的 Issue：[#9](https://github.com/BucketSran/vaEVAS/issues/9)、[#22](https://github.com/BucketSran/vaEVAS/issues/22)、[#24](https://github.com/BucketSran/vaEVAS/issues/24)、[#34](https://github.com/BucketSran/vaEVAS/issues/34)、[#36](https://github.com/BucketSran/vaEVAS/issues/36)–[#47](https://github.com/BucketSran/vaEVAS/issues/47)
- 当前入口：[求解数学](repo:evas/docs/math/solving.md)、[ngspice 差分](repo:experiments/backends/ngspice-differential/README.md)、[性能实验](repo:experiments/performance/README.md)、[ADR 记录](repo:evas/docs/development/DECISIONS.md)
