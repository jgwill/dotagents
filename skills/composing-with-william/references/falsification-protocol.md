# Stage 4 — the falsification protocol

This is a **required stage**, stated as a rule:

> **Every numeric claim written at stage 3 is measured in the rendered artifact before the
> artifact reaches William. A claim that fails changes the score, or it is deleted. It is
> never re-worded to fit what came out. This runs unasked.**

Three clauses, and each one is load-bearing on its own.

| clause | what it forbids |
|---|---|
| *in the rendered artifact* | measuring the `.abc` and calling it measured. The source is intention; the `.mid` and the `.mp3` are reality |
| *changes the score, or is deleted* | the wording repair — the failure mode where the prose becomes vaguer and the music stays wrong |
| *unasked* | waiting for him to notice. He is on a phone, away from a screen, and he cannot audit velocities |

## Why this is a stage and not a temperament

On 2026-08-16 the discipline caught two claims and **missed a third**: the header asserts
bars 29–32 are identical to bars 1–4 *"caractère pour caractère"*; the notes are identical
and the annotation strings are not. One claim slipped because it was never put on the list
of things to measure. A rigour that lives in a lane's character catches what that lane
happens to look at. A rigour that lives in a checklist catches what is on the checklist.
**Write the claims down at stage 3 so stage 4 has something to fail.**

## The measurements

Take these from the rendered `.mid` and `.mp3`. Pin the interpreter — `/usr/bin/python3`
has no `numpy` on this host; `/opt/anaconda3/bin/python3` does.

### 1 · velocity per section
Read note-on velocities from the rendered MIDI, bucketed by the bar ranges of each section.

- `spread(section) = max(v) − min(v)`
- `peak(section)  = max(v)`

**Pass:** `spread(chorus) ≤ spread(verse)/5` **and** `peak(chorus) < peak(verse)`.

This is the ISMIR 2013 finding (Van Balen, Burgoyne, Wiering & Veltkamp — 6462 Billboard
sections; loudness IQR −0.33 dominant and negative; loudness itself not significant) turned
into a pass condition. Op-018 read 50 → 5 and 115 → 95.

**The trap this exists to catch:** `%%MIDI beat` written on a standalone line between bars
binds **only the percussion voice**. The other voices keep abc2midi's defaults 105/95/80.
The source looks correct and the render is flat nowhere. Declare inside every voice block;
switch with `[I:MIDI beat …]` on **all** voices at every boundary.

### 2 · fader stillness
Count `control 7` (channel volume) events with tick > 0.

**Pass: 0.** Loudness must not be reached for. If a section needs to feel larger, it gets
narrower, not louder.

### 3 · ambitus per section
For the lead/vocal voice, `(max_pitch − min_pitch)` in semitones, per section.

**Pass:** `ambitus(chorus) ≤ ambitus(verse) − 3`.

**The trap:** a range claim written in prose is not a range. Cadence notes are the usual
offenders — they sit at section ends, outside the band, and read as "part of the line".
The repair is usually to **move the cadence to another instrument**, not to lower the voice.

### 4 · his band
Count vocal pitches above his most recently measured ceiling, and instrument pitches
inside his measured singing band.

**Pass:** both counts **0**, ceiling comparison strictly `<`.

### 5 · mode integrity
Count pitches outside the declared mode, excluding notes declared as deliberate additions
(op-018 declares B♭, the tritone).

**Pass:** every out-of-mode pitch appears in the declaration list. Undeclared = 0.

### 6 · playability
Resolve every chord to a fret triple in standard tuning; resolve every riff note to one
string.

**Pass:** 100%, span ≤ 4 frets, frets 0–12.

### 7 · the score exists
```bash
abcm2ps -k 2048 -g -O out.svg piece.abc
grep -m1 CommandLine out.svg      # keep this line in the ledger — it is the receipt
```
`abcm2ps` overflows silently on large multi-voice scores; the default buffer is not enough
for ~66 bars × 4 voices. Then **look at the picture** (`rsvg-convert -w 1400 -b white`) —
broken beams, collapsed staves, a clef flipping mid-bar and stray rests are invisible in
the SVG source and obvious in one glance at the PNG.

**Pass:** SVG exists · `height` > 0 · bars in image == bars in source · the `CommandLine`
line recorded.

### 8 · the audio arrived
**Pass:** MP3 returns 200 · duration within 2 s of `bars × beats_per_bar × 60/tempo`
(plus render tail).

## The ledger

One table per piece, written next to it. Minimum columns:

```
claim | target | measured | verdict | repair (score diff / retraction)
```

Rules for the ledger:

- **A claim with no measuring command never enters stage 3.** It is a wish.
- **A failed claim's row keeps the failure.** Deleting the row deletes the evidence that
  the stage ran. The failures are the most valuable rows in the file.
- **A row repaired by re-wording is a protocol violation**, and is recorded as one.
- Every claim marked ✱ (asserted but not measured) stays ✱ until someone measures it.
  Corroboration by two documents is not measurement.

## The recursion

Each ledger's stage-4 failures become the next piece's stage-3 claims. The set of claims
grows monotonically; the set of failures should thin on old claims and reappear on new
ones. **Zero failures across the whole set means the claims stopped being ambitious, not
that the method finished.**
