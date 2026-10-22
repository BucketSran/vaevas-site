"""Fail when hand-written site pages contain material that must stay private.

Pages imported from vaEVAS main and GitHub issue text are already public and
are not scanned here; their fixes belong in the repository or the issue.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"
SKIP = ("evas/manual/", "_generated/")
PATTERNS = {
    "本机绝对路径": r"/Users/|/home/|/private/tmp|~/\.(?:codex|claude|tclaude)",
    "服务器账号": r"\bthu-(?:sui|jin)\b|jinzhihong",
    "内部会话链接": r"codex://",
}


def main() -> int:
    problems = []
    for page in sorted(DOCS.rglob("*.md")):
        rel = page.relative_to(DOCS).as_posix()
        if rel.startswith(SKIP):
            continue
        for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            for name, pattern in PATTERNS.items():
                if re.search(pattern, line):
                    problems.append(f"{rel}:{n}: {name}: {line.strip()[:100]}")
    for p in problems:
        print("ERROR  ", p)
    print(f"公开检查：{len(problems)} 处问题")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
