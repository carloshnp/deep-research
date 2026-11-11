---
name: deep-research
description: Use when asked for deep research. Cited, sourced brief.
version: 0.4.3-hermes.1
author: Feynman (companion-inc), adapted for Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, deep-research, investigation, citations, feynman]
    source: https://github.com/companion-inc/feynman
---

# Deep Research

**Mode rule.** Deep runs as waves of tasks. Use subagent mode unless the harness passes its probe: the one-task probe in `references/deep-mode.md` (queued-task mode, for a harness with a task queue that has parent links).

Hermes: use board mode (kanban cards) only after the dispatcher probe in `references/hermes-board-mode.md` (HERMES ONLY; other agents do not follow that file).

Run a source-heavy investigation at one of three depths. Retrieval order, paper search, and evidence tiers are fixed for all tiers. What changes with depth is execution shape and output structure.

## When to Use

Trigger when the user asks for: deep research, comprehensive analysis, in-depth report, multi-source investigation, "research X thoroughly", "tell me everything about X". Pick the tier (Scout, Standard, Deep) in the plan; default to Scout for single-fact questions and Standard for multi-facet topics unless the user names a tier.

## Standing execution limits

These hold for every tier unless the user approves a specific run in the current session.

- Run nothing on a remote host, because the run changes a machine the user did not ask you to touch. Read-only probes of the local machine (versions, hardware, config files) are fine.
- Run no inference, benchmark, or model download to produce a number: a run on other hardware yields a figure that looks measured without being so. A figure for a configuration nobody ran is computed from a stated profile and labeled that way (see Basis labels under Writing).
- Launch no GUI app to test a deliverable, because a launch changes the user's app state and can stop at a first-run screen. A desk check (parse, static load, fixture comparison) is the default. An approved launch is recorded in the plan as run, with its log path.
- Ask before installing packages or fetching model weights, because installs change the machine. The question states the disk space and the minutes involved.
- An approval covers the run it names. If the user withdraws it, stop at the current state and leave the machine as it is, because a run that continues after withdrawal acts on a permission that no longer exists. Then report what ran and what did not.

## Depth tiers

| Tier | Use for | Execution | Output shape |
|---|---|---|---|
| Scout | Single fact, narrow question, "what is X" explainer | Lead agent only, no subagents | Short brief: summary, findings, open questions |
| Standard | Comparisons, surveys, multi-facet topics | Subagents: 2 to 4 researchers, then a verifier and a reviewer in one batch | Sectioned report: sections with subsections, each subsection expanded |
| Deep | Prototype-grade or publication-grade research | Waves of tasks, each with subagents (mode rule above) | Section plans plus one file per subsection, source packs, coverage map, assembled report |

Pick the tier in the plan and record it. When the user names a level in words, map it: "normal" and "standard" mean Standard, and "deep" means Deep. Never inflate a Scout with subagents unless the user asks for comprehensive coverage, current landscape, benchmarks, or production deployment. Standard always uses subagents. Deep runs in waves of tasks under the mode rule above.

Hermes: before a plan commits to board mode, run the dispatcher probe and read the liveness rule in `references/hermes-board-mode.md`. A board that exists proves nothing about consumption; that file defines the probe, one board per topic, and the fallback to subagent mode.

Structure reference for Standard and Deep: sections with subsections, and at Deep depth every subsection is expanded from a frozen section plan. See `references/depth-tiers.md`.

## Retrieval order (fixed)

R1 Obscura, both channels. MCP browser tools first (`browser_navigate` plus `browser_markdown`). If the MCP transport fails, use the Obscura CLI (`obscura fetch --dump markdown`). If one channel hits a wall the other clears, retry the same URL through the other channel before downgrading. The MCP side caps a navigation chain at ten documents and pauses itself for about 45 seconds once that trips, so switch to the CLI on the first chain-limit error instead of retrying it; mechanics in `references/retrieval-fallbacks.md`.

R2 Hound MCP (`smart_search`, then `smart_fetch` with `focus`, then `smart_crawl` for doc sites).

R3 Firecrawl-backed `web_search` and `web_extract` (runtime tools, see README), plus the fallbacks in `references/retrieval-fallbacks.md` (jina reader, lite DDG, Wayback). For a long page, read the full-text file the tool saved rather than re-fetching; for a repository, clone it with `git clone --depth 1`. Both are in the "Long pages and whole repositories" section of that file. Firecrawl's keyless tier rate-limits with HTTP 429 on source-code and model-documentation pages under load; substitute `raw.githubusercontent.com` for repo files and the GitHub REST API for metadata instead of treating the page as unavailable.

Record which route produced each source. Full mechanics: `references/search-routing.md`.

## Paper search (fixed)

Search everything, not just arXiv: Google Scholar, Semantic Scholar, OpenAlex, Crossref, Unpaywall, arXiv `abs` pages, publisher pages via R1. Chain and fallbacks: `references/search-routing.md`.

## X is P0

X/Twitter is a first-class source alongside web search because practitioner signal surfaces there first. Discovery order is Obscura, then the internal browser, then `portal_x_search` (external requirement, see README; full pattern: `references/search-routing.md`).

Check which of those three is actually present in this session before committing the plan, because the tool catalog and the browser's login state differ between sessions. For an announcement made the same day, read the organization's own handle first (`web_extract` on `https://x.com/<handle>`): search indexes lag, while the profile page already carries the post. When the Portal tool is absent and the browser has no X profile, the highest-yield logged-out route is `web_extract` on `https://x.com/<handle>`: it returns that profile's recent posts with ISO timestamps, status URLs and engagement counts, so a handle walk plus a snowflake ID filter replaces search. Fill gaps with DuckDuckGo HTML through `r.jina.ai`, keep `site:x.com` as a top-up only because its index runs weeks behind, and re-verify every cited post through `api.fxtwitter.com/i/status/<id>`.

Hermes: When the session runs inside the desktop app, the logged-in X route is the preview pane: `desktop_preview` action=open on `https://x.com/search?q=<query>&f=live`, then action=read for the timeline text, which carries handles, timestamps and post bodies, with `drive_preview` scrolling for more. Probe that pair with one open and one read before writing the plan, and read a second time when the first read comes back `The page has not finished loading` with zero characters: the pane answers as soon as the timeline settles, and one early empty read is not a walled channel. `browser_exec` with `local=true` does not substitute: while the desktop app holds the Chromium profile it reports the profile as in use and falls back to a logged-out browser, so the blank timeline there is a sign the shared profile is busy, not a sign X is unreadable.

## Evidence tiers (fixed)

Official docs and specs plus primary papers outrank explainers; community signal (X, Reddit, HN) is searched first-class, quoted, and verified; aggregator mirrors are never the sole source for a claim. Labels `(read)` versus `(URL verified, not read)` versus discovery-only are mandatory. Full table: `references/evidence-tiers.md`.

## Citations (delegated)

Citation is owned by the ledger in `scripts/sources.py`: reset the ledger, register every source at retrieval time, cite while drafting, render the Sources block mechanically, verify before delivery. Never hand-type URLs into a Sources block. For disputed or high-stakes claims use the fact-checking mode in `references/fact-checking.md` (verbatim quotes, `[unverified]` markers).

## Writing rules

All reports follow this wording contract: one idea per sentence with the subject named, no em or en dashes, no filler openers, no borrowed authority (cite author and year, or state the mechanism), mechanism over impression, technical terms explained at first use. Portuguese reports follow `references/report-prose-style-pt.md`; English reports follow `references/writing-contract-en.md` (reader, placement and chain rules). Math follows `references/math-and-latex-style.md`. Run `scripts/post_write_cleanup.py` before delivery (rules: `references/post-write-cleanup.md`), then `python3 scripts/check_report_style.py <report.md> [--lang pt]` on the assembled report. It blocks delivery on any hard error: internal section IDs, process words, pasted label lines, a missing status line, a second title, or a paragraph over 180 words.

When the brief tells the reader what to do, the evidence has to survive translation into steps. Three separate checks, because each one fails on its own:

- Every artifact the steps name carries a repository and an exact filename. A quant label, a model nickname or a product name is not a source, and a reader who cannot locate the file stops at step one.
- Every setting the evidence says was required to get the thing running appears in the command itself. A report that explains the machine needed a smaller context, then prints a command with no context flag, is unusable, and this is the most common way a technically correct draft fails review.
- The section ends with a failure path: the order in which to relax settings when the first attempt refuses to start, plus the log lines that identify which setting is short.

Check the commands against the reader's stated starting point rather than the author's, name the binary and build the command assumes (a prebuilt archive and a source build rarely accept the same arguments), and say which front end the commands target when the tool ships both an app and a terminal.

Basis labels: every figure carries one basis label. `measured`: a command ran on the device the figure describes, and its output is saved. `computed`: arithmetic over inputs, with each input listed and the device profile named. `documented`: a cited source or a file that was read. `recalled`: memory, stated as such, with no verdict built on it until its source is read. A figure for hardware that nothing ran on is never `measured`.

Process notes stay out of the artifact. Decision answers, confidence figures, tier labels and subagent counts belong in the plan and the provenance sidecar, not in the body. A confidence figure inside a research report reads as evidence to every reader who does not know where it came from. Internal identifiers do the same damage: plan and decision IDs, task and wave names, and words such as BRIEFING or 'Lead check' point at the run rather than the subject. Before delivery, the report gate (`scripts/check_report_style.py`, run after cleanup) finds them, and each one is replaced with the claim it stood for.

When the stated window is narrower than the evidence that carries the answer, date the headline where the headline is stated. A window-honest coverage section near the end does not repair a bottom line that reads as current.

Open the report with a status line that names the checks that ran and the checks that did not, with the reason for each gap. A check that appears only in a limitations section reads as passed.

## Step 1: Plan

Pick a run root before the first write, for example `~/research/<slug>/`, and create `outputs/`, `plans/` and `research/` under it. Relative paths in this skill resolve there. The shell's working directory can be `/`, so a relative write lands at the filesystem root, and the scratch directory is pruned, so deliverables do not belong there.

Write `outputs/.plans/<slug>.md` with: tier, key questions, evidence needed, freshness window (for example 2025 to 2026 only, or unset), scale decision, task ledger, verification log, decision log. For Deep, also write section plans under `plans/<id>.md` (frozen before writing) and a `BRIEFING.md` that tasks point at instead of paraphrasing. Each plan entry carries the twelve fields in `templates/template-plano-secao.md`. Run `python3 scripts/check_plan.py plans/*.md` before any writer starts; a non-zero exit stops the start, and its output names each missing, empty or placeholder field.

A freeze binds the writers, not the clock. When a plan boxes a gap it could not fill ("the official text was not supplied") and the gap then closes, write the missing pack and rewrite that plan before any writer starts, rather than annotating the frozen file: a plan that still declares the source missing sends nine writers to write around a hole that is already filled on disk.

Scope first. When the topic's noun names more than one product surface (for example, "plugins" can mean an agent-side Python plugin, a desktop-app UI plugin, a dashboard backend, or a TUI widget), list each surface in the plan's scope section with one line on where it lives and what it can do, then ask through clarify which are in scope. Section plans and briefs inherit the scope, so a wrong surface costs every downstream file. When the research goal is to build or submit an artifact, give "how it is written and coded" its own section: file layout, a minimal working example, the check that proves it runs, the packaging or submission steps, and the failure path.

**Instantiate the artifact the spec judges.** When a challenge, rubric or spec names something the deliverable has to produce (three compared strategies having included the existing one, a migration plan, a worked query), the report carries one worked instance of it, not only instructions for building one. A section that describes how a comparison would work reads finished and fails the reviewer's first test, because applying the report's own abstention rule to a described-only comparison yields no result. Give the instance one committed case: a named place, a named season, dated inputs with sources, and every unsupported cell marked unavailable rather than filled. Where the rubric's weights are unpublished, state the process it does publish and say plainly that no score can be predicted; never import an archived year's rubric as if it were current.

Size from measurements. Probe the execution host before sizing any experiment or model run: CPU, RAM, GPU memory, OS, and runtime versions (for example `lscpu`, `free -h`, `nvidia-smi` where present, and the Node or Python version). Plan around the host the user named, and do not plan around a remote machine the user has not mentioned. The same probe-first rule applies to backend choices. When the user names a target device other than the execution host and rules out runs there, probe only the local host for versions, then size the target from the stated spec as computed arithmetic: list each input, say the spec is assumed, and never present the target's figures as probed.

Probe the discovery channels before writing the plan, not after. One cheap call per channel (a search, a profile fetch, a tool lookup) tells you which routes actually return dated in-window material and which are walled, and it turns the plan's blocked-or-partial expectations into measurements instead of guesses. Record each probe and its result in the verification log, and carry the surviving channel limits into every subagent brief in Step 2. A plan written before probing commits the whole run to a route that may be unavailable. A channel probe is not evidence gathering; it is the measurement the plan needs, and it stays one call per channel rather than turning into a survey.

Write every page, PDF or file the user attached to `research/<area>/` as a pack before the plan, with the URL, the fetch time and a read label at the top. A subagent inherits no session history, so an attached document that stays in the transcript is invisible to every writer and planner: they either paraphrase it from a plan's summary or report it as missing and plan around a gap that does not exist. Keep the verbatim text, not a summary, so writers quote the source instead of restating the lead's reading of it.

When the deliverable is bound to a date (a competition, a conference, a filing window), fetch the official schedule during the probe and put the remaining time in the plan, dated the day it was read. Depth and section count calibrated to an open-ended semester produce a report that lands after the deadline, and a deadline found halfway through forces an amendment to plans that were already frozen.

A deadline is not the build envelope. The date says when it ships; the envelope says how much gets built, and an agent-heavy build with components tested beforehand carries far more than a hand-written sprint. Ask which one governs, record the envelope in the plan beside the date, and put it in the briefing so writers size breadth rather than trim. Default to the user's stated envelope over the one the calendar implies: a two-day event read as a two-day budget is the wrong cap when the team is weeks into prep work and running agents. When the envelope is large, list the full capability set and let the team cut, phase expensive components thin-to-full instead of dropping them, and move the binding constraint from time to validity (wrong joins, unlabelled proxies, unsourced numbers, an unreproducible demo).

Then stop and ask: `Proceed with this deep research plan? Reply "yes" to continue, or tell me what to change.` If the ask returns with every question unanswered and outcome `timed_out`, re-issue the same question set once before falling back to defaults, because a timeout records that nobody saw the form rather than that the user prefers the default; record the defaults you act on so the plan shows which choices were assumed. Explicit "run the plan" counts as approval, and so does "proceed", "go", or "yes" after a revision. Before approval, tool calls are limited to channel and host probes, and to any runtime probe the mode rule names. Full fetches, downloads, source reads and counts wait for approval, because evidence gathered against a plan the user has not seen gets re-scoped when the user corrects it. On a revision, archive the superseded plan and its section plans under `plans/v<n>/`, put a one-line change note at the top of the new version, and record the approval in its status line. After approval, blocked or partial work still delivers artifacts, never chat-only output.

If the requested deliverable is research-backed ingestion into an LLM wiki rather than a standalone report, use the adapted workflow in `references/llm-wiki-ingestion.md` instead of the report path below.

## Step 2: Gather evidence

Scout: the lead searches directly, minimum 3 distinct query angles, notes in `outputs/.drafts/<slug>-research-direct.md`. No subagents.

Standard: write per-researcher briefs first (`outputs/.plans/<slug>-T1.md` and so on), then send them as one subagent batch. When the user names a model for the subagents, pin every child to it through the batch's per-task model option rather than letting the default route decide, because a run promised on one model that half-runs on another cannot be described either way afterwards; deviate only for a child that needs a capability the pinned model lacks, and say so in the brief. The batch returns subagent ids at once and its results arrive in a later turn, so end the turn after the batch goes out and follow the parent-side checks in `references/parallel-fanout-checks.md` while the children run. Give each child one narrow question and one exact output path, and verify each artifact file exists on disk with substantive findings before synthesis. Existence is not accuracy: check the arithmetic inside any count a child reports before quoting it, because a study's total can disagree with its own arms (a paper reported as 194 participants whose post-test arms read 142 and 174), and a sample size that does not add up is a transcription error in the child's note rather than a finding. Quote the arms, or drop the number. Re-run one command the child says it ran and compare its printed output against the figure in the artifact: a self-report of "sixteen rows verified" and a query hit count are cheap to reproduce, and a pack that reproduces neither is a pack to distrust.

Hermes: `delegate_task` in batch mode takes the `tasks` array, and batch results arrive in a later turn. Other agents: their subagent tool. If it returns at once, skip the wait.

Every child brief repeats the environment facts the lead measured, because a child inherits no session history and will either rediscover them at the cost of calls or conclude the topic is unreachable. Paste in, verbatim: which discovery tools are absent from this session, which routes returned stale or walled results, the exact route that does work, and any computed filter bounds (date windows, ID ranges, price bands) the child must apply. A brief that says "search X" without the working route produces a child that reports the channel as broken.

Every child brief also states its output contract: the exact file path, the required table columns, the read-status labels, and the instruction to write "what I could not find" plainly rather than filling gaps. Children cannot ask questions, so an ambiguous brief comes back as an ambiguous artifact.

Deep: run waves of tasks (source-pack, write, deep, audit, fixer, build). Each task points at `BRIEFING.md` and its section plan. A task may fan out parallel fetching to subagents, with one narrow question and one output path per child. Waves drain in sequence, audits gate fixers. Write every wave's brief to disk before it goes out, and record each task in the state file (`state.json`; format in `references/deep-mode.md`). See `references/depth-tiers.md`.

Hermes: the same waves run as kanban cards, with an `idempotency_key` on every create and parent links for the gates. See `references/hermes-board-mode.md`.

After gathering, update the plan ledger and verification log. Record exactly what failed and proceed blocked or partial rather than silently.

For unstable or current claims, search the web first rather than relying on memory: releases, capabilities, pricing, regulations, model availability, recent literature, benchmarks, companies, markets. Distinguish historical claims from current status.

## Step 3: Draft

The lead writes the synthesis. Never delegate synthesis.

Scout writes the brief directly. Standard and Deep write sections as subsections and expand each subsection with mechanism, numbers with units, and worked detail, never compressed summaries. For Deep, one file per subsection under `outputs/sections/subsections/`.

Sweep before citing: every number, benchmark, and load-bearing claim maps to a source URL, research note, raw artifact path, or command output. Downgrade or remove the rest. Mark inferences as inferences. Attribute each recorded result to the binary and version that produced its saved output, copied from that output: a second binary of another version on the PATH does not change which one ran.

Any count the report asserts (posts verified, sources consulted, models compared, items in a table) is computed with code over the evidence files, never tallied while reading. A hand-tally drifts by one or two the moment evidence arrives from several agents, and a wrong count in the summary block is the cheapest error for a reader to find. Compute it, then write the number, and state the denominator when the count could be read two ways ("thirty verified, of which twelve concern the question"). Compute it after the last thread lands rather than while the front matter is being drafted, because a count written before the evidence is complete is wrong by construction and then survives every later consistency check. The unit of count has to be named as well: rows in the source tables, distinct URLs, and rows marked read are three different numbers about the same run, and one "sources consulted" figure hides which one it is. `scripts/count_sources.py research/T*.md` prints all three with the read-status split, and its output is what goes into the front matter and the provenance sidecar. Before quoting any total, check the script's row count against one pack by hand: a pack in a different table layout comes back as one row, which looks like a small count rather than a parse failure. Re-run the script after any fix that changes a row's read status, then update every place the totals appear. Aggregate measurements pool the observations rather than averaging per-file means: the mean of seventeen per-section sentence lengths and the pooled mean over every sentence in those sections are different numbers, and a report that quotes the first while describing the second is wrong in a way no presence check catches. State the pooling and the denominator beside the figure.

Every figure the lead introduces itself, meaning one that came from the lead's own fetch rather than from a child artifact, goes into `outputs/.drafts/<slug>-research-direct.md` at the moment it is used, with its source URL and read-status. A verifier can only trace against files it can read, so a number that lives only in a scratch fetch or in shell scrollback comes back untraceable, and the verifier is right to flag it.

## Step 4: Cite and review

Cite through the ledger in `scripts/sources.py`, never by hand. Then review: Scout self-reviews into `outputs/.drafts/<slug>-verification.md`. Standard runs a verifier and a reviewer subagent with FATAL, MAJOR, MINOR findings and fixes FATALs before delivery. Send both in one batch, because they check different things and neither needs the other's output: the verifier traces every number, citation label and command flag back to an artifact and recomputes every aggregate from the metrics file, because a figure can sit in an artifact and still be the wrong aggregate, while the reviewer walks the deliverable as a stranger, testing whether the verdict is honest, whether the steps can be followed, whether the freshness of the headline claim is disclosed where it is stated, and whether each causal claim survives the strongest counterexample inside the report's own evidence, which is usually the example the recommendation itself cites. Sequence them only when the reviewer's read depends on the verifier's corrections. When the run is anchored on a document the user supplied, give both subagents that file's path and the claims the report makes about it: a subagent inherits no session history, so a verifier that was never handed the basis document cannot check the report's corrections of it, and the draft ships a misreading of the very file it was built on. Deep runs audit tasks over section ranges with the same severity scale, fixer tasks gated behind their audit, then rebuild plus spot verify. Small fixes use localized edits. Section rewrites or more than 3 substantive fixes go to `outputs/.drafts/<slug>-revised.md`. Check each reviewer finding against the source before editing, including its location and its quoted wording: a finding can be right about the problem and wrong about where it sits. Keep a resolution file with one row per finding, the check used, and the disposition.

After fixes, verify on disk that removed wording is gone and replacement wording exists. Do not claim fixes landed without these checks. Write the check as a script with one assertion per change, printing PASS or FAIL with the evidence each one used, and run it after the last edit rather than after each one: a hand-applied multi-file patch loses a change quietly, and a prose claim that everything landed is the one thing a reader cannot audit. Each change gets both directions, a presence assertion for the inserted wording and an absence assertion for the old, because a presence check passes on the fix that never landed and on the fix that landed in one of two places. Treat a fixer's own report as a claim until that script has run: a batch can report eleven repairs, name the files, and leave one of them untouched. The per-change script also catches the change that landed with the wrong value, which a "did the edits apply" check passes happily: a terminology slip inside the inserted text, a count left stale in a second file, a version number that never moved.

Before any write, assert that each target string occurs exactly once in its file, and stop the whole pass if any count differs. Back up each file under the plan's version folder first, so one file can be reverted without the others. After the last write, diff the front matter's summary block against the head of the report, since a summary kept in a separate file drifts silently. Re-resolve every cited pack ID in the changed text against the pack files, and list any ID that is a formula label rather than a pack row. Count the em and en dashes in the final file; the count must be zero. Cleanup runs before the Sources block is rendered, never after: the block's separator is an em dash and the verifier compares that block byte for byte, so a cleanup pass ordered second turns every source line into a mismatch. Order of operations, heading contract and the two regex guards: `references/report-assembly.md`.

## Step 5: Deliver

Final report to `outputs/<slug>.md` (`papers/<slug>.md` for paper-style drafts). Provenance sidecar next to it with: date, tier, rounds, sources consulted (from `scripts/count_sources.py`, with rows, distinct URLs and the read-status split named), accepted, and rejected, retrieval route per source group, X posts consulted, PDFs extracted (URL, pages processed, engine), freshness window, quantitative audit result, plan and research file paths, verification status (PASS, PASS WITH NOTES, BLOCKED). Record the final report's byte count and sha256 after the last edit, and recompute both on disk before delivery; the sidecar goes stale the moment the report changes without it.

End the brief with `## Suggested PDFs/articles for a possible second research pass`. Those are follow-ups only, never counted as consulted evidence.

Less common deliveries have their own procedure in `references/delivery-variants.md`: the queued second pass, relocating the artifact tree, and patching a live skill, config, or repo. Read the matching section when one of those requests arrives.

When the deliverable is a team-facing docs site that carries the report, the site build belongs to the `llm-readable-docs` skill and the report is ingested page by page under it, not summarized into a few pages with the report left as a download: a summary layer is read as a digest of the evidence and gets sent back. Keep the report as the source of truth the pages are generated from, and regenerate rather than edit by hand after any fix pass.

Verify all artifacts exist on disk before responding. The final response defaults to brief: file links plus blocked checks. When the user asks whether the run is complete, answer from the status line: name the checks that have not run, the decisions still parked, and the artifacts still to be written. When the user asks what was found, or asks for it explained, switch to a walkthrough in the chat: what the target does today, what the evidence found, and what can change, in that order, with the numbers inline and no process notes. Length is welcome there and terseness is not, because the artifact already carries the compression and the chat is where the user builds a model of the findings. Answer the format the user asked for over this default.





## Files in this repo

| Need | File |
|---|---|
| Depth tiers and budgets | `references/depth-tiers.md` |
| Mode rule and waves | `references/deep-mode.md` |
| Citation ledger | `scripts/sources.py`, `references/scholarly-metadata-apis.md` |
| Fact-checking mode | `references/fact-checking.md` |
| Fallback retrieval | `references/retrieval-fallbacks.md` |
| Parent-side checks while children run | `references/parallel-fanout-checks.md` |
| Source counts | `scripts/count_sources.py` |
| Post-write cleanup | `scripts/post_write_cleanup.py`, `references/post-write-cleanup.md` |
| Report style gate (blocks delivery) | `scripts/check_report_style.py`, design and thresholds in `references/report-gates.md` |
| Plan gate (blocks writers) | `scripts/check_plan.py` |
| English writing contract | `references/writing-contract-en.md` |
| Assembling a section-per-file report | `references/report-assembly.md` |
| Writing and math style | `references/report-prose-style-pt.md`, `references/math-and-latex-style.md` |
| Briefings and section plans | `references/plans-and-briefings.md`, `templates/` |
| LLM wiki ingestion | `references/llm-wiki-ingestion.md` |
| Search routing and evidence | `references/search-routing.md`, `references/evidence-tiers.md`, `references/delivery-variants.md` |
| Requirements and provenance | `README.md` |
