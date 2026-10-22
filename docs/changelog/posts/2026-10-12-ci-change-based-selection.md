---
date: 2026-10-12
categories:
  - 项目
slug: ci-change-based-selection
---

# CI 改为按改动范围选择检查，并修正"超时被当成数值拒绝"的回归测试

三个直接推送到 main 的提交（不经 PR）：CI 先判断这次改了什么再决定跑哪些检查，Rust 构建加缓存；同时修正一个把 300 秒进程超时算作"正确拒绝"的回归测试，并把非线性失败试算计入共同工作量上限。提交信息记录的本地验证是 1102 项 Python、238 项 Rust（1 项既有忽略）、68 项维护测试，并注明没有做独立审查。

<!-- more -->

## 做了什么

- 按改动选择检查（`158edb23`、`64db8f1c`）：普通说明文档只检查改动行空白和 CI 路由自检；能力表、数学说明、评测标准保留对应校准；EVAS 实现、依赖或构建文件仍跑完整回归、静态检查、ngspice 对照、fuzz 和两平台安装测试；CI 配置或未登记路径全跑。混合修改取并集，删除和重命名也参与选择。
- 调度合并：`numerical-assurance.yml` 成为唯一调度入口，统一的 `ci-result` 检查每个被选中的任务，失败、取消、缺失或意外跳过都不能通过；它替代原来的三个 `*-result` 检查。没有修改 GitHub 分支保护配置。
- 构建缓存：Rust 缓存按操作系统、架构、编译器、依赖清单和任务区分；缓存命中后仍执行构建和全部选中的测试，不缓存"通过"结论。安装测试仍从源码包构建新的 wheel。
- 回归修正（`2ae474bd`）：失败试算和高阶 Taylor 试算计入共同工作量；数值拒绝测试必须核对错误类型，`kernel_timeout`、进程启动失败或协议错误不能证明求解器正确拒绝。Python 回归在 Actions 摘要列出最慢的 20 个测试并保留逐测试耗时附件；`regression` 改用 `opt-level=1`，保留 debug 断言和溢出检查。

## 结果与证据

- 本地诊断报告指出：`test_implicit_dynamics.py` 的模型 `y²+y+t=0` 在 t=0.25 后没有实数解，原请求要求算到 t=0.3，实际返回 `kernel_timeout`、用时 300.013 秒；原测试只断言 `KernelError`，所以超时也被当成通过。
- 同一报告记录发散测试 `y'=y²` 确实返回 `waveform_accuracy` 拒绝，但有 22,037 次失败试算、1,818 个通过局部检查的候选步和 8 轮历史重算，重试成本很高。
- `2ae474bd` 提交信息：1102 项 Python、238 项 Rust（1 项既有忽略）、68 项维护测试通过，固定 Spectre 参考重放；"Independent review was not performed in this side conversation"。
- 规则与用法见 [scripts/README.md](repo:scripts/README.md)、[ci_selection.py](repo:scripts/ci_selection.py)、[numerical-assurance.yml](repo:.github/workflows/numerical-assurance.yml)、[run_regression.py](repo:scripts/run_regression.py)。本地诊断：`current/runs/ci-regression-diagnosis-20261012/REPORT.md`。

## 遗留与下一步

- 提交信息与 README 说明：静态校准通过不代表重新完成 Spectre 对照；CI 不自动执行 Spectre 或原 31×2 矩阵。
- 首次运行的耗时不能用来推算缓存命中后的收益；单次 CI 耗时只是定位线索，不当作可复现的性能提升。
- 这三个提交没有经过 PR 和独立审查（`2ae474bd` 提交信息明确注明）。

## 相关链接

- [158edb23 ci: select checks based on changed files](https://github.com/BucketSran/vaEVAS/commit/158edb23)
- [64db8f1c ci: narrow checks, cache builds and consolidate orchestration](https://github.com/BucketSran/vaEVAS/commit/64db8f1c)
- [2ae474bd fix: bound nonlinear retries and expose CI regression failures](https://github.com/BucketSran/vaEVAS/commit/2ae474bd)
