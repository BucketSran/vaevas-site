---
date: 2026-10-22T16:44:00
categories:
  - EVAS
slug: xspice-branch-preserved
---

# XSPICE 未提交工作保全并推送到分支，只有一个提交可直接取用

XSPICE 工作区里的 266 个未提交文件已分类，并推送到分支 `codex/evas-xspice-entry`。其中只有提交 `5b4e7a1c`（78 个 XSPICE 自有文件）可以直接取用。另外两个提交只是快照，不要合并。没有开 PR，也没有跑测试。

<!-- more -->

## 做了什么

本条为补记，对应 2026-10-22 16:44 的保全工作。

- 把 266 个未提交文件逐个和 main 对比，分成四类：
    - 78 个 XSPICE 自有文件：76 个新文件，加 `GLOSSARY.md` 和 `__main__.py`，提交为 `5b4e7a1c`；
    - 10 个共享文件：PR208 合入前的旧文本，夹杂 XSPICE 编辑，提交为快照 `1a32e23b`；
    - 91 个文件是 PR208 合入前的旧版本，提交为快照 `e5287696`；
    - 87 个文件与 main 相同，没有提交。
- 分支头为 `e5287696`，基于 `35876041`，落后 main 约 125 个提交。
- 原样备份（tar 包和哈希）保存在本地。

## 结果与证据

- `5b4e7a1c` 与当时的 main（`6f3a6b54`）试合并没有冲突，但没有跑测试。
- 两个快照提交不能合并：`1a32e23b` 要对照 main 手工重做其中几处 XSPICE 编辑；`e5287696` 里还有一处无关的旧删除。
- PR208 已合入，所以 XSPICE 线原来“等 PR208”的前置条件已经解除。
- 恢复说明：#176 的[评论](https://github.com/BucketSran/vaEVAS/issues/176#issuecomment-6336514831)。

## 遗留与下一步

- 重做要从最新 main 和 `5b4e7a1c` 起步：
    - 补回 `errors.py` 里的 XSPICE 错误码，以及 `pyproject.toml` 的打包配置；
    - 跑 `test_xspice*.py` 和 `validation/xspice`；
    - 合入前清理证据收据里的本机路径。
- #176 已改为 `stage:planned`，目前没有会话负责。
- 原目标“由 ngspice 托管 EVAS 事件模型”的取舍，仍待维护者决定。

## 相关链接

- Issue176：https://github.com/BucketSran/vaEVAS/issues/176
- 分支：https://github.com/BucketSran/vaEVAS/tree/codex/evas-xspice-entry
