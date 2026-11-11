# Post-write cleanup: rules

Run `scripts/post_write_cleanup.py` on a finished report before delivery. The script edits the file in place. Run it with `--check` first to see the counts without a write.

## What the script changes

English is the default. `--lang pt` switches to the Brazilian Portuguese rules.

| Input | English output | With --lang pt |
|---|---|---|
| em dash in running text | comma and space | comma and space |
| em dash in a table cell | removed; the spacing collapses to one space | same |
| em dash in a heading | colon and space | colon and space |
| en dash range after the word "between" | the word "and" (between 3 and 5) | range word " a " (3 a 5) |
| en dash between two numbers | the word "to" (3 to 5) | range word " a " (3 a 5) |
| en dash range after the word "entre" | the word "to" (3 to 5) | the word "e" (entre 3 e 5) |
| other en dash in running text | comma and space | range word " a " |
| other en dash in a table cell | removed, as for the em dash | range word " a " |
| scientific notation inside math (3.77e-04) | 3.77 \times 10^{-4} | 3{,}77 \times 10^{-4} |

A line with no dash and no scientific notation is written back byte for byte.

## Limits

- Only decimal mantissas convert: 3.77e-04 does, 3e-04 does not.
- Scientific notation converts only inside math spans ($...$ or $$...$$).
- Lines inside fenced code blocks are never changed. Their dashes are counted but left alone.
- A line that holds a dash is re-spaced: runs of two or more spaces collapse to one.
- The word "between" (or "entre" with --lang pt) must come right before the range, with at most a % sign, a degree sign followed by C, F or K, or a unit of three letters or fewer after the first number. A range after another word, such as "from", still becomes "N to M".
- A second value that is a word still joins, so a range written with a dash before "present" reads "between 2019 and present" in English and "entre 2019 e presente" in Portuguese.

## Checks to run by hand

- Inline math: the count of dollar signs, minus twice the count of double dollar signs, must be even. The script prints a warning when it is odd.
- Currency: a dollar sign that is not math, such as US$ or R$ followed by a digit, must be written as the HTML entity &#36;. The script prints a warning for each candidate.
- Display math: each double dollar sign sits alone on its own line.
- Environments: each LaTeX environment in math has double dollar delimiters (see references/math-and-latex-style.md).
- Final count: after the script runs, the report has zero em dashes and zero en dashes outside code blocks.

## Run it inside the rebuild cycle, not once at the end

A report assembled from subsection files is rebuilt every time a fix lands, and each rebuild restores what the previous pass removed. Order the cycle so each step survives the next:

1. Edit the subsection file, never the assembled report, because assembly overwrites the report.
2. Re-assemble from the subsection files.
3. Register every cited URL and render the Sources block from the assembled body (procedure: `scripts/sources.py`).
4. Run this script.
5. Re-run the per-change assertion script, then the citation verify.

**Any normalisation pass you write by hand has to skip fenced blocks.** This script leaves fenced lines alone; a hand-rolled regex does not. Converting `[text]` to italics also converts Mermaid node labels of the form `A[Text]` and leaves every diagram unparseable, so track fence state in the loop or replace only outside code spans. A heading-demotion pass has the same trap: `### ` inside a fence is diagram text, not a heading.

**Currency signs return with every rebuild**, because the source files still hold them. Convert `$` to `&#36;` after each rebuild rather than once, and re-read the relative links as well: a path written from inside a subsection file resolves at a different depth once the text sits in `outputs/<slug>.md`, so a link that works in the fragment 404s in the report.

## The Sources block never gets cleaned

The rendered Sources block separates URL from title with an em dash, and the citation verify compares that block byte for byte against a fresh render, so cleaning the block makes the verify report every line as disagreeing with the ledger. Pick one order and say which in the provenance:

1. Clean the body, render the block last, and let the block keep its dashes. The zero-dash rule then holds for prose only.
2. Clean after rendering and expect block mismatches until it is re-rendered. Never "fix" a mismatch by hand-editing the block.

A source registered with no title renders a dangling separator. The verify parses the line, so one empty title reads as a URL mismatch and takes the whole block down: register a title for every source, even a bare host.

## Pitfalls

- The script changes text in place. Keep the report under version control, so a bad run can be reverted.
- The Portuguese range word applies only with --lang pt. An English report that gets the Portuguese rules shows "a" between numbers.

## Origin

The rules were written from the author's earlier cleanup recipe. `scripts/post_write_cleanup.py` is a new implementation of these rules, not a copy of that recipe's code. Provenance and changes: README.md.
