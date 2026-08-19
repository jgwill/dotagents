---
name: miadi-plan-perspective-registration
description: Register a plan's Miette perspective into medicine-wheel and make it visible in the forgewright Chronicle — session-dir shape, dry-run-first CLI registration, the episode-card node seam, and verification curls. Use when a plan/perspective must become queryable and rendered, or when a registered perspective is "invisible" in the UI. Proven end-to-end in ep137.
version: 1.0.0
metadata:
  hermes:
    tags: [miadi, plan-insight, medicine-wheel, forgewright, miette, registration, episode-137]
    related_skills: [miadi-tmux-lane-delegation, miadi-plan-insight-miette-relational-perspective]
    ep097_capability_family: miadi-episode-intake
---

# Miadi plan-perspective registration

The full pipeline: session files → `@miadi/plan-insight` → medicine-wheel → forgewright. Session files stay authoritative; medicine-wheel is only the queryable projection.

## 1. Session directory shape (what the CLI discovers)

```text
<root>/<session_id>/
  _claude_user_inputs.jsonl        # lineage; CHRONOLOGICAL order (projector takes first/last line as-is)
  plans/
    session_<session_id>_<ts>.md   # the plan snapshot (must match session_*.md glob)
    miette_perspective.md          # the perspective
```

Perspective format (hooks-core parser): title line `# 🌸 Miette's Perspective — <title>`; an opening `🧠 Mia:` paragraph is extracted into `mia_context`; body ≤ 64 KiB.

## 2. Register — DRY-RUN FIRST, always

Upsert key is `plan-perspective:<session_id>` — a wrong first registration persists (episodes union, `registered_at` preserved).

```bash
MIADI_PERSPECTIVE_PRODUCER_SESSION_ID=<sid> MIADI_PERSPECTIVE_MODEL=<model> \
npx -y -p @miadi/plan-insight@0.3.1 plan-insight-register \
  --session <root>/<sid> --episode <episode-dir-name> --dry-run --json
# inspect the projected PerspectiveRecord, then rerun with:
#   --mw-url http://127.0.0.1:8040/api/nodes -H 'content-type: application/json' -d '{
  "id": "chronicle:<episode-dir-name>",
  "type": "knowledge", "name": "Episode NNN — <Title>", "description": "<one line>",
  "direction": "north",
  "metadata": {
    "contract": "miadi.artifact-ref.v1", "kind": "chronicle_episode",
    "schema_version": "chronicle.episode-yaml.v1", "root": "MIADI_CHRONICLE_ROOT",
    "relative_path": "<episode-dir-name>/episode.yaml",
    "parent_id": "chronicle:miadi-chronicle", "status": "active",
    "source_issue": "<owner/repo#n>"
  }}'
```

(Seam filed on jgwill/Miadi#483 — episode-node registration belongs in the relate/register flow; until it lands there, this is manual.)

## 4. Verify (three layers)

```bash
curl -s 'http://127.0.0.1:8040/api/plan-perspectives?episode_path=<episode-dir>' | jq '.count'   # store
curl -s 'http://127.0.0.1:8031/api/chronicle' | jq '.data.episodes[].relativePath'               # card
curl -s 'http://127.0.0.1:8031/api/chronicle/perspectives?episode_path=<episode-dir>' | jq '.data.count'  # render path
```

## Host facts (mia estate)

- Ports 8030 (medicine-wheel) and 8031 (forgewright) on eury are **SSH tunnels to live services on ilex** — never kill them; upgrade the ilex checkouts instead (`repos/jgwill/medicine-wheel`, `repos/miadisabelle/forgewright-plan-episode-4`, served from tmux `miadi-workbench:runtime`).
- On Termux/ilex, `npm install` dies on kuzu's native postinstall — use `npm install --ignore-scripts`.
- Episode vessels: `MIADI_CHRONICLE_ROOT=/srv/miadi/episodes/miadi-chronicle node <mightyeagle>/packages/passages/js/mkepisode.js -n NNN -t "<title>" -g "<goal>" -r <refs>` (build `episodic-memory-schema` + `inquiry-weave` dists first if module-not-found).
