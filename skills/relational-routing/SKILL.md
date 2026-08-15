---
name: relational-routing
version: "1.0.0"
tags:
  - routing
  - chronicle
  - ceremony
  - relational
  - miadi
description: >
  Turn ceremony material and composition recordings into operational follow-up
  routed to their proper chronicle episodes, agents, protocols, or open threads.
  Centers relational accountability over extraction.
---

# Relational Action Routing Skill

## Purpose

Turn ceremony material into operational follow-up without treating the recording as something to mine or strip.

This skill centers:

- **reperage des elans d'action** — locating action impulses
- **transformation en suites operatoires claires** — transforming into clear operational sequences
- **mise en relation avec les bons episodes** — relating to the right episodes, agents, protocols, or work sites
- **acheminement vers le bon lieu de memoire** — routing to the right place of memory or work

## When to Use

Use this skill when a recording or composition contains:

- obvious next steps
- unresolved threads
- implementation wishes
- routing needs across episodes
- requests that should become agent work, issue seeds, protocol updates, or pending actions
- cross-episode lineage that needs to be made explicit for chronicle navigation

## Step 0 — Pull-First Law (Mandatory)

**Before creating or renaming ANY chronicle episode directory:**

```bash
cd /data/data/com.termux/files/srv/miadi/episodes/miadi-chronicle && git pull --rebase
```

1. Re-verify the episode number is free (check `INDEX.md` + `ls` for collisions)
2. After creating the directory, **commit and push promptly** so other agents see the claim

This prevents double-number collisions (as happened with ep140: laskmi vs robustness-weave). This rule is mandatory and non-negotiable.

## Core Pattern — 4-Phase Conversation

### Phase 1: Frame

1. Read the active transcript completely.
2. Read the episode `composition.json`.
3. If labels exist in transcript or composition metadata, use them as routing hints only.
4. Do a transcript revision pass for ASR noise.

### Phase 2: Synthesize

5. Identify action-bearing fragments that are strongly supported by the source.
6. Distinguish between:
   - **immediate action** — do now
   - **deferred action** — queue for later
   - **research thread** — open inquiry
   - **protocol improvement** — skill/workflow update
   - **uncertainty requiring human validation** — flag for Guillaume/Jerry

### Phase 3: Route

7. Route each item to its proper home using the routing destination types:

| Destination Type | Target | Example |
|-----------------|--------|---------|
| `source-ledger` | Episode `source-ledger.md` | Document implementation backbone |
| `transmutation-ledger` | Episode `transmutation-ledger.md` | Clarify lineage between episodes |
| `relational-accountability` | Episode accountability branch | Ground user stories in framework |
| `skill-draft` | `dotagents/skills/` | New or updated skill |
| `issue-seed` | GitHub issue on relevant repo | Actionable development task |
| `open-thread` | Active episode open threads | Unresolved inquiry |
| `cross-reference` | Related episode directory | Validate later |

8. Present the result in compact, legible sections.

### Phase 4: Revise

9. Final revision/validation loop before treating output as usable:
   - Remove likely ASR distortions
   - Reduce inflated certainty
   - Check that each routed action has a reason and a destination
   - Make sure labels did not over-determine the routing
   - Make sure the wording matches the relationship, not just the task
   - Keep only what is supported enough to act on

## Preferred Verbs

Use these relational verbs instead of extractive language:

| Verb | Meaning |
|------|---------|
| reperer | locate, spot |
| transformer | transform |
| relier | relate, connect |
| acheminer | route, convey |
| distribuer | distribute |
| orienter | orient, direct |
| preparer | prepare |
| mettre en attente | put on hold |

Avoid language that implies the source is being depleted, harvested, or detached from context.

## Post-Routing: Chronicle Commit

After routing produces new or updated chronicle content:

1. **Commit to miadi-chronicle** with message format: `[routing] ep<N>: <description>`
2. **Push promptly** so other agents/devices see the claim

## Post-Routing: Forgewright Registration

Register routed episodes in the medicine-wheel store so they render in the Forgewright Chronicle tab:

```bash
# Generic recipe for any routed episode:
curl -X POST http://ilex:8040/api/nodes \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "contract": "miadi.artifact-ref.v1",
      "root": "MIADI_CHRONICLE_ROOT",
      "kind": "chronicle_episode",
      "relative_path": "<episode-dir>/episode.yaml",
      "type": "knowledge"
    }
  }'
```

- Medicine-wheel serves on **ilex:8040** (gaia tunnels localhost:8040)
- Forgewright serves on **ilex:8031**

## Post-Routing: Inquiry-Weave Registration

As the final step, always run:

```bash
inquiry-weave register --episode <ref>
```

This ensures the episode is discoverable by Forgewright and other consumers. Without this step, woven episodes show `count=0` and are invisible.

## Output Structure

### 1. Action Lines
Short operational statements.

### 2. Routing Lines
Examples:
- episode actif -> note de suivi
- Episode 097 -> skill / workflow / protocol note
- pending actions -> unresolved item
- related episode -> cross-reference to validate later

### 3. Validation Notes
What remains uncertain, noisy, or unconfirmed.

## Source Hierarchy

### Primary
- Active transcript

### Secondary
- Active `composition.json`
- Label metadata as provisional hints

### Method Memory
- `skills/transcript_revision_skill.md`
- `skills/relational_narrative_engine_skill.md`
- `skills/compact_relational_synthesis_skill.md`

## Device-Sync Naming Convention

Composition folders use `[episode-number]-[slug]` prefix to enable automated routing when compositions sync from watch/phone to workstation. This naming convention is what makes cross-device routing possible.

## Design Principles

1. **Delivery failure as design material** — Failed audio delivery is not a bug report; it's a user-story artifact that routes through accountability into the next delivery cycle
2. **Transmutation is the commit pattern** — A later episode doesn't replace an earlier one; it transmutes it. Routing recordings make this lineage explicit
3. **9-step sequences as reusable scaffolds** — Stabilization plans provide repeatable routing checklists for future episode openings
4. **Pull-First prevents collisions** — Always pull before creating chronicle directories
