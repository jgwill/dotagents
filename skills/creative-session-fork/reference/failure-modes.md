# Failure modes — six ways a fork lies about itself

Companion to `../SKILL.md`. Every mode here has a **lookalike**: another state that produces
the same reading from where you are standing. Each entry names the one command that
separates the pair. Run that command, not a plausible one.

None of these six announce themselves. Four of them leave a live, answering pane.

---

## A — The silent new session

**Symptom:** you asked for a fork; you got a fresh session wearing the id you supplied.
`--session-id` creates the id whether or not `--resume` inherited anything.

**Lookalike:** a true fork. Both give a live pane, the id you chose, and a transcript file
with that name. Asking the agent "do you remember X" is not a test — a fresh model answers
plausibly about a topic it was just told.

**Separating command**

```bash
ls -l ~/.claude/projects/<landing-projdir>/<child-id>.jsonl \
      ~/.claude/projects/<origin-projdir>/<parent-id>.jsonl
```

**Reading:** a true fork's child is within an order of magnitude of its parent. Measured on
the specimen: child **28,372,205 B**, origin **28,784,144 B**. A silent new session is
kilobytes. This is the single cheapest, most decisive check in the whole procedure — the
inherited past is a physical quantity.

**Prevented by:** nothing in the launch line. This is a verification, not a precaution.
Run it every time.

---

## B — The wrong parent

**Symptom:** `--resume` was given an id that is not the session you meant — most often a
hand-typed truncation. The specimen's own artifact carries `937aa47` for session
`1937aa47-767f-4543-8cdc-257364ae2c52`: one leading character lost, and it survived into the
permanent filename.

**Lookalike:** a correct fork. Size looks right if the wrong parent is also large; the agent
is coherent, because it genuinely inherited *a* past.

**Separating command**

```bash
ls ~/.claude/projects/*/<id-as-you-would-type-it>*.jsonl
```

**Reading:** exactly one file, and its name is the full 36-character UUID you intended. Zero
matches means the id never existed. Two or more means the prefix is ambiguous and whichever
one resumed was chosen by something other than you.

**Prevented by:** never typing an id. `herdr-fork` reads the parent id from the transcript
path and emits both ids into the script and its filename from one variable each, so the name
and the invocation cannot disagree.

---

## C — Instruments that live only by inheritance *(sibling of F)*

**Symptom:** MCP servers are configured, start, and answer — about nothing. `npx -y ${MWCV}`
and `Authorization: Bearer ${HONCHO_MCP_BEARER_TOKEN}` are what a config file contains before
something expands it. Every server in all three configs is env-dependent.

**Lookalike:** working instruments. And here the lookalike is *your own terminal*, because
the values are almost always already there.

**The separator that does not separate.** A first draft of this file said: run
`printenv MWCV MIADI_CHRONICLE_MW_URL HONCHO_MCP_BEARER_TOKEN`, and empty output is the
finding. Measured 2026-08-16 in the strictest form the shell offers —
`bash --noprofile --norc -c 'printenv …'` — all three came back populated, exit 0. They are
**exported into the process environment and inherited**, not sourced from a profile;
`--noprofile --norc` strips rc files, not inheritance. So the check passes in every context
reachable from inside herdr, including the ones where it would have to fail to be useful.
That is the §1 shape exactly: a check returning the reading that lets you keep moving.

**Separating command** — `env -i` is what actually removes inheritance:

```sh
env -i HOME="$HOME" PATH=/usr/bin:/bin bash -lc \
  '. /opt/binscripts/load.sh >/dev/null 2>&1; printenv MWCV MIADI_CHRONICLE_MW_URL HONCHO_MCP_BEARER_TOKEN'
```

**Reading:** values present under `env -i` → the script can stand alone. Values present only
*without* `env -i` → the script is riding on its parent, and will die the first time it is
scheduled, sshed, containerised, or handed to another agent. The contexts with no
inheritance are the real ones: `systemd --user` without `EnvironmentFile`, cron,
`ssh host '<cmd>'`, a container, any `su`/`sudo` that resets the environment.

**Run it in the target context, not in a subshell of an already-loaded session.** A subshell
of a loaded session cannot fail this test, which is why passing it there means nothing.

**Sibling of F.** F is an alias that dies outside its birthing *shell*; C is an environment
that dies outside its birthing *process tree*. Same defect, one layer apart, one cure: the
generated script carries its own `source /opt/binscripts/load.sh` and assumes nothing about
what it was handed.

**Measured values, 2026-08-16** (see `anatomy.md` for the standing note): `MWCV` is
`@medicine-wheel/mcp@4.6.1`; `MIADI_CHRONICLE_MW_URL` is `http://127.0.0.1:8040`, the ilex
tunnel. `HONCHO_MCP_BEARER_TOKEN` is present and inherited — its value is not written down
here or anywhere in this skill. Any config or fixture still naming `mw.tail3b11eb.ts.net` is
stale: that wheel went offline 2026-07-29.

**Prevented by:** `source /opt/binscripts/load.sh` inside the generated script, before
`exec claude`.

**And the same half-life applies to this correction.** The first separator was written from a
true observation about the config files and a false assumption about where their values come
from; it was replaced by *running it*, not by thinking harder. `4.6.1` and the tunnel URL are
readings taken at one moment on one host — re-measure them before acting on them, exactly as
you would re-measure an absence.

---

## D — The false pass from the wrong directory

**Symptom:** you verify MCP registration from a convenient directory, get `✔ Connected`, and
carry it as proof. Project-scoped config resolves against the directory the CLI is invoked
in — a different directory is a different question.

**Lookalike:** a genuine pass. Identical output text. This one has already been paid for at
another layer and is written down in `packages/webweave/MCP-RELATION.md`: a server verified
with `cd /a/src/Miadi-18 && claude mcp list` reported connected, while every session rooted
elsewhere saw no server at all.

**Separating command**

```bash
( cd '<the fork launch cwd>' && claude mcp list ) ; ( cd /tmp && claude mcp list )
```

**Reading:** if the two outputs differ, the answer is scoped to the directory — and only the
first one is about your fork. If you cannot state the directory a pass was taken in, you do
not have a pass.

**Prevented by:** verifying from inside the fork (`/mcp`) or from its own launch cwd, and
never from anywhere else.

---

## E — The orphaned fork *(the one that ran)*

**Symptom:** the fork resolves, launches, runs, answers — and lands in a project dir the
parent has never used. From the origin's folder the child does not exist: it is not offered
by `--resume`, not listed among that project's sessions, and the only record that the two
are related is the 28 MB the child carried inside itself.

**Lookalike:** a completely successful fork. Every other check passes. Size proves it is a
true fork (mode A). The pane answers. Nothing errors, at launch or ever.

**Separating command**

```bash
ls ~/.claude/projects/<origin-projdir>/<child-id>.jsonl \
   ~/.claude/projects/<launch-projdir>/<child-id>.jsonl
```

**Reading:** exactly one of the two exists, and **which one it is, is the entire finding.**
Second path only → the fork is re-homed and invisible from the parent. Both paths identical
(origin cwd was the launch cwd) → lineage is discoverable from either end and nothing needs
recording.

Measured on the specimen: origin under `-home-gmusic`, child under
`-home-gmusic-compositions-jamai`. Orphaned, and running.

**Prevented by:** landing defaults to the origin's cwd, and `--cwd` re-homes only on
purpose, with the re-homing stated in the generated script's header. Re-homing is a
legitimate act; being re-homed by whichever pane the operator was standing in is not.

**Repair, when it has already happened:** do not move a live session's transcript. Write the
lineage down instead — the receipt script names both ids and both project dirs, and that is
what the webweave seam exists to publish.

---

## F — The script that only runs in the shell that birthed it

**Symptom:** a saved fork script that cannot be re-run tomorrow, from cron, from another
pane, or by anyone else. Measured on the specimen: 356 B, mode `-rw-rw-r--`, **no shebang,
no `cd`, no `set -e`**, and its command is the alias `miaclaudeyolo`. `./script.sh` would not
have run it. It worked because it was sourced into an interactive shell that already had the
alias — and for the same reason `$(tlid min)` resolved to `2608161516` there and would
resolve to nothing anywhere else (`tlid` is a pip console script, not a builtin; the stable
absolute spelling is `/home/gmusic/.local/bin/tlidpy`).

**Lookalike:** a durable artifact. It is a real file with a real name, it produced a real
fork, and it sits on disk looking exactly like a receipt.

**Separating command**

```bash
bash --noprofile --norc '<script path>'
```

**Reading:** a durable script runs. An environment-dependent one dies on
`miaclaudeyolo: command not found` — aliases are not inherited by non-interactive shells.
A shorter first pass, if you only want the shape: `head -1 <script>` (a shebang, or not) and
`test -x <script>`.

**Prevented by:** the generated script emits shebang, `set -euo pipefail`,
`source /opt/binscripts/load.sh`, an explicit `cd` to a literal path, and plain `claude` with
every flag written out — including `--dangerously-skip-permissions`, which is
`claudeyolo`'s whole contribution and should be readable in the artifact rather than hidden
two alias hops away. Mode `+x` at write time.

---

## The pattern under all six

Each mode returns, from where you naturally stand, the reading that lets you keep moving. A
live pane says "alive", not "correct". A config filename says `ilex` while the file says
`${MIADI_CHRONICLE_MW_URL}`. A `✔ Connected` says connected *here*. A running fork says
nothing at all about where it landed.

So the verification order in `anatomy.md` is not a checklist to be sampled — it is five
questions that each fail differently, and the pane answering is the last of them, not the
first.
