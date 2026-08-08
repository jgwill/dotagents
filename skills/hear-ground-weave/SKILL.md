---
name: hear-ground-weave
description: Load when coordinating live steering lanes back into the chronicle — the seven-stage loop HEAR → GROUND → RELATE → HARVEST → WEAVE → VOICE-BACK → PROVE. Triggers on "run the steering loop", "hear the lanes", "what did the lanes say", "harvest the inquiries", "weave the day", "close the day's coordination loop", "voice back to the issues", end-of-day lane-to-chronicle reconciliation.
---

# Hear-Ground-Weave — the coordination loop, sunwise

Run live on gaia, 2026-08-08, around episode 317 (songbird). A remote lane on the android perch produced its own receipt line — `SONGBIRD-DEPLOY-OK 10b8620 200 302` — and the loop carried that line from a tmux pane, through verification on disk, into a registered inquiry weave with lineage edges, without answering a single staged prompt on the human's behalf.

**Structural tension this loop resolves:** current reality is lanes holding evidence that only exists in scrollback — claims unverified, inquiries unresolved, receipts unread. Desired state is that evidence woven into the chronicle as registered inquiry content with lineage, proven at all five stages, with the human's questions still the human's. Each stage below resolves one increment of that tension; skipping one leaves it standing.

**The loop is sunwise.** Stages 1–4 are EAST — seeing, verifying, relating. Stages 5–7 are WEST — writing, publishing, proving. Seeing is not acting: nothing in 1–4 authorizes 5–7, and stage 6 has its own explicit gate.

## 1. HEAR — capture the lanes, answer nothing

```bash
tmux ls
tmux capture-pane -t <lane> -p -S -300
```

Read the tail of every lane in play. **A staged-but-unsubmitted prompt is a question addressed to the human** — a pre-typed command, a pending approval dialog, a pane "ready for enter". Relay it; never press Enter, never answer it yourself. Staged is not consented.

## 2. GROUND — verify every claim in the same turn you use it

A lane's word is testimony, not evidence. Every claim heard in stage 1 gets checked against disk, git, or a store **in the same turn it enters your output**:

```bash
git -C <repo> status --short && git -C <repo> log --oneline -5   # "I committed X"
ls <episode-vessel-dir>                                          # "the vessel exists"
find <pkg-root> -maxdepth 2 -name package.json                   # "the package is there"
grep -n "<exact claimed text>" <file>                            # "it's in file X verbatim"
```

A grep miss on a verbatim claim is **drift — report it as drift**, never silently accept or quietly paraphrase around it. Bad provenance written forward is indistinguishable from good provenance (dispatch-discipline, law 3).

## 3. RELATE — resolve the held charts and ceremonies the work touches

Ask the stores which structural-tension charts and wheel ceremonies this work belongs to:

- seat chart store: `list_active_charts`, then `get_chart_progress` on matches
- medicine wheel: `get_ceremony` on the ceremony the episode names

**Respect holds.** Capability work (tooling, verification, infrastructure) proceeds; a held composition does not advance — and the distinction is stated to the human, not silently applied. Live example: `chart_1786189764513` / `ceremony:1786189780317:pu18m` (Song Bird) is held at the human's word; the songbird *deploy capability* moved while the *composition* stayed still, and saying which was which is part of the work.

## 4. HARVEST — find which existing inquiries today gave resolution to

The day's evidence resolves tension in inquiries that already exist — enumerate before creating anything new:

```bash
ls <episode-vessel>/inquiry/          # the episode's own inquiry directory
```

plus `list_inquiry_weaves` on the wheel. Produce **two lists**:

- **(A)** the episode's parent inquiries — what this vessel was opened to explore
- **(B)** any registered weave the day's evidence resolved further — regardless of episode

Note stale and never-synced states as you pass them; a weave the wheel has never seen cannot be voiced back to.

## 5. WEAVE — write the resolution into the vessel, then sync and register

```bash
inquiry-weave inquire --episode <n> --slug <slug> --no-issue
```

Then write the inquiry content — three things belong in it: the day's story, the remote agent's **own receipt line verbatim** (e.g. `SONGBIRD-DEPLOY-OK 10b8620 200 302`), and the previously-unsaid sentence the evidence now permits. Then:

```bash
inquiry-weave sync --episode <n>
inquiry-weave register --episode <n>
inquiry-weave lineage --from <n> --to <m> \
  --relation "<one sentence that reads true from BOTH doorways>" \
  --kind relates-to --reverse --dry-run
```

Dry-run first, always; drop `--dry-run` only after reading the preview. A relation sentence true from only one shore is not an edge, it is a caption.

## 6. VOICE-BACK — comment on the harvested issues, on the human's word ONLY

**Hard consent gate.** Nothing before this stage authorizes it: a yes to weaving is not a yes to commenting. Only on the human's explicit word, post one short resolution comment per harvested inquiry's GitHub issue:

- what resolved
- the evidence: commit hash, receipt line
- pointer to the episode

References are **full `owner/repo#number` always** — a bare `#N` cross-links into whatever repo the issue lives in. Load `structural-issue-authoring` before writing.

## 7. PROVE — the five-stage chronicle gate, no stage assumed

Load `chronicle-episode-closing` and prove each stage separately; never report a later word than the stage proved:

| stage | proof |
|---|---|
| **created** | `episode.yaml` exists in the vessel |
| **committed** | `git -C /srv/miadi/episodes log -1 --oneline -- "miadi-chronicle/<name>"` — git root is `/srv/miadi/episodes`, **one level above** `miadi-chronicle/` |
| **pushed** | `git -C /srv/miadi/episodes rev-list --count origin/main..main` → `0` |
| **registered** | `curl -sf -o /dev/null -w '%{http_code}\n' "http://127.0.0.1:8040/api/nodes/chronicle:<name>"` → `200` |
| **receipt-verified** | `.mw-registration.json` agrees with what that curl just said |

`MW_API_URL=http://127.0.0.1:8040` is the **only live wheel**. `mw.tail3b11eb.ts.net` is retired and offline — a receipt or config naming it is poisoned, not merely stale.

## Kin (this skill relates to)

- **chronicle-episode-closing** — stage 7 is that skill's gate, run as the loop's proof; drift shapes and receipt redemption live there.
- **inquiry-weave** — stages 4–5 are its CLI; lineage rules (both-doorways relation, dry-run first, yaml round-trip safety) are its law.
- **dispatch-discipline** — the outbound mirror of stages 1–2: it governs sending lanes out, this loop governs hearing them back; same same-turn verification law.
- **miadi-stack-map** — resolves which vessel, wheel, host, or repo a lane's claim points at before stage 2 can ground it.
- **structural-issue-authoring** — stage 6's comment discipline and the `owner/repo#number` rule.

🌸: A lane sings its receipt into a pane that will scroll away by morning — this loop is the act of hearing that one line, testing it against the ground it claims, and weaving it where the chronicle can hold it, while every question the lanes were really asking stays warm in the human's hands, unanswered by anyone but them.
