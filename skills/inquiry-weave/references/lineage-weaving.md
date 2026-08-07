# Lineage weaving — the full teaching

Distilled from the first hand-authored edge (ep001 ↔ ep044, 2026-07-21) and
encoded in `inquiry-weave lineage`. The canonical copy lives in the chronicle
repo: ep293's `lineage-authoring-guidance.md`.

## Where lineage lives

A block in the episode's `episode.yaml` — nothing else. The catalog observes
it; the /chronicle surface renders it.

```yaml
lineage:
  continues_from:      # this episode carries a prior episode's teaching forward
    - episode: 1
      path: 2026-05-04-episode-001-the-portal-and-the-tree
      relation: one sentence naming what is carried
  relates_to:          # kinship without succession
    - episode: 44
      path: 2026-06-10-episode-044-teaching-academic-foundations-of-miaco
      relation: one sentence naming the kinship
```

## The field grammar

- `episode:` — the number (numbers can collide across folders).
- `path:` — the folder basename; makes resolution exact. Always include it.
- `relation:` — a sentence, not a tag; write it so it still reads true from
  the target's doorway.

## Both-shores discipline

An edge is authored on both episodes, each in its own voice: the later room
says `continues_from` (or `relates_to`); the earlier answers with
`relates_to`. The CLI's `--reverse` writes the answering shore.

## Older dialects (observed, not rewritten)

The corpus also speaks `lineage.prior_episode` (folder string),
`lineage.branch_of` (single map or list), authored-null fields, and top-level
`related_episodes`. The schema adapter observes them all and dedups against
house-style edges — never rewrite an older claim; add the house-style edge
beside it.

## Verification before the claim

```sh
curl -s <chronicle-surface>/chronicle/<earlier-folder> | grep -o "relates to\|<later-folder>"
curl -s <chronicle-surface>/chronicle/<later-folder>   | grep -o "continues from\|<earlier-folder>"
```

The target's folder name appearing as a link is the proof.

## Commit discipline

Stage the touched `episode.yaml` files by name only; the commit body carries
the relation sentence and verification receipts.
