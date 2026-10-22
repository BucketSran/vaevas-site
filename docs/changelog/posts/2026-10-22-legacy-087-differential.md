---
date: 2026-10-22T01:44:00
categories:
  - EVAS
  - Benchmark
slug: legacy-087-differential
---

# 旧版 EVAS 0.8.7 差分对照：同一套冻结 checker 下 393/400，重建版 342/400

把旧版 EVAS 0.8.7 和 0.8.3 在本地重新编译，用原始 400 题和同一套冻结 checker 跑了一遍：0.8.7 通过 393/400，0.8.3 通过 399/400。当前 main 上的重建版通过 342/400，它的 58 个失败里，旧版 0.8.7 能过 55 个。这些数字都是本地开发对照，不是验收收据，也不代表 Spectre 能过。

<!-- more -->

## 做了什么

- 用 `git archive` 从本地旧仓库导出 v0.8.7（提交 `6cb6fa7a`），另导出标签 v0.8.3。v0.8.3 是 R45 认证时用的版本。导出后在 `/tmp` 下离线编译，`evas --version` 输出 0.8.7。
- 运行脚本是 `harness.py`，做法和开发重放工具 `devrun.py` 一致：
    1. 对每题运行 `python -m evas simulate <deck>`；
    2. 读出 `tran.csv`；
    3. 经冻结的行归一化后交给冻结 checker 判定。
- 对照对象是 main `deb5cf28` 的开发重放结果。
- 全程只读：没有改原题、checker 或 EVAS 源码，没有运行 Spectre，也没有推送。

## 结果与证据

| 版本 | 通过 / 400 | 未通过的题 |
| --- | --- | --- |
| 旧 EVAS 0.8.7 | 393 | 027、057、102、178、185、186、346 |
| 旧 EVAS 0.8.3 | 399 | 102 |
| 重建版 EVAS（main `deb5cf28`） | 342 | 58 题，见 PR208 条目 |

- 重建版的 58 个失败里，0.8.7 能过 55 个。两边都不过的只有 102、186、346。
- 有 4 题（027、057、178、185）重建版能过、0.8.7 拒绝。原因是 0.8.7 新增了"运行时索引状态数组 fail-closed"拒绝，这 4 题在 0.8.3 上都能过。
- 这次对照也修正了根因报告里的几个早期判断：
    - 012、077、079：旧版写出的输出行包含当前引擎的全部行，还多出事件时刻、transition 斜坡点和 `$bound_step` 点。证实问题在"当前引擎少写行"。
    - 039、358、360（动态 transition delay）：旧版能过，有现成的参考实现可以对照。
    - 059、060：旧版给出 double 点值答案，当前版拒绝。这是"认证"和"点值"两种做法的取舍，不是题目本身有问题。
- 证据（本地，未提交）：
    - `current/runs/issue214-claude-20261021/legacy-087/`：README、`harness.py`、`RESULTS-0.8.7.json`、`RESULTS-0.8.3.json`、探针；
    - `current/runs/issue214-claude-20261021/ROOT-CAUSES.md` 中"更正与补充：旧 EVAS 0.8.7 对照"一节。

## 遗留与下一步

- **"legacy 通过"不等于"Spectre 通过"**：两个 EVAS 版本同出一源，结果一致不代表正确。
    - 旧仓库里关于"对齐 Spectre"的说法，没有附 Spectre 原始数据。
    - benchmark r53 绑定 `evas-sim==0.8.7`，但它的门禁不含 Spectre，标为"optional, not run"。
    - R45 的 gold 400/400 是在 0.8.3 上认证的。
- harness 有局限：只做主 checker 判定。基准自己的 runner 用独立二进制，还做时间变换和"激励不足"检查，这里没有做。输出行网格也不一定和当年完全一致。
- `/tmp` 下的编译产物会被清理。要复现，需要重新导出并编译。
- 结论已用于安排后续修复，相关工作在本地分支 `codex/evas-issue214-gap-closure` 上进行，还没有 PR。其中 012/075/077/079 的"补写输出行"划给 EVAS 侧。

## 相关链接

- Issue214：https://github.com/BucketSran/vaEVAS/issues/214
- PR208（重建版对照基线）：https://github.com/BucketSran/vaEVAS/pull/208
- [R45 认证说明](repo:benchmark/material/historyref/v4/R45_RELEASE_CERTIFICATION.md)、[r53 认证说明](repo:benchmark/material/historyref/v4/R53_RELEASE_CERTIFICATION.md)
- 旧 EVAS 来源：https://github.com/Arcadia-1/EVAS （本地副本 `legacy/EVAS`）
