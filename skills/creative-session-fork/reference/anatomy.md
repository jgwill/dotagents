# Anatomy of a fork — the resolution algorithm

Companion to `../SKILL.md`. This file is the derivation; the skill is the law.

## The two clauses, stated once more because everything here depends on them

Measured 2026-08-16 15:18 on this host, on a fork that ran:

1. **Resolution is cwd-independent.** Session `1937aa47-767f-4543-8cdc-257364ae2c52` lives
   under `~/.claude/projects/-home-gmusic/`. `claude --resume` found it while launched from
   `/home/gmusic/compositions-jamai`. No error, no prompt, no fallback.
2. **Landing is cwd-determined.** The child, `71bbe83b-8963-4635-b8a2-40bcffbb3aff`, was
   written to `~/.claude/projects/-home-gmusic-compositions-jamai/` — the slug of the
   **launch cwd**, not of the parent's folder.

The proof that clause 1 really is resolution and not a silent restart is a byte count:
child 28,372,205 B against origin 28,784,144 B. A fresh session with a supplied
`--session-id` would be kilobytes. The child inherited 28 MB of past.

## The slug rule

A project directory name is the absolute launch cwd with every non-alphanumeric character
replaced by `-`. Verified against directories present on this host:

| launch cwd | project dir |
|---|---|
| `/home/gmusic` | `-home-gmusic` |
| `/home/gmusic/compositions-jamai` | `-home-gmusic-compositions-jamai` |
| `/home/gmusic/workspace/abcjs-jamai` | `-home-gmusic-workspace-abcjs-jamai` |
| `/home/gmusic/workspace/aistudio-<id>/.TermivoxAI` | `…-aistudio-<id>--TermivoxAI` |

The leading `-` is the root slash. The doubled `--` in the last row is `/` followed by `.` —
two separators, two dashes. The transform is **lossy and not invertible**: `-home-gmusic-x`
could be `/home/gmusic/x`, `/home/gmusic-x`, or `/home/gmusic.x`. Never reconstruct a cwd
from a project dir name. Read the cwd from the pane record (`herdr pane list` → `cwd`) and
compute forward.

## The chain, link by link

### 1 — pane

Input: a pane id (`w17:p6`) or a label substring (`ATELIER`).
`herdr pane list` is the only source. Ids compact when panes close; resolve them in the same
turn you use them, never from memory. A label substring matching two panes is an error, not
a coin flip — print both and stop.

### 2 — origin cwd

The same pane record carries `cwd`. Take it from there. An operator's recollection of where a
pane was started is the single most common wrong input to this whole chain, because panes get
`cd`'d and the label does not change.

Note the boundary: `cwd` in the pane record is the *shell's current* directory, which for a
long-lived agent pane is normally still its launch directory but is not guaranteed to be.
The authoritative origin folder is confirmed at link 4, from the transcript's own path.

### 3 — parent session id

Find the transcript: `~/.claude/projects/*/<uuid>.jsonl`, newest mtime, whose directory slug
matches link 2. A live session's file is being appended to continuously, so mtime is a
reliable discriminator among candidates in one folder — and only there.

If two folders both hold a plausible candidate, the pane's `cwd` slug decides. If neither
matches, stop and say so; do not fork a session you could not name.

### 4 — origin project dir

`dirname` of the file found in link 3. **This is the authoritative origin folder** — it is
observed, not derived, and it is the value link 5 defaults from. Recomputing it from the
cwd string is how a trailing slash or a symlink quietly produces a second answer.

Symlinks matter here: the launch cwd is slugged as the process sees it. A pane started
through `/home/gmusic/git/clones/...` (symlink) and one started through
`/home/gmusic/salix/repos/...` (target) produce **two different project dirs for one
directory**. Prefer the spelling the transcript's own path already agrees with.

### 5 — landing dir (the decision)

This is the only link with a policy instead of a lookup.

| case | landing | why |
|---|---|---|
| default | the origin cwd | parent and child share one project dir; `--resume` from either end lists both; lineage needs no external record |
| `--cwd <dir>` given | that dir's slug | deliberate re-homing — the child belongs to another context |

Whichever fires, **print it**, and print the origin project dir beside it. A default that is
never shown is a default nobody consented to. When they differ, the generated script's
header says so in words, because the artifact outlives the terminal that printed it.

Re-homing is legitimate. A fork taken to seed a different project genuinely belongs in that
project's folder. What is not legitimate is re-homing **by accident**, as a byproduct of
which pane the operator happened to be standing in — which is exactly what produced the
specimen.

### 6 — child session id

A fresh UUIDv4, generated. Never typed, never derived from the parent, never reused. Passed
as `--session-id`.

The specimen's filename carries `937aa47` for a session that is `1937aa47` — a one-character
hand-typing loss that survived into the permanent name of the artifact. Generated ids and
generated filenames cannot disagree, because they come from one variable.

## The invocation the generator must emit

Shape, not a script — `herdr-fork` is Synth's file:

```bash
#!/usr/bin/env bash
set -euo pipefail
# origin  : <origin project dir>   session <parent uuid>
# landing : <landing project dir>  session <child uuid>
# [RE-HOMED: this child is NOT visible from the origin's folder.]
source /opt/binscripts/load.sh
cd '<landing cwd>'
exec claude \
  --resume '<parent uuid>' --fork-session --session-id '<child uuid>' \
  --mcp-config <file> [<file>…] \
  --dangerously-skip-permissions
```

Five properties, each answering a measured defect in the specimen:

| property | defect it answers |
|---|---|
| shebang + `chmod +x` | the specimen was `-rw-rw-r--`; `./script.sh` would not have run |
| no alias — plain `claude`, explicit flags | the specimen only ran because it was sourced into the shell holding `miaclaudeyolo` |
| `source /opt/binscripts/load.sh` before `exec` | `${MWCV}`, `${MIADI_CHRONICLE_MW_URL}`, `${HONCHO_MCP_BEARER_TOKEN}` are unexpanded in the config files |
| explicit `cd`, literal path | the specimen had no `cd`; its landing was whatever the caller's shell happened to be |
| exactly one `--mcp-config`, all files after it | the specimen passed the flag twice and the resolution is unmeasured |
| every substitution resolved at generation time | `$(tlid min)` worked once, in an interactive shell, and would produce an empty stamp anywhere else |

`--dangerously-skip-permissions` is `claudeyolo`'s entire contribution
(`/opt/binscripts/scripts/fn_llm.sh:8` — `claude "$@" --dangerously-skip-permissions`). Write
it literally. A permission mode is a decision; it should be readable in the artifact that
carries it, not hidden two alias hops away.

## What the instruments actually are

| file | servers | unexpanded vars |
|---|---|---|
| `/home/mia/workspace/.mcp.json` | 6 — `medicine-wheel-miadi-chronicle`, `stcbot-triage-chart`, `mia-seat-chart`, `stateloom`, `miadi-voice`, `qmd` | `${MWCV}`, `${MIADI_CHRONICLE_MW_URL}`, `${CNCV}`, `${MIADI_MINO_STCBOT_TRIAGE_CHART_MEMORY_PATH}`, `${MIADI_MIA_ARCHITECTURE_SEAT_CHART}`, `${workspace}`, `${MIADI_MINO_STATELOOM_PROJECT_FILE}`, `${STATELOOM_BRIDGE_URL}`, `${MIADI_SRC}`, `${MIADI_API_URL}`, `${MIADI_API_TOKEN_WRITER}`, `${MIADI_CHRONICLE_ROOT}`, `${MIADI_ASSEMBLY_VOICE_AUDIO_DIR}` |
| `/usr/local/src/mightyeagle/etc/mcp-config-mw-ilex.json` | 1 — `medicine-wheel-miadi-chronicle` | `${MWCV}`, `${MIADI_CHRONICLE_MW_URL}` |
| `/home/mia/workspace/.mcp.honcho.json` | 1 — `honcho` (http, `https://honcho.tail3b11eb.ts.net/mcp`) | `${HONCHO_MCP_BEARER_TOKEN}` |

### Measured values, 2026-08-16 — and where they come from

| variable | value | note |
|---|---|---|
| `MWCV` | `@medicine-wheel/mcp@4.6.1` | the npm spec `npx -y ${MWCV}` runs |
| `MIADI_CHRONICLE_MW_URL` | `http://127.0.0.1:8040` | the **ilex tunnel** — the live chronicle wheel |
| `HONCHO_MCP_BEARER_TOKEN` | present, inherited | value deliberately not recorded in this skill |

The gaia docker wheel `mw.tail3b11eb.ts.net` has been **OFFLINE since 2026-07-29**. Any
config, env var, fixture or test still carrying that host is stale by more than a year of
episodes; the chronicle wheel is ilex:8040.

**These three are inherited from the launching process, not sourced by any script.** Measured
the same day: `bash --noprofile --norc -c 'printenv MWCV MIADI_CHRONICLE_MW_URL
HONCHO_MCP_BEARER_TOKEN'` returns all three, exit 0 — stripping rc files does not strip
inheritance. So a script that "works" because its parent was loaded is not a working script;
it is a script that has not yet been scheduled, sshed, containerised, or handed to another
agent. `env -i` is the only spelling that tests it. See `failure-modes.md` §C, and its
sibling §F.

### The one line that makes the instruments impossible to lose

The two mechanisms `env -i` bundles together were split and measured separately:

| context, inheritance stripped | result |
|---|---|
| `load.sh` alone — `env -i … --noprofile --norc`, sourcing `/opt/binscripts/load.sh` | all three **SET** |
| login files alone — `env -i … bash -lc`, no `load.sh` | all three **MISSING** |

> `source /opt/binscripts/load.sh` is **necessary and sufficient** for the three instrument
> variables. A login shell is neither. `#!/bin/bash -l` supplies none of them.

Source of record: `/opt/binscripts/etc/bash_env_common:835` and `:841`, reached through
`load.sh`. The honcho token is declared in `bash_env_common` **and** in `~/.bashrc` — and
`~/.bashrc` is not read by a non-interactive shell, which is precisely the context a
generated fork script runs in. That is why the login-shell column is empty, and why a
shebang cannot substitute for the source line.

So §C stops being a warning to check and becomes a construction rule: one line in the
generated script, and the instrument cannot be lost. Same shape as §F's cure.

Standing caution, the same one this skill records about a measured absence: these are
readings from one moment on one host. `4.6.1` will move. And `bash_env_common:841` reads
`${MIADI_CHRONICLE_MW_URL:-http://127.0.0.1:8040}` — a **default with a fallback, not a
constant**, so the ilex tunnel holds only while nothing upstream overrides it. Re-measure
before acting.

Two structural facts fall straight out of that table.

**The ilex file is not an ilex file.** Its single server entry is the same server, with the
same `MW_API_URL: "${MIADI_CHRONICLE_MW_URL}"`, as the one already inside
`/home/mia/workspace/.mcp.json`. The word *ilex* is in the filename and nowhere in the file.
Selecting it changes which servers are *present*; it does not change which wheel they point
at. That is decided by the environment variable, and the correct value is the ilex tunnel
`http://127.0.0.1:8040`. Anything reading `mw.tail3b11eb.ts.net` is stale — that wheel went
offline 2026-07-29.

**The name `medicine-wheel-miadi-chronicle` appears in two of the three files, and `honcho`
would arrive twice** in the specimen's invocation (once from the alias's pair, once from the
human's). Whether repeated `--mcp-config` merges or the last flag wins is **unmeasured**, so
whether that is a collision or a harmless overwrite is unmeasured too. One `--mcp-config`
with a chosen list of files makes the question unaskable.

## Verifying a fork, in the only order that works

```
1. child transcript exists in the INTENDED project dir      → landing correct
2. child transcript size is within an order of the origin's  → true fork, not a new session
3. MCP servers list, with RESOLVED values                    → instruments real
4. MW_API_URL reads http://127.0.0.1:8040                    → pointed at the live wheel
5. the pane is answering                                     → alive
```

Steps 1 and 2 are on disk and can be checked by anyone from anywhere. Steps 3 and 4 must be
run **from inside the fork**, or from its own launch cwd — checking MCP registration from a
different directory produces a false pass, which is the trap `webweave`'s `MCP-RELATION.md`
already paid for once at a different layer.
