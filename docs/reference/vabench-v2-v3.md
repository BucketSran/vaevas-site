# vaBench v2 与 v3

v2 和 v3 都**没有迁入**本仓库。v2 只存在了两天，是一个 5 题的格式样本；v3 是 v1 之后、v4 之前来源仓库的"现行题集"。本仓库只用到了 v3 的导入记录，用来追溯原始 Verilog-A 文件的来源。

两版共用一页，原因是：两者都没有本地原件，本页只能记录身份和去向，内容不足以各成一页。

## 1. 身份

| 项 | v2 | v3 |
| --- | --- | --- |
| 来源目录 | `benchmark-vabench-release-v2/` | `benchmark-vabench-release-v3/` |
| 来源仓库 | <https://github.com/Arcadia-1/behavioral-veriloga-eval> | 同左 |
| 引入 | commit `c48c8bb816b32d23b2bb8441ac77ace3acb5b79e`（2026-06-24，"Introduce v2 benchmark release layout"） | 来源仓库里修改 v3 README 的最早一次提交是 `55b216b1`（2026-06-24）。v3 目录的首次提交**未核实** |
| 结束 | commit `5171f4c14831fbc0df8923329aaeffaf20d85e64`（2026-06-26，"Retire v2 and clarify active benchmark layout"）删除 | 在迁入快照 `7b5616dc`（2026-07-28）里，来源仓库根 README 仍把 v3 写成 "active task release" |
| 本仓库是否迁入 | 否 | 否（[historyref README](repo:benchmark/material/historyref/README.md)：完整包未迁入） |
| 本地副本 | `current/runs/historical-purification-20261022/recovered/v2/benchmark-vabench-release-v2/`（纯化 pilot 恢复的副本，80 个文件，与 `c48c8bb8` 改动的文件数相同；未跟踪，本页未逐字节核对） | 本机旧仓库 clone `legacy/behavioral-veriloga-eval/`，HEAD 为 `fc1f3b36`（2026-07-25），**不是**迁入快照 `7b5616dc` |
| 封印 / SHA | 无 | 包内未见封印。本页未核实 |
| 绑定的仿真器 | 未记录（引入提交的说明写"未做全量 Spectre 认证"） | 根 README 写"用 pinned strict EVAS 作正式判分器，Spectre 只作可选对照"，版本号**未核实** |

## 2. 构成

### v2

数字来自本地恢复副本的 `MANIFEST.json`（`date` 2026-06-24，`status` = `under_construction`）：

- 5 个条目，每个条目 1 个 form，共 5 个 form；核心 4、辅助 1。
- 5 个条目都沿用 v1 的条目名，例如 `vbr1_l1_first_order_lowpass`、`vbr1_l2_weighted_sar_adc_dac_loop`。
- `final_score_enabled_form_count` = 0：**v2 从来没有开启计分**。5 个 form 都在等新的双仿真认证。
- 引入提交的说明把 v2 定位为"文件格式与打包"评审，明确说不要把这 5 题当成最终的 300 题发布。

去向：来源仓库根 README（快照 `7b5616dc`）写明，这 5 题已并入 v3，编号 `283`–`287`。快照里 v3 的这 5 个目录是 `283-weighted-sar-adc-dac-loop`、`284-window-comparator-testbench`、`285-dual-track-sample-hold`、`286-first-order-lowpass-bugfix`、`287-gain-extraction-flow`（目录名来自本机 clone `fc1f3b36`。并入关系按 README 说法记录，本页没有逐题核对内容）。

### v3

数字来自快照 `7b5616dc` 的 `benchmark-vabench-release-v3/README.md` 和 `TASKS.json`：

- **题目单位**：一个带编号的独立任务（`tasks/NNN-name/`），不再像 v1 那样按"条目 + form"组织。每题自带 `instruction.md`、`starter/`、`test_visible/`，以及仅评估端可见的 `test_hidden/`、`solution/`、`negative_variants/`。
- **数量**：`tasks/` 下 001–505 共 505 题（`TASKS.json` 也是 505 条）。另有 54 题因为 Spectre 原样拒绝，归档在 `spectre-unsupported-tasks/`，不进默认分母。
- **分段**：001–300 是"原始已认证的 full-300 面"，其中 001–049、080–089 从 v1 迁来；301–505 是语言扩展候选，按 README 的说法需要单独认证后才能进全集统计。
- **计分口径**：README 说默认 `tasks/` 树就是与 Spectre 兼容的分母。逐题的计分规则本页**未核实**。

### 本仓库用了 v3 的什么

- **导入记录**：[veriloga/SOURCES.md](repo:benchmark/material/historyref/veriloga/SOURCES.md) 根据来源仓库 commit `af6bb188d74762812cde3370f0477046d2476410` 的 v3 导入审计，整理出 184 条任务记录，对应 169 个历史路径、33 个用户目录。这些记录把 v3 的 `NNN-source-*` 任务名连回课题组服务器或 Cadence 安装库里的原始文件。
- **与 v4 的关系**：v4 的 DUT 基底目录名为 `provenance/dut-base-v3-exact-five-hash-bound-v2/`，v4 每个家族的 `task_record.json` 里有一个 `source_slug` 字段，值是一个 v3 风格的任务名。400 个值里有 280 个能在快照 `7b5616dc` 的 v3 任务目录名中找到，其余 120 个找不到（推断：v3 后来因 issue #109 改过编号，未核实）。详见 [v4 页](vabench-v4.md#2-构成)。
- **纯化 pilot**：用 v3 导入记录给 v4 家族找原始文件，见 [v4 页](vabench-v4.md)。

## 3. 已知问题（勘误表）

| 编号 | 题号 | 问题 | 证据 | 状态 | 修订位置 |
| --- | --- | --- | --- | --- | --- |
| — | — | 尚无登记 | — | — | — |

v2 和 v3 都没有本地原件，checker 审计、legacy 差分和纯化 pilot 都没有直接审查 v2/v3 的题目。以后登记时分别用 `v2-E001`、`v3-E001` 起编。

!!! warning "登记前先固定原件身份"
    v2、v3 不在本仓库。登记勘误前，先写明依据的是哪个来源 commit 下的哪个文件（例如 `7b5616dc:benchmark-vabench-release-v3/tasks/153-.../solution/...`），并记录该文件的 SHA256。本机 clone 的 HEAD（`fc1f3b36`）与迁入快照不同，不能混用。

## 4. 修订版

尚无修订版。v2 已在来源仓库退役；v3 如需修订，先按上面的方法固定原件身份。
