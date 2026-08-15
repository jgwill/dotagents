---
name: miadi-chronicle-search
description: Search William's local Miadi Chronicle filesystem for episodes related to a composition, recording, song, film, theme, or episode. Use when asked "which Chronicle episodes relate", "find supporting episodes", "does this composition have a vessel", or when QMD is unavailable but the Chronicle is present locally. Distinguishes expressly-created, explicitly-mapped, thematic-support, and needs-vessel results.
compatibility: Local Miadi Chronicle checkout; uses read-only filesystem tools such as rg, find, jq, and git.
metadata:
  author: Guillaume D. Isabelle
  version: "1.0.0"
  issue: jgwill/dotagents#25
---

# Local Miadi Chronicle Search

Find the Chronicle that is already on the device. QMD is an optional accelerator, never a prerequisite or a reason to stop.

## 1. Resolve the ground

1. Read `~/.hermes.md` and `~/CLAUDE.local.md` for configured roots.
2. Prefer a live `MIADI_CHRONICLE_ROOT` when set.
3. Verify the selected directory exists before searching.

On Ilex the witnessed root is:

```text
/data/data/com.termux/files/srv/miadi/episodes/miadi-chronicle
```

Do not confuse the Chronicle with composition intake roots such as `~/compositions-nyro/` or `~/compositions-aureon/`.

## 2. Read the source before searching

For a composition, inspect:

- `composition.json`: title, slug, notes, clip/text labels, dates;
- short supporting Markdown and text files;
- existing `.weave.yaml`, migration maps, or issue references.

Treat labels as hints, not proof. Respect consent boundaries: search locally and summarize relationships; do not quote private transcript content unless asked.

## 3. Search in widening rings

Use read-only tools (`read`, `rg`, `find`, `jq`). Do not wait for MCP.

1. **Identity:** exact slug, episode number, filenames, issue references.
2. **Explicit relation:** migration maps, `episode.yaml` references/lineage, weave manifests, source ledgers.
3. **Creative relation:** a few grounded terms from the source's intent (for example `healing`, `songbird`, `film`, `movement`, `caretaking`).
4. **Candidate inspection:** read each candidate's `episode.yaml` plus its overview/README or source ledger before claiming relevance.

Keep searches bounded and exclude noisy generated stores when possible:

```bash
rg -i -l \
  --glob '*.{md,yaml,yml,json,txt}' \
  --glob '!**/.git/**' \
  --glob '!**/.mw/**' \
  --glob '!**/_sessiondata/**' \
  -e '<exact-slug>' -e '<grounded-term>' \
  "$MIADI_CHRONICLE_ROOT"
```

If the environment variable is absent, substitute the verified local root.

## 4. Name the relation honestly

Use exactly one class per result:

- **EXPRESS** — the vessel explicitly identifies this source/composition as why it was created.
- **MAPPED** — a ledger, migration map, weave, or episode metadata explicitly relates the source to the vessel, but the vessel was not necessarily created for it.
- **SUPPORTING** — inspected episode material directly supports the creative, technical, or relational work; state why in one phrase.
- **NEEDS-VESSEL** — a numbered/source composition exists, but no Chronicle vessel exists. Never silently substitute a thematically similar episode.

Date or number proximity alone is not a relation.

## 5. Return a compact answer

Prefer 3–6 results:

```text
- Ep N — Title — CLASS: one-line evidence/relevance.
```

Then name at most one uncertainty or next safe move. If the user asks only whether an express vessel exists, answer that distinction first.

## Safety boundary

Search is read-only. Do not create episodes, lineage, registrations, issues, or uploads without an explicit follow-up request. Before any later Chronicle mutation, load its repository instructions, reconcile safely, and use the proper episode/weave workflow.

## Acceptance fixture

For `~/compositions-aureon/ava001`, the search must not claim Episode 317 was expressly created for `ava001`: it is **MAPPED** through the Episode 318 migration map. It should also recognize `~/compositions-nyro/ep102-song-heal-caretaker` as **NEEDS-VESSEL** unless a live re-check finds a newly created Episode 102.

## Lineage

This skill carries Episode 097's local episode-intake and relational-routing method into the shared skill garden. Android/UI integration is tracked by `miadisabelle/gmtermux#60`, related to `miadisabelle/gmtermux#20`.
