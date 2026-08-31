# Recreate the work

**Hand this file to an LLM that is about to do what the two ateliers did.**
`HOW-WE-DID-IT-THIS-TIME-260819.md` is how the file arrives. This file is
what happens after `DÉPÔT`. Without this, the model watches. With it, it
writes music the way they did.

**Pair:** [this time](HOW-WE-DID-IT-THIS-TIME-260819.md) ·
[missing](MISSING-AND-DEPENDENCIES-260819.md) ·
[next time](DRAFT-PI-MONO-EXTENSIONS-260819.md)
**Disc:** `GUILLAUME.md`

---

## Would `.agents` alone have been enough?

No. The skills already hold the craft (`jamai-morning`,
`composing-with-william`). The scripts already hold the watch. What was
missing was **one entry that names the worked examples and the generator
contract**. That is this file.

Do **not** start from the leftover inline loop in
`~/.local/state/ilex-watch/`. Do **not** invent a new watch. The file has
already landed. Compose.

---

## Read in this order, then write

1. This file.
2. The drop that matches who is in the room (README + **one generator**).
3. The matching skill.
4. Then write **one** new generator. Do not edit theirs.

| who | drop | open this generator first | skill |
|---|---|---|---|
| Jerry | `/home/gmusic/atelier-jerry-origin-1937aa47` | `01-generators/gen013.py` | `skills/jamai-morning` |
| William | `/srv/miadi/episodes/miadi-chronicle/2026-08-16-episode-333-the-fork-arrives-launched-not-handed-over/salix/songbird-71bbe83b` | `01-generators/gen018.py` | `skills/composing-with-william` |

Same export shape in both: `01-generators` → `02-scores` → `03-rendered`
→ `04-captures` → `06-analysis`. Jerry's drop also has `00-interpreter/`
and `09-sessiondata/`. Session ids live in `scripts/_env.sh`.

`04-captures/` is voice and body. Read measurements already extracted.
Do not copy those files into git, into `.agents`, or into a new room.

---

## After `DÉPÔT` — one chain

```
jamai-on-drop <file>          already ran, or run it
        │                     ~/.local/state/episode-voice/drops/<name>/
        │                     verdict + notes.txt / mesure.txt / texte.txt
        ▼
open the matching skill       Jerry → jamai-morning
                              William → composing-with-william
        ▼
write one generator           self-contained .py, header contract below
        ▼
emit ABC to stdout            no hardcoded /tmp/claude-* paths
        ▼
four tools, always, in order
        1. abc2midi
        2. abcm2ps + rsvg-convert   (then LOOK at the PNG)
        3. fluidsynth               reverb off (%%MIDI control 91 0 / 93 0)
        4. ffmpeg                   via jamai-defile / jamai-clip /
                                    jamai-publish-melody
        ▼
falsify before he hears it    William: stage 4 is required
                              Jerry: re-run jamai-chords.py on the render
        ▼
return                        score + sound + the three provenance blocks
```

The hook does not compose. You do. The generator is the method. Everything
right of it can be rebuilt. Nothing left of it can.

---

## The generator contract

Every `gen*.py` that produced a piece they kept has this header **in the
ABC it emits**, in this order. A generator without it is a sketch.

```
% ─── MESURÉ ────────────  numbers from HIS file. Commands named.
% ─── DONNÉ PAR LUI ─────  tempo, words, title, a yes. Empty if he gave none.
% ─── IMPOSÉ PAR LA MESURE  what those numbers force (register left empty,
%                           one second of belly = one bar, quarter-note grid…)
% ─── CHOISI PAR MOI ────  and he can undo it with one word.
% ─── ESSAYÉ ET REFUSÉ ──  the attempt, the measurement that killed it.
```

Jerry's `gen013.py` already uses MESURÉ / DONNÉ / CHOISI. William's
`gen018.py` uses TROUVÉ EN MESURANT / CE QUE ÇA IMPOSE / CE QUE JE NE
TOUCHES PAS. Same four facts. Keep them visible in the score, not only
in the chat.

Hard rules, both rooms:

- **No `/tmp/claude-*` paths.** Those floors are gone in 30 days. Inputs
  are argv or files in the current room.
- **Never ask him for a key, a tempo, an instrument, or a form** if the
  take can be measured. If it cannot (Jerry's voice-only, force 0.128),
  say so and wait. `gen013` waited; tempo 100 was DONNÉ, not guessed.
- **Mark every CHOIX.** A confident sentence over an unverified claim is
  the most expensive thing you can leave.
- **Classify by bytes, not extension.** `MThd` in the first four bytes
  is MIDI even when the name says `.m4a`.

---

## Two crafts. Do not mix them.

**Jerry** (`gen013`, `melodie.py`, op-013 Paranoïa → op-015 Annie)

- Measure first. Name what you cannot establish.
- Duration sonnante ≠ valeur rythmique. His melody moves at the quarter
  note; writing the vowel length produced 41% sixteenth-notes and a score
  that sounded twice too fast.
- Octave jumps on isolated frames get folded around the median.
- Only notable ABC values (1 2 3 4 6 8). A 5/8 becomes a triple-dotted
  whole that nobody can read.
- Red playhead, left to right, always. `jamai-defile.py`.
- Attach his source files to the composition they produced.

**William** (`gen018`, songbird + belly JSONL)

- Park voice → anchors become **prohibitions**, never models.
- Measure today's ceiling. Leave that MIDI band empty.
- Movement gives form, not pitches. Stillness cuts stations. One second
  of his belly = one bar at quarter = 60. Units are undeclared; write
  numbers without pretending they are m/s².
- Stage 4 of `composing-with-william` is required: measure every written
  claim in the **render**. A failed claim changes the score, never the
  sentence.
- Two different pieces are both called opus 018 on 2026-08-16. Qualify
  with the room. This drop's 018 is *ta note, et ce qui la change*.
  `compositions-william/op-018-refaire-la-foudre` is the other.

---

## Paid corrections — do not re-learn them

| where | what failed | law |
|---|---|---|
| Jerry `gen013` | 41% sixteenths | write the interval to the next attack, not the vowel |
| Jerry `gen013` | Si4 announced, did not exist | octave error of the pitch tracker; energy at f/4 |
| William `gen018` | Si4 announced, did not exist | same class of error; his home note is si2 |
| William `gen021` | `assert lo <= n <= hi` → `(9, 59, 67)` | the register law, refusing, before it was a package |
| both | `/tmp/claude-…/scratchpad` hardcoded | the floor dies; the generator must not |
| both | interpreter `created N paths` | Bash made the music; Write/Edit did not |

---

## Pass — you did the same work when

- A new generator exists, with the header contract, and **no**
  `/tmp/claude-*` path.
- ABC went through all four tools.
- You looked at the PNG, not the SVG source.
- Every numeric claim in the header was measured in the rendered MIDI
  or audio. Failures show a score diff.
- He can hear it on a phone.
- His source file is attached to the composition.

If you only tailed a log, you recreated the watch. Start again at
"After `DÉPÔT`".
