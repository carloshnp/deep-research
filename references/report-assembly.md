# Assembling a section-per-file report

Deep runs write one file per subsection, then the lead assembles the report. The assembly is mechanical, so the failure modes are mechanical too: a regex that helps the body breaks a block it should not touch, and a cleanup pass ordered after the citation render turns every source line into a mismatch.

## Order of operations

1. Write the subsection files.
2. Assemble the body, sections in plan order, headings by contract below.
3. Run `scripts/post_write_cleanup.py` on the assembled body.
3a. Run `scripts/check_report_style.py` on the cleaned body and fix every hard error before the next step. It runs before the Sources block exists, so URLs and ledger titles cannot trip it.
4. Register the body's URLs in the ledger and render the Sources block, last.
5. Convert currency signs to `&#36;`, set the real counts in the status line, then `verify`.

Evidence that the order is not optional: the ledger render separates a URL from its title with an em dash, and the verifier compares that block byte for byte. Clean the dashes after the render and the separator becomes a comma, so every one of 150 lines reports "block URL does not match the ledger". Clean before the render and the block stays internally consistent.

A URL whose title is empty renders as `url` plus the separator, and cleanup leaves a trailing comma with nothing behind it, which trips the same comparison. Give every ledger entry a title, or post-process lines that end in a comma.

## Heading contract

- Sections: `## <n>. <title>`.
- Subsections: `### <n>.<k> <title>`.
- Anything inside a subsection body: `####`.

Demote internal headings in the assembler, not by hand, and skip fenced code blocks while doing it.

## The demote guard

A demote rule keyed on the section identifier (`^### (?!S\d)`) fails on the assembled file, because assembled subsection headings read `### 1.1`, not `### S1.1`. Key on the level and the fence state only (`^#{3,6} ` outside a fence), and let the assembler write the `###` line from the plan's title. Getting this wrong demotes every subsection one level and the table of contents collapses.

## Bracket to italics conversion

Bracketed glossary terms (`[safrinha]`) become `*safrinha*`, but a naive pass also eats Mermaid node labels (`A[Text]` becomes `A*Text*`) and the diagrams stop parsing. Two guards, both needed:

- Skip lines between ``` fences entirely.
- Do not match when a `(` follows the closing bracket, which is what separates a link from a term.

A label that itself contains brackets (`A[Text [x]]`) survives neither guard; fix those blocks by hand.

## Citation style and `verify`

The report may cite with inline markdown links instead of `[n]` ids. That works, but `verify` then reports every registered source as "uncited inline" and `--strict` fails on them. Choose the style in the briefing so the drift is a decision rather than mixed authorship, run `verify` without `--strict`, and say in the provenance which style applied. Inline links keep URL and claim adjacent, so prefer them for long reports built by writers; the ledger still owns the block.
