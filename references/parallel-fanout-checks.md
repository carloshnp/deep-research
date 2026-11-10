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

Hermes: `delegate_task` in batch mode is the subagent batch, and steering is `delegate_task(action='steer')`.
