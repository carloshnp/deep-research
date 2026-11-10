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

## Liveness

If no card of a wave has moved after about five minutes, check one card with `hermes kanban show <id>`. If the wave is still stalled, switch its tasks to subagent mode (`references/deep-mode.md`) and record the switch in the state file, in the `switch` field.

## Fan-out inside a card

A card worker may fan out parallel fetching with `delegate_task`. Give each child one narrow question and one output path, and check each child's file before you accept it.
