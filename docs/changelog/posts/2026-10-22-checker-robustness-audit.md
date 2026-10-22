---
date: 2026-10-22T06:00:00
categories:
  - Benchmark
  - EVAS
slug: checker-robustness-audit
---

# checker 鲁棒性审计：确认 5 题有真缺陷，20 题需要 Spectre 才能裁决

在没有 Spectre 的条件下，对原始 400 题的 checker 和测试台做了扰动审计。初稿被两位独立核验部分推翻，以修订后的 `FINDINGS.md` 为准：确认 137、142、179、226、058 有真缺陷；20 题要靠 Spectre 才能裁决；079 的 strobeperiod 修复已撤回。原题文件一个没改。

<!-- more -->

## 做了什么

- 对每道题生成多种测试台变体，变体只改 deck，不改 VA 模型：
    - 输出步长缩小（G2/G4）；
    - 刺激时间微扰（TP/TM）；
    - 刺激幅值微扰（AP/AM）；
    - 其他几类微扰。
- 每个变体分别用旧 EVAS 0.8.7 和当前 EVAS（main `deb5cf28`）运行，再交给冻结 checker 判定。看判定会不会因为"输出了哪些行"或"无穷小扰动"而翻转。
- 先请两位审核者审方法，再请两位核验者（Opus 5.5、Sonnet 5.5 max）独立复核结果。初稿保留为 `FINDINGS.draft1.md`，被推翻的结论列在 `FINDINGS.md` 第二节。
- 原题文件的 SHA 与 `INPUT_IDENTITY.json` 逐一核对，0 个不一致。没有运行 Spectre。

## 结果与证据

站得住的结论：

- 145 个判定翻转全部能复现（核验 A 在 25 题上重跑）。
- 8 题的判定取决于 checker 读到哪些行：012、058、075、077、226、247、330、366。其中 226、058 经人工核对，是真 checker 缺陷。
- 400 个 deck 都没有指定输出时刻（没有 `strobeperiod`），输出行完全由模拟器决定。
- 012、075、077、079 上，当前引擎少写输出行，旧版的行集合包含当前引擎的全部行。这 4 题的问题归 EVAS，不归 checker。
- 137、142、179 是真缺陷（核验 B 独立得出），三者分别是：
    - 137：靠浮点误差恰好落在钳位边界；
    - 142：用 `int()` 截断，实数转整数应四舍五入；
    - 179：时间尺度由行跨度估计。

被推翻、已撤回的结论：

- "改 `vth` 就翻转"：checker 里的阈值是硬编码的，审计只挪了 DUT 的阈值，翻转是审计自己造成的。
- "SP/SM 下翻转"：那几个 deck 故意让两个输入相等，变体打破了这个相等。
- 079 的 strobeperiod 修复：加了 strobe 之后，故意删掉 `$bound_step` 的缺陷模型也能通过，等于让 checker 看不出题目要考的点，所以撤回。
- 060 舍入平局：没有数据支持。

`classification.json` 的计数：需要 Spectre 20 题，可选 Spectre 79 题，无标记 244 题。无标记不等于 checker 正确。012、075、077 加 strobe 的候选只能算"在当前引擎上让题目可检验"的手段，不算修复。

证据（本地，未提交）：`current/runs/issue214-claude-20261021/checker-audit/` 下的 `FINDINGS.md`、`METHOD.md`、`classification.json`、`SPECTRE-PROTOCOL.md`、`spectre-manifest.json`、`spectre-bundle/`。

## 遗留与下一步

- 所有结论都没有经过 Spectre。各平局到底哪边对，只有 Spectre 或 LRM 能裁决。Spectre 清单和运行协议已备好，由用户统一跑。协议原稿里两条错误指令已删除。之后清单另加了 140 零边沿探针。
- 修订版 checker 正在另一个本地目录里做，原件只读，独立审查还没有全部返回，不能算定论。截至本条：
    - 058 的修订版已作废；
    - 137 被判为测试台缺陷，不改 checker。
- 012/075/077/079 的补写输出行在 EVAS 侧处理，在本地分支 `codex/evas-issue214-gap-closure` 上进行，未推送。

## 相关链接

- Issue214：https://github.com/BucketSran/vaEVAS/issues/214
- PR208（被审的当前引擎基线）：https://github.com/BucketSran/vaEVAS/pull/208
- 本地证据入口：`current/runs/issue214-claude-20261021/checker-audit/FINDINGS.md`
