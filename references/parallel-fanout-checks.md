# Parent-side checks while children run

Copied section. Runtime-specific wording is generalized, and the one runtime-specific line is marked at the end. Provenance: README.md.

## Parent-side work while children run

- **Batch results arrive after the turn ends.** A subagent batch returns subagent ids at once and runs the children in the background; each result re-enters the conversation as a new message only once the current turn has ended. So write every brief to disk before the batch goes out, do the lead's own first-hand reads and the plan ledger while the children run, then end the turn with a one-line status. Polling transcripts or artifacts does not bring a result sooner.
- **Steer children onto a verified route the moment you find one.** Child prompts cannot know which fetch paths work today; when your own probing finds one that renders (a fetch
  tool, an API endpoint, a browser path), send it to the children as a steering message so they stop re-discovering dead routes. Delivery lands at
  the child's next tool-result boundary; a child already waiting on a long model call will
  not see it in time.
- **Run a bounded first-hand pass on the most load-bearing sources.** Opening the primary
  artifacts yourself is what makes the Step 2 spot-checks cheap, and it calibrates which
  child claims to trust.
- **Keep a parent notes file** (`<output-dir>/parent-findings.md`): verified facts with URLs
  and metrics, open tensions, and which children are running. Children write their own
  files; synthesis merges from disk, so nothing depends on surviving context.
- **Verify hype metrics against the primary API before they enter the report.** Star counts,
  post dates, engagement, and claimed latest versions get checked at the source, not copied from the post or report that cites
  them: `curl -fsS https://api.github.com/repos/<owner>/<repo>` (stars, `pushed_at`) for
  repos, the package registry (e.g. `registry.npmjs.org/<pkg>/latest`) for versions, fxtwitter for posts (see the X routes in references/search-routing.md). Hype windows spawn lookalike projects:
  several repos share one name and most have single-digit stars; the report must say which
  is which.

## After a writer wave: audit each file mechanically

A writer returns a self-report that its section is complete; the file is the evidence. Before accepting a wave, run one loop over every file it produced and read the counts, not the summary:

```bash
for f in <subsections-dir>/S*.*.md; do printf "%s w=%s links=%s em=%s head=%s\n" "$f" \
  "$(wc -w <"$f")" "$(grep -o '](http' "$f" | wc -l)" "$(grep -c -P '\x{2014}' "$f")" "$(head -c 40 "$f")"; done
```

- **Links are what writers drop, not prose.** A subsection with zero inline links when the contract demands them gets a fixer pass before assembly; the fixer works from the pack rows, so it cannot invent a source. The same file can be otherwise excellent, which is why the count is the check and the read is only the confirmation.
- **Normalise file names and heading levels in one pass before assembly.** Children drift (`S4-1-slug.md` beside `S4.1.md`; `##` beside `###`). Assembly keys off the file name and the heading prefix, so a drifted name silently drops or reorders a subsection.
- **Demote only the first heading line.** Rewrite each file's leading `# ` once; a blanket `^# ` substitution also rewrites `#` comments inside fenced code blocks into headings. Take the subsection number from the file name, because writers routinely omit it from the title and the numbers are the reader's map.
- **A check must exercise the artifact under test, not a hand-built equivalent.** A lowering check that compiled a hand-assembled rectangle while the fixture declared its own primitive passed for a whole wave while the compiler could not lower that primitive at all. Point every check at the fixture file and assert the artifact's real output shape (the lowered circle, and the absence of the bare tag).
- **Absence sentences go stale the moment the build lands.** Writers state "the proof file is absent"; after the build wave, grep every subsection for `absent` and `pending` and replace the sentence with the run status and the file that now exists, or name plainly the one that still does not.
- **`count_sources.py` undercounts distinct URLs when a pack carries them as markdown links**, because its URL pattern matches bare URLs only: a count from it can fall far below the true total. Re-count with a link-aware pattern and quote the unit with the number.
- **Demote a writer's internal headings.** Writers emit `### Status` or `### Build the stages` inside a subsection; left alone they read as siblings of `### S<k>.<n>`. Rewrite every `### ` not followed by `S<k>.<n>` to `####`.
- **Check the wave's word totals against the plan budgets.** A section at half its band was truncated, not tightened.
- **A child's report of its own tooling can be wrong.** A file-mutation warning may name a scratch helper the child wrote; re-grep the deliverable for the change instead of trusting the summary either way.
- **Confirm a delegated file exists, with its claimed content, before any pointer to it lands.** A child's "created" is a self-report. A SKILL.md link written first becomes a dead pointer when the child failed or stopped early, and the next agent follows it into a missing file. Read the file back, then add the pointer.

Hermes: `delegate_task` in batch mode is the subagent batch, and steering is `delegate_task(action='steer')`.
