# BRIEFING: <report name>

Everything a worker needs. Read this file first, then your entry. Files go under the workspace root; never write outside it.

Workspace root: <absolute path>

## Purpose and audience

<who reads this report, what it must let them do>

## Language and style (hard rules)

- Language: <PT-BR / EN>. No em dashes and no en dashes anywhere. Ranges read "N a M" (PT) or "N to M" (EN).
- Direct, dense, plain sentences. Explain every technical term at first use. No filler.
- Math: `$...$` inline; display math always on its own line; derivation and solving chains in align blocks (reference: references/math-and-latex-style.md).
- Every non-obvious factual claim carries a real link. Never invent citations, quotes, or numbers.

## Structure (assembly order)

1. Title block + how-to-use paragraph.
2. Sections in order (scope map below).

## Scope map

| Section | Title | One-line scope |
|:--------|:------|:---------------|
| <id> | <title> | <what it must teach> |

## Workspace layout

```
plans/                        section plans
research/                     source packs and excerpts
outputs/sections/subsections/ subsection text files
outputs/sections/             assembled section files
outputs/                      assembled reports
diagrams/                     svg, tikz, mermaid, python
scripts/                      build, render and check scripts
assets/relatorios/            audit and fix reports
```

## Source rules

<what sources are acceptable, where excerpts are saved, how blocked pages are recovered, what to do with books that cannot be fetched>

## Done criteria for every entry

- Files saved at the exact paths given in the entry, listed with sizes in the report.
- The checks for that entry's phase pass (structure, counts, renders, execution).
- Short report: files, counts, blockers.
