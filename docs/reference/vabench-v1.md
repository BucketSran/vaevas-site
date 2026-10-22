# vaBench v1

vaBench 第一版发布包（`benchmark-vabench-release-v1`）。本仓库原样保存了来源快照里的 v1 目录，但这个目录本身不完整：manifest 列了 86 项、300 个 form，目录里只有 79 项、271 个 form。

## 1. 身份

| 项 | 值 | 来源 |
| --- | --- | --- |
| 来源仓库 | <https://github.com/Arcadia-1/behavioral-veriloga-eval>，目录 `benchmark-vabench-release-v1/` | [historyref README](repo:benchmark/material/historyref/README.md) |
| 来源快照 commit | `7b5616dc52195ec275ec6d21c71d7763613702cd`（2026-07-28） | 同上 |
| 包内日期与状态 | `MANIFEST.json`：`date` = 2026-06-23，`status` = `in_progress`；`score_denominator_manifest.json`：`status` = `score_enabled` | [MANIFEST.json](repo:benchmark/material/historyref/v1/MANIFEST.json) |
| 迁入本仓库 | 2026-10-03，commit `6d806a0400af1f4693bce59a6e14fdae95a4180d`（当时路径 `benchmark/reference/v1/`）；2026-10-15 commit `fae1bac2` 移到现路径 | `git log --follow` |
| 现路径 | `benchmark/material/historyref/v1/`，约 23 MB | [v1 README](repo:benchmark/material/historyref/v1/README.md) |
| 封印 / SHA | 包内没有封印文件，也没有逐文件 SHA 清单。身份只能用"来源 commit + 本仓库迁入 commit"认定 | — |
| 绑定的仿真器 | 包内文档写 EVAS 是正式判分器、Spectre 是可选的对照（[EVALUATOR.md](repo:benchmark/material/historyref/v1/EVALUATOR.md)）。**EVAS 和 Spectre 的版本号在包内均未记录**（在 v1 目录全文检索版本号，没有找到） | — |

!!! note "原样迁入是对的，包本身不完整"
    2026-10-22 用 GitHub API 列出来源快照 `7b5616dc` 的 `benchmark-vabench-release-v1/`：只有 `EVALUATOR.*`、`MANIFEST.*`、`README.md`、`evidence/`、`reports/`、`tasks/`，`reports/` 下 16 个文件，与本仓库一致。缺的东西在来源快照里本来就没有，不是迁入时丢的。

## 2. 构成

**题目单位**：一个"条目"（entry）是一个电路功能，例如 `vbr1_l1_clock_divider`；每个条目下有若干 form。form 有四种：`dut`（写模型）、`tb`（写测试台）、`bugfix`（修错误模型）、`e2e`（模型加测试台）。不是每个条目都有四种。

**数量**（manifest 声称）：

| 口径 | 条目 | form |
| --- | ---: | ---: |
| 核心（`track=core`，电路功能） | 73 | 265 |
| 辅助（`track=support`，测量 / 激励） | 13 | 35 |
| 合计 | 86 | 300 |

难度分级（条目）：D1 10、D2 50、D3 26。另有 4 个 L0 conformance 用例，不计分。数字来自 `MANIFEST.json` 的 `summary`。

**计分口径**：分母是 265 个核心 form（`counted_in_score=true`）；13 个辅助条目、35 个 form 单独报告，不进核心分数。判分以 `reports/score_denominator_manifest.json` 为准（[v1 README](repo:benchmark/material/historyref/v1/README.md)）。

**300 任务扩展面**：v1 README 另称有一个 `vabench-300-expansion/` 目录，把 300 个 form 都当作独立任务管理（271 个继承 v1 + 29 个 v1.1 新增），每个任务配 5 个"部分通过"负例，共 1500 个。**这个目录不在包内**，见勘误 `v1-E001`。

**本仓库实际保存了什么**（origin/main 上计数）：

| 内容 | 数量 |
| --- | --- |
| `tasks/` 下条目目录（10 个类别目录：CT01–CT08 核心，SUP01–SUP02 辅助） | 79 个条目 |
| form（以 `release_task.json` 计） | 271 个：dut 59、tb 79、bugfix 54、e2e 79 |
| `evidence/dual/` 双仿真结果 | 271 个 form 各有 `evas_result.json` 与 `spectre_result.json`（来源 rerun 目录名带 `20260526`） |
| `reports/` | 16 个文件：概览、认证矩阵、conformance、prompt 合同、计分分母 |
| 顶层 | `MANIFEST.*`、`EVALUATOR.*`、`README.md` |

**没迁入 / 包内不存在的**：`vabench-300-expansion/`、`conformance/`、`rerun_staging/`，以及 README 列为"事实来源"的 9 份报告（见 `v1-E002`）。

??? info "纯化 pilot 对 v1 的观察（2026-10-22，未定论）"
    本地证据：`current/runs/historical-purification-20261022/`（`pilot-report.html`、`evidence/prematch.json`）。

    - 预匹配脚本处理 v1 时只找到 79 个条目，与上面的计数一致。79 个条目都没有 v3 导入记录可链接到已恢复的 Verilog-A 原文件。
    - pilot 抽了 3 个 v1 条目（`vbr1_l1_first_order_lowpass`、`vbr1_l1_slew_rate_limiter`、`vbr1_l2_programmable_stimulus_sequencer`）。审查者在恢复库里没找到 gold 的来源，审查者原话是"未找到证据，不是证明原创"。
    - 这是来源分级，不是题目缺陷，不进勘误表。全量纯化尚未运行。

## 3. 已知问题（勘误表）

| 编号 | 题号 | 问题 | 证据 | 状态 | 修订位置 |
| --- | --- | --- | --- | --- | --- |
| v1-E001 | 7 个 `vbr11_*` 条目（共 28 form）+ `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:bugfix` | manifest 列 86 条目 / 300 form，包内只有 79 条目 / 271 form。缺的 29 个 form 都是**计入分数**的核心 form，路径指向包内不存在的 `vabench-300-expansion/proposed-tasks/...`。所以 265 个计分 form 里，本仓库能拿到资产的只有 236 个 | `MANIFEST.json` 的 `entries[].release_entry_manifest` 与 `forms[].release_task_manifest`；origin/main `tasks/` 下 79 个条目目录、271 个 `release_task.json`；来源快照 `7b5616dc` 的 v1 目录没有 `vabench-300-expansion/`；纯化 pilot 同样只找到 79 个条目 | 已确认 | 尚无 |
| v1-E002 | 全包 | 认证说法在包内无法复核。README 把 `claim_gate.json`、`dual_certification.json`、`completion_audit.json`、`artifact_index.json` 等列为事实来源，`MANIFEST.json` 的 `reports` 字段列了 10 份报告，其中 9 份包内没有（只有 `score_denominator_manifest.json`）。包内说法也互相矛盾：EVALUATOR.md 同时写"certified forms 300"和"v1.1 proposed pending forms 29"；README 一处说 29 个 v1.1 任务"在 static/EVAS/Spectre 证据齐全前仍待认证"，另一处说 300 个 form 全部双认证；MANIFEST `status` 为 `in_progress`，`claim_boundary` 里写 `release_status_planned_entries=79` | v1 [README](repo:benchmark/material/historyref/v1/README.md)、[EVALUATOR.md](repo:benchmark/material/historyref/v1/EVALUATOR.md)、`MANIFEST.json`；包内双仿真结果只有 271 个 form | 已确认 | 尚无 |

本页没有"待 Spectre""已撤回""归 EVAS 修""进行中"的条目。checker 审计和 legacy 差分都只针对 v4，没有覆盖 v1。

## 4. 修订版

尚无修订版。

如果以后要发 v1 修订版：v1 没有封印文件，修订版需要先记下原件的来源 commit 和每个改动文件的 SHA256，再按[维护原则](index.md#维护原则)放进新目录。
