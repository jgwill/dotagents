# Gerico1007/dotagents — revised issue set (2026-08-01)

Revision 2. Draft 1's five proposals were critiqued by ♠️ Nyro, 🧵 Synth, 🌿 Aureon, 🎸 JamAI
(Jerry's Assembly agents, dispatched against this file). Consensus below; dissent recorded where it
did not resolve.

## Corrections to draft 1 — verified, not taken on report

| draft 1 said | truth | proof |
|---|---|---|
| Fork is **4 commits ahead** of upstream | **2 ahead, 8 BEHIND**, histories diverged | `git fetch upstream` then `git rev-list --count` both ways. Draft 1 read a stale ref. |
| Upstream #13 / #14 open, cannot see the work | **#14 CLOSED** 2026-07-24 via PR #15; #13's answering commit 82b3bb4 **is already upstream** | `gh issue view 14 --repo jgwill/dotagents` |
| P5: the repo has no skills index | `skills/AGENTS.md` **exists, tracked since Jul 23** | it was in draft 1's own `git ls-files` output, unread |
| 3 untracked bodies load live | **2** load; `rispecs/` is symlinked nowhere | `find ~ -type l -lname '*rispecs*'` → empty |
| `~/.hermes/skills/` takes a flat symlink | **category-nested**, 195 skills / 29 categories | `find ~/.hermes/skills -name SKILL.md` depth histogram |
| `feat/assembly-agents-genesis` is orphan | fully contained in main, local-only | `git cherry -v main feat/assembly-agents-genesis` → empty |

**The one that mattered:** draft 1's P3 ("send the commits home") would have opened a PR deleting
**6 upstream skill files, 983 deletions** — `herdr-delegate`, `inquiry-weave` (+references),
`nested-claude-architect`, both `miadi-apt-buildkite-pipeline-*` — and reverting the `.hch`/`.coaia`/`.pde`
ignore rules. Verified: `git diff --name-status upstream/main origin/main | grep '^D'`.
P3 is withdrawn as an issue.

---

## Where the four agreed

| point | ♠️ | 🧵 | 🌿 | 🎸 |
|---|---|---|---|---|
| P5 rests on a false premise — the index exists | ✔ | ✔ | | ✔ |
| P3 must not execute as written | ✔ | ✔ | ✔ | |
| P1 is three unlike objects under one verb | ✔ | ✔ | ✔ | |
| The `name: semiotic-table` "fix" is wrong | ✔ | | ✔ | |
| `~/.claude/skills/herdr` points off-repo, unowned | ✔ | ✔ | | |

**Unresolved dissent — recorded, not averaged.** 🎸 JamAI holds that versioning the untracked
skills must come *first*, because that is the loss actually in motion. 🧵 Synth holds that syncing
upstream must come first, because every commit added to a diverged main widens what a later sync
must resolve. The set below takes Synth's order and accepts JamAI's objection: the loss is real,
and I4 is one day behind I1, not one month.

---

## The six

### I1 — Sync the fork with upstream before anything is sent back
2 ahead / 8 behind / diverged. Any PR from `origin/main` today reads to the maintainer as
"finished work coming home" and lands as 983 deletions.
**Desired state:** fork main contains upstream main; the only divergence left is b9416a3, which can
be offered honestly.
**Steps.** Merge `upstream/main` into fork main · resolve · confirm `git diff --name-status` shows
zero `D` lines against upstream · then, and only then, the fork→upstream PR becomes writable.
**Tension.** A fork standing still while upstream walked resolves by walking the distance before
speaking.

### I2 — Reconcile the skill registry: extend `skills/AGENTS.md`, do not replace it
Three registries disagree today: `skills/AGENTS.md` (18 entries, ~12 with empty STATUS/MMOT,
8 disk folders absent), `.skill-lock.json` (9 vendor skills with provenance), and the live symlinks
(one of which points outside this repo). The existing ledger is developmental — STATUS / MMOT, what
each skill is *becoming*. A symlink inventory would overwrite that with `ls -la`.
**Desired state:** one table where each skill carries family (claude | hermes), install target,
vendor-or-authored, and — 🌿's amendment — an `intentionally-unversioned` column, so deliberate
silence never reads as a defect.
**Steps.** Fill the 8 missing entries · add the drift check (disk vs git) with the unversioned
column honored · record the `~/.hermes` category path per skill, not a flat name.
**Tension.** Knowledge re-derived by every session from `ls -la` resolves by writing the map once,
beside the territory that already half-holds it.

### I3 — A consent contract for relational records, before any crossing
🌿 Aureon's, and the one nobody else saw. `talking-with-nairobi` and `miadi-nairobi-semiotic-table`
are not tooling — they are records *about a named living human*, describing his cognitive load and
his speech disfluency. Draft 1 proposed symlinking one into a second agent family and PR-ing both
into his own repo, unasked.
**Desired state:** every skill declares `kind: tooling | relational-record`; a relational record
carries `subject:` and `consent:` naming the human, the repo, the family, and the scope — and no
relational record enters a commit, a second agent family, or an upstream PR without that field
filled by the named party.
**Steps.** Add the frontmatter fields · classify all 26 · repair the semiotic table's Traceability
line, which claims a Hermes path that does not exist on this disk · ask William once, in writing.
**Tension.** An agent that learns a person, against a person who never agreed to become a tracked
file, resolves by asking before the first push — not by discovering after the merge.
**Gates:** I4a, and the hermes half of the PR-#2 follow-through.

### I4 — Version the untracked work — one home per object, not one verb for three
Split, per ♠️ and 🌿. They are not alike:
- **a. `miadi-nairobi-semiotic-table`** — a private dictionary; gated on I3. Its `name: semiotic-table`
  is *lineage*, matching the Hermes path the skill itself declares — draft 1's "fix the frontmatter
  to match the folder" would have broken a stated contract. Withdrawn.
- **b. `gmusic-open-notebook`** — a host-bound Eury runbook naming container, `0.0.0.0` binding,
  ports 8502/5055. Fork-only or `local/`; not upstream.
- **c. `rispecs/nyro/salix-skillset`** — loads nowhere, so no urgency; commit as documentation.
  Open question inside it: README says 64 skills, `salix-skillset.allowlist` has 86 lines.
**Steps.** One branch per object, `git switch -c <name> main` first — the tree currently sits on the
open PR's branch, and a commit made without switching silently changes what reviewers are reviewing ·
stage by name, never `-A`: this fork's `.gitignore` no longer ignores `.hch`, `.coaia`, `.pde`.
**Tension.** Live authority resting on one machine's disk resolves by moving authorship into the
repo — object by object, at the pace each object's consent allows.

### I5 — `herdr` has no owner
`~/.claude/skills/herdr` → `/workspace/repos/jgwill/dotagents/skills/herdr` — the only live symlink
pointing outside `.agents`, shadowing this repo's own tracked `skills/herdr/`, which therefore loads
never. `CHIMERA_GENESIS_dotagents.md` §3 already records the repoint as *held, awaiting William's word*.
**Desired state:** one named source for `herdr`; the symlink moves on William's word, or the repo copy goes.
**Tension.** Two copies and no owner resolves by naming which one is real, by the person who held the decision open.

### I6 — A composition contract: skills declare their siblings
🎸 JamAI's. `droxul` and `qmd` already declare `metadata.openclaw.requires.bins` — the vocabulary for
*"I need a binary"* exists, while *"I hand off to a sibling"* does not. So
`jsonl-chronicle-extractor → tushell-session-chronicle` survives as the word "probably" in a markdown file.
**Desired state:** every skill names in frontmatter the skills it hands to and receives from, and the
artifact that travels between them — so an agent loads a chain
(`rise-pde-session-multi-agents-v2 → pde-review-companion → mia-miette-session-perspective`),
not a folder.
**Tension.** 26 skills accumulating side by side resolves by writing the cue each one waits for.

---

## Not issues

- **PR #2** — MERGEABLE, CLEAN, no CI, unreviewed. It is a review, not a second tracker. Its hermes
  symlink step is blocked twice over: by the category-nested layout (I2) and by consent (I3).
- **The fork→upstream PR** — gated on I1, and reserved by `CHIMERA_GENESIS_dotagents.md` §7.1:
  *"William names 'when'; Alex orders it."* Draft 1 ordered it. Withdrawn to a held decision.
- **A fork-side Chimera issue** — `jgwill/dotagents#16` is a live room with 13 named invitations
  still open. A twin splits the answers across two rooms with no owner. Comment in the live room;
  the held decisions already live in `CHIMERA_GENESIS_dotagents.md`.
- **`feat/assembly-agents-genesis`** — contained in main, absent from origin, deletable locally.
  Not worth an issue.

## Order

```
I1 sync ──► I4b, I4c ──► the fork→upstream PR   [held: William names "when"]
I3 consent ──► I4a
           └─► PR #2's hermes symlink
I2 registry ──► absorbs the drift check; I5 closes against it
I6 independent
```
