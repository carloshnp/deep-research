# Plans and briefings

Trimmed copy. Provenance and changes: README.md.

Two artifacts keep a long build reviewable: the section plan (what will be written, frozen before writing) and the briefing (the standing spec every worker reads).

## Section plans (plans/<id>.md)

Written in phase 2, one file per section, frozen before writing. Each subsection is an entry with twelve labelled fields: question, reader, entry, point, chain, principle, instance, limit, budget, boundary, source, file.

The plan is the coverage contract: the deep pass must deliver every entry, and the audit checks delivered against planned. Freeze it before writers start; after freeze, changes go through the orchestrator or the user, never through a writer improvising.

Expect the reader and entry fields to be the ones a finished subsection cannot answer from its own text; that failure is the finding, not a formality.

**Write any context-only source into a pack before freezing.** The lead routinely holds a document the children cannot see: a page attached to the prompt, a local file already read, a fetched page from the planning probes. A plan that freezes saying "the pack does not contain X" while X sits in the lead's own context produces sections that hedge around what was actually known, and the writer cannot recover it. Dump the document to `research/<area>/` with its fetch provenance first, then point the entry at it and drop the gap.

A run-level plan (scope, structure, the depth-level stop point) is not a section plan: keep it at the workspace root, because a checker that reads every `.md` under `plans/` reports a global plan as a fact list.

Template: templates/template-plano-secao.md.

## Briefings

Two levels, both at the workspace root:

- Master brief (BRIEFING.md): purpose and audience; language and the hard style rules; structure and assembly order; the scope map (what each section covers); source rules; citation style for the report (inline source links on first mention with the pack's canonical URL, or named sources; pick one, because mixed authorship drifts without an explicit rule); question policy; figure policy; done criteria for every entry; workspace layout.
- Wave brief (BRIEFING-<wave>.md): what this wave changes and why; exact deliverable paths; the item or quality spec (pointing at the reference that defines it, when relevant); what NOT to touch; the checks the wave must pass.

Rules: entries point at the briefing instead of restating it; the briefing wins over any paraphrase; new waves add sibling files rather than rewriting the master. Before freezing a wave brief, reconcile every file list it names against measured counts (word counts, section numbers); a tier or scope list written from memory silently drops files.

**Name the allowed number sources in the master brief, exhaustively.** List every source a figure may hang on (pack row, lead notes row, quoted command output, a local rules file with its line number) and say how an author labels a value that was chosen rather than found. Leave the local rules file out and audits fail every figure that came from it, which pushes writers to delete correct numbers instead of citing them; leave the chosen-input label out and an invented test width reads as documented.

**A build card names its own acceptance artifact.** The brief says which fixture the check must compile and which property of the real output the check asserts, because a build worker otherwise writes a check against a hand-built stand-in that passes while the feature is missing.

Calibrate the section word band against delivered reports before entries are written: measure the section bodies of the existing reports, and take the words-per-section of the most recent report in the current format. An uncalibrated round number is what makes a detailed report read shallow.

**Settle whether the clock or capacity binds before setting the word band.** A hackathon deadline sets the demo window, not the build ceiling, when the team works agent-heavy and tests components in advance. Ask which constraint binds, then write the answer into the master brief as a standing line every worker reads, with the consequence spelled out: breadth over trimming, phase expensive parts thin-to-full instead of dropping them, and shift the hard constraints from time to validity. A plan scoped to the deadline by default trims capability lists the team could have built.

Templates: templates/template-briefing.md, templates/template-briefing-onda.md.
