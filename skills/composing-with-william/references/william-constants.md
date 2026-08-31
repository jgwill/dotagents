# What belongs to William specifically

The procedure in `SKILL.md` is general. This file is not — it is the part that makes a
piece *his*, and it goes stale. Re-measure before trusting any number here.

## How he gives input

He records on a phone, walking, in a park, in a kitchen, on a sidewalk. He is **not at a
screen** when he asks. What arrives is:

| trace | where | what it is |
|---|---|---|
| `.m4a` + `transcription_*_EN.txt` | `compositions-william/op<NNN>-<slug>/` | him thinking out loud — subject, anchors, verdicts |
| Songbird `.mid` | same room | his pitches, played by hand |
| motion capture `.jsonl` | Landbase studio | his torso — the phone is worn on the **belly**, so it counts breath, not steps |
| `.png` / `.jpg` | same room | where he is |

**Never ask him for a musical parameter.** He speaks in artists, feelings and situations.
Key, tempo, instrument, form are **measured** from what he gave, or chosen and declared as
a choice he can undo with one word.

## The anchors, and how they are used

Named by him on 2026-08-16: **Metallica** (*Master of Puppets*, *Enter Sandman*),
**Green Day** (*Basket Case*), **Pink Floyd**.

They enter as **prohibitions**:

> The gesture is idiom and free. The melody is not.

Phrygian ♭2, a tritone at the top of a riff, a power-chord shape, a dropped-in downbeat
with no intro — idiom, unowned. A melodic cell from a named work — living rights-holder,
never. His own transcript is the reason: *"it's really easy for you to have the rights to
remix your media"* and *"it would be my own composition"*. This is his constraint,
surfaced, not an external caution.

His verdict when it worked: *"it really feels like we own that music. I don't feel like
I'm listening to Metallica or Green Day or anything like it."* **That sentence is the
acceptance test for stage 2.**

## Consent — the boundaries he set himself

- **2026-08-08** — *"I don't consent that my voice and my original recording goes outside
  of the boundary here. […] The actual MIDI […] file that was recorded."*
  **The MIDI is the offered part. The voice is not.**
- **2026-08-16** — *"it's really a great privilege to use this sound, nobody is authorized
  to use it without my consent."*

Operationally: triggering a transcription sends his audio to a third party — that is his
gesture, not a lane's, even though he does it himself ten times a day. Bringing a copy back
for analysis is permitted; `shred`-ing it afterwards is part of the permission.
**A yes given for one piece is not a yes for the next.**

## Registers — measured, and perishable

| measurement | value | date | status |
|---|---|---|---|
| Songbird take `260816160542` | 119 notes, B3–F5, mostly C4–D5 | 2026-08-16 20:06 | ✱ asserted in two documents, not measured by the scribe |
| park sung take, held notes | median C3, 94.1% between A2 and E3 | 2026-08-16 | from `rispecs/jamai/ava-experience-creative/` |
| his band to leave empty | MIDI 45–53 | 2026-08-16 | same source |

**A tessitura measured yesterday predicts nothing about today.** He sang four semitones
lower in the park than he had the week before, and landed exactly in the interstice
between the bass and the reserved band. Measure the **most recent** take, every time.

## Numbering — two namespaces, one number, one day

| room | opus 018 is… |
|---|---|
| `compositions-william/` | `op-018-refaire-la-foudre` — E Phrygian metal, 66 bars, 4 voices |
| `ava002`/`ava003` studios (`rispecs/jamai/ava-experience-creative/`) | a different piece — *six stations around his note*, built from motion capture |

Both are his, both dated 2026-08-16. **Always qualify the number with the room.** The same
collision exists at 017.

## Where things live

| | |
|---|---|
| his composition rooms | `/home/gmusic/compositions-william/op<NNN>-<slug>/` |
| op-018 source | `/home/gmusic/compositions-william/op-018-refaire-la-foudre.abc` |
| published artifacts | `/home/gmusic/salix/production/ngrok-mux/static/jamai/melody/` |
| the melody manifest | `.../static/jamai/melody/melodies.json` |
| public listen | `https://gmusicassembly.com/jamai/melody/<slug>.mp3` |
| the neighbouring rispec for the same day | `/home/gmusic/.agents/rispecs/nyro/composing-with-william/` (this lane) and `/home/gmusic/.agents/rispecs/jamai/ava-experience-creative/` (the JamAI lane) |

**`compositions-william/` and the device manifest are owned by the JamAI lane.** A scribe
lane reads them and writes nothing into them.

## The channel

He listens on a phone. Therefore:

- **Publishing is the channel.** A question asked only at a terminal is addressed to
  someone who is not there.
- **Audio is the door, writing is the archive.** Composition notes reached 42 000
  characters on 2026-08-16 and stopped being readable on a phone.
- **Score videos scroll left to right with a red playhead. Always.** His standing request
  of 2026-08-14. Never ship a still image with audio.

## What he asks for, underneath

His words, 2026-08-16: *"I'm curious about trying to use Songbird to record myself singing
to see if that would be an entry door to actually create the score and the music that I
need — pretty much like doing my own karaoke, so I would have my own track, my own rhythm,
my own tempo."*

**He is not asking for songs. He is asking for a machine that returns his own body to him
as music he is allowed to own and able to sing.** Every constraint in this skill —
prohibitions instead of models, his ceiling as a hard ceiling, guitar shapes a hand can
reach, rights held clean — serves that one sentence.
