---
date: 2026-10-22T15:47:00
categories:
  - EVAS
slug: pr220-deadline-order
---

# PR220 合入：原题 186 按已证明的精确顺序处理期限，开发重放 343/400

PR220 已合入 main（`6f3a6b54`），原题 186 通过原 checker。原 400 题的开发重放为 343 通过、5 判错、52 拒绝，还剩 57 题；比上一次 342 零丢失。这是开发证据，不是验收收据，最近的正式检查点仍是 `159c0512` 的 318/19/63。

<!-- more -->

## 做了什么

本条为补记：PR220 由 Issue214 写入会话完成，当时没有写更新日志。

- **原题 186**：两个不同 transition 的期限在 binary64 里相差不到 1 ULP，浮点包络重叠，旧规则一律拒绝。它们的精确有理数时间已经证明不相等，两个 transition 互不读取，先后顺序不改变任何目标或状态。新规则只在下列条件全部满足时按精确顺序处理，其余情况仍然拒绝：
    - 属于不同算子，而且两个都是“独立 transition”（目标只读保持状态和常数）；
    - 两个精确时间都有证明，并且不相等；
    - 较早的那个是连续边沿的结束点；
    - 两个期限的联合区间里没有用户事件。
- **ADR-003**：为“cross 事件体读穿越之后的值”补上 Spectre 证据出处，并写明覆盖范围有限。
- **ADR-005**：记录“按常数 `$bound_step` 增加保存行”评估后不采用。原因是它对 `strobeonly` 写法造成回归，而且没有收益。这样可以避免以后重复尝试。

没有放宽任何容差、证明预算或上限。

## 结果与证据

| 对象 | 结果 | 口径 |
| --- | --- | --- |
| 原题 186 | 通过原 checker | 开发重放 |
| 原 400 题 | 343 通过 / 5 判错 / 52 拒绝；对 342 零丢失 | 开发重放，不是验收收据 |
| Rust | 753 通过 / 0 失败 | PR 分支 |
| Python | 2771 通过，1 失败，5 项预期失败 | 失败项 `test_co_sh_01` 在本机调试内核下超时，在 CI 的优化级别下通过 |
| PR CI | 13 项成功，1 项跳过 | GitHub Actions |
| 独立审查 | Opus 5.5、Sonnet 5.5 各一份，均判可保留 | PR 描述 |

- 新增回归测试：[`test_proven_deadline_order.py`](repo:evas/tests/test_proven_deadline_order.py)（用 Fraction 做独立参考），以及 Rust 负控 `independent_proven_order_controls`。
- 开发重放的日志在本地：`current/runs/issue214-claude-20261021/m14-final2.log`。

## 遗留与下一步

- 剩余 57 题的根因分组见 Issue214 评论。其中 012/077/079 的“少写输出行”仍归 EVAS 侧，但不走 `$bound_step` 保存行这条路线（见 ADR-005）。
- 140（显式零边沿 transition）按用户决定继续拒绝，先观察 Spectre。
- Issue214 已改为 `stage:paused`，等用户的五项决定和统一跑的 21 题 Spectre。

## 相关链接

- PR220：https://github.com/BucketSran/vaEVAS/pull/220
- Issue214：https://github.com/BucketSran/vaEVAS/issues/214
- 剩余 57 题分组：https://github.com/BucketSran/vaEVAS/issues/214#issuecomment-6335640576
- [ADR 记录](repo:evas/docs/development/DECISIONS.md)、[事件数学说明](repo:evas/docs/math/events.md)
