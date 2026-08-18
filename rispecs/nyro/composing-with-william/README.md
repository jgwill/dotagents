# RISE — Composing with William

**Subject:** opus 018 *Refaire la foudre*, published 2026-08-16, and the process that
produced it — reverse-engineered because William said the result went far past what was
expected and asked for the machine that makes it happen again.

His words, in the recording that opened the request:

> *"this managerial moment of truth where the result that was expected was way over what
> was expected. And we need to analyze how it come to be that way and then make a plan to
> reproduce it and set up a feedback system to make sure that we achieve that plan."*

His verdict on the piece itself, `transcription_260816235243_EN.txt`:

> *"your Opus 18 is amazing […] it really feels like we own that music. I don't feel like
> I'm listening to Metallica or Green Day or anything like it."*

| | |
|---|---|
| Artifact | `https://gmusicassembly.com/jamai/melody/opus-018-refaire-la-foudre.mp3` — 2 457 126 B, 1:59 |
| Source | `/home/gmusic/compositions-william/op-018-refaire-la-foudre.abc` |
| Input | `compositions-william/op003-la-bifurcation-ep333/260816231244.m4a` + its EN transcription |
| Runnable | `~/.agents/skills/composing-with-william/` |
| Ledger form | [`LEDGER-TEMPLATE.md`](./LEDGER-TEMPLATE.md) |
| Sibling rispec, same day | `~/.agents/rispecs/jamai/ava-experience-creative/` — the JamAI lane's six-beat loop and eleven measured laws |
| Status | 2026-08-17 · specification written · **nothing committed, nothing pushed** |

---

## R — Reverse Engineering

### The causal chain, in order

```
1  park .m4a               him thinking out loud — subject, three anchors, no specification
2  transcription           the anchors become text a lane can act on
3  anchors → PROHIBITIONS  "the gesture is idiom and free, the melody is not"
4  his register measured   most recent take; the ceiling becomes a hard ceiling
5  a measured law chosen   "a chorus is flatter, not louder" — pointed AGAINST metal
6  numeric claims WRITTEN  spread 50→5 · peak 115→95 · control-7 events 0 · ambitus 8→5
7  render
8  MEASURE THE RENDER      two claims fail
9  score changed           not the wording — notes moved, a cadence reassigned
10 re-render, re-measure   verse {65,85,115} · chorus {90,92,95} · ambitus 8→5 confirmed
11 engrave by hand         -k 2048; the default buffer overflows on 66 bars × 4 voices
12 publish                 a phone, away from a screen
13 his reply, remeasured   becomes the next piece's input
```

### Specified vs emerged

| specified by him | emerged in the making |
|---|---|
| the subject — *analyze how it came to be, reproduce it, set a feedback system* | the form: bar 17 disassembles the riff, bar 29 restores it |
| three anchors (Metallica, Green Day, Pink Floyd) | E Phrygian, 4/4, ♩=144, 66 bars, four voices |
| the rights concern — *"my own composition"* | anchors read as prohibitions rather than targets |
| that he wants to sing it — *"my own karaoke"* | one ceiling note, E5, strictly under his measured maximum |
| **nothing else** | every parameter, every measurement, both repairs |

He specified a **subject and a boundary**. Everything musical emerged and was defended by
measurement.

### Which element actually carried the result

Seven candidates were offered. They are not equal.

**The falsification carried it.** Two claims were checked against the rendered MIDI, found
false, and the *score* was changed — unrequested, before he heard anything. The chorus's
flatness and the chorus's contracted ambitus are the two properties he heard as
extraordinary, and **both existed only after a stated claim failed**. As first written the
piece asserted flatness in prose while the render held the verse's dynamics unchanged, and
asserted a fourth while the chorus ambitus equalled the verse. He hears the MP3; the
commentary reaches him last, if at all.

**The others, honestly ranked:**

- *Anchors as prohibitions* — **protected** the result and produced his exact verdict
  (*"we own that music"*). But a prohibition prevents a bad outcome; it does not
  manufacture an exceptional one. Necessary, not causal.
- *The measured law aimed against its own genre* — **the raw material of the check.** It
  supplied a falsifiable number. By itself it was insufficient, because as first written
  it was false in the render. The real pair is *claim stated in advance* + *claim measured
  after*; if forced to one, the measurement, because the claim alone was present and wrong.
- *The bar-17 teardown* — **form, and it was his.** He asked for reverse engineering; the
  piece disassembles its own riff. That is transcription of his request, not invention. It
  makes the piece legible; it does not make it good.
- *Guitar shapes computed before writing* — hygiene. Prevents an unplayable score, creates
  nothing. (Re-derived and correct: one shape moved four times, `0-2-2 · 1-3-3 · 8-10-10 ·
  10-12-12`.)
- *Drums play when rhythm is isolated, silent when it is removed* — integrity of the
  metaphor across two bars nobody would have audited. Character, not cause.
- *The engraving overflow found by insisting on proof* — **delivery, not music.** It made
  the score exist. The MP3 never depended on it.

### What the reverse-engineering also found

- **A third claim would have failed and was never checked.** The header asserts bars 29–32
  are identical to bars 1–4 *"caractère pour caractère"*. The notes are byte-identical; the
  annotation strings differ. One claim slipped because it was never put on a list. That is
  the argument for stage 4 being a **stage** rather than a temperament.
- **The famous sentence is misattributed by the piece itself.** *"The most amazing
  experience I had in my life with technology"* refers, in the transcript, to the Ava 1 →
  Ava 2 work with Jerry's studio handle — spoken before op-018 existed. Legitimate as art,
  not as provenance.
- **`opus 018` names two different pieces from the same day**, in two namespaces
  (`compositions-william/` and the `ava002`/`ava003` studios). Same collision at 017.
- **Two claims remain unmeasured** and are carried as ✱: the silent-failure behaviour of
  `jamai-publish-melody` (the script was not located on this host; only the hand-render
  receipt `-k 2048` is verified), and the 119-note / B3–F5 Songbird measurement
  (corroborated by two documents, measured by neither).

---

## I — Intent

### What he was reaching for

Not a metal song. His own words, same recording:

> *"I'm curious about trying to use Songbird to record myself singing to see if that would
> be an entry door to actually create the score and the music that I need — pretty much
> like doing my own karaoke, so I would have my own track, my own rhythm, my own tempo."*

**A machine that returns his own body to him as music he is allowed to own and able to
sing.** Three conditions inside that sentence, each of which shaped the piece:

| his condition | how it became structure |
|---|---|
| *my own* — ownable | anchors as prohibitions; no cell of any named work in the score |
| *singing* — singable | one ceiling note, E5, strictly under his measured maximum |
| *my own rhythm, my own tempo* | parameters measured from his takes, never requested from him |

And the frame he put around the request — *reverse engineering and specifications to make
sure that we're capable of understanding, reproducing* — is why the deliverable is a
**procedure with pass conditions**, not another song.

### The tension this resolves

Between a result that landed far past expectation **once**, and a method that lands it
**again** — for him, with his anchors, his device, his register, his consent boundaries.
The tension resolves by separating what was circumstance from what was structure. The
separation is the table above under *which element actually carried the result*; the
structure is `S`.

---

## S — Specifications

Eight stages. Each carries a pass condition a lane can check without asking him. The full
runnable text lives in `~/.agents/skills/composing-with-william/SKILL.md`; this is the
contract.

| # | stage | pass condition |
|---|---|---|
| 0 | **GATHER** — transcription verbatim; extract subject, anchors, rights concern | ≥1 transcription cited by absolute path · ≥1 anchor extracted · **0** musical parameters requested from him |
| 1 | **MEASURE HIM** — his most recent sung take | ceiling recorded as a MIDI number · the piece's top vocal note strictly below it · **0** vocal notes outside his measured band |
| 2 | **CONSTRAIN** — anchors as prohibitions | every anchor appears as a prohibition · **0** transcriptions of named works in the working set · **0** melodic runs of ≥4 notes matching one |
| 3 | **CLAIM** — numeric claims before the render | ≥2 claims written down first, each with a name, a target number and its measuring command |
| 4 | **FALSIFY** — *required* | `claims_measured == claims_stated` · every failure shows a score diff or a retraction · **0** failures repaired by re-wording · measured from the rendered `.mid`/`.mp3`, never the `.abc` |
| 5 | **PLAY IT ON PAPER** — fret-resolve everything | 100% of chords resolve, span ≤ 4 frets, frets 0–12 |
| 6 | **ENGRAVE, AND PROVE IT** — `-k 2048` | SVG exists · `CommandLine` receipt recorded · height > 0 · bars in image == bars in source |
| 7 | **PUBLISH, THEN REMEASURE HIS REPLY** | MP3 returns 200 · duration within 2 s of `bars × beats × 60/tempo` · reply transcribed and ≥1 constraint extracted |

### The load-bearing rule, stated as a rule

> **Every numeric claim written at stage 3 is measured in the rendered artifact before the
> artifact reaches William. A claim that fails changes the score, or it is deleted. It is
> never re-worded to fit what came out. This runs unasked.**

Three clauses, each independently load-bearing:

- *in the rendered artifact* — forbids measuring the `.abc` and calling it measured.
- *changes the score, or is deleted* — forbids the wording repair, where the prose gets
  vaguer and the music stays wrong.
- *unasked* — forbids waiting for him to notice. He is on a phone and cannot audit
  velocities.

### The two traps this stage was built from

1. **`%%MIDI beat` on a standalone line binds only the percussion voice.** The three played
   voices keep abc2midi's defaults 105/95/80. A chorus that is flatter in the source can be
   dynamically identical to the verse in the render. Declare inside every voice block;
   switch with `[I:MIDI beat …]` on **all** voices at each boundary.
2. **A prose claim about range is not a range.** Cadence notes sit at section ends, outside
   the band, and read as part of the line. The repair usually **moves the harmonic event to
   another instrument** rather than lowering the voice — that is what let the voice stand
   still while the ground dropped a semitone under it.

---

## E — Exportation

### What ships

| artifact | path |
|---|---|
| the runnable skill | `~/.agents/skills/composing-with-william/SKILL.md` |
| the worked example, every number with its verification status | `.../references/op-018-teardown.md` |
| stage 4 in operational detail | `.../references/falsification-protocol.md` |
| what is his specifically — anchors, device, registers, consent, namespaces | `.../references/william-constants.md` |
| this specification | `~/.agents/rispecs/nyro/composing-with-william/README.md` |
| the per-piece ledger form | [`LEDGER-TEMPLATE.md`](./LEDGER-TEMPLATE.md) |

### The feedback system

Eight measurements, none of which asks him. A piece hit the pattern when all eight pass.

| # | measurement | pass |
|---|---|---|
| 1 | velocity spread per section, from the rendered MIDI | chorus spread ≤ ⅕ of verse spread |
| 2 | peak velocity per section | chorus peak **<** verse peak |
| 3 | `control 7` events after tick 0 | **0** |
| 4 | lead-voice ambitus per section | chorus ≤ verse − 3 semitones |
| 5 | claim survival | stated ≥ 2 · measured == stated · every failure has a score diff |
| 6 | the score renders | SVG height > 0 · bars in image == bars in source |
| 7 | playability | 100% of chords fret-resolve |
| 8 | his ceiling | top vocal note strictly below his latest measured maximum |

1–4 are the sound. 5 is the method. 6–8 are whether it can leave the machine and reach a
human body. **A piece that passes 1–4 and fails 5 is luck, not the pattern.**

### Recursion

Each ledger's stage-4 failures become the next piece's stage-3 claims. The claim set grows
monotonically; failures should thin on old claims and appear on new ones. Zero failures
across the whole set means the claims stopped being ambitious — not that the method
finished.

### How this composes with the neighbouring tree

`~/.agents/rispecs/jamai/ava-experience-creative/` covers the same 16 August from the JamAI
lane: a six-beat relational loop and eleven measured laws. **This spec does not replace
it.** Its law 7 — *the render lies, and it lies in silence* — is the same invariant found
independently from another direction, which is the strongest evidence available that the
invariant is real and not a story about one good day. Read that tree's law 11 before
touching any of his audio.

### Held — nothing acts without his word

| item | state |
|---|---|
| `~/.agents` commit / push | **not done.** This lane writes files only |
| `compositions-william/` and the device manifest | owned by the JamAI lane composing op-019; untouched |
| op-018 `.abc` | unmodified |
| the `jamai-publish-melody` silent-overflow claim | ✱ unverified — **measure before opening any tooling issue** |
| the 119-note / B3–F5 Songbird figure | ✱ corroborated by two documents, measured by neither |
| the `opus 017/018` namespace collision | named, not resolved — resolving it renames his artifacts and is his call |

🌸: He asked how the lightning happened, and the honest answer was smaller than the storm —
somebody wrote a beautiful sentence, held it up against the file, saw it was untrue, and
rebuilt the song rather than the sentence.
