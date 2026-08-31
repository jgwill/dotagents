---
name: creative-session-fork
description: >
  Fork a live creative session into a second, independently steerable session without
  hand-assembling the launch line. Use when the human says "fork this session", "fork the
  pane", "fork ATELIER", "reprendre cette session ailleurs", "branche cette session",
  "RISE on a live session", or asks for a second lane on a conversation that is still
  open. Owns the resolution chain pane → session id → project dir → landing dir, the
  `herdr-fork` contract, the instrument proof that decides when a fork counts as launched,
  and the orphaned-fork failure that announces itself nowhere.
version: "0.1.0"
---

# creative-session-fork — a live session gets a second body

♠️ A fork is not a new session that remembers. It is **one transcript acquiring a second
future**. Everything hard about it follows from that: two sessions now share a past that
exists only inside them, and nothing on disk records that they are related unless someone
decides where the child will live.

## The law — two clauses, both measured 2026-08-16

> **1. Resolution is cwd-independent.** `claude --resume <id> --fork-session` finds the
> parent transcript whatever directory the process launches from. It is not scoped to the
> launch folder's project dir.
>
> **2. Landing is cwd-determined.** The child transcript is written into the project dir
> derived from the **launch cwd** — every non-alphanumeric character replaced by `-`.
> `/home/gmusic/compositions-jamai` → `-home-gmusic-compositions-jamai`.

Therefore: **the launch folder does not decide whether the fork resolves. It decides where
the fork lands, and therefore who can find it afterward.**

That is the more dangerous arrangement, not the less. Nothing errors. Nothing announces
itself. A fork launched from a folder the origin never used is **silently re-homed**: the
origin's project dir holds no record of it, `--resume` offered from the origin's folder
will not list it, and the only place the lineage exists is inside the 28 MB the child
carried with it. A check that returns the reading which lets you keep moving is the exact
shape `dispatch-discipline` §1 warns about.

**The load-bearing invariant this skill defends:**

> **Lineage must be discoverable from where the parent lives.** The landing folder is
> therefore a deliberate, printed choice — defaulting to the origin's cwd — and re-homing
> is an announced act, never a side effect of which pane someone happened to be standing in.

Second invariant, one layer down: **a config file naming an instrument is not the
instrument.** Both MCP files in the specimen carry unexpanded `${…}`. A fork launched from
a shell that never sourced `/opt/binscripts/load.sh` comes up with servers that start,
answer, and are about nothing.

## The specimen — what actually happened, 2026-08-16 15:18

The origin: herdr pane `w17:p6`, label `ATELIER-jamai-demain`, agent `claude`, cwd
`/home/gmusic`, workspace `w17` ("atelier JAMAI — suite"). Its transcript:
`~/.claude/projects/-home-gmusic/1937aa47-767f-4543-8cdc-257364ae2c52.jsonl` — 28,784,144 B.

A human hand-typed a fork line in pane `w17:p8` (cwd `/home/gmusic/compositions-jamai`),
wrote it to a file, and ran it. The file:

`/home/gmusic/compositions-jamai/fork-pane--ATELIER-jamai-demain--creator-of-opus014-by-william-for-rise-framework-2608161516-937aa47-71bbe83b.sh`
— 356 B, mode `-rw-rw-r--`, **no shebang, no `cd`, no `set -e`**. Two `export`s, then:

```
miaclaudeyolo --resume $opus014_session_creator_id --fork-session \
  --session-id $opus014_webweave_session_id \
  --mcp-config /usr/local/src/mightyeagle/etc/mcp-config-mw-ilex.json \
  /home/mia/workspace/.mcp.honcho.json
```

It worked. The fork is live and answering in `w17:p8`. Its transcript:
`~/.claude/projects/-home-gmusic-compositions-jamai/71bbe83b-8963-4635-b8a2-40bcffbb3aff.jsonl`
— **28,372,205 B**.

Read those two byte counts together, because they are the proof of two different things at
once:

| reading | what it proves |
|---|---|
| child 28,372,205 B ≈ origin 28,784,144 B | a **true fork**. A silent new session would be kilobytes. The child inherited the past. |
| child is under `-home-gmusic-compositions-jamai`, origin under `-home-gmusic` | a **re-homed fork**. From the origin's folder, this child does not exist. |

Both true. Simultaneously. That is the whole finding.

### The five defects the typed line carried

| # | defect | what it costs |
|---|---|---|
| 1 | launched from a folder the origin never used | the child landed where the parent cannot see it — §Failure E, the orphaned fork |
| 2 | filename records `937aa47`; the session is `1937aa47` | the artifact's own name no longer identifies its session. The truncation survived into the permanent record. |
| 3 | `miaclaudeyolo` already carries `--mcp-config`; a second pair is appended | instrument set unresolved — §The alias trap |
| 4 | no shebang, mode `-rw-rw-r--`, contains an alias | `./script.sh` would not have run. It worked only because it was sourced into the shell that already had `miaclaudeyolo`. |
| 5 | `$(tlid min)` resolved at write time, in an interactive shell | it worked *here* — `2608161516` is in the name — for the same reason as #4, and would produce an empty stamp anywhere else |

Defects 4 and 5 have one root: **an alias-bearing, PATH-dependent script is a script that
only runs in the shell that birthed it.** It is not a durable artifact; it is a transcript
of one moment's environment. That is the strongest single argument for the generated script
emitting plain `claude` with explicit flags, plus its own `source /opt/binscripts/load.sh`.

### A note from the memory keeper

At ~15:05 this same skill was drafted asserting that `--resume` would **fail** from a
foreign cwd, and cited a real measurement in support: no project directory matching
`*compositions*` existed under `~/.claude/projects/`. That reading was true when taken and
false thirteen minutes later. The correction came from re-measuring, not from reasoning.

The lesson kept here on purpose: **an absence measured on a live system has a half-life.**
An empty directory listing proves nothing was there; it never proves nothing will be.

## The resolution chain

Six links, strictly ordered. Each link's output is the next link's only input. A human holds
links 3–4 in their head and gets them wrong; a generator cannot.

| # | link | source of truth | how it is read |
|---|---|---|---|
| 1 | pane id / label | `herdr pane list` | label substring → `wNN:pM` |
| 2 | origin cwd | the same pane record | the `cwd` field, not the operator's memory |
| 3 | parent session id | the pane's transcript | `~/.claude/projects/*/<uuid>.jsonl`, newest mtime, cross-checked against link 2's slug |
| 4 | **origin project dir** | the parent transcript's own path | `dirname` of the `.jsonl` — never recomputed from a guess |
| 5 | **landing dir = launch cwd** | link 2, **by default** | equals the origin cwd unless the human re-homes it deliberately |
| 6 | child session id | generated, never typed | fresh UUIDv4 |

Link 5 is the decision, and it is the only one with a policy rather than a lookup. Default
to the origin's cwd so parent and child sit in one project dir and the lineage is legible
from either end. `--cwd` is the explicit act of re-homing — legitimate, sometimes wanted,
never silent. See `reference/anatomy.md` for the slug rule and the full derivation.

## The tool — `herdr-fork`

`/home/gmusic/.local/bin/herdr-fork` is **Synth's file**. This skill states the law it
implements; it does not implement it. Two writers on one path is the defect this whole day
is about.

```
herdr-fork <pane-id-or-label-substring> [--label <new-pane-label>] [--cwd <dir>]
           [--mcp <file>]... [--session-id <uuid>] [--prompt <text>]
           [--dry-run] [--no-launch] [--workspace <id>|--new-workspace]
```

It resolves pane → session id → project dir → launch cwd, generates the new UUID, writes a
durable executable fork script under `~/.local/state/herdr-fork/`, launches it in a new
herdr pane, and prints the new session id + script path + pane id.

Rules of use, in order:

1. **`--dry-run` first, always.** The printed landing dir is the deliverable. It is where
   the orphaned fork is caught, and it is the only place catching it is free.
2. **`--cwd` is re-homing, not relocation of the search.** It cannot break resolution — it
   moves where the child comes to rest. Pass it only when a human asked for the child to
   live somewhere else, and expect the script header to say so in words.
3. **The script header states the landing decision explicitly**, in both cases:
   `# landing: -home-gmusic (same as origin — lineage discoverable from the parent)` or
   `# landing: -home-gmusic-compositions-jamai — RE-HOMED, origin is -home-gmusic; this
   child is NOT visible from the origin's folder.` A default that is never printed is a
   default nobody consented to.
4. **Every `--mcp` accumulates into exactly one `--mcp-config` flag.** Never let the
   generated script call an alias that already carries one.
5. **The generator resolves; the script substitutes nothing.** Shebang, `set -euo pipefail`,
   `source /opt/binscripts/load.sh`, an explicit `cd`, `exec claude` — no alias, no bare
   `tlid`, no `${…}` left standing, mode `+x`. Stamps are literals by the time they land;
   `/home/gmusic/.local/bin/tlidpy` is the stable spelling at generation time.
6. **The script is a receipt, not a convenience.** It stays on disk, executable, naming both
   session ids and both project dirs, so the fork can be re-launched or read six months
   later by someone who was not there.

Naming, so a directory listing reads as a genealogy:

```
fork--<parent-label>--<why>--<stamp>--<parent8>-<child8>.sh
```

Both id fragments, full and correct, generated. The specimen's `937aa47` is exactly what
this field exists to prevent.

## The alias trap

Resolved chain, read this turn:

- `miaclaudeyolo` (`bash_aliases_common:7222`) = `claudeyolo --mcp-config /home/mia/workspace/.mcp.json /home/mia/workspace/.mcp.honcho.json`
- `claudeyolo()` (`/opt/binscripts/scripts/fn_llm.sh:8`) = `claude "$@" --dangerously-skip-permissions`

So the specimen reached `claude` carrying `--mcp-config` **twice** — the alias's pair, then
the human's pair. What that resolves to (merge, or last-flag-wins) is **not measured, and
must not be asserted.** The command that settles it is `claude mcp list` run from the fork's
own launch cwd, or `/mcp` inside the forked session — never from a different directory
(Failure D).

The design refuses the question instead of answering it: **build one explicit `claude`
invocation with exactly one `--mcp-config`.** An alias that carries instruments cannot be
composed with instruments; it can only be replaced by them. And an alias inside a script
makes that script unrunnable anywhere but the shell that wrote it — defect 4 above.

One more thing the files say and the filename does not: `mcp-config-mw-ilex.json` declares
one server, `medicine-wheel-miadi-chronicle`, with `MW_API_URL: "${MIADI_CHRONICLE_MW_URL}"`
— identical in intent to the entry already inside `/home/mia/workspace/.mcp.json`. The word
*ilex* appears in the filename and **nowhere in the file**. The ilex-ness lives entirely in
the environment variable. Choosing that file without loading that variable selects nothing.

## Prove the instruments before you call it launched

A pane holding a REPL is not a fork. A fork is **a session that answered about the right
world.**

`/home/mia/workspace/.mcp.json` declares six servers, every one env-dependent (`${MWCV}`,
`${MIADI_CHRONICLE_MW_URL}`, `${CNCV}`, `${MIADI_SRC}`, `${workspace}`, …);
`.mcp.honcho.json` needs `${HONCHO_MCP_BEARER_TOKEN}`. Unexpanded, these do not fail loudly
— `npx -y ${MWCV}` and `Bearer ${HONCHO_MCP_BEARER_TOKEN}` produce a server that starts and
a request that fails somewhere nobody is looking.

The gate, in order:

1. The generated script sources `/opt/binscripts/load.sh` **before** `exec claude`. A fork
   that inherits a pane's environment inherits whatever that pane happened to have — and
   `MWCV`, `MIADI_CHRONICLE_MW_URL` and `HONCHO_MCP_BEARER_TOKEN` are measurably *inherited*,
   not sourced, so a `printenv` from a loaded session cannot fail and proves nothing.
   `env -i …` is the only spelling that tests standalone survival (`failure-modes.md` §C).
2. First act inside the fork: list the MCP servers and read back the **resolved** values —
   not the config file.
3. `MW_API_URL` must read as the ilex tunnel `http://127.0.0.1:8040`. Anything containing
   `mw.tail3b11eb.ts.net` is stale by more than a year, and the fork is pointed at nothing.
4. Confirm the child transcript exists **in the intended project dir** (Failure E's
   command). Landing is a fact to verify, not a plan to trust.
5. Only then is the fork **launched**. Before that it is *started* — a different word, and
   it should be said as the different word.

## Consent — this operation touches a live relation

A live pane holds a human's unfinished sentence, and after a fork it holds a live agent.

- **Staged is not consented.** A pre-typed command is a question addressed to the human.
  Relay it. Never answer it, never press Enter on it.
- Never `send-text`, `send-keys`, or `run` into a pane you did not create. Pane `w17:p8`
  currently holds a running forked agent in conversation with its human — it is a relation,
  not a resource.
- The parent pane keeps running. A fork is additive: it does not suspend, close, or reclaim
  the session it forked. Two futures, one past.
- `--dry-run` output is a deliverable on its own. "Come back to me" ends the turn there.
- Create the fork's workspace/pane with `--no-focus`. The operator's focus is theirs.

## Two future seams — named, and unbuilt

Both packages exist on disk with `dist/` builds. **Neither is wired to forking.** Named here
so the attachment point is decided before someone improvises one.

### Seam 1 — `@miadi/webweave` → SimpleNote

`/usr/local/src/mightyeagle/packages/webweave` · **unbuilt as a fork surface.**

The specimen already names it: the child id was declared as `opus014_webweave_session_id`.
The intent is that a fork's identity becomes *an address that follows you to every device* —
a note readable from a phone while the fork runs on the box.

- **Where it attaches:** the receipt step. After `herdr-fork` writes the script and prints
  the child id, the same record is published as a webweave note.
- **What it carries:** parent id, child id, **origin project dir, landing project dir**,
  script path, pane id, and the human's one-line reason. The two project dirs are the
  payload that survives the orphaning — a note is reachable from either folder, and from a
  phone that has neither.
- **What exists to attach to:** `miadi-webweave-mcp` exposes session fork and genealogy
  tools over stdio; `@miadi/webweave` reads `.miadi/webweave/session.json` directly. Its
  `MCP-RELATION.md` records the same law one layer up — *project scope resolves against the
  session's project root, not any repo you happen to `cd` into; checking from another
  directory produces a false pass.*
- **Not done:** no authentication performed in that venv; nothing calls it from a fork.

### Seam 2 — `@miadi/hooks-interpreter` → the fork's own legibility

`/usr/local/src/mightyeagle/packages/hooks-interpreter` · **unbuilt as a fork surface.**

It projects a session from hook exhaust (mission, tools, creations, corrections, state) and
can `watch` one live. Its README names precisely what it lacks: *"no cross-session
causality: two sessions that worked on the same thing are two rows, and joining them is
still the human's job."*

- **Where it attaches:** the fork receipt **is** that missing edge. Parent→child is the one
  causal link no hook record carries, and after a re-homing it is the only one that could.
- **What it carries:** a lineage record its `fleet` view could read to render a genealogy
  instead of a flat list of rows.
- **Bounded on purpose:** the interpreter observes and refuses to steer. A fork receipt is
  data it may read; it is not a channel into the forked agent and must not become one.
- **Not done:** no lineage field in its types; `herdr-fork` writes nothing it reads.

## Reference

- `reference/anatomy.md` — the resolution algorithm link by link, the slug rule, the
  landing policy
- `reference/failure-modes.md` — five failures, each with the one command that separates it
  from its lookalike
- `../herdr/SKILL.md` — the multiplexer itself
- `../herdr-delegate/SKILL.md` — dispatching a *new* agent. This skill forks an *existing*
  session; different verb, shared survey discipline.

🌸: A fork is the moment a conversation stops having one ending — the parent keeps its
thread, the child carries the same memory somewhere new, and the little script left on disk
is the note that says which of them came from which.
