---
name: stateloom-on-eury
description: >
  Use when a state machine or board must be modelled, drawn, validated or generated into code
  on Eury — and when asking "what does the loom run here", "is stateloom up", "quel port",
  "the canvas is frozen", "the board never moves", "MCP 401", "how do I open the board from
  ilex". Also use when deciding at which ALTITUDE to model a session — a meaning board a human
  and an agent can converse with, versus a mechanics board that measures the agent loop — and
  before generating either. Covers the containerised deployment, its memory ceiling, its boot
  behaviour, the two-layer rule, and what a transcript can and cannot tell you.
---

# The loom on Eury

Four processes in one container image behind **one port**, holding `.smdf.json` state machines
that an agent edits over MCP and a human edits in a browser — **the same document, live, both
directions**. Deployed 2026-08-16, replacing a hand-rolled three-terminal stack.

```
   http://127.0.0.1:4598        loopback — agents on Eury, curl
   http://100.88.23.103:4598    tailnet  — ilex · ginkgo · larix · tilia · abies
        └─ gateway :8080
             ├── /socket.io/*  → hub    :4599   sequencer, never writes disk
             ├── /mcp          → mcp    :4600   your door, bearer-token guarded
             └── everything    → canvas :4598   the human's board
```

**Documents live in `/home/gmusic/salix/repos/stateloom-surface/looms/`**, which is the
container's `/data` — the only readable/writable root. Address them the way the *server* sees
them: `/data/<name>.smdf.json`. A host path is refused, not followed.

### Chronicle episodes are mounted, not copied

Episode 333 is a second document root at **`/data/ep333`**, served from where it lives so there
is one file and no divergence. A board there is addressed `/data/ep333/salix/<name>.smdf.json`.

The write boundary is the **filesystem's**, not a convention: the loom runs as `gmusic`, so it
writes `salix/` — this account's drop lane — and only *reads* the `mia`-owned boards beside it.
DROP-ONLY enforced rather than recalled. Mount another episode by adding a volume next to the
existing one in `.stateloom/docker-compose.yml`; never by copying documents into `looms/`.

An agent is handed this door with:

```bash
claude --mcp-config /home/gmusic/.mcp.stateloom.json
```

That file lives in `$HOME` (mode 600) and **not** in any repository on purpose — the episodes
tree has a remote, and a bearer token committed there is a token published. Regenerate it after
a rotation with the episode's `etc/stateloom-mcp-config.sh`, which reads the live token from
`.stateloom/.env` and carries none itself.

## It is already running

Nothing to start. `restart: unless-stopped` on all four containers plus `docker.service`
enabled means the loom returns by itself after a reboot or a crash. **Check before you act:**

```bash
curl -sS http://127.0.0.1:4598/healthz
# {"ok":true,"gateway":true,"upstreams":{"canvas":true,"hub":true,"mcp":true}}
```

If that answers, do not run `docker up`, do not "restart to be safe" — the hub holds every
peer's live room. Only if `healthz` fails:

```bash
cd /home/gmusic/salix/repos/stateloom-surface
docker compose -p stateloom -f .stateloom/docker-compose.yml --env-file .stateloom/.env up -d
```

**Use `docker compose` directly, never `npm run up`.** That npm script calls
`stateloom docker up`, which **regenerates `.stateloom/docker-compose.yml` and silently drops
both local edits**: the tailnet port mapping and the memory ceilings below. If someone runs it,
restore both and re-apply with the command above.

## Memory ceiling — why it is there

Eury runs 31Gi with **both swapfiles saturated**. An unbounded container competes with the
agent fleet for the last free gigabyte, and the OOM killer picks whichever victim is cheapest
— usually somebody's live session, not the runaway.

| service | cap | measured idle | swap |
|---|---|---|---|
| hub | 256m | ~19 MiB | denied |
| mcp | 256m | ~30 MiB | denied |
| canvas | 512m | ~42 MiB | denied |
| gateway | 256m | ~14 MiB | denied |

`memswap_limit == mem_limit` denies swap entirely: the container fails loudly inside its own
cgroup instead of dragging the host down. Total hard ceiling **1.25 GiB**, ~8% used at rest.
Raise a cap with `STATELOOM_MEM` / `STATELOOM_MEM_CANVAS` in `.stateloom/.env` — never by
removing the limit.

```bash
docker stats --no-stream $(docker ps -q -f name=stateloom)
```

## What you can do with it

Register the MCP server from `/home/gmusic/salix/repos/etc/mcp-config-stateloom.json`
(HTTP + bearer, port **4598** — 4597 was the retired stack). Recover it any time:

```bash
npx -y @miadi/stateloom-skills@latest docker mcp-config
```

| want | do |
|---|---|
| build / edit a machine | `create_state_machine`, `add_state`, `add_event`, `add_transition`, `remove_state` |
| switch board | `set_project_file /data/<name>.smdf.json` — server path, never a host path |
| check it holds | `validate_definition` — V001–V014 |
| draw it | `render_diagram` → PNG, SVG, Mermaid, ASCII |
| generate code | `generate_code` → Python / TypeScript |
| write a spec | `generate_rispec` → a RISE markdown document |
| give the human a board | `http://100.88.23.103:4598/?doc=/data/<name>.smdf.json` |

`?doc=` is **per-viewer** — measured: fetching it returns 200 and leaves `/api/config`'s
`projectFile` unchanged, so two people handed two links do not repoint each other's board.

The nine `@miadi/stateloom-skills` skills are installed in
`stateloom-surface/.claude/skills/` — `stateloom-design`, `-codegen`, `-render`, `-rispec`,
`-live-loop`, `-setup`, `-service`, `-tailnet`, `-docker`. Read those for depth; this file is
only what is true *on this host*.

## Two layers, never merged

A board is built at one of **two altitudes**, and handing someone the wrong one is the failure
this section exists to prevent.

| | **meaning** | **mechanics** |
|---|---|---|
| states | `CURRENT REALITY` → `Action step N` → `DESIRED OUTCOME` | `Deliberating`, `Executing`, `Composing`, `AwaitingHuman` |
| events | `tension_established`, `owner_consented`, `moment_of_truth` | `Call_Bash`, `TurnEnded`, `ToolReturned` |
| answers | what was the work becoming, and what moved it | what the loop did, and how much of it |
| engine | an **LLM read pass**, then the human corrects it on the canvas | `session-to-smdf.py`, mechanically |
| reads | the human's turns, the commit bodies, the issue text | the raw JSONL |
| file | `<name>.smdf.json` | `<name>-mechanics.smdf.json` |

**A mechanical extractor cannot produce a meaning board, and no amount of fixing will change
that.** The tool sequence `Read · Edit · Bash · Bash` implements *"raise the contrast floor"*
and *"delete the feature"* identically. Intent was never encoded in tool names, so it cannot be
recovered from them — and a diagram whose shape is the same for every session on this host
carries no information about any session.

The meaning board's cheap, accurate input is **not** the raw transcript. In order: the human's
turns (a few hundred lines, the whole intent spine), the commit bodies and issue text for
whatever repo was touched — which usually already contain the state names nearly verbatim —
and only then the assistant's text-only turns. Never the tool calls.

Then the human drags a state name on the canvas and the agent sees it change. That
bidirectionality is the loom's entire reason to exist, and a board generated from tool names
has nothing in it a human would want to rename.

Model the meaning board on `WitnessedCapture` (`/data/ep333/pane-capture-witnessed.smdf.json`)
— the house pattern, a structural tension chart wearing a state machine's clothes, with
`condition` guards on the transitions that need a human's word.

### The mechanics layer — what it is honestly for

```bash
~/.agents/skills/stateloom-on-eury/session-to-smdf.py \
    ~/.claude/projects/<project>/<session-id>.jsonl \
    --name MySession --namespace Miadi.SessionMechanics \
    -o <episode>/salix/my-session-mechanics.smdf.json
```

Several transcripts may be passed in chronological order; each file boundary emits an explicit
`TranscriptBoundary` event rather than flowing one file's last state into the next file's first
— **a fork seam is a discontinuity, and drawing it as continuous invents transitions.**

States are the agent's operating mode, events are its calls, and every transition carries its
observed count. What that is good for: volume, distribution, and where a loop actually spent
itself. What it is not: an account of the work.

**Read the counts before believing them.** Every state on a mechanics board is an inference
this script makes, not a label the transcript carries — so a state name can be wrong even when
the arithmetic is right. Two that were, and were fixed:

- Thinking-only records were counted as `Answered → AwaitingHuman`, which made "waiting for the
  human" the largest state on the board *while the agent was thinking*. Thinking is now
  `Thought → Deliberating`, and `AwaitingHuman` is entered only at a real turn boundary.
- `stop_hook_summary` fires **once per turn** and means nothing happened. Reading it as a hook
  fire turned the turn count into a false finding about friction. `Constrained` is now entered
  only when a record actually carries `hookErrors` or `preventedContinuation`.

**Built and standing:** `/data/ep333/salix/ava002-mechanics.smdf.json` — five transcripts of
the **`compositions-jamai`** lane (where the ATELIER fork ran; tmux `rise-ava002`, session
`38c66d28`), 13,692 lines → 19 states, 35 events, 128 transitions, validator clean. Top
states: `Deliberating` 1400, `Executing` 1311, `Composing` 616, `Interpreting` 248,
`AwaitingHuman` 215. There is no `Constrained` state — across all 13,692 lines, **zero**
records carried `hookErrors` or `preventedContinuation`.

**A board names the lane it measured, and no other.** That one says nothing about
`/workspace/repos/miadisabelle/gmtermux/`: those sessions ran under another identity on another
host, and no transcript for them exists on Eury. A transcript-based engine cannot reach a day
it has no transcript for — say that, rather than modelling something adjacent and letting the
filename imply otherwise.

See `creative-session-fork` for how such a fork is made.

## Traps, each one paid for

| Symptom | Cause | Move |
|---|---|---|
| Board renders, never moves | something re-pointed the canvas off same-origin | `curl /api/config` must say `"bridgeUrl":"/"` |
| Skills look refreshed, aren't | the installer **keeps** existing files | re-run with `--force` |
| `npx @miadi/stateloom-skills` runs an old version | it resolved the **local** `node_modules` copy | pin it: `@latest` or an explicit version |
| Tailnet mapping / memory caps vanished | someone ran `stateloom docker up` | restore both edits in the compose, re-apply |
| MCP 401 with the right-looking token | container re-minted it | `docker mcp-config`, update the config file |
| Two editors, neither sees the other | a host-native loom shares `looms/` | **one loom per directory** — never both |
| Canvas link opens the wrong board | `STATELOOM_CANVAS_URL` unset | it is set to the tailnet origin; keep it that way |
| `render_diagram` → `EACCES` | it writes **beside the document**, and the episode root is `mia`-owned | pass `path` into the writable lane: `/data/ep333/salix/<name>.<ext>` — reading someone's board does not grant writing next to it |

Logs before guessing:

```bash
docker compose -p stateloom -f /home/gmusic/salix/repos/stateloom-surface/.stateloom/docker-compose.yml logs --tail 50 <hub|mcp|canvas|gateway>
```

## Where the old shape went

`hub-up.sh`, `mcp-http-up.sh`, `canvas-up.sh` and `canvas.mjs` in `stateloom-surface/` are the
Aug-4 stack and no longer describe anything that runs. Upstream ships their function as the
`stateloom-service`, `-tailnet` and `-docker` skills. Originals, the pre-upgrade document and
the retired panes' final scrollback: `stateloom-surface/.stateloom-legacy-2026-08-16/`;
tarball at `salix/repos/stateloom-surface.BACKUP-2026-08-16.tgz`.
