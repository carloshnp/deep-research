# Depth tiers

Budgets, execution shapes, and artifact sets per tier. Retrieval order, paper search, evidence tiers, citation delegation, and wording rules are fixed across tiers (see the SKILL.md router).

| | Scout | Standard | Deep |
|---|---|---|---|
| Queries | 3 to 6 | 8 to 20 | per-thread, until coverage map is green |
| Sources | 5 to 10 | 10 to 25 | 25 plus |
| Execution | lead only | 2 to 4 researcher subagents, verifier, reviewer | waves of tasks, subagents inside each wave (see the mode rule in SKILL.md) |
| Structure | brief | sections with expanded subsections | frozen section plans, one file per subsection |
| Source packs | inline list | per-thread research files | excerpt ledger plus pack plus coverage map |

## Standard structure

Reports are organized as sections with subsections: each subsection is expanded with mechanism, numbers with units, and worked detail. Researcher briefs map to report sections so synthesis is assembly plus judgment, not re-research.

## Deep structure

Deep runs in four phases:

1. Source packs (`research/<area>/`, one file per source) with the coverage map.
2. Section plans (`plans/<id>.md`): subsection list, what each covers, worked detail planned, source pointers, subsection file names. Frozen before writing.
3. Deep pass: one writer per section, one file per subsection under `outputs/sections/subsections/<id>.<n>-<slug>.md`; sections assembled from subsections, report assembled from sections.
4. Audit and fix loop over section ranges, then delivery.

## Deep waves

Deep runs in waves of tasks: source-pack, write, deep, audit, fixer, build. Each task points at `BRIEFING.md` and the section plan; never paraphrase specs into task text. Waves drain in sequence; audits gate fixers. Tasks may fan out parallel fetching to subagents, with one narrow question and one output path per child. Completion summaries are self-reports: re-run the load-bearing check (recount, grep the corrected value, verify the file) before accepting a task. The procedure is in `references/deep-mode.md`; the briefing contract is in `references/plans-and-briefings.md`.

Hermes: the same waves run as kanban cards, one board per topic. See `references/hermes-board-mode.md` (HERMES ONLY).

## Artifacts per tier

Scout: `outputs/.plans/<slug>.md`, `outputs/<slug>.md`, `outputs/<slug>.provenance.md`.

Standard adds: per-thread briefs and research files (`outputs/.plans/<slug>-T<n>.md`, `outputs/.drafts/<slug>-research-*.md`), draft, cited, optionally revised drafts, verification file.

Deep adds: `BRIEFING.md`, section plans, source packs and coverage map, subsection files, assembled sections, audit and fix reports.
