---
date: 2026-09-28
categories:
  - EVAS
  - 项目
slug: bootstrap-validation-static-kernel
---

# 仓库起步：独立验证基线、四后端对照与 EVAS 0.2.0 静态仿射内核

仓库初始化次日合入 main 的一组 PR：31 个开发条件的独立验证契约与四后端基线（248 条配置记录，属历史有限观测，不是新内核成绩），以及只做静态求解的 EVAS 0.2.0 / IR v2 内核（31 条件中 9 条可编译、22 条明确拒绝）。

<!-- more -->

## 做了什么

- **独立验证基线（#1）**：建立不依赖 EVAS 实现的验证契约、判定器和四后端基线。31 个开发条件 = 14 个原 v1 条件 + 1 个标准数组低通修订 + 7 张补充卡展开的 16 个新条件。同一 DUT 和数学刺激在 Spectre、旧 EVAS 0.8.7、OpenVAF-R＋ngspice、Gnucap 上各跑两档设置，共 248 条配置记录；失败、不支持和未决结果都保留；`validation-v1` 标签及原始输入快照保持不变。
- **静态仿射内核（#2）**：把语言处理、方程组装和数值求解分开。Python 把限定的 Verilog-A 编成贡献 IR，Rust 同时求解节点电压。支持静态仿射关系、多次贡献相加、非零参考、自反馈和跨实例反馈。版本固定为 EVAS 0.2.0 / IR v2。
- **#3 未合入 main**：#3 固定了参数边界和结构化支路身份。它的改动已完整并入 #2 的开发分支（保留提交 `b877e5b`），GitHub 因此把它标成 merged，但正文写明"没有合入 main"，只作为历史检查点保留。
- **仓库内 skill（#4）**：新增 `evas-develop`、`evas-validate`、`vaevas-review-pr`、`vaevas-prepare-pr` 四个 skill，并在 `AGENTS.md` 加路由索引。
- **分支约定（#5）**：改为以 main 为审过的基线，一个明确任务一个短期分支/PR，中间检查点用小提交记录。

## 结果与证据

#1 的四后端基线（历史运行的有限观测，完整观察资格仍为 I）：

| 后端 | 基础档 / 31 | 细化档 / 31 |
| --- | ---: | ---: |
| Spectre | 31 | 31 |
| 旧 EVAS 0.8.7 | 18 | 8 |
| OpenVAF-R＋ngspice | 16 | 16 |
| Gnucap＋modelgen-verilog | 17 | 16 |

- 这些不是新 EVAS 内核的成绩，没有速度排名；条件已用于诊断，属于开发回归，不能称为未见测试。
- #1 合并前复核：38 项测试通过；冻结 v1 的 36 个历史 Git 工件、4 个快照工件、13 个原运行输入身份一致。没有重新跑四后端成绩。
- #2：33 项 EVAS unittest、Rust 格式和 warnings-as-errors 检查通过。`b877e5b` 记录 9 条件 × 两档、396,018 个静态点满足原独立判据。33 是测试方法数，31 是独立条件数；静态回放不代表瞬态资格。

## 遗留与下一步

- #2 不含时间推进、事件、动态算子或非线性求解，也没有替换旧 EVAS 0.8.7、没有部署到课题组服务器；这些语义扩展另开 PR（见后续"首批动态算子"条目）。
- 同日新建 [Issue #9](https://github.com/BucketSran/vaEVAS/issues/9) 跟踪稀疏排序与分解成本。
- 原始波形、日志和机器配置不进入 Git。

## 相关链接

- [PR #1 test: establish independent validation and four-backend baseline](https://github.com/BucketSran/vaEVAS/pull/1)
- [PR #2 feat(evas): add verified static affine kernel with IR v2](https://github.com/BucketSran/vaEVAS/pull/2)
- [PR #3 feat(evas): stabilize static contracts with IR v2](https://github.com/BucketSran/vaEVAS/pull/3)（未合入 main）
- [PR #4 chore: add repo-local EVAS development and review skills](https://github.com/BucketSran/vaEVAS/pull/4)
- [PR #5 docs: use main as the baseline for short-lived task branches](https://github.com/BucketSran/vaEVAS/pull/5)
- 当前入口：[独立验证说明](repo:evas/validation/README.md)、[EVAS 使用说明](repo:evas/README.md)、[仓库 skill](repo:.agents/skills)
