# Agent instructions

This repo holds the deep-research skill. Read README.md first for requirements, and SKILL.md for the procedure.

## Mode rule

Deep research runs as waves of tasks. Every agent uses subagent mode by default: send each child one brief on disk and one output path, then check each output file yourself. The full procedure is in references/deep-mode.md.

Queued-task mode is allowed only when the harness passes the one-task probe in references/deep-mode.md.

Hermes: board mode (kanban cards) is the Hermes-only mode. Its file is references/hermes-board-mode.md (HERMES ONLY). Other agents do not follow that file.

## Scripts

- scripts/sources.py: the citation ledger (run it with --help).
- scripts/count_sources.py: counts the sources in thread files, with rows, distinct URLs and read status.
- scripts/post_write_cleanup.py: removes dashes and fixes scientific notation in a finished report. Rules: references/post-write-cleanup.md.

## Rules for edits

- Keep em dashes and en dashes out of new text and out of the reports the scripts write.
- Put runtime-specific instructions in their own file, and name that file in the mode rule.
- Run the checks listed in README.md before you finish a change.
