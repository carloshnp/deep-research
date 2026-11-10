"""Clean dashes and scientific notation in a finished markdown report.

Usage:
    python3 post_write_cleanup.py FILE [FILE ...] [--lang en|pt] [--check]

English (default):
    em dash in running text         comma and space
    em dash in a table cell         removed; the spacing collapses to one space
    em dash in a heading            colon and space
    en dash between two numbers     the word "to" (3 to 5)
    en dash after "between"         the word "and" (between 3 and 5)
    other en dash in running text   comma and space
    other en dash in a table cell   removed, as for the em dash
    scientific notation in math     3.77e-04 becomes 3.77 \\times 10^{-4}

Brazilian Portuguese (--lang pt):
    en dash between two numbers     the range word " a " (3 a 5)
    en dash after "entre"           the word "e" (entre 3 e 5)
    other en dash                   the range word " a "
    scientific notation in math     3{,}77 \\times 10^{-4}

Limits: only decimal mantissas convert (3.77e-04 does; 3e-04 does not), and
only inside math spans. Lines inside fenced code blocks are never changed.
A line that holds a dash is re-spaced: runs of two or more spaces collapse to
one. Every other line is written back byte for byte. --check prints the counts
and writes nothing. Exit: 0 on success, 2 on usage error.
"""

import re
import sys

EM = "\u2014"
EN = "\u2013"
RANGE_WORD = {"en": " to ", "pt": " a "}
FENCE = re.compile(r"^\s*(```|~~~)")
RANGE_EN = re.compile(r"(?<=[0-9%])\s*" + EN + r"\s*(?=[0-9A-Za-z])|(?<=[A-Za-z])\s*" + EN + r"\s*(?=[0-9])")
EM_RUN = re.compile(r"\s*" + EM + r"\s*")
EN_RUN = re.compile(r"\s*" + EN + r"\s*")
EM_LEAD = re.compile(r"^(\s*(?:[-*+]|\d+\.)?\s*)" + EM + r"\s*")
MATH = re.compile(r"\$\$.+?\$\$|\$[^$\n]+?\$")
SCI = re.compile(r"(?<![\w.])(\d+\.\d+)e([+-]?)(\d+)(?!\w)")
CURRENCY = re.compile(r"(?<!\\)(?:US|R)\$\s*\d")


def sci_value(match, lang):
    mantissa, sign = match.group(1), match.group(2)
    digits = match.group(3).lstrip("0") or "0"
    exponent = "0" if digits == "0" else ("-" if sign == "-" else "") + digits
    if lang == "pt":
        mantissa = mantissa.replace(".", "{,}")
    return f"{mantissa} \\times 10^{{{exponent}}}"


def sci_in_math(line, lang):
    pieces, last = [], 0
    for span in MATH.finditer(line):
        pieces.append(line[last:span.start()])
        pieces.append(SCI.sub(lambda m: sci_value(m, lang), span.group(0)))
        last = span.end()
    pieces.append(line[last:])
    return "".join(pieces)


def count_sci(line):
    return sum(len(SCI.findall(span.group(0))) for span in MATH.finditer(line))


# A number, optionally followed by a % sign or a short unit, right before the dash.
BETWEEN = {
    "en": re.compile(r"\bbetween\s+[0-9][0-9.,]*\s*(?:%|\u00b0\s*[CFK]|[A-Za-z]{1,3})?$", re.IGNORECASE),
    "pt": re.compile(r"\bentre\s+[0-9][0-9.,]*\s*(?:%|\u00b0\s*[CFK]|[A-Za-z]{1,3})?$", re.IGNORECASE),
}
JOIN_WORD = {"en": " and ", "pt": " e "}


def range_word(m, lang):
    # A range after "between" (English) or "entre" (Portuguese) joins with "and" or "e".
    if m.string[m.end():m.end() + 1].isalnum() and BETWEEN[lang].search(m.string[:m.start()]):
        return JOIN_WORD[lang]
    return RANGE_WORD[lang]


def dash_fix(body, lang):
    head = body.lstrip()
    table = head.startswith("|")
    body = RANGE_EN.sub(lambda m: range_word(m, lang), body)
    if head.startswith("#"):
        body = EM_RUN.sub(": ", body)
    elif table:
        body = EM_RUN.sub(" ", body)
    else:
        body = EM_LEAD.sub(r"\1", body)
        body = EM_RUN.sub(", ", body)
    if lang == "pt":
        body = EN_RUN.sub(RANGE_WORD["pt"], body)
    elif table:
        body = EN_RUN.sub(" ", body)
    else:
        body = EN_RUN.sub(", ", body)
    return body


def tidy(body):
    lead = re.match(r"\s*", body).group(0)
    rest = re.sub(r"[ \t]{2,}", " ", body[len(lead):])
    rest = re.sub(r",(\s*,)+", ",", rest)
    rest = re.sub(r",\s*$", "", rest)
    return lead + rest


def clean(text, lang):
    stats = {"changed": 0, "sci": 0}
    out, in_fence = [], False
    for line in text.split("\n"):
        cr = "\r" if line.endswith("\r") else ""
        body = line[: len(line) - len(cr)]
        if FENCE.match(body):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        n_sci = count_sci(body)
        stats["sci"] += n_sci
        if EM not in body and EN not in body and not n_sci:
            out.append(line)
            continue
        new = sci_in_math(body, lang) if n_sci else body
        if EM in new or EN in new:
            new = tidy(dash_fix(new, lang))
        if new != body:
            stats["changed"] += 1
        out.append(new + cr)
    return "\n".join(out), stats


def counts(text):
    return {
        "em": text.count(EM),
        "en": text.count(EN),
        "inline_dollars": text.count("$") - 2 * text.count("$$"),
        "currency": len(CURRENCY.findall(text)),
    }


def main(argv):
    lang, check, files = "en", False, []
    args = argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--lang":
            if i + 1 >= len(args) or args[i + 1] not in RANGE_WORD:
                print("usage: --lang takes en or pt", file=sys.stderr)
                return 2
            lang = args[i + 1]
            i += 2
            continue
        if arg == "--check":
            check = True
        elif arg in ("-h", "--help"):
            print(__doc__)
            return 0
        elif arg.startswith("--"):
            print(f"unknown option: {arg}", file=sys.stderr)
            return 2
        else:
            files.append(arg)
        i += 1
    if not files:
        print(__doc__)
        return 2
    for path in files:
        with open(path, encoding="utf-8", newline="") as fh:
            text = fh.read()
        new, stats = clean(text, lang)
        before, after = counts(text), counts(new)
        print(f"{path}: em {before['em']} -> {after['em']} | en {before['en']} -> {after['en']} | "
              f"sci fixes {stats['sci']} | lines changed {stats['changed']}")
        if after["inline_dollars"] % 2:
            print("  WARN: inline dollar count is odd, so math may be unbalanced")
        if after["currency"]:
            print(f"  WARN: {after['currency']} sign(s) like R$ 5 or US$ 5; if it is not math, write the dollar sign as &#36;")
        if check:
            print("  --check: nothing written")
        elif new != text:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
