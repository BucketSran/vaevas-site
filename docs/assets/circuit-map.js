/* PROTOTYPE (throwaway): benchmark circuit map. Data: #cm-data from tools/prototype_circuit_map.py */
(() => {
  "use strict";
  const root = document.getElementById("cm");
  const dataNode = document.getElementById("cm-data");
  if (!root || !dataNode) return;
  const DATA = JSON.parse(dataNode.textContent);
  const el = id => document.getElementById(id);
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const by = (list, key) => list.reduce((m, x) => { const k = key(x); (m.get(k) || m.set(k, []).get(k)).push(x); return m; }, new Map());

  const catIndex = new Map(DATA.categories.map((c, i) => [c.id, i + 1]));
  const famById = new Map(DATA.families.map(f => [f.id, f]));
  const caseById = new Map(DATA.cases.map(c => [c.id, c]));
  const tasksByFam = by(DATA.tasks, t => t.family);
  const ideasByFam = by(DATA.ideas, i => i.family);
  const built = t => t.set === "first30" || t.set === "requirement";
  const PRIO = { P0: 0, P1: 1, P2: 2, HOLD: 3 };

  // ---------- 汇总与图例 ----------
  const count = f => (tasksByFam.get(f) || []).length;
  const builtCount = f => (tasksByFam.get(f) || []).filter(built).length;
  const cand = DATA.tasks.filter(t => t.set === "candidate");
  const prio = by(cand, t => t.priority);
  const kpi = (n, label, sub) => `<div class="cm-kpi"><b>${n}</b><span>${label}</span>${sub ? `<small>${sub}</small>` : ""}</div>`;
  el("cm-summary").innerHTML =
    kpi(DATA.tasks.length, "道题", `${DATA.cases.length} 个电路 case`) +
    kpi(DATA.tasks.filter(t => t.set === "first30").length, "建设中", "首批 30，本地 Harbor 改造") +
    kpi(DATA.tasks.filter(t => t.set === "requirement").length, "需求题包", "IR-UWB TX，#223") +
    kpi(cand.length, "规划候选", ["P0", "P1", "P2"].map(p => `${p} ${(prio.get(p) || []).length}`).join(" · ") + ` · 后备 ${(prio.get("HOLD") || []).length}`) +
    kpi(DATA.ideas.length, "需求想法", "还没出成题");
  el("cm-legend").innerHTML = DATA.categories
    .filter(c => DATA.families.some(f => f.cat === c.id))
    .map(c => `<span><i class="cm-swatch" style="background:var(--cm-${catIndex.get(c.id)})"></i>${esc(c.name)}</span>`).join("") +
    `<span><i class="cm-badge-key">N</i>已建或建设中的题数</span>`;

  // ---------- 矩形树图（squarified），类别内的家族相邻 ----------
  function squarify(values, x, y, w, h) {
    const total = values.reduce((a, b) => a + b, 0);
    const areas = values.map(v => v * w * h / total);
    const rects = [];
    const worst = (row, side) => {
      const s = row.reduce((a, b) => a + b, 0), max = Math.max(...row), min = Math.min(...row);
      return Math.max(side * side * max / (s * s), (s * s) / (side * side * min));
    };
    let i = 0;
    while (i < areas.length) {
      const side = Math.min(w, h);
      let row = [areas[i]], j = i + 1;
      while (j < areas.length && worst([...row, areas[j]], side) <= worst(row, side)) row.push(areas[j++]);
      const s = row.reduce((a, b) => a + b, 0);
      if (w >= h) {
        const cw = s / h; let cy = y;
        row.forEach(a => { rects.push({ x, y: cy, w: cw, h: a / cw }); cy += a / cw; });
        x += cw; w -= cw;
      } else {
        const rh = s / w; let cx = x;
        row.forEach(a => { rects.push({ x: cx, y, w: a / rh, h: rh }); cx += a / rh; });
        y += rh; h -= rh;
      }
      i = j;
    }
    return rects;
  }
  const inset = (r, p) => ({ x: r.x + p, y: r.y + p, w: Math.max(0, r.w - 2 * p), h: Math.max(0, r.h - 2 * p) });

  const plot = el("cm-plot");
  let selected = null;
  try { selected = JSON.parse(localStorage.getItem("vaevas-circuit-map") || "null"); } catch (_) { /* 无存储 */ }
  const fromHash = decodeURIComponent(location.hash.slice(1));
  if (famById.has(fromHash)) selected = fromHash;
  if (!famById.has(selected)) selected = [...DATA.families].sort((a, b) => count(b.id) - count(a.id))[0].id;

  function draw() {
    const width = plot.clientWidth;
    if (!width) return;
    const height = Math.max(460, Math.round(width * 0.82));
    plot.style.height = `${height}px`;
    const groups = DATA.categories
      .map(c => ({ cat: c.id, fams: DATA.families.filter(f => f.cat === c.id).sort((a, b) => count(b.id) - count(a.id)) }))
      .filter(g => g.fams.length)
      .map(g => ({ ...g, value: g.fams.reduce((n, f) => n + count(f.id), 0) }))
      .sort((a, b) => b.value - a.value);
    const outer = squarify(groups.map(g => g.value), 0, 0, width, height);
    const html = [];
    groups.forEach((g, gi) => {
      const box = inset(outer[gi], 3);
      const inner = squarify(g.fams.map(f => count(f.id)), box.x, box.y, box.w, box.h);
      g.fams.forEach((f, fi) => {
        const r = inset(inner[fi], 1);
        const n = count(f.id), b = builtCount(f.id);
        const small = r.w < 110 || r.h < 64, tiny = r.w < 60 || r.h < 36, sliver = r.w < 30 || r.h < 22;
        html.push(`<button type="button" class="cm-tile${small ? " small" : ""}${tiny ? " tiny" : ""}" data-fam="${f.id}"
          style="left:${r.x}px;top:${r.y}px;width:${r.w}px;height:${r.h}px;--c:var(--cm-${catIndex.get(f.cat)})"
          title="${esc(f.name)} · ${n} 题，其中已建或建设中 ${b} 题" aria-pressed="${f.id === selected}">
          ${b && !sliver ? `<span class="cm-badge">${small ? b : `建 ${b}`}</span>` : ""}
          ${sliver ? "" : `<span class="cm-name">${esc(tiny ? f.id : f.name)}</span>${tiny ? "" : `<span class="cm-n">${n} 题</span>`}`}
        </button>`);
      });
    });
    plot.innerHTML = html.join("");
  }

  // ---------- 详情 ----------
  const actionChip = a => `<span class="cm-chip" title="${esc(DATA.actions[a])}">${esc(DATA.actions[a])}</span>`;
  function taskLine(t) {
    const bits = [];
    if (t.difficulty) bits.push(t.difficulty.replace(/[BMH]/g, k => DATA.difficulty[k]).replace(/\s*[-–]\s*/g, "–"));
    if (t.set === "candidate") bits.push(t.priority === "HOLD" ? "后备" : t.priority);
    return `<li><a href="${esc(t.url)}" target="_blank" rel="noopener"><code>${esc(t.id)}</code></a> ${actionChip(t.action)}${bits.length ? `<span class="cm-chip muted">${esc(bits.join(" · "))}</span>` : ""}
      ${t.title && (t.set !== "candidate" || t.title !== caseById.get(t.case).title) ? `<div>${esc(t.title)}</div>` : ""}
      ${t.circuit ? `<div class="cm-sub">电路：${esc(t.circuit)}${t.sameSource ? ` · 同源候选 <code>${esc(t.sameSource)}</code>` : ""}${t.familyInferred ? ' · <span title="没有同源候选，家族按草稿分组推断">家族为推断</span>' : ""}</div>` : ""}
      ${t.note ? `<div class="cm-sub">${esc(t.note)}</div>` : ""}</li>`;
  }
  function detail(fid) {
    const f = famById.get(fid);
    const all = tasksByFam.get(fid) || [];
    const first = all.filter(t => t.set === "first30").sort((a, b) => a.slot - b.slot);
    const req = all.filter(t => t.set === "requirement");
    const cands = all.filter(t => t.set === "candidate");
    const p = by(cands, t => t.priority);
    const cases = by(cands, t => t.case);
    const caseRank = id => Math.min(...cases.get(id).map(t => PRIO[t.priority]));
    const caseIds = [...cases.keys()].sort((a, b) => caseRank(a) - caseRank(b) || a.localeCompare(b));
    const buildingCases = new Set(first.map(t => t.case));
    const ideas = ideasByFam.get(fid) || [];
    const cat = DATA.categories.find(c => c.id === f.cat);
    el("cm-detail").innerHTML = `
      <div class="cm-d-label"><span>${esc(cat.name)} · ${esc(f.id)}</span><span>${all.length} 题 · ${new Set(all.map(t => t.case)).size} 个电路 case</span></div>
      <h2>${esc(f.name)}</h2>
      <div class="cm-kpis">${kpi(first.length, "建设中")}${kpi(req.length, "需求题包")}${kpi(cands.length, "规划候选", ["P0", "P1", "P2"].map(k => `${k} ${(p.get(k) || []).length}`).join(" · "))}</div>
      ${first.length ? `<h3>建设中（首批 30）</h3><ul class="cm-list">${first.map(taskLine).join("")}</ul>` : ""}
      ${req.length ? `<h3>需求题包：${esc(caseById.get(req[0].case).title)}</h3><p class="cm-sub">${esc(req[0].note)}</p><ul class="cm-list">${req.map(t => taskLine({ ...t, note: "" })).join("")}</ul>` : ""}
      ${cands.length ? `<h3>规划候选（按电路 case）</h3>${caseIds.map(id => {
        const c = caseById.get(id);
        return `<div class="cm-case"><div class="cm-case-head"><b>${esc(id)}</b> ${esc(c.title)}${buildingCases.has(id) ? '<span class="cm-chip accent">有题在建</span>' : ""}</div>
          ${c.source ? `<div class="cm-sub">原题：${esc(c.source)}</div>` : ""}
          <ul class="cm-list">${cases.get(id).sort((a, b) => PRIO[a.priority] - PRIO[b.priority] || a.id.localeCompare(b.id)).map(taskLine).join("")}</ul></div>`;
      }).join("")}` : ""}
      ${ideas.length ? `<h3>需求想法（尚未出题）</h3><ul class="cm-list">${ideas.map(i => `<li><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.id)}</a> ${esc(i.title)}</li>`).join("")}</ul>` : ""}`;
  }
  function select(fid, scroll) {
    selected = fid;
    try { localStorage.setItem("vaevas-circuit-map", JSON.stringify(fid)); history.replaceState(null, "", `#${fid}`); } catch (_) { /* 无存储 */ }
    plot.querySelectorAll(".cm-tile").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.fam === fid)));
    detail(fid);
    if (scroll && window.matchMedia("(max-width: 820px)").matches) el("cm-detail").scrollIntoView({ block: "start" });
  }
  plot.addEventListener("click", e => { const b = e.target.closest(".cm-tile"); if (b) select(b.dataset.fam, true); });

  const loose = DATA.ideas.filter(i => !i.family);
  el("cm-loose").innerHTML = loose.length ? `<b>没有归入家族的需求想法：</b>${loose.map(i => `<a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.id)}</a> ${esc(i.title)}`).join("；")}` : "";
  const m = DATA.meta;
  el("cm-source").textContent = `数据：${m.bench.branch}@${m.bench.head}${m.bench.dirty ? "（含本地未提交改动）" : ""}；需求题包 ${m.uwb.branch}@${m.uwb.head}；题目链接按 main@${m.main}。`;

  new ResizeObserver(() => { draw(); select(selected, false); }).observe(plot);
  draw();
  select(selected, false);
})();
