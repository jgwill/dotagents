# op-018 "Refaire la foudre" — the worked example, with verification status

Source: `/home/gmusic/compositions-william/op-018-refaire-la-foudre.abc`
Published: `https://gmusicassembly.com/jamai/melody/opus-018-refaire-la-foudre.mp3`
Local artifacts: `/home/gmusic/salix/production/ngrok-mux/static/jamai/melody/opus-018-refaire-la-foudre.{abc,mid,mp3,svg}`

Every row below carries how it was checked. **Rows marked ✱ were not independently
verified by the scribe** — they are recorded as claims with their claimant, not as facts.
Do not promote a ✱ row without measuring it.

## Provenance

| item | status |
|---|---|
| Input recording exists, made in a park | ✅ `compositions-william/op003-la-bifurcation-ep333/260816231244.m4a` + `transcription_260816231244_EN.txt` — the text says *"I'm in a park right now dancing and listening"* |
| Three anchors named in it | ✅ Green Day *Basket Case*, Metallica *Master of Puppets* / *Enter Sandman*, Pink Floyd — all four titles present in that transcription |
| Rights concern is **his**, not imposed | ✅ same file: *"it's really easy for you to have the rights to remix your media"* and *"it would be my own composition"* |
| "The most amazing experience I had in my life with technology" | ⚠️ **present, but its referent is not op-018.** In the transcript it refers to the Ava 1 → Ava 2 work with Jerry's studio handle, spoken **before** op-018 existed. The piece's header quotes it as its own subject. That is a legitimate artistic move; it is not a factual attribution. Say so when citing |
| His verdict on op-018 | ✅ `transcription_260816235243_EN.txt`: *"your Opus 18 is amazing […] it really feels like we own that music. I don't feel like I'm listening to Metallica or Green Day or anything like it"* |
| Title lineage | ✅ his transcription contains *"an agent can make a **reverse lightning**"* — a transcription artefact that became *Refaire la foudre* |

## The measured claims — checked against the source and the artifacts

| claim | status |
|---|---|
| E Phrygian, 4/4, ♩=144, 66 bars, 4 voices | ✅ header `M:4/4 L:1/8 Q:1/4=144 K:Ephr`, `%%score [1 \| 2 \| 3 \| 4]`, bars commented 1→66, `\|]` at 66 |
| Verse velocity `115 85 65` → spread 50, peak 115 | ✅ declared **inside each of the four voice blocks** (not on a standalone line) |
| Chorus velocity `95 92 90` → spread 5, peak 95 | ✅ `[I:MIDI beat 95 92 90 2]` on **all four** voices at bar 33; restored at bar 49 |
| The fader never moves | ✅ `MIDI control 7` occurs 5× in the file: 4 directives, all in the header (one per voice), + 1 mention in prose. **Zero** occurrences after bar 1 |
| Verse vocal ambitus = 8 semitones | ✅ recomputed from V:1 bars 9–16 — lowest `E` (E4/64), highest `c` (C5/72) |
| Chorus vocal ambitus = 5 semitones | ✅ recomputed from V:1 bars 33–48 — lowest `G` (G4/67), highest `c` (C5/72). The repair landed: bar 40 is `A6 z2`, bar 48 is `G6 z2`; no F4, no E4 anywhere in the chorus |
| Phrygian F→E cadence given to the guitars | ✅ V:2 bars 39–40 and 47–48 hold `[=F,,C,=F,]`, resolving to `[E,,B,,E,]` at bar 41 / bar 65 while V:1 stays on A and G |
| Chorus has no rests and no accents | ✅ V:2 bars 33–48 are four equal quarters per bar, no `z` |
| Guitar shapes are computed, not invented | ✅ **arithmetic re-derived**: E5 `[E,,B,,E,]` = E2/B2/E3 → 6/0 5/2 4/2 · F5 = F2/C3/F3 → 6/1 5/3 4/3 · C5 = C3/G3/C4 → 6/8 5/10 4/10 · D5 = D3/A3/D4 → 6/10 5/12 4/12 · tritone `[E,,_B,,]` → 6/0 5/1. All correct in standard tuning; one shape, moved four times |
| Riff stays on string 6, frets 0–6 | ✅ E–F–G–A–B♭ = frets 0,1,3,5,6. Bass mirrors it an octave down |
| Drums **play** when rhythm is isolated (23–24) | ✅ V:4 bars 23–24 carry kick/hat patterns |
| Drums **silent** when rhythm is removed (25–26) | ✅ V:4 bars 25–26 are `z8` |
| Only a hi-hat click during the isolated descent (21–22) | ✅ V:4 bars 21–22 are `^F,,2` ×4 — quarter-note metronome, nothing else |
| Bars 29–32 restore bars 1–4 | ⚠️ **the notes are identical; the claim as written is not.** The header says *"identiques caractère pour caractère"*. Bar 1 carries the annotation `"^LE RIFF …"` and bar 29 carries `"^RESTITUÉ — identique à la mesure 1"`. Note content across V:2/V:3/V:4 is byte-identical; the annotation strings differ. **This is a third claim that would have failed stage 4 and was not caught.** Record it — it is the proof that the falsification stage is a stage and not a temperament |
| Score rendered by hand with `-k 2048` | ✅ **decisive**: the SVG's own header reads `<!-- CommandLine: -k 2048 -g -O …/scratchpad/svg/page.svg … -->`, `abcm2ps-8.14.14`, `Aug 16, 2026 23:41`, `height="18068.20px"` |
| `jamai-publish-melody` cannot engrave past ~66×4 and fails **silently** | ✱ **not verified here.** The script was not located on this host by the scribe, and no note about `-k` exists anywhere under `~/.agents`. What *is* verified is that the delivered SVG was produced out-of-band with `-k 2048` — consistent with the claim, not proof of it. **Measure it before writing it into any tooling issue** |
| His Songbird take: 119 notes, B3–F5 | ✱ **not verified here.** The file exists — `op003-la-bifurcation-ep333/260816160542.mid` — and the count is asserted identically in two independent places (the ABC header and the room manifest label for OPUS 017). Two documents agreeing is corroboration, not measurement |
| Vocal ceiling respected | ✅ **relative to the claim**: the piece's single top note is `e` (E5/76) at bars 65–66, strictly below the claimed F5/77 ceiling. Verified *given* the ✱ row above |
| Duration 1:59 | ✅ `melodies.json` records `"duration_seconds": 119`; 66 bars × 4 beats × 60/144 = 110 s of notated music, plus render tail |

## The two repairs that carried the piece

Both were **self-initiated**. Neither was requested. Both came from reading the render
instead of the intention.

**Repair 1 — the flat chorus was not flat.**
Written: `%%MIDI beat` on standalone lines between bars. Measured: only V:4 followed;
V:1/V:2/V:3 held the defaults 105/95/80 in the verse **and** the chorus, so the section
that the whole piece is built around was dynamically identical to the one before it.
Repaired by declaring the directive inside every voice block and switching it with
`[I:MIDI beat …]` on all four voices at bars 33 and 49.
Measured after: verse {65, 85, 115} · chorus {90, 92, 95}.

**Repair 2 — the fourth was not a fourth.**
Written: *"the chorus sits in a fourth."* Measured: two cadence notes (F4 at bar 40, E4 at
bar 48) fell outside the band, making the chorus ambitus **equal** to the verse with larger
leaps. Repaired by moving those two notes inside (A4, G4) and giving the Phrygian F→E
cadence to the guitars. Ambitus 8 → 5.

The second repair is the more instructive one: the fix was not to lower the voice. It was
to **move the harmonic event to another instrument** so the voice could stay still while
the ground moved a semitone underneath it. A claim that fails often names the wrong
instrument, not the wrong note.

## What a reproducing lane should carry forward

1. The **claim → render → measure → repair** cycle, run before he hears anything.
2. Anchors as prohibitions, stated in one line so the derivation reads as a decision.
3. A prior measured law aimed **against** its own genre — that is where the surprise lives.
4. The form taken from **his own words**, not invented. He asked for reverse engineering;
   the piece disassembles its riff at bar 17 and restores it at bar 29.
5. The ledger itself. A piece with no measurement record cannot be told from luck.
