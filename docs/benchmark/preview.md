# Benchmark：预览版本

!!! danger "预览，未录取，成绩不可引用"
    正式清单 [`benchmark/tasks/benchmark.toml`](repo:benchmark/tasks/benchmark.toml) 当前为空：`tasks = []`，`state = "draft"`。

    下面列出的 {{ bench_drafts }} 个题包**全部是草稿**，没有一道通过本版人工题目审核。一道题有参考解、跑通过仿真或已合入 main，都不等于录取。不要把这里的题目当作正式 benchmark，也不要引用任何基于它们的成绩。

**数据来源**：每次构建网站时从 main@{{ main_short }}（提交日期 {{ main_date }}）自动生成下面的计数和逐题表。题目清单取自草稿批次目录，名称和电路功能组取自 [`tasks.json`](repo:benchmark/material/draftbench/tasks.json)，工程动作取自各题 `task.toml` 的 `engineering_action`，中文名称按 [`catalog.json`](repo:benchmark/material/draftbench/catalog.json) 对照，状态取自[正式清单](repo:benchmark/tasks/benchmark.toml)和 `task.toml` 的 `stage`、`pending`。题号链接到 main 上该题的题面。

题目怎么组织、怎么验收，见[构成方式](index.md)。

## 三个草稿批次

!!! note "v2-01、v3-01 不是 vaBench v2、v3"
    这两个批次是本仓库自己建设的草稿题包。批次名沿用题号前缀 `v2-`、`v3-`，仓库文档说明它们是“建设批次，不是难度等级”。它们不是历史 vaBench（behavioral-veriloga-eval）的 v2、v3 发布版，只是编号相同。不少题的素材来自 vaBench v4，所以来源组写成 `v4-xxx`。历史 vaBench 见 [Reference](../reference/index.md)。

| 批次 | 题数 | 主题 | 当前状态 |
| --- | ---: | --- | --- |
| [v2-01](repo:benchmark/material/draftbench/batches/v2-01/README.md) | {{ bench_batch:v2-01 }} | 五类工程动作的首批题，覆盖 10 个电路功能组中的 9 个（没有连续 OTA） | 已有题包、参考解、独立 checker 和历史作者校准记录（现有评分证据以 Spectre 为准）；还有历史模型试做记录。本版完整题目审核尚未进行，没有录取记录 |
| [v3-01](repo:benchmark/material/draftbench/batches/v3-01/README.md) | {{ bench_batch:v3-01 }} | 五条扩充路线：OTA（3）、LDO（2）、滤波与 RF（5）、PLL 与模拟校准（3）、DAC/ADC（6） | 已有题包、参考解、独立 checker 和历史作者校准记录（现有评分证据以 Spectre 为准）；没有模型解题实验。本版完整题目审核尚未进行，没有录取记录 |
| [r01-sampling-01](repo:benchmark/material/draftbench/batches/r01-sampling-01/README.md) | {{ bench_batch:r01-sampling-01 }} | R01 采样功能组的两道跟踪保持题，按新题包规范编写 | ideal 题已有设计和实现，Spec 的范围与精度仍在讨论，作者校准还要先解决后端缺口；basic 题只有合同草稿。两题都没有模型解题实验 |
| 合计 | {{ bench_drafts }} | | |

v2-01、v3-01 的作者记录分别在 [`experiments/benchmark_v2`](repo:experiments/benchmark_v2/README.md) 和 [`experiments/benchmark_next`](repo:experiments/benchmark_next/README.md)。这些历史记录对应当时的题目版本，不能据此推断本版题目已经录取。更早的 41 个题包已归入[历史题包](repo:benchmark/material/historyref/tasks/README.md)，不在这 {{ bench_drafts }} 个草稿之内。

### 按工程动作统计

--8<-- "_generated/benchmark-counts.md"

计数按各题 `task.toml` 的 `engineering_action` 统计。v2-01、v3-01 两列与 [56 题总览](repo:benchmark/material/draftbench/TASKS.md)中的计数表一致。

## 逐题表

- **电路功能组**后的括号是审核编号（R01–R10），R01 即“采样与多通道读出”。
- **状态**：v2-01、v3-01 的批次 README 对每一题都记为“待审核；原位保留”，下表简写为“待审核”。
- v2-01、v3-01 的题面沿用旧格式（题面中的路径是 `/work/`，语言中英混合）；只有 r01-sampling-01 两题按新规范编写（英文题面，交付 `/app/circuit.va`）。

不在 `tasks.json` 里的题（目前是 r01-sampling-01 的两题），名称取自题面的一级标题，电路功能组按批次名前缀对应审核编号（`r01` → R01）。

--8<-- "_generated/benchmark-tasks.md"

两题的 `review_status` 都是 `pending`，后端字段都写 `spectre`，路线都是全 Verilog-A（`circuit_route = "all-va"`）。

## 数据来源

- [批次入口](repo:benchmark/material/draftbench/batches/README.md)及三个批次 README（题数、主题、状态）
- [`tasks.json`](repo:benchmark/material/draftbench/tasks.json)（v2/v3 共 56 题的名称与电路功能组）
- [`catalog.json`](repo:benchmark/material/draftbench/catalog.json)（工程动作的中文名称）
- 各题 `task.toml`（工程动作、R01 两题的阶段与待定项）
- [56 题总览 `TASKS.md`](repo:benchmark/material/draftbench/TASKS.md)（计数核对）
- [工作区总览](repo:benchmark/material/draftbench/README.md)与 [benchmark 入口](repo:benchmark/README.md)
