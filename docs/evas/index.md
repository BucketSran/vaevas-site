# EVAS

EVAS 是开源的电压域 Verilog-A 仿真器。它的首要目标是：使用者**不依赖商业仿真器**，也能运行和验证目标范围内的 Verilog-A 行为模型，同时为 benchmark 提供开源复现环境。

## 为什么需要 EVAS

### 行为模型需要仿真，但开源路线覆盖不了关键行为

工程师常用 Verilog-A 写行为模型：采样保持、迟滞比较器、定时与复位、VCO、边沿与滤波。这些模型的正确性取决于几件事：

- 在正确的时刻采样；
- 事件发生后保持已经读到的状态；
- 边沿、滤波和积分使用一致的历史。

商业仿真器 Spectre 能处理这些行为，但需要授权。开源路线主要有 ngspice + OpenVAF-R 和 Gnucap + modelgen-verilog。在下面的对比里，这两条路线在事件、定时、积分相关的用例上经常编译失败、初始化失败或漏事件。[OpenVAF-R 事件诊断](repo:experiments/backends/support/README.md#ngspice-events)还说明：模型编译成功、甚至仿真跑完，也可能根本没有实现这些行为。

### benchmark 需要能复现的评分环境

benchmark 要让别人能复现成绩。如果每道题都只能用 Spectre 判分，没有授权的人就无法复现。EVAS 为目标范围内的题目提供开源的运行与验证路径。遇到 EVAS 还不支持的能力时，benchmark 继续用已校准的 Spectre 验收，不要求题目等 EVAS 补齐。

### EVAS 做什么、不做什么

| 做 | 不做 |
| --- | --- |
| 把限定范围内的 Verilog-A 电压关系编译成方程，联立求解节点电压 | 晶体管器件模型 |
| 理想电压域行为：增益、限幅、采样、事件计数、连续时间算子（transition、idt、laplace 等） | 电流 / 电荷方程 |
| 事件定位、时间推进和误差检查；在受支持的瞬态路径上，不能证明满足精度就拒绝，而不是给一个可疑的点值 | 完整 SPICE 网表求解 |

前端用 Python 解析、绑定并生成 IR，Rust 内核完成求解和时间推进。原理见[数学原理](math.md)。

## 和其他仿真器的对比

下面的数字从 main 上的[四后端对比表](comparison.md)自动统计，每次构建网站都会重新计算，不需要手工维护。当前来源：main@{{ main_short }}（{{ main_date }}）。

--8<-- "_generated/comparison-summary.md"

### 怎么读这张表

- **用例是本项目选的。** 它们覆盖 EVAS 的目标范围，即电压域行为模型，从语言特性、单个算子，一直到完整信号链和复杂交互。这张表不衡量通用电路仿真能力，晶体管级电路本来就不在 EVAS 的范围内。
- **结果来自不同版本。** 原表写明：“结果来自不同版本，不代表当前 main 的一次全量验收，也不覆盖所有合法写法。”
- **✓ 有精度档。** Q1 / Q2 / Q3 是验收上限：1 V 刻度下分别为 10.1 µV / 1.01 µV / 101 nV。判据见[对比评测标准](manual/COMPARISON-METHODOLOGY.md)。
- **失败要区分原因。** 按[项目的验收要求](repo:README.md#研究验收与论文实验)，后端对照要区分真实能力缺口、使用或配置问题和尚未验证的行为。没配置成功某个工具，不能当作它不支持的证据。
- **不说明速度。** 现有测量还不能证明 EVAS 普遍快于 Spectre。现有对照支持 EVAS 在已测范围内可用，但不能据此宣称 EVAS 全面优于 Gnucap，也不能宣称它的精度总是更高。

### 维护方式

对比表只在仓库里维护一份，即 [`evas/docs/COMPARISON.md`](repo:evas/docs/COMPARISON.md)。网站构建时从 main 导入它的前五节，统计上面的数字，并把表里的链接改成指向同一提交的 GitHub 链接。改表的流程是：在仓库里提 PR，合入 main 以后重新构建网站。原表第六节“统一功能缺口与推进路线”是开发进度记录，网站不导入，需要时[到原文查看](repo:evas/docs/COMPARISON.md#engineering-status)。

## 进一步阅读

- [四后端对比表](comparison.md)：全部用例和每格的结果
- [数学原理](math.md)：读者版导读
- [完整数学手册](manual/math/README.md)：维护者手册，从 main 导入
- [EVAS 使用说明](repo:evas/README.md)：构建、运行和模型移交
