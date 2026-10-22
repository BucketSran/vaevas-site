"""Project board for the local vaEVAS site, rendered from GitHub issues.

GitHub Issues stay the only task record; this hook only draws them. Data comes
from ``docs/_generated/github.json`` (written by ``tools/sync_issues.py``).

Placeholders:
- ``{{ board }}``: alerts, milestones and the stage columns (board page).
- ``{{ board_active }}``: links to in-progress issues (home page).
- ``{{ board_alert_count }}``: number of open alerts (home page).
"""

from __future__ import annotations

import datetime as dt
import html
import json
import logging
import re
from pathlib import Path

log = logging.getLogger("mkdocs.plugins.vaevas.board")

REPO_URL = "https://github.com/BucketSran/vaEVAS"
NEW_IDEA_URL = REPO_URL + "/issues/new?template=idea.md&labels=stage%3Aidea"
COMPARISON_URL = REPO_URL + "/blob/main/evas/docs/COMPARISON.md"
STAGES = [("idea", "想法"), ("design", "设计中"), ("planned", "已排期"), ("active", "进行中"), ("paused", "暂停")]
AREAS = {"area:evas": ("EVAS", "evas"), "area:benchmark": ("Benchmark", "benchmark"), "area:project": ("项目", "project")}
STALE_ACTIVE_DAYS = 14
STALE_OPEN_DAYS = 30
RECENT_DONE_DAYS = 14
DONE_CARDS = 8  # older closures stay one click away on GitHub
BULK_MENTION = 6  # a PR that mentions this many issues is a roundup, not a delivery
SUMMARY_CHARS = 90

_data: dict = {}
_posts: list[dict] = []
_status_date: dt.date | None = None
_bulk_prs: set[int] = set()


def _parse_time(value: str | None) -> dt.datetime | None:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def _days_ago(value: str | None) -> int:
    """Calendar days in local time, so yesterday evening is not "today"."""
    t = _parse_time(value)
    return (dt.date.today() - t.astimezone().date()).days if t else 0


def on_config(config):
    docs = Path(config["docs_dir"])
    source = docs / "_generated" / "github.json"
    _data.clear()
    if source.exists():
        _data.update(json.loads(source.read_text(encoding="utf-8")))
    else:
        log.warning("缺少 docs/_generated/github.json：先运行 ./site.sh sync")
    _posts.clear()
    for post in sorted((docs / "changelog" / "posts").glob("*.md")):
        text = post.read_text(encoding="utf-8")
        date = re.search(r"^date:\s*(\d{4})-(\d{2})-(\d{2})", text, re.M)
        slug = re.search(r"^slug:\s*(\S+)", text, re.M)
        title = re.search(r"^# (.+)$", text, re.M)
        if not (date and slug and title):
            continue
        mentions = {int(n) for n in re.findall(r"(?:issues|pull)/(\d+)", text)}
        mentions |= {int(n) for n in re.findall(r"(?<![\w/&])#(\d+)\b", text)}
        _posts.append({
            "date": dt.date(*map(int, date.groups())),
            "url": f"changelog/{date.group(1)}/{date.group(2)}/{date.group(3)}/{slug.group(1)}/",
            "title": title.group(1).strip(),
            "mentions": mentions,
        })
    global _status_date
    status = re.search(r"^status_date:\s*(\d{4}-\d{2}-\d{2})", (docs / "index.md").read_text(encoding="utf-8"), re.M)
    _status_date = dt.date.fromisoformat(status.group(1)) if status else None
    counts: dict[int, int] = {}
    for issue in _data.get("issues", []):
        for pr in issue["prs"]:
            counts[pr["number"]] = counts.get(pr["number"], 0) + 1
    _bulk_prs.clear()
    _bulk_prs.update(n for n, c in counts.items() if c >= BULK_MENTION)
    return config


def _stage(issue: dict) -> list[str]:
    return [label.split(":", 1)[1] for label in issue["labels"] if label.startswith("stage:")]


def _summary(body: str) -> str:
    text = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    current = re.search(r"^#{2,4} *(?:当前摘要|当前进展|本轮结果)[^\n]*\n(.*?)(?=^#{1,4} |\Z)", text, re.M | re.S)
    for para in re.split(r"\n\s*\n", current.group(1) if current else text):
        para = para.strip()
        if not para or para.startswith(("#", "|", "<", "```", "- [", "* [")):
            continue
        if "统一清单" in para or "只维护在" in para:
            continue  # boilerplate pointer to the EVAS feature list
        para = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", para)
        para = " ".join(re.sub(r"[*`>]", "", para).split())
        return para[:SUMMARY_CHARS] + ("…" if len(para) > SUMMARY_CHARS else "")
    return ""


def _alerts() -> list[str]:
    issues = [i for i in _data.get("issues", []) if i["state"] == "OPEN"]
    out = []

    def refs(items):
        return "、".join(f"[#{i['number']}]({i['url']})" for i in items)

    untriaged = [i for i in issues if len(_stage(i)) != 1]
    if untriaged:
        out.append(f"**待分诊**（没有阶段标签或不止一个）：{refs(untriaged)}")
    no_area = [i for i in issues if not any(label in AREAS for label in i["labels"])]
    if no_area:
        out.append(f"**缺领域标签**：{refs(no_area)}")
    contradiction = [i for i in issues if "wontfix" in i["labels"]]
    if contradiction:
        out.append(f"**状态矛盾**（标了 wontfix 却还开着）：{refs(contradiction)}")
    stale_active = [i for i in issues if _stage(i) == ["active"] and _days_ago(i["activeAt"]) > STALE_ACTIVE_DAYS]
    if stale_active:
        out.append(f"**进行中却超过 {STALE_ACTIVE_DAYS} 天没更新**：{refs(stale_active)}")
    idle = [i for i in issues if _stage(i) not in (["active"], ["paused"]) and _days_ago(i["activeAt"]) > STALE_OPEN_DAYS]
    if idle:
        out.append(f"**超过 {STALE_OPEN_DAYS} 天没更新**：{refs(idle)}")
    mentioned = set().union(*(p["mentions"] for p in _posts)) if _posts else set()
    unlogged = [p for p in _data.get("merged_prs", []) if p["number"] not in mentioned]
    if unlogged:
        unlogged.sort(key=lambda p: p["number"])
        shown = "、".join(f"[#{p['number']}]({p['url']})" for p in unlogged[:20])
        more = f" 等 {len(unlogged)} 个" if len(unlogged) > 20 else ""
        out.append(f"**已合入但没写进更新日志的 PR**：{shown}{more}")
    if _posts and _status_date and max(p["date"] for p in _posts) > _status_date:
        out.append(f"**首页状态卡（{_status_date}）比最新一条更新日志旧**：核对“最新阶段”是否要更新")
    return out


def _card(issue: dict, prefix: str, done: bool = False) -> str:
    e = html.escape
    area = next((AREAS[label] for label in issue["labels"] if label in AREAS), None)
    area_html = f'<span class="vb-area vb-area-{area[1]}">{area[0]}</span>' if area else ""
    days = _days_ago(issue["closedAt"] if done else issue["activeAt"])
    when = "今天" if days == 0 else f"{days} 天前"
    stale = not done and (
        (_stage(issue) == ["active"] and days > STALE_ACTIVE_DAYS)
        or (_stage(issue) not in (["active"], ["paused"]) and days > STALE_OPEN_DAYS))
    prs = [p for p in issue["prs"] if p["number"] not in _bulk_prs]
    bulk = len(issue["prs"]) - len(prs)
    pr_html = " ".join(
        f'<a class="vb-pr vb-pr-{p["state"].lower()}{" vb-pr-draft" if p.get("isDraft") else ""}" href="{e(p["url"])}" '
        f'title="{e(p["title"])}">#{p["number"]}</a>' for p in prs[-4:])
    if bulk:
        pr_html += f' <span class="vb-muted">另有 {bulk} 个汇总 PR 提及</span>'
    logs = [p for p in _posts if issue["number"] in p["mentions"]][-2:]
    log_html = "".join(
        f'<div class="vb-log">日志 <a href="{prefix}{p["url"]}">{p["date"]:%m-%d} {e(p["title"][:28])}</a></div>' for p in logs)
    gaps = list(dict.fromkeys(re.findall(r"GAP(\d{2})", issue["body"])))[:4]
    gap_html = "".join(f'<a class="vb-gap" href="{COMPARISON_URL}#gap-{g}">GAP{g}</a>' for g in gaps)
    reason = ""
    if done:
        reason = '<span class="vb-done">完成</span>' if issue["stateReason"] == "COMPLETED" else '<span class="vb-dropped">不做</span>'
    summary = "" if done else _summary(issue["body"])
    return (
        f'<div class="vb-card{" vb-stale" if stale else ""}">'
        f'<div class="vb-head"><a href="{e(issue["url"])}">#{issue["number"]}</a>{area_html}{reason}</div>'
        f'<div class="vb-title"><a href="{e(issue["url"])}">{e(issue["title"])}</a></div>'
        + (f'<div class="vb-summary">{e(summary)}</div>' if summary else "")
        + f'<div class="vb-meta">{"关闭" if done else "更新"}于 {when}{" · PR " + pr_html if pr_html else ""}</div>'
        + log_html
        + (f'<div class="vb-gaps">{gap_html}</div>' if gap_html else "")
        + "</div>"
    )


def _columns(prefix: str) -> str:
    issues = _data.get("issues", [])
    open_issues = [i for i in issues if i["state"] == "OPEN"]
    cols = []
    untriaged = [i for i in open_issues if len(_stage(i)) != 1]
    if untriaged:
        cols.append(("untriaged", "待分诊", untriaged, False))
    for key, name in STAGES:
        cols.append((key, name, [i for i in open_issues if _stage(i) == [key]], False))
    recent = [i for i in issues if i["state"] == "CLOSED" and _days_ago(i["closedAt"]) <= RECENT_DONE_DAYS]
    cols.append(("done", f"最近 {RECENT_DONE_DAYS} 天关闭", recent, True))
    parts = ['<div class="vb-board">']
    for key, name, items, done in cols:
        items = sorted(items, key=lambda i: i["closedAt" if done else "activeAt"] or "", reverse=True)
        shown = items[:DONE_CARDS] if done else items
        cards = "".join(_card(i, prefix, done) for i in shown) or '<div class="vb-empty">暂无</div>'
        if len(shown) < len(items):
            cards += (f'<div class="vb-more"><a href="{REPO_URL}/issues?q=is%3Aissue+is%3Aclosed+sort%3Aupdated-desc">'
                      f'另外 {len(items) - len(shown)} 个 →</a></div>')
        parts.append(f'<div class="vb-col vb-col-{key}"><div class="vb-col-head">{name}'
                     f'<span class="vb-count">{len(items)}</span></div>{cards}</div>')
    parts.append("</div>")
    return "".join(parts)


def _milestones() -> str:
    ms = [m for m in _data.get("milestones", []) if m["state"] == "open"]
    if not ms:
        return (f"还没有里程碑。在 GitHub 上[建立里程碑]({REPO_URL}/milestones)（例如“DAC 投稿冻结”，填上截止日期），"
                "再把相关 Issue 归进去，这里就会显示完成进度。")
    rows = ["| 里程碑 | 截止 | 进度 |", "| --- | --- | --- |"]
    for m in ms:
        total = m["open"] + m["closed"]
        pct = round(100 * m["closed"] / total) if total else 0
        due = (m["due_on"] or "")[:10] or "未定"
        rows.append(f"| [{m['title']}]({m['url']}) | {due} | {m['closed']}/{total}（{pct}%） |")
    return "\n".join(rows)


def _board(prefix: str) -> str:
    issues = _data.get("issues", [])
    open_n = sum(i["state"] == "OPEN" for i in issues)
    active_n = sum(i["state"] == "OPEN" and _stage(i) == ["active"] for i in issues)
    done_n = sum(i["state"] == "CLOSED" and _days_ago(i["closedAt"]) <= RECENT_DONE_DAYS for i in issues)
    alerts = _alerts()
    alert_md = (f'!!! warning "需要处理的提醒（{len(alerts)}）"\n' + "".join(f"    - {a}\n" for a in alerts)
                if alerts else '!!! success "没有需要处理的提醒"\n')
    fetched = _data.get("fetched_at", "未抓取").replace("T", " ")
    return "\n".join([
        f'[:material-lightbulb-on-outline: 记一个想法]({NEW_IDEA_URL}){{ .md-button .md-button--primary }} '
        f'[:material-github: 在 GitHub 上查看全部 Issue]({REPO_URL}/issues){{ .md-button }}',
        "",
        f"开着的 Issue {open_n} 个，其中进行中 {active_n} 个；最近 {RECENT_DONE_DAYS} 天关闭 {done_n} 个；"
        f"已合入 PR {len(_data.get('merged_prs', []))} 个。Issue 数据抓取于 {fetched}。",
        "",
        alert_md,
        "## 里程碑",
        "",
        _milestones(),
        "",
        "## 看板",
        "",
        _columns(prefix),
        "",
    ])


def on_page_markdown(markdown, page, config, files):
    prefix = "../" * page.url.count("/")
    if "{{ board }}" in markdown:
        markdown = markdown.replace("{{ board }}", _board(prefix))
    if "{{ board_active }}" in markdown:
        active = [i for i in _data.get("issues", []) if i["state"] == "OPEN" and _stage(i) == ["active"]]
        links = "、".join(f"[#{i['number']} {i['title']}]({i['url']})" for i in active) or "无"
        markdown = markdown.replace("{{ board_active }}", links)
    if "{{ board_alert_count }}" in markdown:
        markdown = markdown.replace("{{ board_alert_count }}", str(len(_alerts())))
    return markdown
