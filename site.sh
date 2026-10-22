#!/bin/sh
# 本地 vaEVAS 网站：./site.sh serve | build | sync [--no-fetch] | new-entry ...
set -eu
cd "$(dirname "$0")"
PY=.venv/bin/python
if [ ! -x "$PY" ]; then
  uv venv -q --python 3.12 .venv
  uv pip install -q --python "$PY" -r requirements.txt
fi
cmd="${1:-serve}"
[ $# -gt 0 ] && shift
case "$cmd" in
  sync) "$PY" tools/sync_main.py "$@" && "$PY" tools/sync_issues.py ;;
  build) "$PY" tools/sync_main.py "$@" && "$PY" tools/sync_issues.py && "$PY" -m mkdocs build --strict && "$PY" tools/check_links.py && "$PY" tools/check_public.py ;;
  serve) "$PY" tools/sync_main.py "$@" && "$PY" tools/sync_issues.py && "$PY" -m mkdocs serve -a 127.0.0.1:8765 ;;
  new-entry) "$PY" tools/new_entry.py "$@" ;;
  *) echo "用法: ./site.sh serve|build|sync [--no-fetch] | new-entry --help" >&2; exit 2 ;;
esac
