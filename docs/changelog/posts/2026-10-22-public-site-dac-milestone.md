---
date: 2026-10-22T16:00:00
categories:
  - 项目
slug: public-site-dac-milestone
---

# 网站公开发布到 GitHub Pages；建立 DAC 2027 里程碑

项目网站已公开发布到 <https://bucketsran.github.io/vaevas-site/>：推送到网站仓库或每过 6 小时，网站会自动从 vaEVAS 的 main 和 Issue 重新构建。同时合入了 Issue 标签规则（[PR #219](https://github.com/BucketSran/vaEVAS/pull/219)），以“不做”关闭了 [#16](https://github.com/BucketSran/vaEVAS/issues/16)，并建立了里程碑“DAC 2027 投稿”。

<!-- more -->

## 做了什么

- **公开发布**：
    - 网站源码移到公开仓库 [BucketSran/vaevas-site](https://github.com/BucketSran/vaevas-site)。
    - GitHub Actions 在三种情况下构建并发布到 GitHub Pages：推送、每 6 小时定时、手动运行。
    - 构建时只按需读取 vaEVAS 的几个目录（文档、benchmark 草稿和正式清单），Issue 数据用 Actions 自带的令牌读取。
- **公开前清理**：
    - 服务器账号名改为“课题组服务器”。
    - 首页许可一节只保留“尚未确定、分三块确定”。
    - 页脚去掉“本地网站”字样。
    - 新增 `tools/check_public.py`：手写页面里出现本机绝对路径、服务器账号或内部会话链接时，构建失败。
    - 公开仓库只放一个新的初始提交，早期的本地提交没有推送。
- **Issue 与里程碑**：
    - PR #219 合入 main（合并提交 `52150362`）。
    - #16 写明结论和重开条件后，以“不做”关闭。结论是：Spectre 21.1.0.509.isr12 的重复赋值行为与语言规范不一致，EVAS 按规范实现（#12），版本范围未知。这条外部差异继续记在统一功能清单的 GAP16。
    - 新建里程碑“DAC 2027 投稿”，截止 2026-11-18，归入 #214、#96、#119、#159。

## 结果与证据

- 首次发布的 Actions 运行，构建和部署都成功：导入 main@52150362，读到 54 个 Issue、154 个已合入 PR、1 个里程碑；链接检查和公开内容检查都是 0 处问题。
- 线上核对：首页、看板、EVAS、数学原理、Benchmark 预览、Reference、更新日志都返回 200。数学页 140 处公式正常显示，看板显示 19 张卡片，浏览器里没有失败的请求。
- DAC 2027 的日期和规则来自[官方投稿说明](https://dac.com/2027/program/research-manuscript-submissions)：摘要 2026-11-11、全文 2026-11-18（美西时间 17:00）；双盲评审；允许先发 arXiv，但要求尽力保持匿名。

## 遗留与下一步

- 双盲评审期间，论文里不要链接本网站或 GitHub 仓库，需要时改用匿名化的链接。
- 许可还没定。
- 里程碑里归入哪些 Issue 是本会话的判断，可以在 GitHub 上调整。
- 网站风格要不要改成之前那页汇报材料的样式，还没定。

## 相关链接

- 网站：https://bucketsran.github.io/vaevas-site/
- 网站仓库：https://github.com/BucketSran/vaevas-site
- PR #219：https://github.com/BucketSran/vaEVAS/pull/219
- #16 关闭说明：https://github.com/BucketSran/vaEVAS/issues/16
- 里程碑：https://github.com/BucketSran/vaEVAS/milestone/1
