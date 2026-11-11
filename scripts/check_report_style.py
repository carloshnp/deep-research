#!/usr/bin/env python3
"""Report style gate: blocks an assembled report that reads like process notes.

Hard errors (exit 1): one level-1 title, a status line near the top that names
a check that did not run (SKILL.md, "Open the report with a status line"), no
internal section IDs (S5.5), no process-note words (BRIEFING, Lead check,
subagent, "wave N"), no pasted label lines (Confidence:, Basis:, Verdict:,
Decision:, Status:), and no paragraph over 180 words.

Warnings (exit 0): a sentence over 40 words, and list density above 25 bullets
per 1000 words once there are at least 12 bullets.

Usage:
    python3 check_report_style.py report.md [--lang en|pt]
Exit: 0 passes (warnings allowed), 1 hard defects, 2 usage error.
"""
import re
import sys

PARA_MAX_WORDS = 180
SENT_WARN_WORDS = 40
BULLETS_MIN, BULLETS_PER_1000 = 12, 25
STATUS_WINDOW = 1200

PROCESS = [
    (re.compile(r"\bBRIEFING\b"), "BRIEFING (process word)"),
    (re.compile(r"Lead check"), "Lead check (process note)"),
    (re.compile(r"\bsubagents?\b", re.I), "subagent (process word)"),
    (re.compile(r"\bwave \d"), "wave N (process word)"),
]
INTERNAL_ID = re.compile(r"\bS\d+\.\d+\b")
STATUS = re.compile(r"(?i)\b(did not run|not run|not checked|skipped|blocked)\b")
LABELS = {
    "en": re.compile(r"^(Confidence|Basis|Verdict|Decision|Status):\s", re.M),
    "pt": re.compile(r"^(Confiança|Base|Veredito|Decisão):\s", re.M),
}
BULLET = re.compile(r"^\s*([-*]|\d+\.)\s")


def prose_lines(text):
    """Yield (line_no, line) outside fenced code blocks."""
    fenced = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            yield i, line


def sentences(text):
    """Yield (line_no, word_count) for prose sentences, inline code removed."""
    for i, line in prose_lines(text):
        s = line.strip()
        if not s or s.startswith(("#", "|", "<", "!")):
            continue
        s = re.sub(r"`[^`]*`", "x", s)
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z(])", s):
            n = len(part.split())
            if n:
                yield i, n


def check(path, lang):
    text = open(path, encoding="utf-8").read()
    errors, warnings = [], []
    lines = list(prose_lines(text))

    titles = [i for i, ln in lines if ln.startswith("# ")]
    if not titles:
        errors.append((0, "no level-1 title"))
    elif len(titles) > 1:
        errors.append((titles[1], "second level-1 heading: the report has one title"))

    if not STATUS.search(text[:STATUS_WINDOW]):
        errors.append((0, f"no status line in the first {STATUS_WINDOW} characters "
                          "naming the checks that did not run"))

    for i, ln in lines:
        for pat, name in PROCESS:
            if pat.search(ln):
                errors.append((i, f"process note: {name}"))
        if INTERNAL_ID.search(ln):
            errors.append((i, f"internal section ID: {INTERNAL_ID.search(ln).group(0)}"))

    for m in LABELS[lang].finditer(text):
        line_no = text[: m.start()].count("\n") + 1
        errors.append((line_no, f"label line: {m.group(0).strip()}"))

    for i, ln in lines:
        s = ln.strip()
        if not s or s.startswith(("#", "|", "<", "!")) or BULLET.match(ln):
            continue
        words = len(s.split())
        if words > PARA_MAX_WORDS:
            errors.append((i, f"paragraph of {words} words: split it (limit {PARA_MAX_WORDS})"))

    for i, n in sentences(text):
        if n > SENT_WARN_WORDS:
            warnings.append((i, f"sentence of {n} words (warn above {SENT_WARN_WORDS})"))

    bullets = sum(1 for _, ln in lines if BULLET.match(ln))
    words = len(text.split())
    if bullets >= BULLETS_MIN and words and bullets * 1000 / words > BULLETS_PER_1000:
        warnings.append((0, f"list density: {bullets} bullet lines in {words} words "
                            f"(warn above {BULLETS_PER_1000} per 1000)"))

    print(f"== {path} ==")
    for i, msg in sorted(errors):
        print(f"ERROR line {i}: {msg}")
    for i, msg in sorted(warnings):
        print(f"WARN line {i}: {msg}")
    print(f"-- {len(errors)} errors, {len(warnings)} warnings, {words} words --")
    return 1 if errors else 0


def main(argv):
    lang = "en"
    args = []
    it = iter(argv[1:])
    for a in it:
        if a == "--lang":
            lang = next(it, "")
        elif a == "--report":
            continue
        else:
            args.append(a)
    if len(args) != 1 or lang not in LABELS:
        print(__doc__)
        return 2
    return check(args[0], lang)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
