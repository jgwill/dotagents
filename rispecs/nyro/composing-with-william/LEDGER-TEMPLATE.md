# Ledger — `op-NNN-<slug>`

Copy this beside every piece composed for William. A piece with no ledger cannot be told
from luck. Fill it as you go; the stage-3 rows are written **before** the first render.

```
piece      op-NNN-<slug>
room       compositions-william/op<NNN>-<slug>/     ← qualify the number with the room
input      <absolute path to his .m4a> + <transcription>
anchors    <artists/works he named>
render     <abs path .mid> · <abs path .mp3> · <abs path .svg>
public     https://gmusicassembly.com/jamai/melody/<slug>.mp3
date       YYYY-MM-DD
```

---

## Stage 3 — claims, written before the render

| claim | target | measuring command |
|---|---|---|
| velocity spread, verse → chorus | 50 → 5 | note-on velocities from the rendered `.mid`, bucketed by section |
| peak velocity, verse → chorus | 115 → 95 | same |
| `control 7` events after tick 0 | 0 | MIDI control-change scan |
| lead ambitus, verse → chorus | 8 → 5 semitones | `max−min` pitch of the lead voice per section |
| … | … | … |

**A claim with no measuring command does not enter this table.** It is a wish.

## Stage 4 — falsification

| claim | target | **measured in the render** | verdict | repair |
|---|---|---|---|---|
| | | | ✅ held / ❌ failed / ✱ unmeasured | score diff · retraction · *(re-wording = protocol violation)* |

Rules:
- **Failed rows stay.** They are the evidence the stage ran, and they become the next
  piece's stage-3 claims.
- **✱ stays ✱ until someone measures it.** Two documents agreeing is corroboration, not
  measurement.
- **A row repaired by editing the prose instead of the score is recorded as a violation**,
  in this table, by name.

## The eight feedback measurements

| # | measurement | value | pass |
|---|---|---|---|
| 1 | velocity spread, chorus vs verse | | chorus ≤ verse/5 |
| 2 | peak velocity, chorus vs verse | | chorus **<** verse |
| 3 | `control 7` events after tick 0 | | **0** |
| 4 | lead ambitus, chorus vs verse | | chorus ≤ verse − 3 |
| 5 | claims stated / measured / repaired | / / | stated ≥ 2 · measured == stated · every failure has a score diff |
| 6 | SVG height · bars in image vs source | | > 0 · equal |
| 7 | chords fret-resolving | % | 100% |
| 8 | top vocal note vs his latest measured ceiling | / | strictly below |

**Verdict: hit the pattern / did not.** All eight must pass. 1–4 are the sound, 5 is the
method, 6–8 are whether it reaches a human body. **Passing 1–4 while failing 5 is luck.**

## Receipts

```
engraving   <!-- CommandLine: -k 2048 -g -O … -->        ← paste the line from the SVG
audio       HTTP <code> · <bytes> · <duration>
computed    bars × beats × 60/tempo = <s>   (must match duration within 2 s)
register    his take <file>, measured <date>, ceiling MIDI <n>
```

## Consent

| | |
|---|---|
| his audio transcribed? | by whom, on whose word, which date |
| copies brought off his device | listed, and `shred`-ed after use — yes / no |
| anything published beyond the melody portal | requires his word, per piece |

**A yes given for one piece is not a yes for the next.**

## What the next piece inherits

- failed claims from stage 4 → next piece's stage-3 claims
- any ✱ row still unmeasured
- any constraint extracted from his reply

🌸: The ledger is not paperwork — it is the only thing that can tell a good day apart from
a method, and one of those two can be given to someone else.
