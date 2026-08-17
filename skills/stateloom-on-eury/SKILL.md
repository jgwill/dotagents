---
name: stateloom-on-eury
description: >
  Use when a state machine, a board, or a session's behaviour needs to be modelled, drawn,
  validated or generated into code on Eury — and when asking "what does the loom run here",
  "is stateloom up", "quel port", "the canvas is frozen", "the board never moves", "MCP 401",
  "how do I open the board from ilex". Also use when a Claude Code session transcript must be
  turned into something inspectable: "what states did that session pass through", "map the
  events of that session", "understand the ATELIER fork", "modélise la session". Covers the
  containerised deployment, its memory ceiling, its boot behaviour, and the transcript→SMDF path.
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

An agent is handed this door with the episode's own config:

```bash
claude --mcp-config /srv/miadi/episodes/miadi-chronicle/2026-08-16-episode-333-the-fork-arrives-launched-not-handed-over/etc/mcp-config-stateloom-ep333.json
```

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

The nine `@miadi/stateloom-skills` skills are installed in
`stateloom-surface/.claude/skills/` — `stateloom-design`, `-codegen`, `-render`, `-rispec`,
`-live-loop`, `-setup`, `-service`, `-tailnet`, `-docker`. Read those for depth; this file is
only what is true *on this host*.

## Turning a session into a state machine

The reason this is deployed. A Claude Code transcript is 10k+ JSONL lines nobody reads; the
same session as a validated machine is 18 states and 115 transitions you can look at.

```bash
~/.agents/skills/stateloom-on-eury/session-to-smdf.py \
    ~/.claude/projects/<project>/<session-id>.jsonl \
    --name MySession --namespace Miadi.Session \
    -o /home/gmusic/salix/repos/stateloom-surface/looms/my-session.smdf.json
```

Pass **several transcripts in chronological order** to model a fork lineage as one machine —
forks share a history, and the interesting motion is usually across the seam, not inside one
file. Then `set_project_file /data/my-session.smdf.json`, `validate_definition`, and hand the
human the canvas URL.

States are the agent's operating mode (`Executing`, `Reading`, `Writing`, `Delegating`,
`Constrained`, `AwaitingHuman`); events are the calls and interruptions that moved it; every
transition carries its observed count. Nothing is invented — an unrecognised tool becomes its
own state rather than being folded into a bucket that hides it.

**Built and standing:** `/data/ep333/salix/ava002-lineage.smdf.json` — the ATELIER-jamai-demain lineage
(`ava002-fork-pane--ATELIER-jamai-demain--creator-of-opus014-by-william-for-rise-framework`,
forked into tmux `rise-ava002`, session `38c66d28`), five transcripts, 13,681 lines → 18
states, 34 events, 115 transitions, validator clean. `Constrained` — hook fires — was entered
**212 times**, the single loudest signal in that lineage after tool execution itself.
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
