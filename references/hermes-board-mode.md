# Hermes board mode

HERMES ONLY. Other agents: do not follow this file. Use references/deep-mode.md.

Board mode runs a Deep wave as kanban cards on a Hermes board. Use it only on Hermes, and only after the dispatcher probe below passes.

## Dispatcher probe

Probe the dispatcher through its effects, not through process names:

1. Read the dispatch_in_gateway setting in the kanban section of the Hermes config.
2. Read the gateway state file, ~/.hermes/gateway_state.json.
3. Run `hermes kanban boards list` and read the active board. Never assume that the default board is active.

A board that exists proves nothing about consumption. Boards persist after runs stop, so confirm that a dispatcher is consuming cards before you commit a plan to board mode.

## One board per topic

Use one board per topic. Creating a board is a database change, so confirm with the user before you create one: `hermes kanban boards create <slug>`. If the active board belongs to an unrelated project, ask before you use it.

## Card types and order

Cards use the task types in references/deep-mode.md: source-pack, write, deep, audit, fixer, build. Waves drain in sequence. Create each fixer with its audit card as a parent, so the fixer waits for the audit.

**Gate a card on every artifact it reads, not only on the wave's source cards.** A coverage map that maps planned subsections to pack rows reads the section plans, so the plans card is its parent; gated on the packs alone it sits in `todo` past a `plans/` that is still empty, then blocks correctly rather than inventing a subsection inventory. Before creating a card, list its inputs and make each one a parent, then re-read the order: an artifact-order mistake looks identical to a worker failure from the board.

## Kanban tools

- kanban_create: create a card. Pass an idempotency key on every create, and pass parent ids so the gates hold.
- kanban_show: read a card with its comments and events.
- kanban_list: list the cards on the board.
- kanban_link: add a parent-child dependency between two cards.
- kanban_comment: add a comment to a card.
- kanban_complete: mark a card done.
- kanban_block and kanban_unblock: mark a card blocked, or clear the block.
- kanban_request_review and kanban_request_changes: send a card to review, or send it back with changes.

## Shell checks

- `hermes kanban boards list`
- `hermes kanban boards create <slug>`
- `hermes kanban list`
- `hermes kanban show <id>`

## Liveness and worker exit

Two different failures look alike from the board, so read before acting:

- **Nothing moves for about five minutes and no file exists**: check one card with `hermes kanban show <id>`. If the wave is still stalled, switch its tasks to subagent mode (`references/deep-mode.md`) and record the switch in the state file, in the `switch` field.
- **The worker exited without its file** (a `worker_result` carrying a protocol violation or a "kept retrying" message, output path empty): the card stays `running` while nothing consumes it, and the stale timeout is hours. Run that task yourself as a subagent, brief it with the route that actually works, cap the retries in the brief ("stop retrying a route after two failures"), and record the switch with its reason. Re-creating the identical brief just stalls again.
- **A file exists and the card is still running**: the worker is in its closing checks. Read the file's mtime before calling it stuck; a card that writes every few minutes is working, however long it has run.

## Accepting a card

The completion summary is a self-report. Re-run the load-bearing check the card names. On a build card also read the saved output itself: a suite that prints `PASS` counters while `failed_commands` sits above zero has checks that crash before printing a `FAIL` line, so the counters look clean and the summary cites them. Grep the output for `Traceback` and for non-zero return codes before accepting.

## Fan-out inside a card

A card worker may fan out parallel fetching with `delegate_task`. Give each child one narrow question and one output path, and check each child's file before you accept it.
