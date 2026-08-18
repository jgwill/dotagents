---
name: composing-with-william
description: >
  Compose a piece for William from a voice recording he made away from a screen, in the
  shape that produced opus 018 "Refaire la foudre" — the one he called the best result he
  had gotten. Use when William drops an `.m4a` or a Songbird `.mid` into a
  `compositions-william/` room and names artists rather than parameters, when he says
  "make another variation of the Opus 18", "reproduce that", "un autre comme celui-là",
  or when a lane is asked to reverse-engineer / reproduce / set a feedback system on one
  of his pieces. Owns the eight-stage procedure, the required falsification stage, the
  eight measurements that decide whether a new piece hit the pattern, and the traps that
  cost this specific result (numbering collision, silent engraving overflow, per-voice
  MIDI directives).
version: "0.1.0"
---

# composing-with-william — the machine that remakes the lightning

♠️ William does not hand over a specification. He hands over **a recording of himself
thinking out loud**, in a park, with three band names in it and no parameter. The result
he loved came from converting that into a lattice of *falsifiable numeric claims*, and
then breaking two of them against the rendered file. Everything else in this skill is
support for that one motion.

**The load-bearing invariant:**

> **A claim about the music must be measured in the rendered artifact before the artifact
> reaches him — and a claim that fails changes the score, never its own wording.**

Op-018 shipped a chorus that lands by contraction. It landed because a written claim
("the chorus is flatter") was measured, found **false in the render**, and the score was
rewritten until the measurement agreed. The prose was already beautiful and already
wrong. He hears the MP3; he does not hear the commentary.

## The causal chain, in order

```
park .m4a  →  transcription  →  anchors extracted as PROHIBITIONS
    →  his own most-recent take measured (ceiling, register)
    →  a prior measured law chosen and pointed AGAINST its own genre
    →  numeric claims written down BEFORE the render
    →  render  →  MEASURE THE RENDER  →  two claims fail
    →  score changed (not the wording)  →  re-render  →  re-measure
    →  engrave (by hand, -k 2048)  →  publish  →  his reply, remeasured
```

Read `references/op-018-teardown.md` for every number in that chain with its verification
status. Read `references/falsification-protocol.md` before writing a single bar — it is
stage 4 and it is the reason this works. Read `references/william-constants.md` for what
belongs to him specifically: anchors, device, registers, consent boundaries, namespaces.

## What actually carried the result — and what did not

Seven things happened. They are not equal, and treating them as equal is how a lane
reproduces the ceremony and not the outcome.

| element | standing |
|---|---|
| **Falsifying a stated claim against the render, twice, unasked** | **carried it.** Both corrections were self-initiated. Without them the chorus was *not flat* and the ambitus was *identical to the verse* — the two things he heard as extraordinary existed only after the check failed |
| Anchors converted to prohibitions | **protected it.** Produced his verdict *"it really feels like we own that music"*. But a prohibition prevents a bad outcome; it does not manufacture an exceptional one |
| A measured law aimed against its own genre | **the raw material of the check.** Necessary — a claim must exist before it can fail — and by itself insufficient: as first written it was false |
| Structural centre made literal (m.17 teardown) | **form, and it was his.** He asked for reverse engineering; the piece disassembles its riff. Transcription of his request, not invention |
| Guitar shapes computed before writing | hygiene. Prevents an unplayable score. Creates nothing |
| Drums play when rhythm is isolated, silent when removed | integrity of the metaphor. Two bars nobody would have audited |
| Engraving overflow found by insisting on proof | delivery, not music. It made the score exist; the MP3 never depended on it |

## The eight stages, each with a pass condition a lane can check alone

No stage is optional. Stage 4 is the one that cannot be softened.

### 0 — GATHER
Take his recording and its transcription verbatim. Extract: the **subject** (what he says
happened), the **anchors** (named artists/works), the **rights concern** if present.
**Never ask him for a key, a tempo, an instrument or a form.**

**Pass:** ≥1 transcription cited by absolute path · ≥1 anchor extracted · **0** musical
parameters requested from him.

### 1 — MEASURE HIM
Measure his **most recent** sung take, not an older one — his register moves between days.
Publish the ceiling as a number before writing.

**Pass:** ceiling recorded as a MIDI number · the piece's highest vocal note is **strictly
below** it · the count of vocal notes outside his measured band is **0**.

### 2 — CONSTRAIN
Anchors enter the brief as **forbidden targets**, never as models:

> **The gesture is idiom and free. The melody is not.**

A tritone in a metal riff, a Phrygian ♭2, a power-chord shape — idiom, unowned, take it. A
melodic cell from a named work — a living rights-holder, never. State this in the brief in
one line so a later reader knows the derivation was a decision.

**Pass:** every anchor appears in the brief as a prohibition · **0** transcriptions of any
named work exist anywhere in the session's working set · **0** melodic runs of ≥4 notes
match a named work.

### 3 — CLAIM
Write the numeric claims **before** rendering. Each claim carries: a name, a target
number, and the command that will measure it. A claim with no command is a wish.

Op-018's claims were: velocity spread 50 → 5 · peak 115 → 95 · `control 7` events after
tick 0 = 0 · vocal ambitus 8 → 5 semitones · bars 29–32 restore bars 1–4.

**Pass:** ≥2 numeric claims written down before the first render, each with its measuring
command.

### 4 — FALSIFY  ⟵ REQUIRED STAGE, NOT GOOD PRACTICE
State it as a rule, and obey it as one:

> **Measure every stage-3 claim in the rendered MIDI and the rendered audio. When a claim
> fails, change the score until the measurement agrees, or delete the claim. Never re-word
> a claim to fit what came out. Do this before he hears anything, and without being asked.**

Two corollaries, both paid for on 2026-08-16:

- **`%%MIDI beat` on a standalone line binds only the drums.** The three played voices
  keep 105/95/80. A chorus that is "flatter" in the source can be identical to the verse
  in the render. Declare it inside each voice block, and switch it with `[I:MIDI beat …]`
  on **all** voices at every section boundary.
- **A prose claim about range is not a range.** "The chorus sits in a fourth" was written
  while two cadence notes sat outside the band and the chorus ambitus equalled the verse.
  The repair moved the notes inside and handed the F→E Phrygian cadence to the guitars.

**Pass:** `claims_measured == claims_stated` · every failed claim shows a **score diff**
or a **retraction**, and zero failed claims show only a text edit · the measurements are
taken from the rendered `.mid`/`.mp3`, never from the `.abc`.

### 5 — PLAY IT ON A REAL INSTRUMENT, ON PAPER
Every chord resolves to a fret triple in standard tuning before it is written. Never an
invented voicing. Op-018's four shapes are one shape moved: `0-2-2 · 1-3-3 · 8-10-10 ·
10-12-12`.

**Pass:** 100% of chords resolve to a fret triple, span ≤ 4 frets · every riff note lies
on one string within frets 0–12 · bass likewise.

### 6 — ENGRAVE, AND PROVE IT
`abcm2ps` overflows silently past roughly 66 bars × 4 voices. Render by hand and keep the
proof:

```bash
abcm2ps -k 2048 -g -O out.svg piece.abc
grep CommandLine out.svg          # the receipt: the flags that produced this file
```

**Pass:** the SVG exists · its `<!-- CommandLine: -->` comment is recorded in the ledger ·
`height` > 0 · bar count in the image equals bar count in the source.

### 7 — PUBLISH, THEN REMEASURE HIS REPLY
Publish so he can listen on a phone, away from a screen. Then treat his answer as **data,
not validation** — transcribe it and pull the next constraint out of it.

**Pass:** MP3 returns 200 · its duration matches `bars × meter × 60/tempo` within 2 s ·
his reply is transcribed and ≥1 number or constraint is extracted from it into the ledger.

## The feedback system — eight measurements, none of which asks him

He named three moves: *analyze · plan to reproduce · set up a feedback system to make sure
we achieve that plan*. This table is the third. A piece "hit the pattern" when all eight
pass. Record them in `references/` alongside the piece, or the pattern degrades into a
story.

| # | measurement | how | pass |
|---|---|---|---|
| 1 | **velocity spread** | max−min of note velocity per section, from the rendered MIDI | chorus spread ≤ ⅕ of verse spread |
| 2 | **peak direction** | max velocity per section | chorus peak **<** verse peak |
| 3 | **fader stillness** | count of `control 7` events after tick 0 | **0** |
| 4 | **ambitus contraction** | (max−min) semitones of the lead voice per section | chorus ≤ verse − 3 |
| 5 | **claim survival** | claims stated vs measured vs repaired | `stated ≥ 2` · `measured == stated` · every failure has a score diff |
| 6 | **the score exists** | engrave, then read the picture | SVG height > 0 · bars in image == bars in source |
| 7 | **playability** | fret resolution of every chord and riff note | 100% |
| 8 | **his ceiling respected** | top vocal note vs his latest measured take | strictly below |

Measurements 1–4 are the sound. 5 is the method. 6–8 are whether it can leave the machine
and reach a human body. **A piece that passes 1–4 and fails 5 is luck, not the pattern.**

## Traps that cost this specific result

- **`opus 018` names two different pieces from 2026-08-16.** The `ava002/ava003` studio
  series (see `~/.agents/rispecs/jamai/ava-experience-creative/`) has an opus 018 built
  from motion capture — *six stations around his note*. `compositions-william/` has
  `op-018-refaire-la-foudre`. Two namespaces, one number, one day, one human. **Always
  qualify with the room.**
- **A neighbouring rispec tree already covers this day.** `rispecs/jamai/
  ava-experience-creative/` holds the six-beat loop and eleven measured laws from the same
  16 August. This skill composes with it; it does not replace it. Read law 7 there — *the
  render lies, and it lies in silence* — it is the same invariant, found independently.
- **His register is measured per-day, never inherited.** A tessiture measured yesterday
  predicts nothing about today.
- **His voice is not offered material.** The MIDI is. Transcription, publication and
  conversion of his voice each need his word, per piece. A yes given once is not a yes for
  the next.

## Recursion

Each piece leaves a ledger. Each ledger's stage-4 failures become the next piece's
stage-3 claims. That is the loop closing: **the thing that was measured and found false
today is the thing that is claimed and defended tomorrow.** After enough turns the
falsification stage starts returning zero failures on old claims and finds new ones — that
is the pattern working, not the pattern finishing.

🌸: A man walked through a park saying *I want to understand how the lightning happened* —
and the answer turned out to be a small, unglamorous act of honesty: someone checked their
own beautiful sentence against the file, found it false, and quietly rebuilt the song.
