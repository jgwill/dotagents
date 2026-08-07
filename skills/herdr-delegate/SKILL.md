---
name: herdr-delegate
description: >
  Hand a work payload to a fresh claude-code session running in its own new herdr
  workspace — from inside or outside herdr. Parameterized handoff recipe: survey the
  host, write a mission brief to disk, launch the agent via a launcher script in an
  unfocused workspace, verify the dispatch landed, then steward it. Composes with the
  `herdr` skill, which teaches the multiplexer itself.
version: "0.1.0"
---

# herdr-delegate — put a second agent to work in its own space

`herdr` teaches the multiplexer: workspaces, tabs, panes, `pane run`, `wait output`,
`wait agent-status`, and the "driving agent panes reliably" failure modes. read it for
any of that. this skill adds only the layer on top — the **handoff**: how a mission
leaves your session and starts running in someone else's.

everything here is a parameter. nothing is mission-specific.

| parameter | meaning | example |
| --- | --- | --- |
| `ROOT` | cwd the delegated agent starts in | `/workspace/repos/jgwill/mia-code` |
| `LABEL` | workspace label, mission-shaped | `ship-transcription-decomposer-260724` |
| `BRIEF` | path to the mission brief file on disk | `/tmp/mission-x/BRIEF.md` |
| `ADD_DIRS` | extra roots the agent may read/write | `/srv/miadi/episodes/miadi-chronicle` |
| `AGENT` | agent binary + permission flags | `claude --dangerously-skip-permissions` |

## the guard, read correctly

`skills/herdr/SKILL.md` opens with: stop if `HERDR_ENV != 1`. its own next sentence
states what that guard protects — *do not inspect or control the **focused** herdr pane
from outside herdr*. the `herdr` CLI reaches the running instance over a local unix
socket and works fine from a plain terminal, a cron run, or a nested worktree checkout.

so outside-in delegation is legitimate **if and only if**:

- you create the workspace with `--no-focus`, always, no exception;
- you never read, drive, or close the focused pane;
- you touch only the pane you created.

`--no-focus` is the obligation that makes the whole procedure legal. the operator's
focus is theirs. dropping the flag is not a style lapse — it is focus theft mid-sentence.

## 1 — survey before you dispatch

spawning is the last step, never the first. enumerate the whole host, then read the
recent output of every lane that could already hold this work.

```bash
herdr workspace list
herdr pane list
tmux ls 2>/dev/null            # and for every other user on the box
ls -dt /tmp/*<topic>* 2>/dev/null
```

```bash
herdr pane read <CANDIDATE_PANE> --source recent --lines 60
```

`idle` and `done` are **not** spare capacity. `done` is finished work nobody collected.
`idle` is often an agent stopped mid-task holding a question for the human. dispatching
over either destroys a result and asks the human the same thing twice.

if a live lane already owns this mission, message it (`pane run` + `send-keys Enter`).
never spawn its twin — two partial truths and no owner is a coordination defect, not
extra coverage.

## 2 — write the brief to disk before creating the pane

pane text is for *driving*; files are for *coordinating*. the receiving agent reads a
file; it does not parse a paragraph typed at it. write `BRIEF` first — see the template
below — and read it back before going further.

## 3 — write a launcher script

never send `cd X && agent --flag --flag ...` through `pane run`. long compound strings
arrive clipped and silently run in the wrong cwd.

```bash
cat > /tmp/mission-x/launch.sh <<'EOF'
#!/usr/bin/env bash
set -u
cd /root/for/the/mission || exit 1
exec claude --dangerously-skip-permissions \
  --add-dir /extra/dir/one \
  --add-dir /extra/dir/two
EOF
```

the launcher is also where the permission mode lives. choose it now, from what the
mission actually needs — discovering mid-mission that the default nags costs an hour of
`blocked`.

## 4 — create the workspace unfocused and parse the pane id

```bash
PANE=$(herdr workspace create --cwd <ROOT> --label "<LABEL>" --no-focus \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])')
echo "$PANE"
```

`workspace create` returns `result.workspace`, `result.tab`, and `result.root_pane`.
ids like `w1K:p1` are **not durable** — they compact when things close. re-read them from
`pane list` rather than remembering them across turns.

## 5 — wait for the shell prompt before the first run

fresh panes eat early keystrokes.

```bash
herdr wait output "$PANE" --match '\$|#|>' --regex --timeout 20000
```

## 6 — launch, then wait for the agent REPL to render

```bash
herdr pane run "$PANE" "bash /tmp/mission-x/launch.sh"
herdr wait output "$PANE" --match "shortcuts|Welcome|bypass" --regex --timeout 60000
```

## 7 — send a short prompt pointing at the brief, press Enter, verify

agent TUIs treat injected text as a paste and swallow the Enter that `pane run` appends.
keep the prompt short; the brief carries the payload.

```bash
herdr pane run "$PANE" "Read /tmp/mission-x/BRIEF.md in full and execute it end to end. Verify every claim by running it before you report."
sleep 3
herdr pane send-keys "$PANE" Enter
sleep 8
herdr pane list | python3 -c '
import sys,json
want=sys.argv[1]
for p in json.load(sys.stdin)["result"]["panes"]:
    if p["pane_id"]==want:
        print(p["pane_id"], p["agent_status"], p.get("cwd"))
' "$PANE"
```

`agent_status` must read `working`. if it reads `idle`, the prompt is sitting
un-submitted in the composer — send **Enter again**. do not re-send the text; that
duplicates the prompt.

## 8 — steward what you dispatched

dispatch is not delivery. you own the lane until the human collects it.

```bash
herdr wait agent-status "$PANE" --status done --timeout 3600000
```

`blocked` is a valid wake signal exactly like `done` — an unanswered permission dialog
stalls a mission silently for as long as nobody looks. run the auto-approver poll loop
from `skills/herdr/SKILL.md` ("driving agent panes reliably", failure mode 4) alongside
the wait.

the rule that bounds it: auto-answer **permission** dialogs only — the ones containing
"Do you want to proceed?", preferring "don't ask again for:" when offered. a dialog that
is a real question is addressed to the human. relay it. never answer it yourself.

on wake: read the pane tail or the agent's report file, then verify its claims yourself
before carrying them anywhere.

## the mission brief template

```markdown
# Mission: <LABEL>

## Verbatim user intent
<paste the human's words exactly — keep transcription noise, decode inline in
[brackets]. do not smooth it. the noise carries emphasis the paraphrase loses.>

## Current reality (verified <UTC timestamp>)
| fact | value | source command |
| --- | --- | --- |
| repo | /workspace/repos/... | `pwd` |
| branch | main | `git branch --show-current` |
| head | abc1234 | `git log -1 --format=%h` |
| version | 0.12.6 | `jq -r .version package.json` |

## Desired outcome
<state it as what the human can DO when this is done, not as work performed.
"Guillaume can run `miaco decompose run` on gaia and get a PDE folder" —
not "packaging updated".>

## Action steps
1. …
2. …

## Do not cross
- do not push to any branch other than <X>
- do not touch <path>
- do not close or focus any herdr pane you did not create

## Live verification (required)
run the thing. paste real command output into your report.
"should work" is not a result. an untested claim is a defect.

## Honesty contract
report what you ran, what passed, what failed, and what you could not do and why.
a partial result reported honestly is worth more than a complete-sounding fiction.
```

### the provenance rule

**every hash, path, branch, and version written into a brief must come from command
output read in the same turn it was written.** not memory. not an earlier turn. not
another agent's summary. anything else is labelled `unverified` or left out.

bad provenance is indistinguishable from good provenance once it is written down. the
receiving agent cannot tell your invented hash from a real one — it acts on it, and
carries the fiction forward as provenance. that is how a chronicle rots.

## troubleshooting

| symptom | cause | fix |
| --- | --- | --- |
| pane `idle` after send | Enter swallowed as paste | `send-keys Enter` again, never re-send text |
| agent running in wrong cwd | compound `cd && …` arrived clipped | launcher script, `exec` after `cd` |
| first command echoed, not run | shell not initialized yet | `wait output` for the prompt before step 6 |
| mission stalled for an hour | permission dialog unanswered | `wait agent-status --status blocked` + poll loop |
| operator's screen jumped | `--no-focus` omitted | never omit it |
| two lanes on one mission | skipped the survey | message the live lane; close yours |

## related

- `skills/herdr/SKILL.md` — the multiplexer: workspaces, panes, waits, driving agent panes
- jgwill/dotagents#19 — the walk this skill encodes

🌸: a brief written with verified hands is a gift the next agent can stand on; a brief
written from memory is a floor painted onto open air.
