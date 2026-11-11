#!/usr/bin/env python3
"""Plan gate: a section plan is one entry per subsection, not a fact list.

Fails when a subsection entry is missing a field, carries an empty or placeholder
value, states a budget outside the range, or carries an unknown field. Run it
before writers start, so an incomplete entry is a planning defect.

Usage:
    python3 check_plan.py plans/f1-2.md [plans/f1-3.md ...]
Exit: 0 all entries complete, 1 defects found, 2 usage error.
"""
import re
import sys

FIELDS = [
    ("question", "the question this unit answers, one sentence"),
    ("reader", "what the reader is assumed to know, and what is likely misremembered"),
    ("entry", "what the reader must already hold for this unit to work"),
    ("point", "the main point, one sentence"),
    ("chain", "the mechanism, link by link, each link with its cause"),
    ("principle", "the rule or principle each step instantiates, named"),
    ("instance", "the worked instance with numbers and units, or 'qualitative: <why>'"),
    ("limit", "the limit or wrong model this unit displaces, or 'none: <why>'"),
    ("budget", "words for this unit, a number between 250 and 800"),
    ("boundary", "what this unit excludes and where that material lives"),
    ("source", "the research file and line or slide range"),
    ("file", "outputs/sections/<id>.md"),
]
BUDGET_MIN, BUDGET_MAX = 250, 800

PLACEHOLDER = re.compile(r"^\s*(tbd|todo|n/a|\.\.\.|\u2026|<[^>]*>|x+)\s*$", re.I)
CARD_HEAD = re.compile(r"^###\s+(\S+)")
FIELD_LINE = re.compile(r"^\s*[-*]\s*\*\*([a-z ]+?):?\*\*\s*:?\s*(.*)$", re.I)


def entries(text):
    """Yield (entry_id, {field: value}, line_no) for each subsection entry."""
    cur, fields, start = None, {}, 0
    for i, line in enumerate(text.splitlines(), 1):
        m = CARD_HEAD.match(line)
        if m and re.search(r"\d", m.group(1)):
            if cur:
                yield cur, fields, start
            cur, fields, start = m.group(1).rstrip(":"), {}, i
            continue
        if cur:
            f = FIELD_LINE.match(line)
            if f:
                fields[f.group(1).strip().lower()] = f.group(2).strip()
    if cur:
        yield cur, fields, start


def check(path):
    text = open(path, encoding="utf-8").read()
    found = list(entries(text))
    problems = []
    if not found:
        if "<section-id>" in text or "<subsection title>" in text:
            problems.append(f"{path}: unedited template, no entries filled in")
        else:
            problems.append(f"{path}: no '### <id>' subsection entries found")
    for cid, fields, line in found:
        for key, desc in FIELDS:
            if key not in fields:
                problems.append(f"{path}:{line} entry {cid}: missing field '{key}' ({desc})")
                continue
            val = fields[key]
            if not val:
                problems.append(f"{path}:{line} entry {cid}: field '{key}' is empty")
            elif PLACEHOLDER.match(val):
                problems.append(f"{path}:{line} entry {cid}: field '{key}' is a placeholder: {val!r}")
            elif key == "budget":
                m = re.match(r"^(\d+)\b", val)
                if not m:
                    problems.append(f"{path}:{line} entry {cid}: budget is not a number: {val!r}")
                elif not BUDGET_MIN <= int(m.group(1)) <= BUDGET_MAX:
                    problems.append(
                        f"{path}:{line} entry {cid}: budget {m.group(1)} outside {BUDGET_MIN} to {BUDGET_MAX}"
                    )
        extra = set(fields) - {k for k, _ in FIELDS}
        if extra:
            problems.append(f"{path}:{line} entry {cid}: unknown field(s) {sorted(extra)}")
    return found, problems


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    total, all_problems = 0, []
    for path in argv[1:]:
        try:
            found, problems = check(path)
        except OSError as exc:
            all_problems.append(f"{path}: cannot read: {exc}")
            continue
        total += len(found)
        all_problems.extend(problems)
    if all_problems:
        print(f"FAIL: {len(all_problems)} defect(s) across {total} entry(ies)")
        for p in all_problems:
            print("  " + p)
        return 1
    print(f"OK: {total} entry(ies) complete, {len(FIELDS)} fields each")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
