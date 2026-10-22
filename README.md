# vaEVAS 项目网站

[vaEVAS](https://github.com/BucketSran/vaEVAS) 的项目网站，公开地址：<https://bucketsran.github.io/vaevas-site/>。

## 发布与自动更新

GitHub Actions（`.github/workflows/deploy.yml`）在三种情况下重新构建并发布网站：

- 本仓库 `main` 有推送，例如新增一条更新日志；
- 每 6 小时定时一次，重新读取 vaEVAS 的 main 和 Issue；
- 在 Actions 页面手动运行。

所以对比表、数学手册、benchmark 题数和项目看板会自动跟上 vaEVAS 的进展。手写的页面和更新日志，要提交并推送到本仓库才会更新。

本仓库是公开的。写进来的内容会被所有人看到：不要写本机绝对路径、服务器账号、内部会话链接或费用。`tools/check_public.py` 会在构建时检查前三类。

## 本地预览

本地 clone 放在 vaEVAS 工作区的 `local/site/`，与 `current/` 同级。

```sh
./site.sh serve        # 读取 vaEVAS main 和 GitHub 数据，然后在 http://127.0.0.1:8765 预览
./site.sh build        # 同上，再做严格构建、链接检查和公开内容检查；产物在 build/site/
./site.sh sync         # 只读取数据，不启动服务；离线加 --no-fetch
```

第一次运行时，脚本会用 `uv` 建 `.venv`，并按 `requirements.txt` 安装固定版本的依赖。MkDocs 固定在 1.6.1：Material 团队预告 MkDocs 2.0 会让现有插件失效，所以不要随手升级。公式（KaTeX）和流程图（Mermaid）放在 `docs/assets/vendor/`，各自附有 MIT 许可文件。

## 内容从哪里来

| 内容 | 来源 | 维护方式 |
| --- | --- | --- |
| 四后端对比表、汇总数字 | main 上的 `evas/docs/COMPARISON.md` 前五节 | 自动导入，不要手改；改表请在仓库里提 PR |
| 完整数学手册、对比评测标准 | main 上的 `evas/docs/math/`、`evas/docs/COMPARISON-METHODOLOGY.md` | 自动导入到 `docs/evas/manual/` |
| 介绍、EVAS、数学导读、Benchmark、Reference、成绩榜 | `docs/` 下手写的页面 | 修改后提交并推送 |
| 更新日志 | `docs/changelog/posts/` 下每条一个文件 | 见下一节 |

`tools/sync_main.py` 通过 `git show` 读取 vaEVAS 的 main（本地默认读 `../../current` 的 `origin/main`，Actions 里读稀疏 checkout 的 `HEAD`），不改动任何 checkout。它会把相对链接改写好：导入页面之间的链接留在站内，其余链接指向同一提交的 GitHub 文件。手写页面里写 `repo:<仓库路径>#锚点`，构建时同样改成 GitHub 链接；如果路径不在 main 上，严格构建会失败。git 忽略的本地证据（`current/runs/...`）不做链接，写成相对 vaEVAS 工作区的行内代码路径。

Benchmark 预览页的计数和逐题表、首页的 benchmark 题数，同样在构建时从 main 生成。首页状态卡里其余的数字仍是手写，日期写在 `docs/index.md` 的 `status_date`；超过 14 天没更新，或者比最新一条更新日志旧，页面上会出现提醒。

`sync_main.py` 默认先 `git fetch`；离线时加 `--no-fetch`。

<a id="board"></a>

## 项目看板

想法、设计和任务只记在 GitHub Issues 上，网站不另存任务表。`tools/sync_issues.py` 用本机的 `gh` 登录读取 Issue、PR 和里程碑，写到 `docs/_generated/github.json`；抓取失败时沿用上次的快照。`hooks/board.py` 按标签把 Issue 画成看板：

- 阶段标签：`stage:idea`、`stage:design`、`stage:planned`、`stage:active`、`stage:paused`；Issue 关闭后不需要阶段标签。
- 领域标签：`area:evas`、`area:benchmark`、`area:project`。
- 卡片显示 Issue 顶部摘要、引用它的 PR、提到它的更新日志和最近一次正文或评论的时间。一次提到 6 个以上 Issue 的汇总 PR 只计数。
- 页面顶部列出要处理的提醒：待分诊、缺领域标签、状态矛盾、停滞、已合入却没写进日志的 PR、状态卡落后。

规则原文在仓库的 `docs/agents/issue-tracker.md`，标签一节随 [PR #219](https://github.com/BucketSran/vaEVAS/pull/219) 加入。用户已授权（2026-10-22）：会话可以直接新建想法 Issue、修改阶段和领域标签。关闭 Issue、改别人记录的范围、合并 PR 仍要先问。

用户说“记个想法：……”时，会话按下面的步骤做：

1. 用 `gh issue list -R BucketSran/vaEVAS --state all --search "<关键词>"` 查有没有同一目标的 Issue。有就在那里补一条评论，到此为止。
2. 没有就按想法模板写正文（想法、为什么值得做、可能的做法、怎么判断做成了），新建 Issue：`gh issue create -R BucketSran/vaEVAS --title "<稳定的目标>" --label stage:idea --label area:<evas|benchmark|project> --body-file <文件>`。
3. 把 Issue 链接告诉用户。看板在下次构建或 `./site.sh sync` 后出现这张卡片。

<a id="add-changelog"></a>

## 新增更新日志

用户会在会话结束时说“总结一下，加到更新日志”。收到这句话的会话按下面的步骤做。

1. 建条目文件：

    ```sh
    ./site.sh new-entry --title "一句话说清这次更新" --slug short-english-slug --category EVAS
    ```

    `--category` 可以重复，只能取 `EVAS`、`Benchmark`、`项目`。`--date` 默认是当前时间；补写过去的事件时，写事件当天的日期。

2. 填写模板里的五部分：
    - **摘要**（`<!-- more -->` 之前）：一到两句，说清结果，数字带口径。
    - **做了什么**：本次会话实际完成的工作。
    - **结果与证据**：数字和结论，每条写清来源，例如 PR、提交、收据路径。
    - **遗留与下一步**：没完成的、失败的、等待决定的事项。
    - **相关链接**：PR 和 Issue 写完整 URL；main 上的文件写 `repo:` 链接；本地证据写行内代码路径。

3. 口径规则：
    - 区分“已合入 main”和“本地、未推送、草稿 PR”。
    - 开发中的数字不是验收结论，正式检查点要和开发数分开写。
    - 失败、撤回和限制照实写。
    - 只写本次会话有证据的事实；不确定的写“未核实”。

4. 如果首页“最新阶段”的事实变了，同时更新 `docs/index.md` 的状态表和 `status_date`。本次会话推进了哪个 Issue，就在日志里写 `#编号`，并把它的阶段标签改对（例如开始做改成 `stage:active`，暂停改成 `stage:paused`）。

5. 运行 `./site.sh build`，必须通过。然后提交并推送，Actions 会在几分钟内发布：

    ```sh
    git -C <本目录> add -A && git -C <本目录> commit -m "changelog: <标题>" && git -C <本目录> push
    ```

    用户 2026-10-22 决定公开部署本网站，并要求每次会话把总结加进更新日志。会话按本节完成的日志和状态卡更新可以直接推送到本仓库 `main`。

一次会话写一条。工作跨了几天的，写在结束那天。

## 目录

```text
mkdocs.yml            网站配置与导航
site.sh               入口：serve / build / sync / new-entry
.github/workflows/    发布到 GitHub Pages
tools/sync_main.py    从 main 导入文档、生成对比汇总和 benchmark 预览表
tools/sync_issues.py  读取 GitHub Issue、PR、里程碑，供项目看板使用
tools/check_links.py  构建后检查站内链接与锚点
tools/check_public.py 检查手写页面里不该公开的内容
tools/new_entry.py    新建更新日志条目
hooks/site_hooks.py   repo: 链接、页脚来源、状态卡提醒、数字占位符、勘误汇总
hooks/board.py        项目看板与提醒
docs/                 页面；docs/_generated/ 和 docs/evas/manual/ 是生成物，不进 Git
```
