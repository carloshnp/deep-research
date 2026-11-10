# Deep mode: waves of tasks

This file applies to every AI agent. It names no tool from any one harness. An agent whose harness has a task queue of its own, with parent links, can use queued-task mode after the probe below. Every other agent uses subagent mode.

## Waves

Deep runs in waves. A wave is a set of tasks that run together. Waves drain in sequence: the next wave starts only after the previous one has finished. An audit task gates the fixer tasks that follow it, so a fixer starts only after its audit has finished.

Each wave runs in one of two modes:

1. Subagent mode (default). The lead sends each task to a subagent from the harness's subagent tool.
2. Queued-task mode. Use it only when the harness has a task queue with parent links, and workers that the lead does not run itself. Run the probe below before the first wave.

If the probe fails, or the harness has no such queue, use subagent mode.

## Queued-task probe

Run the probe once, with one task:

1. Create one task with a body and a parent link.
2. Let a worker that the lead does not drive claim and run the task.
3. Read back done or blocked for that task.

If any step fails, use subagent mode. A partial pass counts as a failure.

## Subagent mode

- Keep at most four subagents in flight. When one finishes, start the next.
- Write every brief to disk before you send it. A brief carries every input its child needs, because a child cannot ask questions.
- Give each child one output path. No two children share a path.
- Check each child's output file on disk before you accept it.

## First-task gate (both modes)

The first task of the first wave runs alone. Check its output with the load-bearing check named in its brief: a recount, a grep for the corrected value, or a read of the file. Start the rest of the wave only after that check passes. If the check fails, stop and report the failure.

## No movement in queued-task mode

If a queued-task wave makes no progress for about five minutes, stop waiting on it. The lead runs that wave's remaining tasks in subagent mode, keeps the order (each audit before its fixers), and writes the switch in the switch field of each affected entry, with the reason. A switch changes how the remaining tasks run. It never reopens outputs that were already accepted.

## Self-reports

A task's or child's final message is a self-report. Before you accept it, re-run the load-bearing check: recount, grep the corrected value, verify that the file exists. Never accept a summary without that check.

## Task types

Deep waves use these task types, in this order: source-pack, write, deep, audit, fixer, build. Each task points at BRIEFING.md and at its section plan instead of paraphrasing them.

## State file

Keep one state file per run, named state.json, at the run root that the plan names. Each task has one entry with these fields:

- task: the task name
- mode: subagent or queued
- handle: the queued task's id, empty in subagent mode
- status: pending, running, done, blocked, or switched
- output: the output path
- check: the load-bearing check and its result
- switch: empty, or the switch made and why
