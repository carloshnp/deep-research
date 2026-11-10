# Plans and briefings

Trimmed copy. Provenance and changes: README.md.

Two artifacts keep a long build reviewable: the section plan (what will be written, frozen before writing) and the briefing (the standing spec every worker reads).

## Section plans (plans/<id>.md)

Written in phase 2, one file per section, frozen before writing. Each subsection is an entry with twelve labelled fields: question, reader, entry, point, chain, principle, instance, limit, budget, boundary, source, file.

The plan is the coverage contract: the deep pass must deliver every entry, and the audit checks delivered against planned. Freeze it before writers start; after freeze, changes go through the orchestrator or the user, never through a writer improvising.

Expect the reader and entry fields to be the ones a finished subsection cannot answer from its own text; that failure is the finding, not a formality.

A run-level plan (scope, structure, the depth-level stop point) is not a section plan: keep it at the workspace root, because a checker that reads every `.md` under `plans/` reports a global plan as a fact list.

Template: templates/template-plano-secao.md.

## Briefings

Two levels, both at the workspace root:

- Master brief (BRIEFING.md): purpose and audience; language and the hard style rules; structure and assembly order; the scope map (what each section covers); source rules; citation style for the report (inline source links on first mention with the pack's canonical URL, or named sources; pick one, because mixed authorship drifts without an explicit rule); question policy; figure policy; done criteria for every entry; workspace layout.
- Wave brief (BRIEFING-<wave>.md): what this wave changes and why; exact deliverable paths; the item or quality spec (pointing at the reference that defines it, when relevant); what NOT to touch; the checks the wave must pass.

Rules: entries point at the briefing instead of restating it; the briefing wins over any paraphrase; new waves add sibling files rather than rewriting the master. Before freezing a wave brief, reconcile every file list it names against measured counts (word counts, section numbers); a tier or scope list written from memory silently drops files.

Calibrate the section word band against delivered reports before entries are written: measure the section bodies of the existing reports, and take the words-per-section of the most recent report in the current format. An uncalibrated round number is what makes a detailed report read shallow.

Templates: templates/template-briefing.md, templates/template-briefing-onda.md.
