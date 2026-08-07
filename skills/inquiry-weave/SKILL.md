---
name: inquiry-weave
description: Use inquiry-weave to relate artefacts and episodes (the three-identity weave), author episode-to-episode lineage edges, build the chronicle catalog, and enumerate the Twine story library (MIADI_STORIES_ROOT).
license: MIT
compatibility: Requires the inquiry-weave CLI from @miadi/inquiry-weave.
metadata:
  author: Guillaume D. Isabelle
  version: "0.6.0"
  kin:
    - miaco
    - passages
allowed-tools: Bash(inquiry-weave:*)
---

# inquiry-weave — the relational weave CLI

`inquiry-weave` records relationships instead of copying content: artefact ↔
episode (the three-identity weave), episode ↔ episode (lineage), and episode ↔
book form (the story library). It relates and syncs; it never generates
inquiry content.

## Status

!`inquiry-weave --help >/dev/null 2>&1 && echo "inquiry-weave available" || echo "Not installed: npm install -g @miadi/inquiry-weave"`

## Lineage authoring (cycle two)

Author an episode-to-episode edge in house style ({episode, path, relation}),
both shores, dry-run first:

```bash
inquiry-weave lineage --from <folder|num> --to <folder|num> \
  --relation "one sentence naming what flows between the rooms" \
  --kind relates-to --reverse --dry-run
```

Drop `--dry-run` to write. Rules the tool enforces for you: yaml round-trip
safety (comments, key order, and unknown fields survive), idempotency by
target, never overwriting a non-map `lineage`. Rules you enforce: the
relation sentence must read true from BOTH doorways, and verification comes
before the claim — the folder name rendering as a link on the /chronicle
surface is the proof, not the yaml edit. See
`references/lineage-weaving.md` for the full teaching.

## Three-identity weave

```bash
inquiry-weave relate  --artefact <name|path> --episode <num|name|path> [--issue owner/repo#N]
inquiry-weave promote --artefact <name|path> --new-episode <slug> [--title <t>]
inquiry-weave sync    --episode <ref> [--all]
inquiry-weave status  --episode <ref> [--json]
inquiry-weave register --episode <ref> [--dry-run]
```

## Story library (cycle three seam)

The published-story shelf is enumerated from `MIADI_STORIES_ROOT` (default
`/home/mia/Documents/Twine/Stories`) into a StoryLibraryManifest; episode
identity is parsed from shelf names (`Episode_040...`, `Episode-044-...`)
and joined onto chronicle entries as their book forms. Identity rule for
published books: IFID first, story name second, never pid — the published
HTML is a render, never a record.

## Environment

`MIADI_CHRONICLE_ROOT` (chronicle corpus) · `MIADI_INQUIRY_ROOT` (artefact
vessels) · `MIADI_STORIES_ROOT` (Twine shelf) · `MW_API_URL` (medicine
wheel). Flags `--chronicle-root` / `--inquiry-root` override per call.

## Kin (this skill relates to)

- **miaco** — the decomposition ceremony. inquiry-weave records the
  relationships a decomposition discovers; `miaco skill show` teaches the
  PDE-tree path that usually precedes a weave.
- **passages / mkepisode** — vessel creation. Episodes are born with
  `mkepisode` (never by hand); inquiry-weave then relates what grows in them.
- **the /chronicle surface** — where every edge this tool writes becomes a
  visible link in a room's Lineage card; verification happens there.
- **foundations/twine-ecosystem** (chronicle repo) — the grounded decisions
  (D1–D5) behind the story-library layer and the episode→book cycle.
