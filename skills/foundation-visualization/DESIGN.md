# Foundation Visualization — Design Rationale

This proposal generalizes a hand-built one-off — the event-driven-documentation
foundation visualization — into a reusable generator any agent can run against
any `foundations/<topic>/` packet. It relates to `jgwill/Miadi#530`
(event-driven documentation workflow, the packet the exemplar visualized) and
`jgwill/Miadi#529` (Atlas, the entity the constellation of foundations feeds).

The deliverable is three files under
`rispecs/skills/foundation-visualization/`:
`SKILL.md` (the agent-facing contract), `template.html` (the parameterized,
artifact-ready page), and this `DESIGN.md` (the rationale). The rispecs copy is
the **spec / proposal**; the live install location is recommended below.

## The core tension it resolves

- **Current reality:** one exquisite visualization exists, welded to one packet.
  Its centerpiece is a MAPE-K loop — true for event-driven-documentation, wrong
  for a packet like content-visualization-and-exposure, which has no cycle at
  all.
- **Desired outcome:** a single generator that reads *any* packet and produces an
  apt page — the loop only where the packet is a loop, a constellation where the
  packet is a set, a pipeline where it is a flow.

The resolving move is to separate the **generalizable frame** (hero, tension
band, field cards, provenance, footer — identical shape across packets) from the
**variable centerpiece** (chosen from the packet's own content). Forcing every
packet into the loop would oscillate; choosing the centerpiece from the content
advances.

## Archetype set + selection rule

Five centerpiece archetypes, all built from one shared vocabulary of ring / node
/ spoke SVG classes and the four-direction medicine-wheel palette, so adding an
archetype never forks the token system:

| Archetype | Fits a packet whose core is… |
|-----------|------------------------------|
| **radial-loop** | a named cycle that returns to origin (MAPE-K, OODA, autonomic cadence) |
| **field-constellation** | N co-equal fields, cross-referenced but unordered — the **default** |
| **pipeline** | an ordered, non-cyclic flow (input → transform → output) |
| **tension-arc** | a dominant before→after transformation with few fields (≤2) |
| **layered-stack** | fields with explicit dependency / containment order |

Selection is a deterministic, first-match-wins heuristic (full text in
`SKILL.md`): a **declared** `centerpiece:` in `context-layer.md` wins outright;
else named-loop → radial-loop; else ordered-flow → pipeline; else layered → 
layered-stack; else transformation-dominant-with-≤2-fields → tension-arc; else →
field-constellation. The two real packets exercise both poles: EDD names MAPE-K
→ radial-loop; content-visualization-and-exposure is three unordered modes →
field-constellation. The template ships both of these stubbed in full; the other
three are composed by editing the kept block (they reuse the same classes).

**Heuristic vs declared:** the heuristic makes the skill work on packets that
know nothing about it (zero coupling — important, since the packet contract is
owned by `deep-research-foundations`). The declared `centerpiece:` escape hatch
lets a packet author override when they know better. Shipping both, heuristic as
default, keeps existing packets working while giving new ones a clean opt-in.

## Packet → slot mapping (only real fields)

Every slot binds to a field that actually appears in the two packets read
(event-driven-documentation, content-visualization-and-exposure). Nothing is
invented: hero title from the README `# ` heading; thesis from the Purpose
sentence; chips from README front-matter + `source-ledger.meta`; the tension band
from `intent-understanding.md`'s Current-reality / Desired-outcome (prose in one
packet, a Before/After table in the other — both distil to one sentence a side);
field cards from the "Fields covered" table with grounded/reused read off the
reuse crosswalk; the provenance strip from `source-ledger.yaml`. Where a packet
lacks a source (e.g. content-visualization has no "related entity" and no
`Visualization:` URL yet), the rule is **delete the slot, never fill it with
fiction**. Full table in `SKILL.md`.

## Staying within artifact-design fundamentals

The template inherits the exemplar's discipline verbatim where it counts:

- **Theme:** token-level palette on `:root`, redefined under
  `@media (prefers-color-scheme: dark)` and again under `:root[data-theme="dark"]`
  / `:root[data-theme="light"]` so the viewer's toggle wins in both directions.
  Components style through tokens only.
- **Neutrals, chosen:** blue-biased greys (`#f5f7f9` / `#0b0d13`), not flat mid-grey.
- **CSP-safe:** system font stacks only (monospace-as-display for the systems-
  instrument voice, sans for body); no CDN fonts, no external scripts or images,
  no `fetch`. The one diagram is inline SVG.
- **Responsive:** `clamp()` type scale, `auto-fit` field grid, the tension band
  collapses to one column under 640px; no element forces horizontal body scroll.
- **Motion:** the sole animation (a ring pulse / travelling dot) is disabled under
  `prefers-reduced-motion: reduce`.
- **Content-only contract:** the file is `<title>` + `<style>` + body, no
  `<!doctype>`/`<html>`/`<head>`/`<body>` — the Artifact wrapper supplies those.
- **Structure is information:** the medicine-wheel colors are not decoration —
  they encode field identity, and grounded vs reused is carried by tag color +
  node fill, echoed between the constellation nodes and the field cards.

## How **every agent** invokes it

### Recommendation 1 — a SKILL, not an agent definition

Ship this as a **skill**, not a `.claude/agents/*` definition. Why: the capability
is a bounded, invocable transform (packet in → artefact URL out) that any agent
should trigger mid-task without spawning a separate seat; a skill is the shared,
discoverable primitive that installs once and is available to every agent,
whereas an agent definition is project-local, Claude-only, and models a persona
rather than a reusable procedure. It also pairs one-to-one with its sibling skill
`deep-research-foundations` — author-the-packet and render-the-packet belong in
the same shelf.

### Recommendation 2 — where the live skill installs

The rispecs copy is the proposal. The **live** skill installs next to its sibling
in the version-controlled shared skills repo:

- **Authoritative:** `/home/mia/.agents/skills/foundation-visualization/` —
  the **jgwill/dotagents** repo, which is where the maintainer directed this work
  and where `deep-research-foundations` exists as a *real directory* under
  version control. Being a git repo is the deciding property: the skill can be
  committed, reviewed, and pushed like any other shared artifact.

**Correction to an earlier reading.** An initial pass recommended
`/home/mia/.claude/skills/`. That root is misleading: its
`deep-research-foundations` entry is a **symlink** to
`/usr/local/src/mightyeagle/skills/deep-research-foundations`, so installing
there would actually write into the mightyeagle repo, not a shared skills repo.
This is the "same skill in multiple places" hazard — resolve it by treating
`/home/mia/.agents/skills/` (dotagents) as the source of truth and letting the
other roots symlink to it rather than hold divergent copies.

Explicitly **not** `/a/src/mia-code/skills` (which `/src/mia-code/skills`
symlinks to): that root is the miaco / PDE-specialized set (deep-search, qmd,
miaco-pde-*) and does **not** carry `deep-research-foundations`; installing the
visualization companion there would separate the pair.

Invocation is then uniform: any agent says, in effect, "visualize the
`foundations/<topic>/` packet", the skill loads, and the workflow in `SKILL.md`
carries it to a recorded URL with no session-specific context.

## Open questions

1. **Install root — settled, but the other roots need reconciling.** The source of
   truth is `/home/mia/.agents/skills/` (jgwill/dotagents). Open: should
   `/home/mia/.claude/skills/` and `/home/mia/.openclaw/workspace/skills/` carry
   symlinks *into* dotagents so every agent resolves one copy? Today
   `/home/mia/.claude/skills/deep-research-foundations` symlinks into the
   mightyeagle repo instead — two shelves for one skill, which is exactly the
   drift this question exists to close.
2. **Centerpiece: heuristic vs declared.** Proposal ships both (heuristic
   default, declared `centerpiece:` override in `context-layer.md`). Should the
   `deep-research-foundations` packet contract be extended to make
   `centerpiece:` a first-class, documented field so authors reach for it
   deliberately?
3. **Where the filled HTML lives.** Scratchpad (ephemeral) vs
   `foundations/<topic>/viz.html` (committed alongside the packet, regenerable).
   Committing it makes the source reviewable and diffable; scratchpad keeps the
   packet lean. Which does the maintainer want as default?
4. **Redeploy identity.** The README stores one `Visualization:` URL; passing it
   back as `url` updates in place. Is one canonical URL per packet the intended
   model, or should regenerations mint new URLs and keep a history?
5. **Registry / constellation.** Once many packets each carry a `Visualization:`
   URL, should Atlas (`jgwill/Miadi#529`) compose them into a single constellation
   page — a foundation-of-foundations — and if so, does that become a sixth,
   packet-of-packets archetype?
6. **The remaining three archetypes.** pipeline / tension-arc / layered-stack are
   specified and composable from the shared classes but not yet stubbed in full.
   Should they be fully stubbed before install, or grown from real packets that
   demand them?
