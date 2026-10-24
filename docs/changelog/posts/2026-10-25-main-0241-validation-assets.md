---
date: 2026-10-25T01:11:00
categories:
  - EVAS
  - 项目
slug: main-0241-validation-assets
---

# 主线到 0.24.1：迁入回归、idt 复位与验证资产合入

main 现为 `2a790344`，版本 0.24.1。10 月 22 日日志之后，文档刷新、回归迁入、idt 脉冲复位、验证资产和能力目录的 CI 路由已合入；原 400 题没有在这批提交上重跑。

<!-- more -->

## 做了什么

- **文档刷新**：[PR224](https://github.com/BucketSran/vaEVAS/pull/224) 已于 2026-10-22 20:22 合入 main（`a4d2b875`）。上一条日志写它还没合并；这里更正。它只刷新当时 main `6f3a6b54` 上的状态描述。
- **回归迁入**：[PR228](https://github.com/BucketSran/vaEVAS/pull/228) 已于 2026-10-22 23:05 合入（`b2e407fe`）。迁入 #226、#227、#65 的回归和 D7 的 Spectre 证据。只加测试和证据，不改 EVAS 源码。已知错误标成预期失败。
- **idt 脉冲复位**：[PR234](https://github.com/BucketSran/vaEVAS/pull/234) 已于 2026-10-24 21:45 合入（合并提交 `21c061dc`，实现头 `58d98504`），对应 #230。数学手册中的算子页随 main 自动更新。
- **验证资产**：[PR238](https://github.com/BucketSran/vaEVAS/pull/238)、[PR239](https://github.com/BucketSran/vaEVAS/pull/239)、[PR237](https://github.com/BucketSran/vaEVAS/pull/237)、[PR240](https://github.com/BucketSran/vaEVAS/pull/240) 已于 2026-10-24 晚合入，止于 `c44e7ebf`。内容是 DVS 科学定义、共享波形读取器的依赖身份、模型与 paper 输入构造、夹具 freshness 和引用接线。
- **能力目录**：[PR241](https://github.com/BucketSran/vaEVAS/pull/241) 已于 2026-10-25 00:28 合入（`1639384e`），新增 [能力目录](repo:evas/capabilities/README.md)。该目录不在网站自动导入的路径里。
- **CI 路由**：[PR242](https://github.com/BucketSran/vaEVAS/pull/242) 已于 2026-10-25 01:07 合入（`2a790344`）。能力目录的改动走维护检查，不进入求解回归；四片回归按最近一次完整计时重新分配，并把 Rust 全量留在预留的分片上。这次不改仿真行为。

## 结果与证据

| 项目 | 现状 | 口径 |
| --- | --- | --- |
| main | `2a790344`，版本 0.24.1 | 已合入 |
| 原 400 题 | 343 通过 / 5 判错 / 52 拒绝 | 开发重放，只属于 main `6f3a6b54`（2026-10-22）；这批新提交没有重跑 |
| 正式检查点 | `159c0512`：318 通过、19 失败、63 拒绝 | 已验收；本条没有新的验收收据 |
| 正式 benchmark | 构建时从 main 的正式清单读取；清单里的 `tasks` 仍为空 | 开发中 |

#234 实现头 `58d98504` 的交付 CI 已通过：[run 40076435431](https://github.com/BucketSran/vaEVAS/actions/runs/40076435431)。#230 正文记录该次为 Python 2797 通过、10 项预期失败，Rust 759 通过、1 项原有性能探针忽略。同一节写明同源 Spectre 配对还没有做，这次合并不是对齐验收。

## 遗留与下一步

- #226、#227 仍开着。对应修复是草稿 [PR236](https://github.com/BucketSran/vaEVAS/pull/236) 和 [PR235](https://github.com/BucketSran/vaEVAS/pull/235)，未合并。
- #230 的修复已在 main。Issue 仍开着，阶段仍是 `stage:planned`。本条不关闭 Issue，也不改标签。
- [PR243](https://github.com/BucketSran/vaEVAS/pull/243) 开着，头 `48be0488`，从 `1639384e` 拉出，356 个文件。当前 main 已是 `2a790344`。它是 IR33 统一候选，尚未合并。本地诊断数字不写入本条。
- #214 仍暂停。21 道 Spectre 必跑题仍未作为本条的新结果。

## 相关链接

- PR224：https://github.com/BucketSran/vaEVAS/pull/224
- PR228：https://github.com/BucketSran/vaEVAS/pull/228
- PR234：https://github.com/BucketSran/vaEVAS/pull/234
- PR237：https://github.com/BucketSran/vaEVAS/pull/237
- PR238：https://github.com/BucketSran/vaEVAS/pull/238
- PR239：https://github.com/BucketSran/vaEVAS/pull/239
- PR240：https://github.com/BucketSran/vaEVAS/pull/240
- PR241：https://github.com/BucketSran/vaEVAS/pull/241
- PR242：https://github.com/BucketSran/vaEVAS/pull/242
- PR243：https://github.com/BucketSran/vaEVAS/pull/243
- Issue226：https://github.com/BucketSran/vaEVAS/issues/226
- Issue227：https://github.com/BucketSran/vaEVAS/issues/227
- Issue230：https://github.com/BucketSran/vaEVAS/issues/230
- 能力目录：repo:evas/capabilities/README.md
