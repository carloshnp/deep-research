# deep-research

Source-heavy research for AI agents at three depths (Scout, Standard, Deep). The skill includes a citation ledger that rejects any quote which is not verbatim in the fetched text, a source counter, a cleanup script for dashes and scientific notation, and writing rules for English and Brazilian Portuguese reports.

Read AGENTS.md for the rules and SKILL.md for the procedure.

## Mode rule

Deep research runs as waves of tasks. Use subagent mode by default: write each brief to disk, give each child one output path, and check each output file yourself. Use queued-task mode only when the harness passes the one-task probe in references/deep-mode.md. That file has the full procedure.

Hermes ONLY: references/hermes-board-mode.md is for Hermes. Other agents: do not follow it.

## Requires

Items are marked required or optional. Parameters and response fields named in the references (for example max_results or crawl_urls) are not tools and need nothing installed.

Required for any run:

- Python 3. The scripts use the standard library only.
- A shell, and a tool to read files: `read_file`, or the agent's equivalent.

Required for Standard and Deep:

- A subagent tool.

Hermes: the subagent tool is `delegate_task`. Its batch results arrive in a later turn.

Required for web research:

- `web_search` and `web_extract`, or the agent's equivalents.

Hermes: `web_search` and `web_extract` use the backends set as `search_backend` and `extract_backend` in the Hermes config (Firecrawl in the author's config).

- The public HTTP services named in references/scholarly-metadata-apis.md and references/search-routing.md: Crossref, OpenAlex, Semantic Scholar, Unpaywall, arXiv, the Wayback Machine, r.jina.ai and DuckDuckGo HTML. Check each service's terms, including any contact-email rule.

Optional (each route has a fallback):

- Obscura browser tools: `browser_navigate`, `browser_markdown`, `browser_search`, `browser_links`, `browser_evaluate`.
- Chrome MCP tools (dynamo-chrome): `navigate_page`, `new_page`, `take_snapshot`, `evaluate_script`.
- Hound MCP tools: `smart_search`, `smart_fetch`, `smart_crawl`. The repo writes them without the mcp_ prefix.
- X routes: `portal_x_search`, reached through the runtime tool loader. This is an external requirement. The repo copies nothing from the portal-x-search skill. Without it, the X routes in references/search-routing.md do not run.
Hermes: `tool_search`, `tool_describe` and `tool_call` reach `portal_x_search`.
Hermes: desktop app preview pane, `desktop_preview` and `drive_preview`.
- Earthdata Login, only for the downloads named in references/search-routing.md. Without it those downloads are marked BLOCKED.

Hermes: the local browser tool is `browser_exec`, used with `local=true`.

Hermes only, in references/hermes-board-mode.md:

Hermes: board mode runs a wave as kanban cards with the `hermes kanban` commands and the kanban tools (kanban_create, kanban_show, kanban_list, kanban_link, kanban_comment, kanban_complete, kanban_block, kanban_unblock, kanban_request_review, kanban_request_changes). Its create calls take an `idempotency_key` parameter, and a card worker may fan out with `delegate_task`.

## Install

- Copy this folder into the agent's skills directory, or clone it. Keep the folder name `deep-research`.

Hermes: `hermes skills install <url>` copies only SKILL.md (not tested). A tap install that copies the whole folder is not tested.

## Provenance

Every file in this repo, its source, and what changed. "User skill" means a skill from the author's own skill collection. "Upstream feynman" means the MIT-licensed deep-research skill named in SKILL.md (companion-inc/feynman).

| File | Source | Changes |
|---|---|---|
| LICENSE | upstream feynman, MIT | copied; Copyright (c) 2026 Companion, Inc. |
| README.md | new | this file |
| AGENTS.md | new | root instructions for agents |
| .gitignore | new | caches and outputs |
| SKILL.md | pre-port local copy deep-research | Mode rule and Hermes labels added; Sci-Hub step removed; X routes marked as an external requirement; R3 and citation pointers rewritten as in-repo pointers; Related skills table replaced by Files in this repo; Deep text reworded as waves of tasks. Added by the Hermes curator during the port, not in the source skill, and unsourced: the chain-limit sentence in the R1 paragraph. Added after the pre-port snapshot: the desktop-preview sentences, now a Hermes line in the X section; wording in the basis-label, process-note, sizing, ask and totals hunks |
| references/deep-mode.md | new | all agents: waves, probe, subagent mode, state file |
| references/hermes-board-mode.md | new | HERMES ONLY: board mode |
| references/depth-tiers.md | pre-port local copy | study-guide labels removed; Deep text reworded as waves of tasks; Hermes label added; teaching-pack paragraph removed |
| references/evidence-tiers.md | pre-port local copy | unchanged from the pre-port copy |
| references/delivery-variants.md | pre-port local copy | author text, added after the pre-port snapshot: section on shipping a built artifact; intro sentence reworded |
| references/search-routing.md | pre-port local copy | Sci-Hub step removed; runtime tools marked as external requirements (X routes included); R3 Hermes label and in-repo pointer; added after the pre-port snapshot: Space Apps and Earthdata lines, and the desktop-preview route in the X list and discovery order |
| references/llm-wiki-ingestion.md | pre-port local copy | one bullet reworded, with its Hermes-only readiness clause moved to a Hermes-labelled line; that line added |
| references/fact-checking.md | user skill grounded-citations, section "Fact-Checking Mode" | extracted; heading renamed; em dashes replaced with punctuation |
| references/report-prose-style-pt.md | user skill, productivity/study-guide/references/writing/guide-prose-style-pt.md | renamed from guide-prose-style-pt.md; trimmed: study-guide chapter sections and the Termos introduzidos bullet removed; SOUL.md reference removed; "guide" changed to "report"; one sentence added so that a range after "entre" joins with "e", as scripts/post_write_cleanup.py does |
| references/math-and-latex-style.md | user skill study-guide, references/math-and-latex-style.md | trimmed; script references removed |
| references/plans-and-briefings.md | user skill study-guide, references/plans-and-briefings.md | trimmed; record term changed to entry |
| references/post-write-cleanup.md | user skill, productivity/study-guide/references/writing/post-write-cleanup.md | rules restated; script is a new implementation |
| references/parallel-fanout-checks.md | user skill parallel-research-verification, section "Parent-side work while children run" | extracted; wording generalized |
| references/retrieval-fallbacks.md | user skill web-retrieval-fallbacks, sections for the R3 route | extracted; plus an Obscura section (22 lines, with the ten-document chain limit and the 45-second pause) added by the Hermes curator during the port, not in the source, and unsourced; em dashes replaced with punctuation |
| references/scholarly-metadata-apis.md | user skill web-retrieval-fallbacks, references/scholarly-metadata-apis.md | verbatim copy, except em dashes replaced with punctuation |
| scripts/count_sources.py | pre-port local copy | header-row fix: a read-status header row with no URL is skipped (HEADER pattern added for it) |
| scripts/sources.py | user skill grounded-citations, scripts/sources.py | environment names and default ledger path renamed to DEEP_RESEARCH_*; em dashes in messages and comments replaced with hyphens (one en dash kept, inside a regex); docstring lines edited |
| scripts/post_write_cleanup.py | new | implements the rules in references/post-write-cleanup.md; not the recipe's code |
| templates/template-briefing.md | user skill study-guide, templates/template-briefing.md | trimmed; record term changed to entry |
| templates/template-briefing-onda.md | user skill study-guide, templates/template-briefing-onda.md | trimmed |
| templates/template-plano-secao.md | user skill study-guide, templates/template-plano-secao.md | trimmed; record term changed to entry |

## Notes

- The ledger default is now ~/.cache/deep-research/citations/ledger.json, or $DEEP_RESEARCH_HOME/citations/ledger.json when that variable is set. To reuse a ledger from an earlier install, set DEEP_RESEARCH_LEDGER to its path.

## Upstream

Upstream: companion-inc/feynman (MIT). At that repo's HEAD, skills/deep-research/SKILL.md is an 8-line file, and website/src/content/docs/workflows/deep-research.md is a docs page with the headings Usage, How it works, Output and Customization. No other file in this folder exists at that HEAD, so for those files the origin is the pre-port local copy, not a verified upstream file. LICENSE is the upstream license.

## Testing

- Tested: scripts/sources.py under `python3 -B -S` with an empty environment except HOME: reset, add, quote (positive and negative), verify --evidence, render --replace-in, verify --strict, unknown id, and the default ledger path.
- Tested: scripts/count_sources.py on a four-row sample: rows 4, distinct URLs 3, read 2, verified unread 1, discovery only 1.
- Tested: scripts/post_write_cleanup.py on a sample: --check writes nothing; the English and Portuguese rules, including the "between" and "entre" joins and percent ranges; scientific notation changed only in math; code blocks untouched.
- Not tested: installing the whole folder from a URL or a tap; a subagent run end to end; the queued-task probe on a live queue.

## Checks

Before you finish a change:

1. Add no em or en dash to any file, except the one en dash inside a regex in scripts/sources.py.
2. Every references/, scripts/ and templates/ path cited in a .md file must exist, except in the Provenance table.
3. The scripts must run: `python3 -B -S scripts/sources.py --help`, `python3 -B -S scripts/count_sources.py FILE...` (prints the totals), and `python3 -B -S scripts/post_write_cleanup.py --check FILE`.
