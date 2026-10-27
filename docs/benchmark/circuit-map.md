---
hide:
  - navigation
  - toc
---

# Benchmark：电路地图

!!! warning "本地原型，未发布"
    数据来自 Benchmark 线的工作区和需求题包分支，还没有合入 main。合入后改为构建时从 main 读取，再上线。

每一块是一个功能家族，面积是这个家族的题数：规划候选、首批 30 题和需求题包都算在内。右上角的数字是已建或正在建设的题。点一块，右侧列出这个家族的题目和它们对应的具体电路 case。

<div class="cm" id="cm" markdown="0">
  <div class="cm-summary" id="cm-summary"></div>
  <div class="cm-legend" id="cm-legend" aria-label="颜色图例"></div>
  <div class="cm-layout">
    <div class="cm-plot" id="cm-plot" role="group" aria-label="功能家族的矩形树图，面积是题数"></div>
    <aside class="cm-detail" id="cm-detail" aria-live="polite"></aside>
  </div>
  <p class="cm-caption">面积按题数计，同一电路 case 的不同题分别计数。规划候选还没有建题；首批 30 题是本地 Harbor 改造稿，尚未校准和录取。</p>
  <p class="cm-loose" id="cm-loose"></p>
  <p class="cm-source" id="cm-source"></p>
</div>

--8<-- "_generated/circuit-map-data.html"

## 逐题对照

??? note "全部题目对应的电路 case（展开）"

    --8<-- "_generated/circuit-map-table.md"
