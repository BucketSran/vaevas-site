"""Import canonical vaEVAS docs from a Git ref into the local site.

The site never copies tables or manuals by hand. This script reads the
requested ref (default ``origin/main``) through ``git show``, rewrites
relative links, and writes generated files under ``docs/evas/manual/`` and
``docs/_generated/``. Run it before every build; ``site.sh`` does so.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import posixpath
import re
import subprocess
import sys
import tomllib
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
DOCS = SITE / "docs"
DEFAULT_REPO = SITE.parents[1] / "current"
GITHUB = "https://github.com/BucketSran/vaEVAS"

# Repository path -> site page path (relative to docs/). Whole-file imports.
WHOLE_IMPORTS = {
    "evas/docs/math/README.md": "evas/manual/math/README.md",
    "evas/docs/math/solving.md": "evas/manual/math/solving.md",
    "evas/docs/math/events.md": "evas/manual/math/events.md",
    "evas/docs/math/operators.md": "evas/manual/math/operators.md",
    "evas/docs/math/continuous.md": "evas/manual/math/continuous.md",
    "evas/docs/COMPARISON-METHODOLOGY.md": "evas/manual/COMPARISON-METHODOLOGY.md",
}
# The comparison table is imported partially (sections 1-5) into this page.
COMPARISON_SRC = "evas/docs/COMPARISON.md"
COMPARISON_PAGE = "evas/comparison.md"
COMPARISON_LAST_SECTION = 5
BACKENDS = ["Spectre", "ngspice + OpenVAF-R", "Gnucap + modelgen-verilog", "EVAS"]
OPEN_SOURCE = ["ngspice + OpenVAF-R", "Gnucap + modelgen-verilog"]

DRAFT_BATCHES = "benchmark/material/draftbench/batches"
DRAFT_TASKS_JSON = "benchmark/material/draftbench/tasks.json"
DRAFT_CATALOG = "benchmark/material/draftbench/catalog.json"
FORMAL_LIST = "benchmark/tasks/benchmark.toml"

LINK_RE = re.compile(r"(?<!!)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^()\s]+)\)")
ANCHOR_ID_RE = re.compile(r'<a id="([^"]+)"')
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def gh_slug(text: str) -> str:
    """Approximate the GitHub / pymdownx heading slug (keeps CJK)."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*]", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors_in(markdown: str) -> set[str]:
    found = set(ANCHOR_ID_RE.findall(markdown))
    for _, title in HEADING_RE.findall(markdown):
        found.add(gh_slug(title))
    return found


class LinkRewriter:
    def __init__(self, sha: str, repo_paths: set[str], partial_anchors: dict[str, set[str]]):
        self.sha = sha
        self.repo_paths = repo_paths
        self.repo_dirs = {posixpath.dirname(p) for p in repo_paths}
        for path in list(self.repo_dirs):
            while path:
                path = posixpath.dirname(path)
                self.repo_dirs.add(path)
        self.page_of = dict(WHOLE_IMPORTS)
        self.page_of[COMPARISON_SRC] = COMPARISON_PAGE
        self.partial_anchors = partial_anchors
        self.external = 0
        self.internal = 0

    def github(self, path: str, anchor: str) -> str:
        kind = "tree" if path in self.repo_dirs and path not in self.repo_paths else "blob"
        url = f"{GITHUB}/{kind}/{self.sha}/{path}"
        return url + (f"#{anchor}" if anchor else "")

    def target(self, src_repo_path: str, dest_page: str, href: str) -> str:
        if href.startswith("#"):
            # Same-file anchor that was cut away by a partial import.
            anchors = self.partial_anchors.get(src_repo_path)
            if anchors is not None and href[1:] not in anchors:
                self.external += 1
                return self.github(src_repo_path, href[1:])
            return href
        if re.match(r"^[a-z][a-z0-9+.-]*:", href):
            return href
        path, _, anchor = href.partition("#")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(src_repo_path), path))
        page = self.page_of.get(resolved)
        if page and (resolved not in self.partial_anchors or not anchor
                     or anchor in self.partial_anchors[resolved]):
            if page == dest_page and anchor:
                return f"#{anchor}"
            self.internal += 1
            rel = posixpath.relpath(page, posixpath.dirname(dest_page))
            return rel + (f"#{anchor}" if anchor else "")
        self.external += 1
        return self.github(resolved, anchor)

    def rewrite(self, markdown: str, src_repo_path: str, dest_page: str) -> str:
        return LINK_RE.sub(
            lambda m: f"[{m.group(1)}]({self.target(src_repo_path, dest_page, m.group(2))})",
            markdown,
        )


def split_comparison(markdown: str) -> str:
    """Keep the preamble and sections 1..COMPARISON_LAST_SECTION."""
    cut = re.search(rf"^## {COMPARISON_LAST_SECTION + 1}\. ", markdown, re.M)
    if not cut:
        raise SystemExit(f"{COMPARISON_SRC}: section {COMPARISON_LAST_SECTION + 1} heading not found")
    kept = markdown[: cut.start()]
    # Drop the trailing anchor that belongs to the next section.
    kept = re.sub(r'\n<a id="[^"]+"></a>\s*$', "\n", kept.rstrip() + "\n")
    # The page supplies its own title.
    return re.sub(r"\A# [^\n]*\n", "", kept)


def parse_tables(markdown: str) -> list[dict]:
    sections = []
    current = None
    for line in markdown.splitlines():
        heading = re.match(r"^## (\d+)\. (.+)$", line)
        if heading:
            current = {"no": int(heading.group(1)), "title": heading.group(2).strip(), "rows": []}
            sections.append(current)
            continue
        if current is None or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 1 + len(BACKENDS) or cells[0].startswith("---") or cells[0] == "能力与测试范围":
            continue
        name = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cells[0])
        current["rows"].append({"name": name, **dict(zip(BACKENDS, cells[1:]))})
    return [s for s in sections if s["no"] <= COMPARISON_LAST_SECTION]


def passed(cell: str) -> bool:
    return cell.startswith("✓")


def summary_markdown(sections: list[dict], short: str) -> str:
    head = "| 层级 | 用例 | " + " | ".join(BACKENDS) + " |"
    sep = "| --- | ---: | " + " | ".join("---:" for _ in BACKENDS) + " |"
    lines = [head, sep]
    totals = {b: 0 for b in BACKENDS}
    n_total = 0
    for s in sections:
        n = len(s["rows"])
        n_total += n
        counts = []
        for b in BACKENDS:
            c = sum(passed(r[b]) for r in s["rows"])
            totals[b] += c
            counts.append(f"{c}")
        lines.append(f"| {s['no']}. {s['title']} | {n} | " + " | ".join(counts) + " |")
    lines.append(f"| **合计** | **{n_total}** | " + " | ".join(f"**{totals[b]}**" for b in BACKENDS) + " |")

    rows = [r for s in sections for r in s["rows"]]
    evas_only_open = [r for r in rows if passed(r["EVAS"]) and not any(passed(r[b]) for b in OPEN_SOURCE)]
    evas_only = [r for r in rows if passed(r["EVAS"]) and not any(passed(r[b]) for b in BACKENDS[:-1])]
    evas_fail = [r for r in rows if not passed(r["EVAS"])]

    def bullet(rs: list[dict], cols: list[str]) -> list[str]:
        if not rs:
            return ["- 无"]
        return [f"- {r['name']}：" + "；".join(f"{c} {r[c]}" for c in cols) for r in rs]

    out = [
        f"<!-- 由 tools/sync_main.py 从 main@{short} 的 {COMPARISON_SRC} 生成，请勿手改 -->",
        "",
        "表中数字是“该档通过”（✓）的用例数，口径与完整对比表相同：✓ 表示本行全部必测用例的数值、时间、状态和关键边界均通过所标精度档。",
        "",
        *lines,
        "",
        f'??? success "EVAS 通过、两个开源后端未通过或未验收：{len(evas_only_open)} 项"',
        "",
        *["    " + x for x in bullet(evas_only_open, OPEN_SOURCE)],
        "",
        f'??? success "其他三个后端都未通过或未验收：{len(evas_only)} 项"',
        "",
        *["    " + x for x in bullet(evas_only, BACKENDS[:-1])],
        "",
        f'??? warning "EVAS 未通过或未验收：{len(evas_fail)} 项"',
        "",
        *["    " + x for x in bullet(evas_fail, ["EVAS"])],
        "",
    ]
    return "\n".join(out)


def benchmark_markdown(show, repo_paths: set[str], sha: str) -> tuple[str, str, dict]:
    """Action counts, per-batch task tables and totals for the benchmark preview page.

    Snippets are inserted after the page hooks run, so links are full GitHub URLs.
    """
    short = sha[:8]
    formal = tomllib.loads(show(FORMAL_LIST)).get("tasks", [])
    formal_ids = {t if isinstance(t, str) else t.get("id", t.get("name")) for t in formal}
    tasks_json = json.loads(show(DRAFT_TASKS_JSON))
    groups = tasks_json["function_groups"]
    by_id = {t["task_id"]: t for t in tasks_json["tasks"]}
    actions = json.loads(show(DRAFT_CATALOG))["categories"]

    found: dict[str, list[str]] = {}
    for path in sorted(repo_paths):
        m = re.fullmatch(rf"{DRAFT_BATCHES}/([^/]+)/tasks/([^/]+)/task\.toml", path)
        if m:
            found.setdefault(m.group(1), []).append(m.group(2))
    # Keep the order of the batch index; batches it does not list go last.
    listed = re.findall(r"^\| \[([^\]]+)\]\(", show(f"{DRAFT_BATCHES}/README.md"), re.M)
    batches = {b: found[b] for b in listed if b in found}
    batches.update({b: t for b, t in found.items() if b not in batches})

    def group_label(key):
        g = groups.get(key)
        return f"{g['title']}（{g['review_id']}）" if g else "未记录"

    out = [f"<!-- 由 tools/sync_main.py 从 main@{short} 生成，请勿手改 -->", ""]
    counts: dict[str, dict[str, int]] = {}
    sections = []
    for batch, task_ids in batches.items():
        rows = []
        for i, task_id in enumerate(task_ids, 1):
            base = f"{DRAFT_BATCHES}/{batch}/tasks/{task_id}"
            meta = tomllib.loads(show(f"{base}/task.toml")).get("metadata", {})
            action = actions.get(meta.get("engineering_action", ""), meta.get("engineering_action") or "未记录")
            counts.setdefault(action, {}).setdefault(batch, 0)
            counts[action][batch] += 1
            entry = by_id.get(task_id)
            if entry:
                title, group = entry["title"], group_label(entry["function_group"])
            else:
                title = task_id
                if f"{base}/instruction.md" in repo_paths:
                    head = re.search(r"^# (.+)$", show(f"{base}/instruction.md"), re.M)
                    title = head.group(1).strip() if head else task_id
                prefix = re.match(r"(r\d\d)-", batch)
                key = next((k for k, g in groups.items()
                            if prefix and g["review_id"].lower() == prefix.group(1)), None)
                group = group_label(key)
            if task_id in formal_ids:
                status = "已录取"
            elif meta.get("stage"):
                pending = "、".join(meta.get("pending", [])) or "无"
                status = f"待审核（`stage = {meta['stage']}`；待定：{pending}）"
            else:
                status = "待审核"
            doc = f"{base}/instruction.md" if f"{base}/instruction.md" in repo_paths else f"{base}/task.toml"
            rows.append(f"| {i} | [`{task_id}`]({GITHUB}/blob/{sha}/{doc}) | {title} | {action} | {group} | {status} |")
        sections += [f"### {batch}（{len(task_ids)} 题）", "",
                     "| # | 题号 | 名称 | 工程动作 | 电路功能组 | 状态 |",
                     "| ---: | --- | --- | --- | --- | --- |", *rows, ""]

    names = list(batches)
    order = [a for a in actions.values() if a in counts] + [a for a in counts if a not in actions.values()]
    out += ["| 工程动作 | " + " | ".join(names) + " | 合计 |",
            "| --- | " + " | ".join("---:" for _ in names) + " | ---: |"]
    for action in order:
        row = [counts[action].get(b, 0) for b in names]
        out.append(f"| {action} | " + " | ".join(map(str, row)) + f" | {sum(row)} |")
    totals = [len(batches[b]) for b in names]
    out += ["| **合计** | " + " | ".join(f"**{n}**" for n in totals) + f" | **{sum(totals)}** |", ""]
    stats = {
        "formal": len(formal_ids),
        "drafts": sum(totals),
        "batches": {b: len(batches[b]) for b in names},
    }
    banner = f"<!-- 由 tools/sync_main.py 从 main@{short} 生成，请勿手改 -->"
    return "\n".join(out), "\n".join([banner, "", *sections]), stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=DEFAULT_REPO, help="any checkout of vaEVAS (read-only use)")
    ap.add_argument("--ref", default="origin/main")
    ap.add_argument("--no-fetch", action="store_true", help="skip git fetch (offline)")
    args = ap.parse_args()

    if not args.no_fetch:
        try:
            git(args.repo, "fetch", "-q", "origin")
        except subprocess.CalledProcessError as exc:
            print(f"warning: git fetch failed, using local {args.ref}: {exc.stderr.strip()}", file=sys.stderr)
    sha = git(args.repo, "rev-parse", f"{args.ref}^{{commit}}").strip()
    short = sha[:8]
    date = git(args.repo, "show", "-s", "--format=%cs", sha).strip()
    repo_paths = set(git(args.repo, "ls-tree", "-r", "--name-only", sha).splitlines())

    def show(path: str) -> str:
        return git(args.repo, "show", f"{sha}:{path}")

    comparison = split_comparison(show(COMPARISON_SRC))
    rewriter = LinkRewriter(sha, repo_paths, {COMPARISON_SRC: anchors_in(comparison)})
    banner = f"<!-- 由 tools/sync_main.py 从 main@{short} 导入，请勿手改 -->\n\n"

    for src, dest in WHOLE_IMPORTS.items():
        out = DOCS / dest
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(banner + rewriter.rewrite(show(src), src, dest), encoding="utf-8")

    generated = DOCS / "_generated"
    generated.mkdir(exist_ok=True)
    (generated / "comparison-tables.md").write_text(
        banner + rewriter.rewrite(comparison, COMPARISON_SRC, COMPARISON_PAGE), encoding="utf-8"
    )
    sections = parse_tables(comparison)
    (generated / "comparison-summary.md").write_text(summary_markdown(sections, short), encoding="utf-8")
    bench_counts, bench_tasks, bench = benchmark_markdown(show, repo_paths, sha)
    (generated / "benchmark-counts.md").write_text(bench_counts, encoding="utf-8")
    (generated / "benchmark-tasks.md").write_text(bench_tasks, encoding="utf-8")
    (generated / "repo-files.txt").write_text("\n".join(sorted(repo_paths)) + "\n", encoding="utf-8")
    (generated / "source.json").write_text(
        json.dumps(
            {
                "ref": args.ref,
                "sha": sha,
                "short": short,
                "commit_date": date,
                "synced_at": dt.datetime.now().isoformat(timespec="seconds"),
                "comparison_rows": sum(len(s["rows"]) for s in sections),
                "benchmark": bench,
                "comparison_passed": {
                    b: sum(passed(r[b]) for s in sections for r in s["rows"]) for b in BACKENDS
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"synced {args.ref} -> main@{short} ({date}); "
        f"{len(WHOLE_IMPORTS)} manual pages, {sum(len(s['rows']) for s in sections)} comparison rows; "
        f"links: {rewriter.internal} in-site, {rewriter.external} to GitHub"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
