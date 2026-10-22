"""Check in-site links and anchors in the built HTML.

MkDocs does not see anchors written as raw ``<a id="...">``, so this script
reads the final HTML instead. Hand-written pages must have no broken links;
pages imported from main only report counts, because their anchors are owned
by the repository and fixed there.
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urljoin, urlparse

SITE = Path(__file__).resolve().parents[1] / "build" / "site"
IMPORTED = ("evas/manual/", "evas/comparison/")


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])


def main() -> int:
    pages: dict[str, Collector] = {}
    for html in SITE.rglob("*.html"):
        c = Collector()
        c.feed(html.read_text(encoding="utf-8"))
        pages[html.relative_to(SITE).as_posix()] = c

    own, imported = [], []
    for rel, c in pages.items():
        if rel in ("404.html",) or rel.startswith("assets/"):
            continue
        base = "file:///" + rel
        for href in c.hrefs:
            if urlparse(href).scheme in ("http", "https", "mailto"):
                continue
            target, frag = urldefrag(urljoin(base, href))
            path = unquote(urlparse(target).path).lstrip("/")
            if path.endswith("/") or path == "":
                path += "index.html"
            if path not in pages:
                if (SITE / path).exists():
                    continue  # asset
                problem = f"{rel}: 链接目标不存在 {href}"
            elif frag and unquote(frag) not in pages[path].ids:
                problem = f"{rel}: 锚点不存在 {href}"
            else:
                continue
            (imported if rel.startswith(IMPORTED) else own).append(problem)

    for p in own:
        print("ERROR  ", p)
    print(f"链接检查：手写页面 {len(own)} 处问题；导入页面 {len(imported)} 处（归仓库维护，仅计数）")
    for p in imported[:10]:
        print("  imported:", p)
    return 1 if own else 0


if __name__ == "__main__":
    sys.exit(main())
