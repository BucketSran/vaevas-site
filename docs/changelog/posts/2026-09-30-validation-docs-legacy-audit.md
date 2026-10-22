---
date: 2026-09-30T20:50:00
categories:
  - 项目
  - EVAS
slug: validation-docs-legacy-audit
---

# 协作规范与技术手册成形，旧 EVAS v0.8.7 迁移审查归档

9 月 29–30 日合入 main 的 6 个文档/测试 PR：统一协作入口和 EVAS 技术手册，归档对旧 EVAS v0.8.7 的源码审查，补齐 S1 与事件检查器的独立校准，并把 main 文档校准到 EVAS 0.9.0 / IR v11、两档各 24/31（已有收据的有限观测开发证据，不是新实验）。

<!-- more -->

## 做了什么

- **协作入口与手册（#11）**：`AGENTS.md` 从 1,276 词压到 519 词；分支、授权、并行分工等规则移到 `CONTRIBUTING.md` 按需读取。`evas/docs/` 成为公共手册入口，能力表用 14 个稳定能力 ID 分别记录 main 范围、分支状态、证据和缺口。另存 timer、transition、absdelay、slew 的独立候选契约和 13 组手算锚点。
- **旧 EVAS 迁移审查（#17）**：把 2026-09-29 完成的旧 EVAS 源码审查归档，固定旧 `v0.8.7` 提交 `6cb6fa7a`。逐项记录语法、积分、相位、一阶滤波、纯函数/静态循环和波形源候选的可复用范围与验收条件；旧状态槽、事件历史和节点覆盖执行器只作反例保留。不导入旧运行时。
- **S1 与事件校准（#20）**：S1 补 4,001 点独立正例、7 个语义负控和 8 个容差边界控制；E1/E2/C1 的 9 个既有条件改用手算有理数锚点，不再与生成器共享参考函数。
- **review 规范（#21）**：`vaevas-review-pr` 区分 merge-base 与指定端点比较；`vaevas-prepare-pr` 要求写清触发案例、关键方程或状态规则和前后证据。
- **文档校准（#27、#28）**：验证入口单列 #26 的两档各 24/31 与剩余 7 条拒绝（5 个前端、2 个内核）；`evas/README.md` 从 470 行精简到 223 行，当前状态改为 EVAS 0.9.0 / IR v11。

## 结果与证据

- #17：47 条诊断观测 = 35 + 8 + 4，其中 16 次要求完整 Rust 模型路径，12 次返回、4 次拒绝。返回结果包含错误输出，47 不是通过数，也不改变原 31 条件的分母或成绩。证据核对脚本只证明归档材料内部一致；本轮没有新增仿真。
- #20：S1 9 个方法、事件 9 个方法、全部 checker 66 个方法通过；没有执行后端，不能据此增加仿真器通过数。
- #27、#28：只改 Markdown；分别核对 87 个本地链接/21 个锚点、473 个本地链接（含 114 个锚点）；冻结 v1 的 36 个 Git 工件、4 个快照、13 个原始输入身份通过。
- 24/31 来自已有 #26 收据，正式 DVS 资格仍为 I。

## 遗留与下一步

- #17 的实施建议属于当时规划；剩余候选（如 `idtmod`、一阶 `laplace_nd`）以能力表为准，后续实现仍需各自契约、回归和 review。
- #20 指出：只看波形发现不了不改变输出的重复事件，需要独立计数探针或事件记录。
- 旧审查目录后来于 10-02 从当前文件树移除（提交 `1527502c`），固定提交里的原报告仍可查看。

## 相关链接

- [PR #11 docs(evas): unify branch policy, capability tracking and technical handbook](https://github.com/BucketSran/vaEVAS/pull/11)
- [PR #17 docs(evas): 记录旧 EVAS 迁移候选与探针证据](https://github.com/BucketSran/vaEVAS/pull/17)
- [PR #20 test(validation): 补齐 S1 与事件采样复位的独立校准](https://github.com/BucketSran/vaEVAS/pull/20)
- [PR #21 docs: 强化 EVAS review 与 PR 证据规范](https://github.com/BucketSran/vaEVAS/pull/21)
- [PR #27 docs(validation): 同步已合并 EVAS 结果与原 31 条件缺口](https://github.com/BucketSran/vaEVAS/pull/27)
- [PR #28 docs: 校准 main 文档并精简重复历史记录](https://github.com/BucketSran/vaEVAS/pull/28)
- [旧 EVAS 迁移审查冻结报告（固定提交 0b7576a）](https://github.com/BucketSran/vaEVAS/blob/0b7576a13a32aa36d88b760b3f3471def2016ef5/experiments/legacy-evas-migration/README.md)
- 当前入口：[协作说明](repo:CONTRIBUTING.md)、[EVAS 手册](repo:evas/docs/README.md)、[能力表](repo:evas/docs/CAPABILITIES.md)、[定时算子契约](repo:evas/validation/TIMED_OPERATOR_CONTRACTS.md)
