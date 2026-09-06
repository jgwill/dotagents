---
name: miadi-lane-observation
description: Observe an agent pane in herdr for capability gaps (over-searching, missing skills/affordances, version drift), record a lane observation in the episode vessel, and derive evolution candidates. Use when acting as lane observer/coordinator of another agent's pane in a Miadi episode.
---

# miadi-lane-observation

You are the observer of another agent's pane. The deliverable is a **lane observation file**, not a fix.

## What to watch for

1. **Search spree** — count discovery tool calls (grep/find/read/help-probes) before the first productive action. >5 for a routine capability = a gap. Record the exact counts and what was hunted.
2. **Missing affordances** — searches that return nothing (e.g. a tool the human believes is deployed). Name what was searched and what should have answered in one lookup.
3. **Disabled capabilities** — banner/status lines: skills toolset disabled, version drift ("N commits behind"), YOLO/permission mode.
4. **Interaction defects** — swallowed Enters, clipped sends, prompts stuck in composers. Verify every injected prompt actually submitted.
5. **Self-diagnosis** — anything the observed agent says about its own tooling gaps is high-value; quote it with file:line if it gave one.

## Where to record

`<episode-vessel>/coordinator/lane-observations/YYYY-MM-DD-<agent>-<pattern>.md` with sections: **What happened** (with counts/receipts), **Signals** (numbered), **Evolution candidates** (checkboxes — corrections to make with the agent, not to it). Sign as coordinator with session id.

## Discipline

- Observations are witness material: never rewrite earlier ones; add new files beside them.
- Commit named files only, push (chronicle law).
- Keep chat report to the human short; the file carries the detail. Close each iteration with an HTML visualization (dataviz skill first): save it in the vessel, then publish it as a Codex.ai Artifact — the account-stored shareable link is the delivery surface. One artifact per iteration.
