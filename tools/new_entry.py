"""Create a new changelog entry for the local vaEVAS site.

Example:
    ./site.sh new-entry --title "PR208 合入 main" --category EVAS --slug pr208-merged
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

POSTS = Path(__file__).resolve().parents[1] / "docs" / "changelog" / "posts"
CATEGORIES = ("EVAS", "Benchmark", "项目")
TEMPLATE = """---
date: {date}
categories:
{categories}
slug: {slug}
---

# {title}

{summary}

<!-- more -->

## 做了什么

## 结果与证据

## 遗留与下一步

## 相关链接
"""


def existing_slugs() -> set[str]:
    slugs = set()
    for post in POSTS.glob("*.md"):
        match = re.search(r"^slug:\s*(\S+)", post.read_text(encoding="utf-8"), re.M)
        if match:
            slugs.add(match.group(1))
    return slugs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True, help="中文标题，一句话说清这次更新")
    ap.add_argument("--slug", required=True, help="英文小写和连字符，全站唯一")
    ap.add_argument("--category", action="append", choices=CATEGORIES, required=True,
                    help="可重复：EVAS / Benchmark / 项目")
    ap.add_argument("--date", default=dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    help="默认当前时间；同一天多条靠时间排序")
    ap.add_argument("--summary", default="一到两句摘要：结果是什么，数字带口径。")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        ap.error("slug 只能用英文小写、数字和连字符")
    if args.slug in existing_slugs():
        ap.error(f"slug 已存在：{args.slug}")
    day = args.date[:10]
    dt.date.fromisoformat(day)
    path = POSTS / f"{day}-{args.slug}.md"
    if path.exists():
        ap.error(f"文件已存在：{path}")

    POSTS.mkdir(parents=True, exist_ok=True)
    path.write_text(
        TEMPLATE.format(
            date=args.date,
            categories="\n".join(f"  - {c}" for c in dict.fromkeys(args.category)),
            slug=args.slug,
            title=args.title,
            summary=args.summary,
        ),
        encoding="utf-8",
    )
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
