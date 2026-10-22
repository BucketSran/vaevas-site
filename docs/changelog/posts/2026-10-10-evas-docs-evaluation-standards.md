---
date: 2026-10-10
categories:
  - 项目
  - EVAS
slug: evas-docs-evaluation-standards
---

# EVAS 文档重组：统一支持总表、核心条件重新取证与评测规范

2026-10-09 至 10-10 合入 5 个文档类 PR：EVAS 文档按阅读目的分层，`COMPARISON.md` 成为唯一支持总表；核心 12 条件重新取证后，EVAS 按 core-v1 判据计为 12 P（只覆盖规定的有限观测，不代表与 Spectre 全面对齐）；另补面向读者的评测标准，以及误差恢复和同精度性能比较的开发要求。

<!-- more -->

## 做了什么

- #120：把接口说明、数学原理、开发维护和历史证据分开，形成 `README`、`CAPABILITIES`、`UPDATE` 加 `reference/`、`math/`、`development/` 的目录。能力概览从 16,017 字符缩到 1,605 字符，根目录文件从 17 个收拢为 3 个，文档总数仍为 22 个。
- #121：把分散在 README、能力清单和历史比较表中的支持结论统一到 `evas/docs/COMPARISON.md`，按语言特性和算子展示四后端实测；补充 15 项专项模型、独立检查器和 27 条件 × 4 后端的精简证据。
- #122：在服务器重新构建 EVAS 并运行原 12 条核心条件，记录 cargo/rustc、Cargo.lock 和内核身份；另跑 Spectre 两项 17 位输出预检。
- #126：新增面向读者的评测标准说明，用采样保持解释误差依据；四个后端采用共同的外部精度要求，可各自选用预先规定的内部配置。
- #127：在验证规范中加入按误差来源选择恢复动作、验证下游效果的要求，并规定性能优化先测瓶颈、在固定工程精度下比较完整请求。

## 结果与证据

- #121：Gnucap 原有 13 项端点阻塞经补测确认为 dtmin 时间量化；调整时间分辨率后 9 通过、3 输出超差、1 输入异常，另有 2 项原编译失败。共 179 次配置尝试、108 个主比较位置，原失败和两档设置均保留。
- #121 时核心 12 条件仍为原 I/X；#122 重新取证后 EVAS 12 次执行全部完成，`core_report.py` 重算为 12 P。Spectre 两项预检仍为 I，缺失精确中心和 CP-02 终点未改写或放宽。
- 108 个主比较位置不变，含历史尝试共 193 个配置；原 48 槽、全部失败、22 条事件边界 I 与 8 条环回边界 I 保留。
- 这几项 PR 都没有修改 EVAS 编译器或求解器；#120 检查 4,943 个本地链接，新增断链 0，原有 8 处失效链接保留记录。
- #122 的审查记录在本地 `current/runs/core-evidence-20261009/review/`；完整 raw/build/log 为 local-only。

## 遗留与下一步

- #126：具体数值门槛、配置和检查器尚未定稿，当前表格成绩和旧 checker 范围保持不变。
- #127 保留 #57～#59 的延期决定和重新选题条件。
- 事件、transition 和 VCO 边界差异继续在支持表中可见；#96、#119 继续开放。

## 相关链接

- PR：[#120](https://github.com/BucketSran/vaEVAS/pull/120)、[#121](https://github.com/BucketSran/vaEVAS/pull/121)、[#122](https://github.com/BucketSran/vaEVAS/pull/122)、[#126](https://github.com/BucketSran/vaEVAS/pull/126)、[#127](https://github.com/BucketSran/vaEVAS/pull/127)
- Issue：[#96](https://github.com/BucketSran/vaEVAS/issues/96)、[#119](https://github.com/BucketSran/vaEVAS/issues/119)
- 仓库：[EVAS 文档入口](repo:evas/docs/README.md)、[支持总表](repo:evas/docs/COMPARISON.md)、[评测方法说明](repo:evas/docs/COMPARISON-METHODOLOGY.md)、[验证规范](repo:docs/contributing/validation.md)
