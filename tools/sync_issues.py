"""Fetch GitHub issues, PRs and milestones for the project board.

Writes ``docs/_generated/github.json``. Uses the local ``gh`` login. When GitHub
is unreachable, the previous snapshot is kept so the site still builds; the
board page shows when the data was fetched.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO = "BucketSran/vaEVAS"
OUT = Path(__file__).resolve().parents[1] / "docs" / "_generated" / "github.json"
BODY_CHARS = 4000

ISSUES_QUERY = """
query($cursor: String) {
  repository(owner: "BucketSran", name: "vaEVAS") {
    issues(first: 50, after: $cursor, orderBy: {field: CREATED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title url state stateReason createdAt updatedAt closedAt lastEditedAt body
        comments(last: 1) { nodes { updatedAt } }
        labels(first: 20) { nodes { name } }
        milestone { title }
        timelineItems(itemTypes: [CROSS_REFERENCED_EVENT, CONNECTED_EVENT], first: 50) {
          nodes {
            __typename
            ... on CrossReferencedEvent { source { __typename ... on PullRequest { number title url state isDraft } } }
            ... on ConnectedEvent { subject { __typename ... on PullRequest { number title url state isDraft } } }
          }
        }
      }
    }
  }
}
"""


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def fetch_issues() -> list[dict]:
    issues, cursor = [], None
    while True:
        args = ["api", "graphql", "-f", f"query={ISSUES_QUERY}"]
        if cursor:
            args += ["-f", f"cursor={cursor}"]
        page = json.loads(gh(*args))["data"]["repository"]["issues"]
        for node in page["nodes"]:
            prs = {}
            for item in node["timelineItems"]["nodes"]:
                pr = item.get("source") or item.get("subject") or {}
                if pr.get("__typename") == "PullRequest":
                    prs[pr["number"]] = {k: pr[k] for k in ("number", "title", "url", "state", "isDraft")}
            issues.append({
                "number": node["number"],
                "title": node["title"],
                "url": node["url"],
                "state": node["state"],
                "stateReason": node["stateReason"],
                "createdAt": node["createdAt"],
                "updatedAt": node["updatedAt"],
                # Label edits also bump updatedAt; activity counts only text and comments.
                "activeAt": max(t for t in (node["createdAt"], node["lastEditedAt"],
                                            *(c["updatedAt"] for c in node["comments"]["nodes"])) if t),
                "closedAt": node["closedAt"],
                "labels": [label["name"] for label in node["labels"]["nodes"]],
                "milestone": (node["milestone"] or {}).get("title"),
                "body": (node["body"] or "")[:BODY_CHARS],
                "prs": sorted(prs.values(), key=lambda p: p["number"]),
            })
        if not page["pageInfo"]["hasNextPage"]:
            return issues
        cursor = page["pageInfo"]["endCursor"]


def main() -> int:
    try:
        issues = fetch_issues()
        merged = json.loads(gh("pr", "list", "-R", REPO, "--state", "merged", "--limit", "1000",
                               "--json", "number,title,mergedAt,url"))
        open_prs = json.loads(gh("pr", "list", "-R", REPO, "--state", "open", "--limit", "200",
                                 "--json", "number,title,url,isDraft,updatedAt"))
        milestones = json.loads(gh("api", f"repos/{REPO}/milestones?state=all&per_page=100"))
    except (subprocess.CalledProcessError, FileNotFoundError, KeyError, json.JSONDecodeError) as exc:
        detail = getattr(exc, "stderr", "") or exc
        if OUT.exists():
            print(f"warning: GitHub 数据抓取失败，沿用上次的快照：{str(detail).strip()[:200]}", file=sys.stderr)
            return 0
        print(f"warning: GitHub 数据抓取失败，看板为空：{str(detail).strip()[:200]}", file=sys.stderr)
        issues, merged, open_prs, milestones = [], [], [], []
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "fetched_at": dt.datetime.now().isoformat(timespec="seconds"),
        "issues": issues,
        "merged_prs": merged,
        "open_prs": open_prs,
        "milestones": [{
            "title": m["title"], "url": m["html_url"], "state": m["state"], "due_on": m["due_on"],
            "open": m["open_issues"], "closed": m["closed_issues"], "description": m["description"],
        } for m in milestones],
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"github: {len(issues)} issues, {len(merged)} merged PRs, {len(open_prs)} open PRs, "
          f"{len(milestones)} milestones")
    return 0


if __name__ == "__main__":
    sys.exit(main())
