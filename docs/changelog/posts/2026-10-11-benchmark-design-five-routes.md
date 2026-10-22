---
date: 2026-10-11T02:53:00
categories:
  - Benchmark
slug: benchmark-design-five-routes
---

# benchmark 设计定型：五类任务、35 题历史资产、后端政策与首批五条建设路线

2026-10-09 至 10-11 合入 3 个 PR 和 1 个直接提交：任务定义改为五类工程动作，旧七类方案的 35 个 Harbor 资产及校准入库（35 个参考解在 112 个条件上全部通过）；确认在已验证的 ngspice 范围内可由 ngspice 独立给正式成绩；并把 v4 迁移材料整理为 62 个候选来源 / 17 个功能组和首批五条路线。这些都还是设计与历史资产，不是已验收的新评分题。

<!-- more -->

## 做了什么

- #105（10-09）：采用五类任务：按规格构建模型、从数据建立模型、扩展与集成、诊断与修复、电路测试与表征。新增五份材料专题和统一学习入口。同时保留旧七类方案建设的 35 个 Harbor 资产（32 个同源组：30 个工作单元、4 个小工程、1 个原创完整仓库）及其校准和试跑记录。
- 直接提交 `c81b8c7c`（10-10）：新增 benchmark 逐题设计工作区，首批登记 POR 测试台、LDO 启动测量、运放压摆率三个候选；改写后端政策：任务完整处于已验证的 ngspice 支持范围、且有可信独立 checker 时，可由 ngspice 独立给正式成绩；每题固定后端和工具链，后端能力不足导致合规候选失败应归为环境缺陷。
- #125（10-10）：新增 `benchmark/docs/`，分别维护设计目标、五类任务合同、评测与复现原则。
- #128（10-11）：把 benchmarkv4 的审核和迁移材料整理成建设清单：39 个代表来源 + 23 个行为变体 → 62 个候选来源 / 17 个功能组；首批先建采样、比较器表征、时钟、电源复位、放大器测量五条路线。

## 结果与证据

- #105 历史资产校准：35 个参考解 112 个条件全部通过；140 个负例提交每个至少一个条件被拒绝；Harbor 0.23.0 静态解析 35 份配置通过，不冒充 35 次 Oracle Trial。
- #105 历史固定模型试跑：七个代表题 × 两个请求标识共 14 次，请求 glm-5.3 等权合计 5/7，请求 glm-5.3-flash 3/7；本轮未观察到独立服务端模型 ID。86 次公开仿真响应中 84 次 `backend_error`、2 次 `ok`。结果不能外推到 35 题，也不能给题目难度定级。
- #128：P1/P2/P3 分别为 32/11/19 个来源；共 18 张设计卡，均不等于已验收评分题。另保存 400 家族、1200 旧包的 GLM 静态审核摘要和全库取舍索引。
- 这几项都没有修改 EVAS；#125、#128 没有新增仿真、checker 校准或 Agent 解题实验。
- GitHub 记录 10-10 另开 #133–#137 五个 spec issue，分别对应五类任务的规划，均于 10-11 关闭。

## 遗留与下一步

- 历史试跑暴露的公开电路反馈和 Agent 可读凭据问题仍需处理；历史资产未取得无需商业工具的重评分资格。
- 下一步按五条路线建立可独立验收的代表任务；总体建设由 #72、五类定义由 #107 继续跟进。

## 相关链接

- PR：[#105](https://github.com/BucketSran/vaEVAS/pull/105)、[#125](https://github.com/BucketSran/vaEVAS/pull/125)、[#128](https://github.com/BucketSran/vaEVAS/pull/128)
- 提交：[c81b8c7c](https://github.com/BucketSran/vaEVAS/commit/c81b8c7c)
- Issue：[#72](https://github.com/BucketSran/vaEVAS/issues/72)、[#107](https://github.com/BucketSran/vaEVAS/issues/107)、[#133](https://github.com/BucketSran/vaEVAS/issues/133)、[#134](https://github.com/BucketSran/vaEVAS/issues/134)、[#135](https://github.com/BucketSran/vaEVAS/issues/135)、[#136](https://github.com/BucketSran/vaEVAS/issues/136)、[#137](https://github.com/BucketSran/vaEVAS/issues/137)
- 仓库：[首批校准与执行](repo:experiments/benchmark_first_batch/README.md)、[非性能校准](repo:experiments/benchmark_first_batch/CALIBRATION.md)、[pilot 报告](repo:experiments/benchmark_first_batch/agentic/PILOT.md)、[设计工作区检查脚本](repo:scripts/benchmark_workbench.py)
