# vaBench v4

vaBench v4 以 400 个电路家族为单位，每个家族派生出 DUT、testbench、bugfix 三种题，共 1200 题。本仓库保存了最后一个发布快照 r53。课题组现在用来回归测试 EVAS 的 "400 个原题"，就是 r53 里的 400 道 DUT 题。

## 1. 身份

| 项 | 值 | 来源 |
| --- | --- | --- |
| 来源仓库 | <https://github.com/Arcadia-1/behavioral-veriloga-eval>，目录 `benchmark-vabench-release-v4/` | [historyref README](repo:benchmark/material/historyref/README.md) |
| 来源快照 commit | `7b5616dc52195ec275ec6d21c71d7763613702cd`（2026-07-28）。这个提交本身就是 r53 的发布提交："Promote r53 on EVAS 0.8.7 (#507)" | 同上；来源仓库提交历史 |
| 更早的发布 | 来源仓库标签 `v4-r44`（`ed20fd2071b2`）和 `v4-r45`（`1e2917267b1a`），都在 2026-07-18 | 来源仓库标签 |
| 迁入本仓库 | 2026-10-03，commit `6d806a0400af1f4693bce59a6e14fdae95a4180d`；2026-10-15 commit `fae1bac2` 移到现路径 `benchmark/material/historyref/v4/` | `git log --follow` |
| 发布快照 | `release/benchmarkv4-r53`，`release_revision` = `r53`，`immutable` = `true`，`release_status` = `r53_immutable_source_certification_reused` | [RELEASE_SEAL.json](repo:benchmark/material/historyref/v4/release/benchmarkv4-r53/RELEASE_SEAL.json) |
| 封印文件 SHA256 | `RELEASE_SEAL.json` 本身：`f5614d08eca5e45a0b52ecb6823625cae63e2b61a9831c79d2e60accbb2d9b82` | 2026-10-22 对 origin/main 计算 |
| 封印核对 | 封印列出的 7 个产物（`AUDIT_REPORT.json`、`MANIFEST.json`、`RUNTIME_INGESTION_EVIDENCE.json`、`TASK_INDEX.json`、`prompt_modes/manifest.json`、`prompt_modes/modes.json`、`skills/SNAPSHOT_MANIFEST.json`）和 `EXPERIMENT_POLICY.json` 的 SHA256，在 origin/main 上逐一重算，**全部一致** | 2026-10-22 重算 |
| 绑定的仿真器 | 封印的 `runtime_requirements` 写 `evas-sim` **0.8.7**。但 gold 和负例的认证不是在 0.8.7 上做的：r53 按哈希复用了来源认证（`simulation_rerun_required_for_materialization` = `false`）。最近一次实跑认证是 R45，用的是 EVAS **0.8.3** | [R53 认证](repo:benchmark/material/historyref/v4/R53_RELEASE_CERTIFICATION.md)、[R45 认证](repo:benchmark/material/historyref/v4/R45_RELEASE_CERTIFICATION.md) |
| Spectre | r53 门禁不含 Spectre，也没有跑（R53 认证文档原文："Spectre is not part of the r53 gate and is not run"）。需求文档规定 Spectre 只能做不阻塞的对照研究 | 同上；[需求文档 §3 第 7 条](repo:benchmark/material/historyref/v4/V4_TRI_FORM_BENCHMARK_REQUIREMENTS.md#3-core-design-decisions) |

R45 认证记录（[R45_RELEASE_CERTIFICATION.md](repo:benchmark/material/historyref/v4/R45_RELEASE_CERTIFICATION.md)）：EVAS 0.8.3、`evas2` 引擎，gold 400/400 通过，2000/2000 个变异体被检出。

## 2. 构成

**题目单位**：电路家族（circuit-function family）。每个家族派生三种题（[需求文档 §2](repo:benchmark/material/historyref/v4/V4_TRI_FORM_BENCHMARK_REQUIREMENTS.md#2-benchmark-unit-and-numbering)）：

| 形式 | 编号 | 派生规则 | 要交的东西 |
| --- | --- | --- | --- |
| DUT | 001–400 | 家族本身 | Verilog-A 模型（单文件或多文件） |
| Testbench | 501–900 | DUT 编号 + 500 | 一个 Spectre 兼容的 `.scs` 测试台 |
| Bugfix | 1001–1400 | DUT 编号 + 1000 | 修好的 Verilog-A 模型 |

例：家族 `001` 对应 DUT `001`、testbench `501`、bugfix `1001`。401–500、901–1000、1401–1500 保留不用。需求文档要求：1200 题分别计分，但不能说成 1200 个独立电路家族，因为同一家族的三种题在统计上相关。

**计分口径**（[需求文档 §18 Reporting](repo:benchmark/material/historyref/v4/V4_TRI_FORM_BENCHMARK_REQUIREMENTS.md#18-reporting)，三种形式分开报告）：

- DUT：完整合同通过率（按题 0/1）。
- Testbench：满分通过率。测试台要合法、能让正确 DUT 通过，并且在行为上检出全部 5 个负例 DUT，才算通过。
- Bugfix：完整合同修复通过率。
- 判分器是 release 钉住的 strict EVAS，不用 Spectre。

**本仓库保存了什么**（约 194 MB）：

- 全部 SOP、需求、认证文档（R44、R45、R52、R53），以及 `provenance/`、`evidence/`、`operations/`、`runners/`、`schemas/`、`scripts/`、`reports/`、`public-agent-runtime/`。
- `release/benchmarkv4-r53/`：`tasks/` 下 1200 个题目目录（DUT、testbench、bugfix 各 400），外加封印、manifest、任务索引、prompt 模式和技能快照。
- `provenance/dut-base-v3-exact-five-hash-bound-v2/`：400 个家族的 DUT 基底，每个家族带 5 个变异体（"exact-five"）。

**没迁入**：`release/benchmarkv4` 基线和 r45–r52 共 9 个累积快照里的 8 个（约 1 GB，内容大量重复）。需要时去来源仓库 `7b5616dc` 取。

**"400 个原题"就是 r53 的 DUT 题**：已核对。EVAS 回归测试的 400 个 case 中，每个 case 的 `INPUT_IDENTITY.json` 都把 `original_task` 指向 `benchmarkv4-r53/tasks/<001–400>-*`，编号与 `family_id` 一一对应；`SOURCE_IDENTITY.json` 的范围说明是 "400 v4 r53 DUT-family gold solutions against their unchanged trusted replay test decks"。抽查 001：deck 和 gold 的 SHA256 与 r53 原件一致。本地证据：`current/runs/v4-gold-main-20261016-232304/`。

### 来源记录

v4 没有记录 gold 模型的真实来源，也就是它来自 Cadence 库还是课题组用过的某个文件。每个家族在 DUT 基底的 `task_record.json` 里有一个 `source_slug` 字段，但它记的是家族从哪道 v3 题来，不是电路模型从哪里来。核对结果（2026-10-22）：

- 400 个家族里，34 个的 `source_slug` 与家族目录名完全相同；366 个不同，通常只差编号（例如家族 `014-segmented-dac` 的 `source_slug` 是 `015-segmented-dac`）。
- 400 个 `source_slug` 中，280 个能在来源快照 `7b5616dc` 的 v3 任务目录名里找到。

所以，要追到真实来源，只能借 v3 的导入记录（[SOURCES.md](repo:benchmark/material/historyref/veriloga/SOURCES.md)）。纯化 pilot 的预匹配结果：

| v4 家族 | 数量 |
| --- | ---: |
| 通过 v3 导入记录链接到已恢复的原始文件 | 97 |
| 有导入记录，但原始文件未恢复 | 43 |
| 没有链接 | 260 |

本地证据：`current/runs/historical-purification-20261022/evidence/prematch.json`。

??? info "纯化 pilot（2026-10-22）：在做什么、到哪一步"
    本地证据：`current/runs/historical-purification-20261022/`（`pilot-report.html`、`pilot.json`、`reviews/`、`reviews2/`）。

    - **两种价值**：practicalwork 看 gold DUT 有没有真实来源，即 Cadence 库或课题组真实用过的 Verilog-A；theorywork 看任务定义和工程价值是否清楚。一个家族可以两样都有。
    - **来源分级**：P3 逐字、P2 改编，这两级计入；P1 存疑、P0 无，这两级不计入。P0 的意思是"没找到证据"，不是"证明原创"。
    - **试点规模**：14 个家族（10 个 v4、3 个 v1、1 个对照），每个家族由 5 个模型独立审查（DeepSeek、Opus、Sonnet、GLM、Kimi）。报告汇总：来源维度"否"7、"分歧"1、"是"6；任务维度"分歧"5、"是"9。
    - **结论**：来源分级在不同模型之间一致性好；theory 的评分标准还不能用。这一条是主会话的判断，本页没有独立复核。
    - **全量纯化尚未运行**。来源分级是资产属性，不是题目缺陷，不进勘误表。

### 当前 EVAS 与 Spectre 在这 400 题上的情况

| 仿真器 | 通过数 | 证据 |
| --- | ---: | --- |
| legacy EVAS 0.8.3（R45 认证版） | 399/400，唯一失败 102 | `current/runs/issue214-claude-20261021/legacy-087/RESULTS-0.8.3.json` |
| legacy EVAS 0.8.7（r53 绑定版） | 393/400：027、057、102、178、185、186 报错，346 判失败 | `.../legacy-087/RESULTS-0.8.7.json` |
| 重建后的 EVAS（main，2026-10-21） | 342/400 | `current/runs/issue214-claude-20261021/m12-main.log` |
| 重建后的 EVAS（main `6f3a6b54`，2026-10-22，PR220 之后） | 343/400 | `current/runs/issue214-claude-20261021/m14-final2.log` |
| Spectre | 只有约 10 题有记录在案的运行 | 见下 |

各行 EVAS 结果都用同一套冻结 checker，由同一个本地 harness 运行。harness 只跑主 checker，网格未必与当年基准的 runner 完全一致（见 `legacy-087/README.md`）。

!!! warning "legacy EVAS 通过不等于 Spectre 通过"
    两个 legacy 版本与当前 EVAS 同源，结果一致不能证明正确。据主会话统计，400 题里只有约 10 题有记录在案的 Spectre 运行：091、320、261–264、267、271、275、276。本页只核到 261–264、267 的历史 Spectre 结论（`current/runs/evas-source-shape-20261017/overnight-integer-20261018/issue214-checker-spectre-pilot-20261020/execution/analysis/REPORT-final.md`），其余题号**未核实**。

当前 EVAS 剩下的 57 题属于 EVAS 引擎的工作（Issue214），本身不是 v4 的勘误。只有能归因到题目材料，或经审计判定归 EVAS 修的题，才进下面的表。

## 3. 已知问题（勘误表）

主要证据是 2026-10-22 的 checker 审计：`current/runs/issue214-claude-20261021/checker-audit/FINDINGS.md`。该文件经过两位独立核验，以它为准；`FINDINGS.draft1.md` 是被推翻的初稿。审计全程没有改原件：原题文件的 SHA 与 `INPUT_IDENTITY.json` 逐一核对，0 个不一致。审计没有用 Spectre。

Spectre 清单是 `checker-audit/spectre-manifest.json`：`needed` 21 题（审计列出的 20 题，加上用户 2026-10-22 决定补充的 140 零边沿探针），`optional` 79 题。

| 编号 | 题号 | 问题 | 证据 | 状态 | 修订位置 |
| --- | --- | --- | --- | --- | --- |
| v4-E001 | 137 | checker 平局：低钳位点的 target 恰为 −0.4，靠浮点值 −0.4000000000000001 才被计为"低"。去掉低钳位的变异体仍然通过 | FINDINGS 一.5；核验 B 独立得出。按审计的协议，真伪靠算术判断，Spectre 帮不上 | 已确认 | 见表后说明 |
| v4-E002 | 142 | checker 用 `int()` 截断，实数转整数应四舍五入。两个引擎实测的 DUT 输出都是对的 | FINDINGS 一.5；核验 B | 已确认 | 见表后说明 |
| v4-E003 | 179 | checker 的 `_trace_time_scale` 根据 vout 行的跨度估计时间尺度，时间扰动会让估值从 1.0 变成 1.5 | FINDINGS 一.5；核验 B | 已确认 | 见表后说明 |
| v4-E004 | 226 | checker 用 `sigin − previous > 0.05` 判断升降沿。网格越密，相邻两行的差越小，上升沿就看不到了 | FINDINGS 一.2；核验 A 人工核对。该题也在 Spectre 清单里，Spectre 结果只回答原 gold 在 Spectre 下过不过，不影响这条缺陷的认定 | 已确认 | 见表后说明 |
| v4-E005 | 058 | checker 每个 key 只保留最后一行。网格加密后，这一行可能落在跳变中途 | FINDINGS 一.2；核验 A 人工核对。说明同 E004 | 已确认 | 见表后说明 |
| v4-E006 | 全部 400 题 | 400 个 deck 都没有指定输出时刻（无 `strobeperiod`），写哪些行完全由仿真器决定。已证实"读到哪些行"会改变判定的有 8 题：012、058、075、077、226、247、330、366 | FINDINGS 一.2、一.3。做法是把细网格结果删回原行集，判定随之恢复 | 已确认 | 尚无。审计在当前引擎上加过 `strobeperiod`，被证明会掩盖缺陷，不能当修复，见 E026 |
| v4-E007 | 全部 | r53 封印绑定 `evas-sim==0.8.7`，但 gold 和负例的认证是按哈希复用的，最近一次实跑是 R45，用的是 0.8.3。r53 门禁也没有跑 Spectre | `RELEASE_SEAL.json` 的 `certification_reuse` 与 `runtime_requirements`；R53、R45 认证文档 | 已确认 | 不适用（发布元数据，修订版须写明自己绑定的仿真器和实跑证据） |
| v4-E008 | 027、057、102、178、185、186、346 | 本地 harness 下，legacy 0.8.7 有 6 题报 `rust_lower` 错误、346 判失败；legacy 0.8.3 有 102 失败（`same_seed_sequence_mismatch`），与 R45 的 400/400 不符 | `legacy-087/RESULTS-0.8.7.json`、`RESULTS-0.8.3.json`；harness 与基准 runner 不完全相同（`legacy-087/README.md`） | 进行中 | 尚无。先查清是 harness 差异还是发布绑定的问题 |
| v4-E009 | 059 | 核验 B 逐题审查后认为 gold 本身做了两次舍入 | FINDINGS 三（注）、五.4。只有一位核验看过。题在 Spectre 清单里，但审计的协议写明 059 的真伪靠算术或 LRM 判断，Spectre 帮不上 | 进行中 | 尚无 |
| v4-E010 | 012 | 当前引擎比 legacy 少写 102 行（事件时刻、transition 斜坡点、`$bound_step` 点），两版判定相反：legacy 通过，当前失败 | FINDINGS 一.4；当前引擎没有写出任何 legacy 没有的行 | 归 EVAS 修 | EVAS 侧 |
| v4-E011 | 075 | 当前引擎少写 93 行，判定与 legacy 相反 | FINDINGS 一.4 | 归 EVAS 修 | EVAS 侧 |
| v4-E012 | 077 | 当前引擎少写 213 行，判定与 legacy 相反 | FINDINGS 一.4 | 归 EVAS 修 | EVAS 侧 |
| v4-E013 | 079 | 当前引擎少写 75 行，只写了 0、20n、34n 三行，忽略了模型里的 `$bound_step(0.5n)` | FINDINGS 一.4 | 归 EVAS 修 | EVAS 侧 |
| v4-E014 | 075 | 与 E011 无关的另一个平局：规格要求严格大于，但 10.5 ns 不能用浮点精确表示，两个引擎的噪声符号相反（+2.3e-15 / −7e-16），没有唯一的分支。审计认为完整修复要把 rst 沿移离 500p 网格，并给 checker 阈值加保护带 | FINDINGS 四（核验 B） | 待 Spectre | 尚无 |
| v4-E015 | 081 | 微小扰动会翻转判定（TIE_HARMFUL）；网格敏感只在不合法的 RMIN 变体下出现。注意：该题的输入是刻意设成相等的，不能把刺激挪离平局 | FINDINGS 三、五；`spectre-manifest.json` | 待 Spectre | 尚无 |
| v4-E016 | 170 | TIE_HARMFUL，尚未逐题做语义核验 | FINDINGS 三（注） | 待 Spectre | 尚无 |
| v4-E017 | 189 | TIE_HARMFUL，尚未逐题核验。输入是刻意设成相等的 | FINDINGS 三、五 | 待 Spectre | 尚无 |
| v4-E018 | 245 | TIE_HARMFUL，尚未逐题核验 | FINDINGS 三（注） | 待 Spectre | 尚无 |
| v4-E019 | 247 | checker 判定随输出行集改变（GRID_CHECKER_STRONG），尚未人工核对是不是 checker 缺陷 | FINDINGS 一.2 | 待 Spectre | 见表后说明 |
| v4-E020 | 330 | 同 E019 | FINDINGS 一.2 | 待 Spectre | 尚无 |
| v4-E021 | 346 | TIE_HARMFUL；legacy 0.8.7 在原 deck 上就判失败（`mismatch_count=5`），0.8.3 通过 | FINDINGS 三；`RESULTS-0.8.7.json` | 待 Spectre | 尚无 |
| v4-E022 | 347 | TIE_HARMFUL；两版 EVAS 在共同时刻写出的值不同（从 `rst_n_core` 开始），判定相反 | `spectre-manifest.json`（标签 SIMDIFF） | 待 Spectre | 尚无 |
| v4-E023 | 360 | TIE_HARMFUL，尚未逐题核验 | FINDINGS 三（注） | 待 Spectre | 尚无 |
| v4-E024 | 366 | GRID_CHECKER_STRONG；波形对平局敏感，但两个分支 checker 都判通过 | FINDINGS 一.2；`spectre-manifest.json` | 待 Spectre | 尚无 |
| v4-E025 | 140 | 零边沿 `transition(x,0,0,0)`、且没有 `default_transition` 时，边沿时间怎么定？当前 EVAS 拒绝这种写法，legacy 通过。用户 2026-10-22 决定先看 Spectre 怎么处理；EVAS 侧不实现，保持拒绝 | `spectre-bundle/140-zero-edge-probe/README.md`（18 个探针 deck 加原题 deck） | 待 Spectre | 尚无 |
| v4-E026 | 079 | **已撤回**：初稿给 079 的 deck 加 `strobeperiod` 作为修复。撤回原因：删掉模型里的 `$bound_step` 得到缺陷模型，它在当前引擎加 strobe 后**通过**，说明这个修复会掩盖题目要考的 `$bound_step` | FINDINGS 二；`checker-audit/repaired/_WITHDRAWN/079/WITHDRAWN.md`；核验 A 发现，主会话复现 | 已撤回 | — |
| v4-E027 | 075、243、306、378、400 | **已撤回**：初稿称"`vth` 挪 1e-9 判定就翻转，说明 gold 靠平局通过"。撤回原因：075、243、306、378 的 checker 把阈值硬编码为 0.45，审计只挪了 DUT 的 `vth`，是审计自己造成两边不一致。同步挪动 checker 阈值后，翻转全部消失。`DUT_PARAM_FRAGILE` 标签作废 | FINDINGS 二（核验 B 实测；主会话读过 checker 源码确认） | 已撤回 | — |
| v4-E028 | 017、206、214、218、325 | **已撤回**：初稿称这些题在 SP/SM 扰动下翻转。撤回原因：这些 deck 刻意让两个输入相等（例如 017、206 都是 `vinp=vinn=0.45`）。SP/SM 给每个源乘上不同的系数，打破了相等，等于改了测试。保持相等时两个引擎都通过 | FINDINGS 二（核验 B；主会话读 deck 确认） | 已撤回 | — |
| v4-E029 | 012、077、079 | **已撤回**：初稿称这三题是 checker 缺陷。撤回原因：证据指向当前引擎少写行，改归 EVAS 修，见 E010、E012、E013 | FINDINGS 二（核验 A） | 已撤回 | — |
| v4-E030 | 060 | **已撤回**：初稿称 060 是舍入平局。撤回原因：060 没有任何判定翻转，说法没有数据支持 | FINDINGS 二（核验 A） | 已撤回 | — |
| v4-E031 | 021 022 030 033 035 079 081 088 302 320 358 361 364 | **已撤回**：初稿把 21 题归为网格敏感 checker（GRID_CHECKER）。撤回原因：其中这 13 题只在 RMIN 变体下翻转，而 RMIN 会删掉事件行和拐点，不是合法网格。这 13 题现单列为 `GRID_CHECKER_RMIN_ONLY`，未证实；成立的只有 E006 列出的 8 题 | FINDINGS 二（核验 A） | 已撤回 | — |

**表后说明（修订位置的详细情况）**

- **v4-E001**：尚无修订版。后续（未定论）：修订 checker 那一路的 `current/runs/issue214-claude-20261021/checker-audit/revised-checkers/REPORT.md` 把 137 判为**测试台缺陷**：0–40 ns 内目标值最小恰为 −2/5，低钳位从未被激励，所以不改 checker；要修只能改 deck（推断，未跑）。审查 A 用有理数运算独立确认，审查 B 未回
- **v4-E002**：尚无修订版。修订 checker 草稿已出（改为按 LRM 四舍五入），审查 A 判 SAFE，审查 B 未回，未定论（`current/runs/issue214-claude-20261021/checker-audit/revised-checkers/REPORT.md`）
- **v4-E003**：尚无修订版。修订 checker 草稿已出（时间尺度固定为 1.0），审查 A 判 SAFE，但对原作者的设计意图有分歧；审查 B 未回，未定论（`current/runs/issue214-claude-20261021/checker-audit/revised-checkers/REPORT.md`）
- **v4-E004**：尚无修订版。修订 checker 草稿已出（改为滞回判沿），审查 A 判 SAFE，审查 B 未回，未定论（`current/runs/issue214-claude-20261021/checker-audit/revised-checkers/REPORT.md`）
- **v4-E005**：尚无修订版。后续（未定论）：修订 checker 那一路给 058 做的修订版**已作废**（`current/runs/issue214-claude-20261021/checker-audit/revised-checkers/REPORT.md`，主会话已复现）：把金标里的 `> vth` 全改成 `> 0.3` 得到错误 DUT，原 checker 判 FAIL，修订版却判 PASS。审查 A 提了新改法，尚未采纳，审查 B 未回
- **v4-E019**：尚无。修订 checker 那一路顺带出了草稿（改为滞回判定），审查 A 判 SAFE，审查 B 未回，未定论（`current/runs/issue214-claude-20261021/checker-audit/revised-checkers/REPORT.md`）

!!! note "关于"无任何标记"的 244 题"
    审计里有 244 题没有任何标记，但这**不等于** checker 正确。其中 88 题没有 `vth` 类参数可以扰动；25 题至少有一个仿真器拒绝了原 deck；102、186 两个仿真器都拒绝，等于没测；080、147、187、195、202 这 5 题的 deck 没有电压源，无法扰动（FINDINGS 三）。另有 79 题列为可选 Spectre，只有波形层面的迹象，未登记为勘误。

## 4. 修订版

尚无修订版。

修订版 checker 正在另一个会话里制作：放在新目录，原件只读，尚未完成。截至 2026-10-22，那一路的报告（`current/runs/issue214-claude-20261021/checker-audit/revised-checkers/REPORT.md`）自己注明"未经独立审核，不可视为定论"：142、179、226、247 有修订草稿；137 不改 checker；058 的修订已作废；330、366、012、075、077、079 不修。完成并登记后，按[维护原则](index.md#维护原则)发布为新的修订版本号，例如 `v4-r53-e1`。修订版只收改动过的题，每题写明对应的原件路径、原件 SHA256，以及解决了哪几条勘误。勘误表"修订位置"一栏同时更新。
