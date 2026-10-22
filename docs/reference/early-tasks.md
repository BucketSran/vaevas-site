# 本仓库早期题包（41 个）

这 41 个题包是本仓库自己建的，不来自 vaBench 来源仓库。建于 2026-10-04 到 10-08 前后，分两组：8 个早期 VA 资产（`va01`–`va08`），以及旧七类首批的 33 个专属目录。它们不计入当前的草稿批次，也不计入正式题集。

## 1. 身份

| 项 | 值 | 来源 |
| --- | --- | --- |
| 来源 | 本仓库（vaEVAS）自建；原路径 `benchmark/tasks/<id>/`，曾暂存于 `benchmark/material/draftbench/tasks/` | [早期题包 README](repo:benchmark/material/historyref/tasks/README.md) |
| 建题时间 | 按首次提交：`va01-and2` 2026-10-04（`c60cdd4e`），`va08-adc-linearity` 2026-10-06，`spec-sigma-delta`、`optimize-vco-step` 2026-10-08。其余题未逐一查 | `git log --follow` |
| 移入现路径 | 2026-10-15，commit `fae1bac209650fcd1ba8fe6f1b1214d258aecbfd`，现路径 `benchmark/material/historyref/tasks/` | 同上 |
| 封印 / SHA | 没有统一的封印文件。身份靠封存收据里的哈希：非性能题看 `calibration_receipt.json`，优化题看 `formal_calibration_receipt.json`。README 写明：搬迁只改导航和读取路径，封存回执、源码快照、结果 JSON 和哈希不改写 | [CALIBRATION.md](repo:experiments/benchmark_first_batch/CALIBRATION.md)、[优化收据](repo:experiments/benchmark_first_batch/optimization/formal_calibration_receipt.json) |
| 绑定的仿真器 | 前六类 30 题的校准核验的是**已经执行过的 Spectre 作业**，审计时没有重跑仿真器。Spectre 版本号本页**未核实**。CALIBRATION.md 写明，不能据此说第三方已能用 EVAS 重新评分 | [CALIBRATION.md](repo:experiments/benchmark_first_batch/CALIBRATION.md) |

## 2. 构成

**两组题包**（[早期题包 README](repo:benchmark/material/historyref/tasks/README.md)）：

| 组 | 数量 | 说明 |
| --- | ---: | --- |
| 早期 VA（`va01`–`va08`） | 8 | `va01`–`va06` 是"真实来源 Verilog-A 能力初筛"的 6 题，原始来源分别是课题组文件（4 题）和 Cadence 安装库（2 题）（[初筛说明](repo:experiments/va_screen/README.md)）。`va07`、`va08` 后来被旧首批复用 |
| 旧七类首批专属目录 | 33 | 旧首批清单共 35 题（七类工程动作 × 5 题），其中 2 题复用 `va07`、`va08`，所以专属目录只有 33 个 |
| 合计 | 41 | |

七类工程动作：按规格构建模型、从数据建立模型、扩展与集成、诊断与修复、开发验证工具、测量与表征、改善仿真实现。每类 5 题（[首批建设记录](repo:benchmark/material/historyref/legacy-authoring/first-batch/README.md)）。

**题目形式**：每个题包是一个 Harbor 任务：`instruction.md`、`environment/public/`（公开上下文和起始工程）、`solution/`（参考解与 `solve.sh`）、`tests/`（终评条件）、`SOURCE.md`（来源、同源组、人工故障原因）。同源关系记在 `source_group` 字段：首批共 32 个同源组，见 [METADATA.md](repo:benchmark/material/historyref/legacy-authoring/first-batch/METADATA.md)。

**计分 / 校准口径**（当时的批次口径，不是现在的录取结论）：

- 校准评价的是参考解和人工错误版本，**不是模型成功率**。
- 前六类 30 题（[CALIBRATION.md](repo:experiments/benchmark_first_batch/CALIBRATION.md)）：30 个参考解 97 个条件全部通过；110 个语义错误版本共 247 个条件，拒绝 226、通过 21，每个错误版本至少有一个条件被拒绝。
- 优化类 5 题：5 个参考的 15 个条件全部通过；30 个负例的 90 个条件中，63 个因语义错误被拒绝、5 个因性能不足被拒绝、22 个通过（首批建设记录）。
- 模型试跑：首批的 agentic pilot 跑了 14 个固定单元，`glm-5.3` 5/7、`glm-5.3-flash` 3/7。公开仿真反馈大量失败，所以这组成绩不能用来给题目难度定级，也不能外推为 35 题的整体通过率。早期 VA 初筛 6 题的首轮成绩是 `gpt-6.1-sol` 6/6、`glm-5.3` 3/6。

**本仓库保存了什么**：41 个题包、五份原清单（`first_batch-*.json`，保留搬迁前的字节）、首批建设记录与同源元数据，以及共享 checker 和早期 replay 工具（`legacy-authoring/checkers/`）。校准工具和简明证据在 `experiments/benchmark_first_batch/`；原始波形和完整审计输出在本地被 git 忽略的 `runs/` 里，没有公开下载地址。

**不包括**：首批里保留为候选的"采样 DAC 重复解码"和"SC 滤波器重复系数计算"，它们不占正式题量。

!!! note "复用规则"
    早期题包可以作为新批次的材料，但要先说明新的工程工作与原题的关系。旧的审核、运行资格和分发许可**不继承**（[早期题包 README](repo:benchmark/material/historyref/tasks/README.md)）。

## 3. 已知问题（勘误表）

| 编号 | 题号 | 问题 | 证据 | 状态 | 修订位置 |
| --- | --- | --- | --- | --- | --- |
| — | — | 尚无登记 | — | — | — |

目前没有针对这 41 个题包的审计或差分。CALIBRATION.md 自己列出的证据边界不算勘误，但值得知道：空 PLL 数据和全零 ADC 码的防御检查只有本地行级测试，没有做过实际 VA 注入试验。以后登记时用 `early-E001` 起编。

## 4. 修订版

尚无修订版。
