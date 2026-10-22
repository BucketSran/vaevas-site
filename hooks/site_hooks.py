"""MkDocs hooks for the local vaEVAS site.

- ``repo:<path>#anchor`` links become GitHub links pinned to the synced main
  commit; unknown paths are reported (and fail ``--strict`` builds).
- The footer names the main commit the site content was imported from.
- ``{{ cmp_evas }}``-style placeholders take numbers from the synced comparison table.
- The status card on the home page shows a reminder when it is stale.
- ``{{ errata_summary }}`` counts the errata tables of the Reference pages and
  checks that every row has a unique ID and one of the allowed states.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import re
from pathlib import Path

log = logging.getLogger("mkdocs.plugins.vaevas")

GITHUB = "https://github.com/BucketSran/vaEVAS"
STATUS_STALE_DAYS = 14
REPO_LINK_RE = re.compile(r"\]\(repo:([^)#\s]+)(#[^)\s]*)?\)")
ERRATA_ROW_RE = re.compile(r"^\|\s*((?:v1|v2|v3|v4|early)-E\d{3})\s*\|", re.M)
ERRATA_STATES = ["已确认", "待 Spectre", "已撤回", "归 EVAS 修", "进行中"]
# Reference page -> label in the summary table, in display order.
ERRATA_PAGES = {
    "vabench-v1.md": "v1",
    "vabench-v2-v3.md": "v2 / v3",
    "vabench-v4.md": "v4",
    "early-tasks.md": "早期题包",
}
ERRATA_ANCHOR = "#3-已知问题勘误表"

_source: dict = {}
_repo_files: set[str] = set()
_repo_dirs: set[str] = set()


def on_config(config):
    generated = Path(config["docs_dir"]) / "_generated"
    source = generated / "source.json"
    if not source.exists():
        raise SystemExit("缺少 docs/_generated/source.json：先运行 ./site.sh sync")
    _source.clear()
    _source.update(json.loads(source.read_text(encoding="utf-8")))
    _repo_files.clear()
    _repo_files.update((generated / "repo-files.txt").read_text(encoding="utf-8").split())
    _repo_dirs.clear()
    for path in _repo_files:
        parts = path.split("/")[:-1]
        for i in range(1, len(parts) + 1):
            _repo_dirs.add("/".join(parts[:i]))
    config["copyright"] = (
        f"内容导入自 main@{_source['short']}（提交日期 {_source['commit_date']}，"
        f"同步于 {_source['synced_at'].replace('T', ' ')}）"
    )
    return config


def _repo_url(match: re.Match, page) -> str:
    path = match.group(1).strip("/")
    anchor = match.group(2) or ""
    if path in _repo_files:
        kind = "blob"
    elif path in _repo_dirs:
        kind = "tree"
    else:
        log.warning("%s: repo:%s 不在 main@%s 上", page.file.src_uri, path, _source["short"])
        kind = "blob"
    return f"]({GITHUB}/{kind}/{_source['sha']}/{path}{anchor})"


def _placeholders() -> dict[str, str]:
    passed = _source.get("comparison_passed", {})
    bench = _source.get("benchmark", {})
    batches = bench.get("batches", {})
    return {
        "bench_formal": str(bench.get("formal", "?")),
        "bench_drafts": str(bench.get("drafts", "?")),
        "bench_batches": "、".join(f"{b} {n}" for b, n in batches.items()) or "?",
        "main_short": _source["short"],
        "main_date": _source["commit_date"],
        "cmp_total": str(_source.get("comparison_rows", "?")),
        "cmp_spectre": str(passed.get("Spectre", "?")),
        "cmp_ngspice": str(passed.get("ngspice + OpenVAF-R", "?")),
        "cmp_gnucap": str(passed.get("Gnucap + modelgen-verilog", "?")),
        "cmp_evas": str(passed.get("EVAS", "?")),
    }


def _errata_summary(docs_dir: Path) -> str:
    seen: dict[str, str] = {}
    rows = []
    totals = {state: 0 for state in ERRATA_STATES}
    for name, label in ERRATA_PAGES.items():
        counts = {state: 0 for state in ERRATA_STATES}
        text = (docs_dir / "reference" / name).read_text(encoding="utf-8")
        for line in text.splitlines():
            match = ERRATA_ROW_RE.match(line)
            if not match:
                continue
            errata_id = match.group(1)
            if errata_id in seen:
                log.warning("勘误编号重复：%s（%s 与 %s）", errata_id, seen[errata_id], name)
            seen[errata_id] = name
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            state = cells[4] if len(cells) >= 6 else ""
            if state not in counts:
                log.warning("%s: %s 的状态“%s”不在允许的五种状态里", name, errata_id, state)
                continue
            counts[state] += 1
            totals[state] += 1
        rows.append(f"| [{label}]({name}{ERRATA_ANCHOR}) | "
                    + " | ".join(str(counts[s]) for s in ERRATA_STATES)
                    + f" | {sum(counts.values())} |")
    head = "| 版本 | " + " | ".join(ERRATA_STATES) + " | 合计 |"
    sep = "| --- | " + " | ".join("---:" for _ in ERRATA_STATES) + " | ---: |"
    total = ("| **合计** | " + " | ".join(f"**{totals[s]}**" for s in ERRATA_STATES)
             + f" | **{sum(totals.values())}** |")
    return "\n".join([head, sep, *rows, total])


def on_page_markdown(markdown, page, config, files):
    markdown = REPO_LINK_RE.sub(lambda m: _repo_url(m, page), markdown)
    for key, value in _placeholders().items():
        markdown = markdown.replace("{{ " + key + " }}", value)
    batches = _source.get("benchmark", {}).get("batches", {})

    def batch_count(match):
        if match.group(1) not in batches:
            log.warning("%s: main 上没有草稿批次 %s", page.file.src_uri, match.group(1))
            return "?"
        return str(batches[match.group(1)])

    markdown = re.sub(r"\{\{ bench_batch:([\w.-]+) \}\}", batch_count, markdown)
    if "{{ errata_summary }}" in markdown:
        markdown = markdown.replace("{{ errata_summary }}", _errata_summary(Path(config["docs_dir"])))
    status_date = page.meta.get("status_date")
    if status_date:
        if isinstance(status_date, str):
            status_date = dt.date.fromisoformat(status_date)
        age = (dt.date.today() - status_date).days
        if age > STATUS_STALE_DAYS:
            log.info("%s: 状态卡已 %d 天未更新", page.file.src_uri, age)
            markdown = markdown.replace(
                "<!-- status-stale -->",
                f'!!! warning "状态卡已 {age} 天未更新"\n    下面的数字可能过时，以链接的原始记录为准。\n',
            )
    return markdown
