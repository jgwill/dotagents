---
name: artefact-decompose
version: "1.0.0"
tags:
  - composition
  - artefact
  - decompose
  - transcription
  - pde
  - miaco
  - composition-browser
description: >
  Browse, inspect, and decompose artefact recorded which was composition recordings using <new name>-browser
  and miaco decompose artefact. Reads transcriptions, classifies form and intent,
  routes to decomposition strategies, and produces PDE artifacts via LLM engines.
---

# OLD NAME:Composition Decompose Skill

## STATUS:

* 260820 will need some work to support both miadisabelle/gmtermux musical-composition studio along with the episode module which uses something more called 'capture' than artefact.

## Purpose

Enable agents on this Android terminal to autonomously browse, classify, and decompose
composition recordings into structured Process Definition Entities (PDEs). This skill
bridges the gap between raw voice recordings captured via Pixel Recorder and actionable,
routed work items that can feed into the chronicle and episode workflows.

## Tools

### `composition-browser` (bash script)

Interactive terminal UI for browsing and acting on compositions.

**Location:** `~/bin/composition-browser`
**Requires:** `composition` (@miadi/composition), `fzf`, `jq`
**Optional:** `transcription` (@miadi/transcription), `miaco` (mia-co)

| Subcommand | Usage | Purpose |
|------------|-------|---------|
| _(none)_ | `composition-browser` | Interactive fzf picker with live previews |
| `list` | `composition-browser list` | List all composition slugs |
| `show <slug>` | `composition-browser show ep108-...` | Observe + classify + transcription |
| `segments <slug>` | `composition-browser segments ep108-...` | Transcription segment breakdown |
| `decompose <slug>` | `composition-browser decompose ep108-... [--run] [-e claude]` | Delegates to `miaco decompose composition` |

### `miaco decompose composition` (Node.js CLI)

The decomposition engine. Reads compositions, classifies transcriptions, routes to
strategies, and optionally runs LLM decomposition to produce PDEs.

**Location:** `$PREFIX/bin/miaco` (symlink to mia-co npm package)
**Version:** 0.13.0

| Option | Purpose |
|--------|---------|
| `--dry-run --run` | Preview what would be decomposed without calling engine |
| `--run -e claude` | Run decomposition using Claude (sonnet) as engine |
| `--run -e hermes` | Run decomposition using local Hermes agent |
| `--segments` | Show transcription segment breakdown |
| `--full` | Show full segment text (not just gists) |
| `--json` | Machine-readable JSON output |
| `--index <n>` | Process only one transcription at index n |
| `-s <strategy>` | Override strategy: `standard`, `iterative-refinement`, `adversarial-consensus` |
| `-w <path>` | Override PDE working directory (default: `~/.pde/`) |
| `--parent <uuid>` | Nest PDEs under an existing PDE |
| `--force` | Process compositions classified as unsafe-or-ambiguous |

## Composition Root

```
COMPOSITIONS_ROOT="${COMPOSITIONS_ROOT:-$HOME/compositions-nyro}"
```

Each composition folder contains `composition.json` with metadata, transcription text files,
and optional audio clips.

## PDE Output

PDEs are written to `~/.pde/<YYMMDDHHmm>--<uuid>/` with:
- `meta.json` — provenance, engine, model, strategy, session info
- `pde-<uuid>.json` — structured decomposition (primary action, secondary actions, ambiguities)
- `pde-<uuid>.md` — human-readable Four Directions format (East/South/West/North)

## Workflow: Decompose a Composition

### 1. Discover available compositions

```bash
composition-browser list
```

### 2. Inspect a composition (non-destructive, offline)

```bash
composition-browser show <slug>
# or equivalently:
miaco decompose composition ~/compositions-nyro/<slug>
```

This prints: form classification, intent, segment moves, routing strategy — all without
calling any engine.

### 3. Dry-run to preview decomposition plan

```bash
miaco decompose composition ~/compositions-nyro/<slug> --dry-run --run -e claude
```

Shows the prompt size and strategy that would be used, without spending tokens.

### 4. Run actual decomposition

```bash
miaco decompose composition ~/compositions-nyro/<slug> --run -e claude
```

Produces PDEs in `~/.pde/`. Each transcription in the composition gets its own PDE.

### 5. Review PDE outputs

```bash
ls ~/.pde/
# Read a specific PDE:
cat ~/.pde/<folder>/pde-<uuid>.md
# Or inspect structured data:
jq . ~/.pde/<folder>/pde-<uuid>.json
```

## Routing Strategies (automatic)

The decomposer routes each transcription based on its form and segment structure:

| Route | Strategy | When |
|-------|----------|------|
| `direct` | `standard` | Short, clear intent — single-pass decomposition |
| `layered` | `iterative-refinement` | Long monologues/journals — multi-pass to preserve thinking |
| _(adversarial)_ | `adversarial-consensus` | Manual override only — cross-checks via opposing passes |

## Design Principles

1. **Read-only on compositions** — miaco never writes to the composition folder. PDEs land in `.pde/`.
2. **Offline-first** — Classification, segmentation, and routing need no API. `--run` is opt-in.
3. **32KB prompt ceiling** — Full text for most transcriptions; segment gists for very long ones.
4. **Musician ownership** — The composition belongs to whoever recorded it. Decomposition is a separate concern.

## Engines Available on This Device

| Engine | Notes |
|--------|-------|
| `claude` | Uses Claude sonnet via API (default for `--run`) |
| `hermes` | Local Hermes agent (haiku-based, see `~/src/hermes-agent/`) |
| `ollama` | Local Ollama if running |
| `pi` | Pi coding agent |

## Known Observations (from v0.13.0 testing)

- All 3 test compositions decomposed successfully with `claude` engine
- `iterative-refinement` strategy correctly chosen for monologues and journals with 9+ segments
- `standard` strategy correctly chosen for direct handoff-intent compositions
- French and English transcriptions both handled well
- Duplicate PDEs accumulate if the same composition is decomposed multiple times (no dedup)
- `composition-browser decompose` correctly delegates to `miaco` via `npx mia-co`
- Meta provenance tracks slug, take, language, form, intent, and routing approach
- The `.md` output uses Four Directions framing (East/South/West/North) which aligns with the medicine-wheel integration
