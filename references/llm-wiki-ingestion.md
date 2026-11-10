# LLM-wiki stack research and ingestion pattern

Use this reference when a deep-research session is not asking for a standalone report, but for research-backed ingestion into a project LLM wiki.

## When this applies

- The user provides a plan whose deliverable is wiki pages, specialist maps, or skill drafts.
- The user explicitly says to run the plan, not merely to propose one.
- The target wiki has a schema/index/log discipline.

Hermes: when the deliverable includes Kanban readiness, the procedure is in `references/hermes-board-mode.md` (HERMES ONLY).

## Adapted workflow

1. **Treat explicit “run the plan” as approval to execute the attached plan.** Do not stop after re-planning if the user already gave execution authority.
2. **Orient in the wiki first:** read `SCHEMA.md`, `index.md`, and recent `log.md`; search existing notes for duplicate topics.
3. **Ground in current project state:** read manifests/configs/source/spec files and run the baseline commands requested by the plan. If provided paths are stale, search once under the project root and record the actual path.
4. **Research source hierarchy:** official docs and release notes first, local installed package READMEs second, GitHub/issues and X/social as warning signals only unless cross-checked.
5. **Ingest, do not just summarize:** create/update wiki pages with frontmatter, project-specific file mapping, coding patterns, pitfalls, verification commands, specialist routing, and open questions.
6. **Update schema/index/log in the same run:** add tags before using them, list new pages in `index.md`, and append a log entry with sources, verification baseline, created pages, and updated files.
7. **Verify on disk:** expected files exist, frontmatter present, minimum wikilinks present, schema/index/log markers present.

## Good final response

- Briefly list created/updated paths.
- Include actual verification output.
- Call out blocked/degraded checks, such as unavailable web extraction, without turning them into permanent tool limitations.

## Pitfalls

- Do not force the standard deep-research `outputs/.plans` report artifact path when the requested artifact is a maintained wiki.
- Do not write one-session narratives into skills; use class-level wiki/skill pages and references.
- Do not record transient setup failures as durable constraints. Capture the workaround pattern if useful.
