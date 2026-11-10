# Delivery variants

Deliveries that come after the main report, plus the case where the run also ships a built artifact. Read the section that matches the request; the main Step 5 in SKILL.md covers the normal delivery.

## Shipping a built artifact alongside the report

When the run produces something that runs (a scaffold, a starter repo, a working config) as well as a report, the artifact is part of the deliverable and it is judged against the report's own recommendations. Two failure shapes:

- **The artifact contradicts the report.** A report whose section 3 says every page needs a Markdown mirror, beside a scaffold that emits `llms.txt` only, is a reader following the advice into a repo that does not do it. Before delivery, list each recommendation in the report that names a file, command or setting, and check the artifact for it with a real command. Close the gap, or state in the artifact itself which recommendations are not implemented and why. Never leave the contradiction to a limitations section, because the artifact is what the team runs.
- **The report describes the artifact from memory.** Every measurement the report prints about the artifact (page count, build time, output sizes, file counts) is re-derived from the built output after the last edit, not from the build log of an earlier run. The scaffold changes as the report is written; a size quoted from the first build is stale by the time the report is read.

The verification order that catches both: build the artifact, run its own verify commands, then diff the report's claims about it against the command output in one pass. Record the artifact path and its measurements in the provenance sidecar, because an artifact delivered without its measured state is a claim rather than an artifact.

## The queued second pass

When the user asks for the queued second pass, run it as one focused follow-up round with a per-item verdict: promote to read, keep qualified, or drop, each recorded with page counts or content_ok notes. If a queued URL resolves to a stub (contents-only PDF, JS shell), recover the full text through a verified mirror and cite both the stub and the mirror. Promoted items must have their read-status labels updated everywhere they appear, including the coverage-limits section; then re-render the Sources block and re-verify.

## Relocating the artifact tree

When the user asks for the artifacts to be relocated, copy the tree first, then rewrite the absolute paths stored inside it: the provenance sidecar is an index of paths and goes stale the moment the root changes. Walk with `os.walk`, not `glob('**/*.md')`, because glob skips hidden directories such as `.drafts` and those files silently keep the old paths. Prove the relocation with a grep for the old root that returns nothing before deleting the source, and spot-check that the report body itself is byte-identical apart from the rewritten paths.

## Patching a live skill, config, or repo

When the deliverable is a patch to a live skill, config or repo, re-read each target immediately before writing it. Another session may have applied part of the patch already, and an evidence file it created can duplicate one you are about to write; verify the part that exists instead of rewriting it, and record the deviation in the patch document. That document states its own status, so flip the status when it changes: a proposal still saying "nothing has been applied" after application is a lie the next session will act on.
