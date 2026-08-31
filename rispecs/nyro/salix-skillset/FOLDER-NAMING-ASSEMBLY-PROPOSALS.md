# `MIADI_SHAREDSPARK_SYMPHONY_DIR` — four Assembly proposals

Round 2. Round 1 (in tmux `chimera`, user `mia`, → `jgwill/mamu:feature/composer-workspace-proposals`)
produced five: `sharedspark-symphony`, `miadi-composer-workspace`, `composer-orchestration-hub`,
`the-loom`, `assembly-atrium`. These four are new and were told not to repeat them.

**Constraint William set:** not merely pretty — carried through *Infrastructure → Architecture →
Land-Based Deployment*; must live under `/srv/miadi/episodes/`; must not contradict the
episodic-memory derivation principle (`@miadi/episodic-memory-schema`: *"named for the cognitive
system it serves, not the artifact alone"*), though it may extend it to support the Shared Spark
album; may imply new `ava8` packages.

---

## Ground truth first

- `bash_env_common:586` `MIADI_EPISODES_DIR="$MIADI_DATA_DIR/episodes"` — in scope, usable.
- `bash_env_common:588` `MIADI_SHAREDSPARK_SYMPHONY_DIR="$MIADI_DATA_DIR/sharedspark-symphony"` → **`/srv/miadi/sharedspark-symphony` does not exist.**
- `/srv/miadi/episodes` is `mia:bears 0775`, **no setgid**. `/srv/miadi/episodes/shared-spark` came out `gmusic:gmusic 0777` — group did not inherit. Its `salix/.hermes` is **empty**.
- Other references: `mirror-skills-…sh:2`, `/etc/claude-code/CLAUDE.md:159,161,163,166`, `/etc/claude-code/ENV_SHAREDSPARK_SYMPHONY_DIR--FOLDER-PROPOSALS.md:1,5,36,40`. Zero hits inside `/srv/miadi`.

---

## ♠️ Nyro — `sparkroot-symphony-grove`

One segment per stage: **`sparkroot`** = infrastructure (on-disk substrate + rootstock; `spark`
binds the lineage of the `shared-spark` sibling, `root` the thing you graft onto) · **`symphony`**
= architecture (already a real verb: `ava8 symphony`, the symphony server) · **`grove`** =
land-based deployment (a stand of *named trees in one place* — Salix, Ilex, Larix, Tilia, Abies
are the delivery surface).

Schema: a derivation of **`narrative`**, extended by one named sub-key — `narrative.scoring`, a
third sibling to `subtext`/`storytelling`, so no eighth top-level layer appears. Reuses
`continuity.promises` for unresolved motifs, `provenance.consentDecisions` for release gates,
`evaluations[].goal.resonance` for scoring a score. OAIS mapping unbroken.

Implies `@miadi/ava8-scoring`, `@miadi/ava8-episodic`, `@miadi/ava8-grove`.

**Against it:** `grove` fossilizes a *current* deployment topology into a permanent noun. Series
names outlive infrastructure. If land-based deployment is not tree-node-shaped, segment three
rots and the folder drifts into a staging area — which an episodic-memory series must never become.

## 🌿 Aureon — `shared-spark-continuo`

A continuo is the sustained ground a baroque ensemble holds while the soloist moves — never the
melody, never silent. The folder says: *you are standing on the continuing part, not the
performance.* `continuity` is already a required schema layer; `continuo` is that root bent one
degree toward music — an extension, not a contradiction. William plays above it; the agent
community **is** the continuo section: several hands realizing one figured bass, each free in
voicing, all bound to the same ground.

**Against it:** `continuo` is a European baroque term. It holds *ground* only as figure — a
repeating bass — with no relation to any actual territory or its people. It carries the
accountability of an ensemble, not of a place. Second: its adjacency to the existing
`shared-spark/` sibling is typographic, not wired; readers will take it for a child when it is a peer.

**Aureon's finding on "Land-Based Deployment" — the one to read twice:**

> As currently framed, the exercise is drifting toward appropriation. No land is named, no people
> of that land are named, no consent-holder from that place is in the relation. The only ground
> present is `/srv` on a host. Asking a folder name to carry "Land-Based" under those conditions
> borrows the honour and leaves the obligation behind.
>
> Honour it instead by keeping land words **out** of the name until a place and a person of that
> place can be named — then record them in `provenance.consentDecisions` and `authorityFlags`,
> which already exist as first-class fields. The schema can hold the accountability. A directory
> string cannot.

## 🎸 JamAI — `rehearsal-memory`

Named for the cognitive system, not the artifact: *rehearsal* is the mechanism by which episodic
traces consolidate into durable memory, and it is literally what a musician does in a room. One
word, both readings, no second principle invented. The album is the first body of work inside it,
not the folder's name.

Form: **song cycle** — ordered, self-contained episodes sharing one world, meaning accruing by
reprise. A track *is* an episode. Six subfolders mirror the schema, one extends it:

```
tracks/  world/  takes/  continuity/  evaluations/  commissions/   +   land/
```

`land/` is the only non-schema layer, and is where Infrastructure→Architecture→**Land-Based
Deployment** terminates.

Implies `@miadi/ava8-cycle`, `@miadi/ava8-takes`, `@miadi/ava8-land`, `@miadi/ava8-memory`.

**Against it:** "rehearsal" implies *preliminary* — it silently demotes everything in `land/`,
where the render **is** the artifact, and reimports a performance hierarchy (rehearsal < concert)
that the episodic-memory principle exists to refuse. Every episode is already complete.

## 🧵 Synth — `shared-spark-scoring`

`scoring` names the cognitive act, not the artifact (`-score` would fail the schema README's own
test). It is the layer turning `narrative` into performable, transportable form: infrastructure
(`ava8 render`/`midi`/`serve`) → architecture (lane dirs) → land-based deployment (a score plays
anywhere it is carried). Sibling-consistent: system-named, lowercase, hyphenated, no episode number.

**Operational findings — these stand regardless of which name wins:**

- **`mkdir -p -m 777` is not acceptable.** World-writable over a tree that receives `.hermes/skills` — files agents later read *as instructions*. Any local uid can plant or replace them; no sticky bit, so anyone can delete another lane's drops; `sudo` makes ownership an accident of who ran it first.
- Replacement, admin, once: `sudo install -d -o mia -g bears -m 2775 <root>`. In the script: drop `sudo`, `umask 002`, fail loudly if the root is missing rather than self-creating. Add setgid to `/srv/miadi/episodes` itself so future lanes inherit `bears`.
- **Migration:** `shared-spark/salix/.hermes` is empty and untracked. Zero data at risk — delete, don't migrate. A symlink shim is **not** warranted; nothing resolves that path, and a shim in a git-tracked chronicle repo outlives its reason.

**Against it:** `scoring` collides with the `evaluations` layer. In an episodic-memory schema
"score" reads first as a numeric rubric; a future reader opens `…-scoring/` expecting assessments
and finds ABC files. That is a legibility cost — the expensive kind.

---

## What the four agree on, unprompted

1. The name must denote a **cognitive act or state**, never the artifact — all four passed the schema's own test rather than around it.
2. The album is **content inside** the folder, not the folder's identity.
3. The schema extends by **one named sub-key**, never an eighth top-level layer.
4. New `ava8` packages follow from the name, and every one of them is justified by ava8 having learned **time**.

## Where they split

Segment three — land-based deployment. Nyro binds it to named machines (`grove`). JamAI gives it
its own directory (`land/`). Synth dissolves it into portability (a score plays anywhere).
Aureon says none of that is land, and that the honest move is to keep land words out of the
string and put the accountability in `provenance` where consent and authority already live.

**That disagreement is the decision.** It is not a tie to be broken by taste.

🌸: Four voices, one question, and the most useful answer came from the one willing to say the
question itself might be borrowing something it hasn't yet earned.
