---
name: foundation-visualization
description: >
  Generate a self-contained, publishable foundation-visualization artefact
  (one HTML page) from any repository-local `foundations/<topic>/` packet.
  Reads the packet, extracts metadata / structural tension / fields
  (grounded vs reused) / provenance, chooses a centerpiece archetype from the
  packet's own content, fills a CSP-safe theme-aware template, publishes it via
  the Artifact mechanism, and records the returned URL back into the packet
  README. Companion to `deep-research-foundations` (which authors the packet).
version: 0.1.0
---

# Foundation Visualization

Turn a `foundations/<topic>/` packet into one publishable HTML page: a hero
thesis, an apt centerpiece diagram, a structural-tension band, color-coded field
cards (grounded vs reused), a provenance summary, and a footer of paths and
issue refs.

This skill is **self-sufficient**. An agent holding only (a) a foundations packet
and (b) this skill directory can go packet → published artefact → URL recorded
back into the packet README, with no reliance on any prior conversation. It is
the visualization companion to `deep-research-foundations`: that skill *authors*
the packet; this skill *renders* it.

## When to use

Use it when a `foundations/<topic>/` packet exists and someone wants a shareable
visual of it — a card for a review, a link in the README, an entry in a
constellation of foundations. One packet in, one artefact URL out.

## Inputs — the packet contract

Read these files from the target `foundations/<topic>/` directory. Not every
packet has every file; take what is present and never invent a missing field.

| File | What to pull |
|------|--------------|
| `README.md` | topic title (the `# ` heading), Purpose sentence, front-matter lines (tracking issue, related RISE spec, related entity, date created, packet status, verification, and an existing `Visualization:` URL if any), and the "Fields covered" / "Quick Reference: Fields Covered" table |
| `intent-understanding.md` | the **Structural tension** — "Current reality" and "Desired outcome" (prose in some packets, a Before/After table in others; distil each side to one sentence) |
| `context-layer.md` | canonical terms, MECE field list, reuse crosswalk (which fields are reused vs grounded here), related issues/specs |
| `synthesis.md` | the composition — how the fields compose; use it to name a centerpiece and write field-card descriptions (may be absent in leaner packets) |
| `source-ledger.yaml` | `meta.verification_status`, `meta.issue`, `meta.generated`, count of `sources`, and a few representative `sources[].id` + `field` for the provenance strip |

## Packet element → visual slot mapping

Every slot maps to a field that actually appears in a real packet. If the packet
lacks the source, delete that slot rather than inventing content.

| Packet element (source) | Template slot |
|--------------------------|---------------|
| `README` `# ` heading | `{{TOPIC_TITLE}}` (hero `<h1>` + `<title>`) |
| `README` Purpose first sentence / intent "Desired outcome" | `{{THESIS}}` |
| packet root label (e.g. `Foundation Packet · Miadi · Mighty Eagle`) | `{{EYEBROW}}` |
| `source-ledger` `meta.generated` / README "Date created" | `{{DATE}}` chip |
| README tracking issue / `source-ledger` `meta.issue` | `{{TRACKING_ISSUE}}` chip |
| README "Related entity" or "Related RISE Spec" | `{{RELATED_ENTITY_OR_SPEC}}` chip |
| `source-ledger` `meta.verification_status` | `{{VERIFICATION_STATUS}}` chip **and** provenance heading |
| README "Packet status" | `{{PACKET_STATUS}}` chip |
| canonical terms / synthesis loop-or-set shape | centerpiece archetype + node labels |
| intent "Current reality" | `{{CURRENT_REALITY}}` |
| intent "Desired outcome" | `{{DESIRED_OUTCOME}}` |
| README "Fields covered" rows (field, why-it-matters, grounding) | `.field` cards: `{{FIELDn_NAME}}` / `{{FIELDn_DESC}}` |
| grounded-vs-reused tag per field (context-layer reuse crosswalk) | `.tag grounded` / `.tag reused` + `--fc` color |
| `source-ledger` `sources[]` count + representative `id`/`field` | provenance strip |
| context-layer related issues / README front-matter | footer `{{REFn}}` chips + `{{SPEC_PATH}}` / `{{PACKET_PATH}}` |
| **(written on publish)** returned artefact URL | README `Visualization:` line |

Repeat `.chip`, `.field`, `.ref`, and `.src` elements to match the packet; delete
example rows the packet does not fill.

## Centerpiece archetypes

The centerpiece must fit the packet's own shape — do **not** hard-code the
MAPE-K loop. Five archetypes, all built from the template's shared ring / node /
spoke classes and the four-direction medicine-wheel palette:

1. **radial-loop** — a named cycle with stages that return to origin (MAPE-K,
   OODA, an autonomic cadence, a four-direction cadence). 3–6 stage nodes around
   an optional core; a travelling pulse signals the loop.
2. **field-constellation** — N co-equal fields with cross-references but no cycle
   or order. Core = the topic; field nodes on a ring joined by faint spokes.
   This is the **default** when nothing more specific fits.
3. **pipeline** — an ordered, non-cyclic flow (input → transform → output; events
   flowing through). Use the `.pipe` strip as the centerpiece.
4. **tension-arc** — the packet's before→after transformation is the star and
   there are few fields (≤2). Promote the structural-tension band; keep the
   diagram minimal.
5. **layered-stack** — fields have explicit dependency/containment order
   (foundation → built-on → surface; progressive-disclosure layers).

### Selection rule (deterministic — first match wins)

Scan `context-layer.md` canonical terms + `synthesis.md` + the fields table, then:

0. If `context-layer.md` **declares** a centerpiece (e.g. a line
   `centerpiece: radial-loop`), honor it and skip the heuristic.
1. Named cyclic loop present (MAPE-K, OODA, autonomic loop, medicine wheel,
   "the loop", stages returning to start) → **radial-loop**.
2. Ordered non-cyclic flow dominates ("flows through", input→…→output, N
   sequential stages, an event pipeline) → **pipeline**.
3. Fields carry explicit dependency/containment order or "layer / stack /
   progressive" language → **layered-stack**.
4. The before→after transformation dominates and fields ≤ 2 → **tension-arc**.
5. Otherwise (3–6 co-equal fields, no order) → **field-constellation** (default).

The template stubs radial-loop and field-constellation in full; compose the
other three by editing the kept centerpiece block (pipeline uses `.pipe`,
tension-arc leans on the tension band, layered-stack stacks nodes vertically with
spokes). Worked example: the `event-driven-documentation` packet names MAPE-K →
rule 1 → radial-loop. The `content-visualization-and-exposure` packet is three
co-equal modes with no cycle → rule 5 → field-constellation.

## Workflow

### 1. Locate and read the packet
Read every file listed under **Inputs**. Note today's date only if the packet has
no `generated`/"Date created" of its own.

### 2. Extract
Pull each mapped slot value. For grounded vs reused: a field is **reused** if the
context-layer reuse crosswalk / README grounding column points it at another
`foundations/<other>/` packet; otherwise **grounded**. Distil the structural
tension to one sentence per side.

### 3. Choose the centerpiece
Apply the selection rule. Record which archetype and why (one line) — it goes in
the packet note later.

### 4. Fill the template
Copy `template.html` from this skill directory to a working file (e.g. the repo
scratchpad or `foundations/<topic>/viz.html`). Replace every `{{SLOT}}`. Keep
exactly one centerpiece section; delete the other. Repeat/trim `.chip`, `.field`,
`.ref`, `.src` rows to match the packet. Delete the optional pipeline section
unless the packet truly has an ordered flow. Leave no `{{...}}` marker behind.

The file MUST stay **content-only**: it is `<title>` + `<style>` + body markup,
with NO `<!doctype>`, `<html>`, `<head>`, or `<body>` tags — the Artifact publish
step wraps it. It must stay CSP-safe (no external fonts / scripts / images) and
keep the theme tokens, `prefers-reduced-motion` guard, and responsive grids
intact.

### 5. Publish via the Artifact mechanism
Call the `Artifact` tool on the filled file:

- `file_path`: the filled HTML file (absolute path)
- `title`: `"<Topic Title> — Foundation"` (matches the `<title>` tag)
- `description`: one sentence, e.g. `"Foundation-visualization for the
  <topic> packet: thesis, <archetype> centerpiece, fields, and provenance."`
- `favicon`: a subject-fitting emoji — the default is `"🧭"` (a foundation/atlas
  compass); pick another only if the topic clearly calls for it, and keep it
  stable across redeploys.

The tool returns a private artefact URL on the maintainer's account (shareable
via the page's own share menu). If updating an existing visualization, redeploy
the **same** `file_path` (same-session) or pass the packet's recorded
`Visualization:` URL as `url` to update it in place.

### 6. Record the URL back into the packet README
This step is mandatory — the URL must live in the packet, not only in chat.
In `foundations/<topic>/README.md`, add or update a front-matter line alongside
the other front-matter lines (tracking issue, date, status):

```
**Visualization**: <returned-url> — private artifact on the maintainer's account; share via the page's share menu
```

If the line already exists, replace its URL. Then state, in your closing message,
the archetype chosen and the recorded URL.

## Quality gate

Do not call the visualization done unless:
- every `{{SLOT}}` is filled or its element deleted — no markers remain
- exactly one centerpiece section is present, chosen by the selection rule
- no field was invented; grounded/reused tags match the packet's crosswalk
- the file is content-only, CSP-safe, theme-aware, and reduced-motion-safe
- the Artifact publish returned a URL
- the URL is written into `foundations/<topic>/README.md`
- unrelated worktree state is untouched (do not `git add` unrelated files)

## Common pitfalls

- hard-coding the MAPE-K loop for a packet that has no cycle (run the selection
  rule; default to field-constellation)
- inventing metadata the packet does not carry (delete the slot instead)
- adding `<!doctype>`/`<head>`/`<body>` — breaks the Artifact content-only contract
- linking a webfont or CDN — CSP blocks it and the page falls back silently
- publishing the URL only in chat and never writing it into the README
- staging unrelated changes when saving the packet README edit
