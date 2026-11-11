# Report and plan gates: design and calibration

Use this when adding or changing a deterministic check on a finished report or on section plans. The two gates are `scripts/check_report_style.py` (report, run after cleanup and before the Sources block) and `scripts/check_plan.py` (plan, run before any writer starts).

## Derive every pattern from the skill's own wording

Before writing a pattern for a required element (the status line, the title, a plan field), search SKILL.md for the sentence that requires it and match the words that sentence uses. The first status-line pattern required the labels `Checks run:` and `Not run:`, which the skill never asked for; it would have rejected a valid status sentence such as "Not run: live search." Match the contract's terms, not a format invented while writing the gate.

## Write the defective fixtures first, then the gate

Write one fixture per hard defect and per warning, plus a control that must pass. Run the suite and confirm each defect fails for the stated reason before writing the gate. Then run the gate on a copy of the most recent real report, read-only. A hit on real output is a finding about the report only after the flagged line is read in context; check each hit before editing either the report or the gate.

## Ban pasted labels, keep the sentence

A line that starts with `Confidence:`, `Basis:`, `Verdict:`, `Decision:` or `Status:` reads as a form field, and the reader takes it as the report's own voice. Drop the label and keep the sentence. The gate flags the label, not the claim.

## Thresholds and why each one is hard or a warning

- Hard (exit 1): a paragraph over 180 words, an internal section ID (`S<d>.<d>`), a process word (BRIEFING, Lead check, subagent, `wave N`), a pasted label line, a second level-1 title, and no status line in the first 1200 characters naming a check that did not run.
- Warning (exit 0): a sentence over 40 words, and list density above 25 bullets per 1000 words once there are at least 12 bullets. Long sentences are often correct in a technical report, so the writer decides; a warning keeps the count visible without blocking delivery.
- The 250 to 800 budget range in `check_plan.py` came from the study-guide gate. Confirm it against `references/depth-tiers.md` before relying on it for a Deep run.

## Test the plan gate against the blank template

Run `check_plan.py` on `templates/template-plano-secao.md` before anything else. It must fail with the unedited-template message. A placeholder check that passes the blank template is not catching the template's own shape.

## Vocabulary in gate code and messages

The gate scripts follow the repo's word rules: no `card` or `cards` (use `entry`), and `dispatch` or `kanban` only on lines that start with `Hermes`. Use `start` where a process would say dispatch.
