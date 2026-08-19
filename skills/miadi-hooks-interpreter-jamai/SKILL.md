---
name: miadi-hooks-interpreter-jamai
description: >
  Export a JamAI atelier session the way songbird-71bbe83b and
  atelier-jerry-origin-1937aa47 were dropped — run @miadi/hooks-interpreter
  on a session_id, classify the /tmp scratchpad creations off the 30-day
  tmp cleanup, write MANIFEST.tsv, and land the tree under
  /home/gmusic/<meaningful-name>. Use when someone says "export this
  session", "like songbird", "hooks-interpreter on Jerry's session_id",
  "reproduce the atelier drop", or points at .agents/scripts/_env.sh.
  Reusable. First successful run was 1937aa47 on 2026-08-19; the
  script takes any session_id.
version: "0.1.0-draft"
---

# miadi-hooks-interpreter-jamai — get the floor off `/tmp`

A JamAI atelier lives in two places that do not share a fate:

1. **sessiondata** at `/a/src/_sessiondata/<id>/` — the hook exhaust.
   Durable. `@miadi/hooks-interpreter` reads this.
2. **scratchpad** at `/tmp/claude-<uid>/<cwd-slug>/<id>/scratchpad/` —
   the generators, scores, renders, captures. Mode `700` the session
   owner. Subject to `D /tmp 1777 root root 30d`.

The interpreter answers *what the session became*. The scratchpad *is*
what it made. Export both, or the next reader has a projection of a
floor that `/tmp` already swept.

Worked examples:

| drop | session | who |
|---|---|---|
| `/home/gmusic/atelier-jerry-origin-1937aa47` | `1937aa47-767f-4543-8cdc-257364ae2c52` | Jerry, the origin |
| `…/episode-333-…/salix/songbird-71bbe83b` | `71bbe83b-8963-4635-b8a2-40bcffbb3aff` | Guillaume / ava002, the fork |

## When to use

- A `_env.sh` (or a human) names a `session_*_id` and someone wants
  that session referenceable later.
- The live scratchpad is still under `/tmp/claude-*`.
- You are about to compare two atelier sessions (origin vs fork) and
  need both floors in the same shape.

Do **not** use this to commit anything. The drop is a drop.

## The procedure

### 1. Resolve the session id — do not invent it

```bash
# first look
cat /home/gmusic/.agents/scripts/_env.sh
```

On 2026-08-19 that file carried:

- `session_jerry_origin_id` → Jerry's atelier (this skill's first drop)
- `session_fork_ava002_id` → Guillaume's fork (already exported as songbird)
- `session_jamai_william_observer_opus003_metal_id` → a third session,
  observer, not the origin

If several ids are present, **ask which one**, or take the one the
human named ("Jerry's creation that I forked" = origin, not observer).

Confirm the directory exists:

```bash
ls /a/src/_sessiondata/<id>/_claude_user_inputs.jsonl
```

### 2. Project the session before you copy anything

```bash
miadi-hooks-interpret session  <id> --root /a/src/_sessiondata
miadi-hooks-interpret aspects  <id> --root /a/src/_sessiondata
miadi-hooks-interpret agents   <id> --root /a/src/_sessiondata
miadi-hooks-interpret ceremony <id> --root /a/src/_sessiondata
```

`--json` on each, keep both text and json. These go in `00-interpreter/`.

Read the projection. Two numbers decide the rest of the night:

- `created N path(s)` — the Write/Edit list. Usually ~20. **Not** the
  opus. The 500 Bash calls that ran `abc2midi` / `fluidsynth` /
  `ffmpeg` after each generator are invisible here.
- the first scratchpad path in `created` — that is the floor. On Jerry
  it was `/tmp/claude-1000/-home-gmusic/<id>/scratchpad/`.

### 3. Find the scratchpad, then test whether you can read it

```bash
# cwd-slug is the session cwd with / → -
# Jerry's atelier ran in /home/gmusic        → -home-gmusic
# Guillaume's fork ran in compositions-jamai → -home-gmusic-compositions-jamai
ls /tmp/claude-*/-home-gmusic*/<id>/scratchpad
```

`/tmp/claude-1000` is `700 gmusic`. An agent running as `mia` gets
`Permission denied`. `sudo -n true` first; if it works, `sudo ls`.
If it does not work, stop and say so — do not pretend the floor is gone.

If the directory is already gone, the sessiondata still projects, and
`created` still names the paths. Export `00-interpreter/` +
`09-sessiondata/` and write in the README that the floor was lost.

### 4. Name the destination before you touch a byte

Pattern: `/home/gmusic/<who>-<what>-<short-id>`

- `atelier-jerry-origin-1937aa47`
- `songbird-71bbe83b` (Guillaume's name, kept)

Refuse to overwrite. If the dest exists, stop.

### 5. Classify, copy, hash

```bash
sudo python3 ~/.agents/skills/miadi-hooks-interpreter-jamai/scripts/export-jamai-session.py \
    --session-id <id> \
    --dest /home/gmusic/<meaningful-name>
```

The script:

- dumps interpreter text+json into `00-interpreter/`
- copies the scratchpad into `01`–`07` by extension and a short capture rule
- snapshots living Write/Edit files the interpreter named into
  `08-session-writes/` (current-on-disk bytes, **not** first-write bytes)
- copies sessiondata (minus `last_*` tails) into `09-sessiondata/<id>/`
- writes `MANIFEST.tsv` (`class · path · bytes · mtime · sha256`)
- chowns the tree `gmusic:gmusic`

Then you write the `README.md`. The script will not — the README is
where the judgment lives (see *What the README must say*).

### 6. Prove the copy

```bash
# at least two generators and one score, src vs dest
sudo sha256sum /tmp/claude-1000/.../scratchpad/genNNN.py
sha256sum /home/gmusic/<dest>/01-generators/genNNN.py
```

Spot-check fails → do not keep the dest. Delete it and rerun.

## Classification

| class | what goes in | replaceable? |
|---|---|---|
| `00-interpreter/` | `session`, `aspects`, `agents`, `ceremony` × {txt,json} + `SOURCE.txt` | yes — rerun the CLI |
| `01-generators/` | `*.py` | **no** |
| `02-scores/` | `*.abc` | only if the generator is proven deterministic |
| `03-rendered/midi` | `*.mid` that are not device captures | yes — `abc2midi` |
| `03-rendered/audio` | `*.wav` `*.mp3` rendered `*.m4a` | yes — fluidsynth + ffmpeg |
| `03-rendered/video` | `*.mp4` | yes — jamai-defile / jamai-clip |
| `03-rendered/scores` | `*.png` `*.svg` | yes — abcm2ps + rsvg-convert |
| `04-captures/` | timestamped device `*.m4a` / Songbird `*.mid`, named source recordings | **no** |
| `06-analysis/` | `note-*.md` `say-*.txt` `*.log` leftover txt | working memory |
| `07-surface/` | HTML the session published (jamai-cast, tables) | snapshot |
| `08-session-writes/` | living files the interpreter listed as Write/Edit, outside the scratchpad | snapshot of *now* |
| `09-sessiondata/` | the JSONL exhaust, no `last_*` | yes — still on `/a/src` until it isn't |

Keep relative subdirs (`ilex/gen_ava2.py` stays `01-generators/ilex/gen_ava2.py`).
Colliding basenames across subdirs are why.

The four tools that always run after a generator writes ABC:

1. `abc2midi`
2. `abcm2ps` + `rsvg-convert`
3. `fluidsynth` (cut reverb: `%%MIDI control 91 0` / `93 0`)
4. `ffmpeg`, usually via `jamai-defile.py` / `jamai-clip` / `jamai-publish-melody`

That is the chain GUILLAUME.md asked Jerry to list. It is also why
`03-rendered/` is 99% of the bulk and why the interpreter cannot see it.

## What the README must say

Write it by hand, after the copy, from the projection and two or three
`06-analysis/note-*.md`. Minimum:

- session id, who, date window, dest path
- where the bytes came from, and why they had to move (`/tmp` 30d, mode 700)
- the sister drop, if this is one half of a fork
- the chain diagram (generators → scores → midi → audio/video)
- the table of dirs with file count, size, replaceable?
- what the interpreter could and could not see (Write/Edit vs Bash)
- **who the captures belong to** — see the next section
- "nothing here has been committed"
- how to replay the interpreter against `09-sessiondata/`

## Ilex is not Jerry's Android

Ilex (`ilex.ferret-harmonic.ts.net`) is **William's** Android. Jerry's
Android is another node. A scratchpad folder named `ilex/` means those
files *passed through this floor*, not that Jerry was watching Ilex.

Classify timestamped `ilex/*.m4a` and `ilex/ava1/*.mid` as `04-captures`
and say so in the README. Do not write "Jerry's device captures" unless
the human has named the node and the files match it.

A capture of a person's voice entering a **pushed** git repository
cannot be withdrawn. Leave `04-captures/` out of any commit. The
manifest still names every file.

## Traps (paid for once)

| trap | what happens | guard |
|---|---|---|
| agent is not the scratchpad owner | `Permission denied` on `/tmp/claude-1000`, looks like "floor is gone" | `id`; `sudo -n true`; `sudo ls` |
| dest already exists | a second run would mix two copies | refuse to overwrite |
| trusting `created N path(s)` as the opus | you export 24 files and leave 2 GB of music in `/tmp` | always walk the scratchpad |
| committing `03-rendered/` | 2.4 GB of regenerable blobs in git forever | drop, don't repo; keep generators + manifest |
| committing `04-captures/` | a voice you cannot recall | named in README, left untracked |
| `08-session-writes/` as "the original" | those files have been edited since the Write | README says "current-on-disk" |
| `last_*` in sessiondata | tails of ledgers you already copied | skip them |
| assuming cwd-slug | Jerry's floor was `-home-gmusic`, Guillaume's was `-home-gmusic-compositions-jamai` | take the path from the projection |
| writing the ceremony | `written=false` is the contract | never POST it from this skill |
| calling Ilex Jerry's phone | wrong person, wrong consent boundary | see above |

## Replay against the drop (no `/a/src` required)

```bash
miadi-hooks-interpret session  <id> \
    --root /home/gmusic/<dest>/09-sessiondata
miadi-hooks-interpret aspects  <id> \
    --root /home/gmusic/<dest>/09-sessiondata
```

Same projection, same aspects (deterministic, no LLM, ≤55 words). If
the bytes differ, the drop is incomplete or the package moved.

## Boundary

This skill owns:

- finding a JamAI session id and its scratchpad
- running `@miadi/hooks-interpreter` as the observer
- classifying the floor off `/tmp`
- writing a drop a second reader can act on

This skill does **not** own:

- the interpreter itself (`@miadi/hooks-interpreter`)
- the morning method (`jamai-morning`) or the clip method (`jamai-montage`)
- writing into Medicine Wheel
- turning the RISE aspects into pi-coding-agent extensions
  (that is the work GUILLAUME.md pointed at
  `miadi-orchestration-kit/pi/jamai-extensions`)
