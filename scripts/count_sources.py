"""Count the sources a research run consulted, from its thread files.

Each thread file carries a source table whose rows have a URL and a read-status label. The
report front matter and the provenance sidecar need three different numbers from that table
(rows, distinct URLs, rows marked read) and a single "sources consulted" figure hides which
one it is. Print all of them.

Usage:
    python3 count_sources.py research/T*.md
    python3 count_sources.py --json research/T*.md
    python3 count_sources.py research/T1-*.md research/T2-*.md   # per-file breakdown

Exit: 0 on success, 2 on usage error. This is a measurement, not a gate: an unreachable
source is counted, not failed, because the read-status split is what reports it.
"""
import glob
import json
import re
import sys

URL = re.compile(r"^https?://", re.I)
SEP = re.compile(r"^[:\-\s]+$")
HEADER = re.compile(r"^read[\s\-_]*status\b", re.I)


def classify(cell):
    """Map a read-status cell to read, verified_unread, discovery or unknown."""
    s = cell.strip().lower()
    if not s:
        return "unknown"
    if "verified" in s and "not read" in s:
        return "verified_unread"
    if s.startswith("discovery"):
        return "discovery"
    if s.startswith("read") or s.startswith("lido"):
        return "read"
    return "unknown"


def rows_in(path):
    """Yield (url, status) for every source-table row in one file."""
    for line in open(path, encoding="utf-8", errors="replace"):
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        if all(SEP.match(c) or not c for c in cells):
            continue
        url = next((c for c in cells if URL.match(c)), "")
        status = next((c for c in cells if classify(c) != "unknown"), "")
        if not url and HEADER.match(status):
            continue  # header row: a read-status label with no URL
        if not url and not status:
            continue  # prose row
        yield url, classify(status)


def norm(url):
    u = re.sub(r"^https?://(www\.)?", "", url.strip().lower()).rstrip("/")
    return u


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    as_json = "--json" in argv
    if not args:
        print(__doc__)
        return 2
    paths = []
    for a in args:
        hits = sorted(glob.glob(a))
        paths.extend(hits or [a])

    per_file, all_urls, totals = {}, set(), {"read": 0, "verified_unread": 0, "discovery": 0, "unknown": 0}
    rows = no_url_total = 0
    for p in paths:
        try:
            pairs = list(rows_in(p))
        except OSError as exc:
            print(f"cannot read {p}: {exc}", file=sys.stderr)
            return 2
        rows += len(pairs)
        no_url_total += sum(1 for u, _ in pairs if not u)
        urls = {norm(u) for u, _ in pairs if u}
        all_urls |= urls
        counts = {"read": 0, "verified_unread": 0, "discovery": 0, "unknown": 0}
        for _, st in pairs:
            counts[st] += 1
            totals[st] += 1
        per_file[p] = {"rows": len(pairs), "distinct_urls": len(urls), **counts}

    result = {
        "files": len(paths),
        "rows": rows,
        "distinct_urls": len(all_urls),
        "rows_without_url": no_url_total,
        **totals,
        "per_file": per_file,
    }

    if as_json:
        print(json.dumps(result, indent=1))
        return 0

    width = max((len(p) for p in per_file), default=10)
    print(f"{'file':<{width}}  rows  urls  read  unread  disc")
    for p, v in per_file.items():
        print(f"{p:<{width}}  {v['rows']:>4}  {v['distinct_urls']:>4}  {v['read']:>4}  "
              f"{v['verified_unread']:>6}  {v['discovery']:>4}")
    print()
    print(f"TOTAL rows {rows} | distinct URLs {len(all_urls)} | read {totals['read']} | "
          f"verified unread {totals['verified_unread']} | discovery only {totals['discovery']} | "
          f"unlabelled {totals['unknown']}")
    print("Quote the unit with the number: rows, distinct URLs and rows marked read are three")
    print("different counts about the same run.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
