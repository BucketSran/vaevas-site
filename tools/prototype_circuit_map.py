"""PROTOTYPE (throwaway): data for the benchmark circuit map page.

The map shows the screened benchmark tasks and the circuit case behind each one:

- planning candidates: ``planning/history-candidates/register.json`` (+ ``sources.json``)
- first batch under construction: ``batches/harbor30-01/selection.json``
- requirement-driven task packages recorded in issues (IR-UWB TX, #223)
- requirement ideas that are not tasks yet (#159, #225), listed without area

Until the candidate data reaches main, the benchmark files are read from the
Benchmark worktree and the UWB batch from its branch. Writes

- ``docs/_generated/circuit-map-data.html``  JSON for the map, included by the page
- ``docs/_generated/circuit-map-table.md``   per-task circuit table (Markdown)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
DOCS = SITE / "docs"
WORKSPACE = SITE.parents[1]
GITHUB = "https://github.com/BucketSran/vaEVAS"

DRAFT = "benchmark/material/draftbench"
PLANNING = f"{DRAFT}/planning/history-candidates"
SELECTION = f"{DRAFT}/batches/harbor30-01/selection.json"
UWB_BATCH = f"{DRAFT}/batches/uwb-tx-01"
V4_TASKS = "benchmark/material/historyref/v4/release/benchmarkv4-r53/tasks"
BENCH_BRANCH = "codex/benchmark-final-candidates"
UWB_BRANCH = "claude/ir-uwb-tx"

# Seven colour groups (dataviz categorical slots 1-7, fixed order); families map onto them.
CATEGORIES = [
    ("conv", "数据转换"),
    ("clock", "时钟与时间"),
    ("amp", "放大与滤波"),
    ("rf", "RF 与均衡"),
    ("power", "电源与复位"),
    ("decide", "比较与校准"),
    ("logic", "逻辑与基础"),
]
FAMILY_CATEGORY = {
    "R01": "conv", "R09": "conv", "R10": "conv", "R04": "clock", "R07": "amp", "FILTER": "amp",
    "R06": "rf", "R03": "power", "R08": "decide", "R05": "decide",
    "LOGIC": "logic", "BASE": "logic", "TOOL": "logic",
}
ACTIONS = {"S": "按规格建模", "R": "诊断与修复", "T": "测试与表征", "I": "扩展与集成", "D": "从数据建模"}
ACTION_OF = {"spec-modeling": "S", "diagnosis-repair": "R", "testing-characterization": "T",
             "extension-integration": "I", "data-modeling": "D"}
DIFFICULTY = {"B": "基础", "M": "中", "H": "难"}

# First-batch drafts without a same-source candidate: family by their draft review group,
# with these explicit choices where the draft group was split or renamed in the register.
DRAFT_GROUP_FAMILY = {"R01": "R01", "R02": "R07", "R03": "R03", "R04": "R04", "R05": "R05",
                      "R07": "R07", "R08": "R08", "R09": "R09", "R10": "R10"}
FIRST30_FAMILY_OVERRIDE = {
    "v3-filter-ctle": "R06",                 # 连续时间均衡
    "v3-filter-sweep-measurement": "FILTER",
    "v3-filter-programmable-lp": "FILTER",
    "v3-converter-adc-spectrum": "R09",      # ADC 指标表征；登记里 U04-T1 的 ADC 表征归 R09
}
# Circuits of first-batch drafts that are not a single v4 family.
OTHER_CIRCUITS = {
    "jku-sampling-stage": "JKU SKY130 SAR ADC 采样级（真实电路）",
    "tiny-tapeout-adpll": "Tiny Tapeout ADPLL（真实电路）",
    "jku-ota-dynamics": "JKU 晶体管 OTA（真实电路）",
    "verilogalib-ctle": "开源 Verilog-A 库 CTLE",
    "original-uvlo-chain-case0009": "原创 UVLO 与复位控制链",
    "original-filter-measurement": "原创滤波器扫频测量",
    "first-batch-measure-adc-spectrum": "早期题包的 ADC 码流记录",
    "repository-owned-dac-scan": "仓库自建 DAC 扫描（va08 改编）",
}
# Requirement ideas recorded in issues that are not tasks yet (prototype transcription).
IDEAS = [
    {"id": "R01-E01", "family": "R01", "title": "连续跟踪与有限建立：窗口内输入变化，保留连续动态及前拍历史",
     "issue": 159, "url": f"{GITHUB}/issues/159#issuecomment-6107406228"},
    {"id": "R01-E02", "family": "R01", "title": "采样性能表征：采集结束误差、满足精度的采集时间和保持误差",
     "issue": 159, "url": f"{GITHUB}/issues/159#issuecomment-6107406228"},
    {"id": "R01-E03", "family": "R01", "title": "多路切换后的建立：选择器加共享采样级，处理前一通道残留",
     "issue": 159, "url": f"{GITHUB}/issues/159#issuecomment-6107406228"},
    {"id": "R01-E04", "family": "R01", "title": "保持与切换非理想：保持电压漂移、进入保持时的电压台阶",
     "issue": 159, "url": f"{GITHUB}/issues/159#issuecomment-6107406228"},
    {"id": "#225", "family": None, "title": "由真实电路数据建立并验证 Verilog-A 行为模型（IP 交付场景）",
     "issue": 225, "url": f"{GITHUB}/issues/225"},
]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def slugify(text: str) -> str:
    """GitHub-style heading anchor for candidate IDs such as C056-S1."""
    return re.sub(r"[^\w\- ]", "", text).strip().lower().replace(" ", "-")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bench", type=Path, default=WORKSPACE / "worktrees" / "benchmark-final-candidates",
                    help="Benchmark worktree (read-only; working copy is used)")
    ap.add_argument("--repo", type=Path, default=WORKSPACE / "current", help="any vaEVAS checkout (read-only)")
    args = ap.parse_args()

    bench = args.bench
    read = lambda rel: (bench / rel).read_text(encoding="utf-8")  # noqa: E731
    bench_head = git(bench, "rev-parse", "HEAD").strip()
    bench_dirty = bool(git(bench, "status", "--porcelain", "--", PLANNING, SELECTION).strip())
    main_sha = git(args.repo, "rev-parse", "origin/main").strip()
    uwb_sha = git(args.repo, "rev-parse", f"origin/{UWB_BRANCH}").strip()
    v4_dirs = {p.rsplit("/", 1)[1] for p in git(args.repo, "ls-tree", "--name-only", main_sha, V4_TASKS + "/").split()}
    v4_slug = {d[:3]: d[4:] for d in v4_dirs if re.fullmatch(r"\d{3}-.+", d) and int(d[:3]) <= 400}

    register = json.loads(read(f"{PLANNING}/register.json"))
    sources = json.loads(read(f"{PLANNING}/sources.json"))
    families = register["families"]
    cases_by_id = {c["case_id"]: c for c in register["cases"]}
    cand_page = f"{GITHUB}/blob/{BENCH_BRANCH}/{PLANNING}/CANDIDATES.md"

    tasks, cases = [], {}

    def add_case(case_id, family, title, kind, label, url):
        case = cases.setdefault(case_id, {"id": case_id, "family": family, "title": title, "kind": kind,
                                          "source": label, "url": url, "tasks": []})
        return case

    # ---- planning candidates ----------------------------------------------------------
    primary_v4 = {}
    for c in register["candidates"]:
        src = sources.get(c["primary_source"], {})
        label = src.get("label", "")
        m = re.match(r"v4:(\d{3})-", label)
        if m and c["family"] in families:
            primary_v4.setdefault(m.group(1), c)
        unit = c.get("case_anchor") or c["unit_id"]
        case_title = cases_by_id.get(unit, {}).get("title") or c["title"]
        case = add_case(unit, c["family"], case_title, "history" if unit.startswith("C") else "new",
                        label, f"{cand_page}#{slugify(c['task_id'])}")
        held = c["priority"] == "HOLD" or c["status"] == "conditional_reserve"
        tasks.append({
            "id": c["task_id"], "set": "candidate", "family": c["family"], "case": unit,
            "title": c["title"], "action": c["action"], "difficulty": c["difficulty"],
            "priority": "HOLD" if held else c["priority"],
            "status": "后备" if held else f"规划 {c['priority']}",
            "note": c.get("difference", ""), "url": f"{cand_page}#{slugify(c['task_id'])}",
        })
        case["tasks"].append(c["task_id"])

    # ---- first batch under construction --------------------------------------------------
    selection = json.loads(read(SELECTION))
    tasks_json = json.loads(read(f"{DRAFT}/tasks.json"))
    groups = tasks_json["function_groups"]
    draft_meta = {t["task_id"]: t for t in tasks_json["tasks"]}
    inferred = []
    for t in selection["tasks"]:
        task_id, source = t["task_id"], t["source_group"]
        nums = re.findall(r"(?<![\d])(\d{3})(?![\d])", source) if re.match(r"(v4|fractional|calibration|case-0018)", source) else []
        nums = [n for n in nums if n in v4_slug]
        same = primary_v4.get(nums[0]) if nums else None
        meta = draft_meta.get(task_id, {})
        review = groups.get(meta.get("function_group"), {}).get("review_id")
        if same:
            family = same["family"]
        else:
            family = FIRST30_FAMILY_OVERRIDE.get(task_id) or DRAFT_GROUP_FAMILY.get(review)
            inferred.append(task_id)
        if not family:
            raise SystemExit(f"{task_id}: no family")
        if source in OTHER_CIRCUITS:
            circuit = OTHER_CIRCUITS[source]
        elif nums:
            circuit = " + ".join(f"v4-{n} {v4_slug[n]}" for n in nums)
        else:
            raise SystemExit(f"{task_id}: source group {source!r} not mapped")
        case_id = same.get("case_anchor") or same["unit_id"] if same else f"src:{source}"
        if not same:
            add_case(case_id, family, circuit, "draft", source, None)
        cases[case_id]["tasks"].append(task_id)
        tasks.append({
            "id": task_id, "set": "first30", "slot": t["slot"], "family": family, "case": case_id,
            "title": meta.get("title", task_id), "action": ACTION_OF[t["engineering_action"]],
            "difficulty": None, "priority": None, "status": "建设中（首批30）",
            "circuit": circuit, "sameSource": same["task_id"] if same else None,
            "familyInferred": not same,
            "url": f"{GITHUB}/blob/{main_sha}/{DRAFT}/batches/{t['path'].replace('../', '')}/instruction.md",
        })

    # ---- requirement-driven task packages (IR-UWB TX, #223) ------------------------------
    uwb_readme = git(args.repo, "show", f"{uwb_sha}:{UWB_BATCH}/README.md")
    diff_of = {m.group(1): m.group(2).strip() for m in
               re.finditer(r"^\| \[([\w-]+)\]\([^)]*\) \| [^|]* \| ([^|]*) \|", uwb_readme, re.M)}
    uwb_case = add_case("uwb-tx-seed", "R06", "IR-UWB TX 种子链（8DPPM+8FSK 发射系统）", "requirement",
                        "#223", f"{GITHUB}/blob/{uwb_sha}/{DRAFT}/circuits/ir-uwb-tx/README.md")
    uwb_paths = git(args.repo, "ls-tree", "-r", "--name-only", uwb_sha, f"{UWB_BATCH}/tasks/").split()
    for path in sorted(p for p in uwb_paths if p.endswith("/task.toml")):
        task_id = path.split("/")[-2]
        meta = tomllib.loads(git(args.repo, "show", f"{uwb_sha}:{path}")).get("metadata", {})
        inst = git(args.repo, "show", f"{uwb_sha}:{path.rsplit('/', 1)[0]}/instruction.md")
        head = re.search(r"^# (.+)$", inst, re.M)
        tasks.append({
            "id": task_id, "set": "requirement", "family": "R06", "case": "uwb-tx-seed",
            "title": head.group(1).strip() if head else task_id,
            "action": ACTION_OF.get(meta.get("engineering_action", ""), "S"),
            "difficulty": diff_of.get(task_id), "priority": None, "status": "已建题包（需求驱动）",
            "note": "家族待定：#223 记录放进射频类或新开无线发射类，尚未决定",
            "url": f"{GITHUB}/blob/{uwb_sha}/{path.rsplit('/', 1)[0]}/instruction.md",
        })
        uwb_case["tasks"].append(task_id)

    # ---- assemble ------------------------------------------------------------------------
    used = [f for f in families if any(t["family"] == f for t in tasks)]
    data = {
        "meta": {
            "bench": {"branch": BENCH_BRANCH, "head": bench_head[:8], "dirty": bench_dirty},
            "uwb": {"branch": UWB_BRANCH, "head": uwb_sha[:8]},
            "main": main_sha[:8],
            "inferredFamily": inferred,
        },
        "categories": [{"id": c, "name": n} for c, n in CATEGORIES],
        "families": [{"id": f, "name": families[f], "cat": FAMILY_CATEGORY[f]} for f in used],
        "actions": ACTIONS,
        "difficulty": DIFFICULTY,
        "cases": list(cases.values()),
        "tasks": tasks,
        "ideas": IDEAS,
    }
    out = DOCS / "_generated"
    out.mkdir(exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (out / "circuit-map-data.html").write_text(
        f'<script type="application/json" id="cm-data">{payload}</script>\n', encoding="utf-8")

    fam_name = {f["id"]: f["name"] for f in data["families"]}
    case_title = {c["id"]: c["title"] for c in data["cases"]}
    order = {"first30": 0, "requirement": 1, "candidate": 2}
    lines = ["<!-- PROTOTYPE：由 tools/prototype_circuit_map.py 生成 -->", "",
             "| 题目 | 名称 | 功能家族 | 动作 | 电路 case | 状态 |", "| --- | --- | --- | --- | --- | --- |"]
    for t in sorted(tasks, key=lambda t: (used.index(t["family"]), order[t["set"]], t["id"])):
        lines.append(f"| [`{t['id']}`]({t['url']}) | {t['title']} | {fam_name[t['family']]} | "
                     f"{ACTIONS[t['action']]} | {case_title[t['case']]} | {t['status']} |")
    (out / "circuit-map-table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    by_set = {s: sum(t["set"] == s for t in tasks) for s in order}
    print(f"circuit map: {len(tasks)} tasks {by_set}, {len(cases)} circuit cases, {len(used)} families; "
          f"benchmark {BENCH_BRANCH}@{bench_head[:8]}{' + local changes' if bench_dirty else ''}, "
          f"uwb {UWB_BRANCH}@{uwb_sha[:8]}")
    print("  first-batch families inferred from draft groups:", ", ".join(inferred) or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
