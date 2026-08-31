---
name: jamai-morning
description: Run a music session with Jerry in the jamai atelier — read the MIDI and audio he dropped in the Pixel Recorder, transcribe them to ABC, engrave, render, publish to his melody portal, and build the piece with him across turns. Use whenever the subject is Jerry's own compositions rather than his repositories: he says "j'ai déposé des mélodies", "regarde ce que j'ai joué", "transcris ça", "ajoute une mesure", "change l'accord", or launches `jamai-morning`. Not for episode/worktree/repository work — that lives in the episodes atelier.
---

# JamAI morning session

Jerry records music on a phone or a pad, drops it into the Pixel Recorder, and
wants to build the piece with you. He is often not at a screen. This skill is how
that session runs.

The transport (say, listen, note, text, image, video) is the `episode-voice-channel`
skill — read it too. **This file is the method**: how to be right about music you
did not play, and how not to lose it.

## Start

```bash
~/.agents/skills/jamai-morning/scripts/jamai-morning
```

Jerry runs this; it launches the session with a brief already written. It finds
which recorder serves the `jamai` atelier (two run side by side — getting it wrong
writes the music into the episodes atelier silently), runs preflight, lists what is
**still unread**, and claims the next opus number.

**Unread means "not yet attached to any composition"** — not "arrived recently",
and not "arrived since the last launch". Jerry can drop something at ten in the
evening and ask for it two days later; a timestamp marker would have buried it the
moment any session opened in between. So the launcher asks disk the real question:
a file that has been worked on is attached somewhere.

Two consequences: **nothing expires** — a drop stays listed until it is used,
however old — and **reading consumes nothing**, so the command can be run any
number of times and always says the same thing. `--since 2026-08-01` narrows the
window when the backlog gets long.

The corollary is a duty: **attach his source files to the composition they
produced**, not just your own renders. If you transcribe three MIDI into a piece
and never attach them, they stay listed as unread forever and the piece has no
record of what it came from.

If you were launched by it, the brief already carries verified state. Do not
re-verify it. Start by reading his files.

## Compositions are numbered: `op-NNN-slug`

```bash
episode opus "Boucle de minuit"     # -> op-003-boucle-de-minuit
```

Parallel to `ep-NNN-` for episodes, so the two never collide and both sort by when
they happened. "Opus trois" is as unambiguous out loud as "episode four" — Jerry
never has to invent a name before he knows what the piece is. Name it once you can
hear what it is, not before.

*(`boucle-de-minuit`, from 2026-08-02, predates this and keeps its unnumbered slug.
Read it as opus one.)*

## The one rule that decides everything: establish, do not guess

Jerry's material is evidence. Measure it before you say anything about it.

- **MIDI** reads note for note. Parse it and print the actual notes, durations,
  velocities. Three files that look like three ideas may be three layers of one
  loop — that is exactly what happened on the first session, and only the numbers
  showed it.
- **Audio** is measurable: tempo by onset autocorrelation, harmony by pitch-class
  profile, timbre by band energy and spectral centroid. `numpy` and `scipy` are on
  the box; `mido` and `librosa` are **not** (Gerico1007/jamai-melody#3).
- **Name what you hear before proposing anything.** "You landed on the flat sixth
  and left it hanging" tells him you listened. Jumping to a suggestion tells him
  you did not.

And when measurement narrows the field but does not decide, **say that you chose**:

> J'ai CHOISI la grosse caisse. Une ligne à changer : `%%MIDI drummap E 45`
> Aucune comparaison de banques de sons n'a été faite.

A confident sentence covering an unverified claim is the most expensive thing you
can leave behind, because the next reader cannot tell it from a measured one.

## Never name a chord by eye

```bash
python3 ~/.agents/skills/jamai-morning/scripts/jamai-chords.py source.mid 4
```

It prints the chord sounding on **every beat**, marks where it changes, and ends
with the exact list of symbols to place and where. Run it on Jerry's MIDI before
writing a single symbol, then run it again on your rendered ABC and compare: same
labels at the same beats, or **the score is lying to whoever reads it**.

This exists because a chord symbol written once over a bar claims that chord holds
for the whole bar, and his playing changes inside the bar more often than not. On
opus 001 a single `Gadd9` covered four beats; the ninth sounded on exactly one of
them and the other three were `Gsus2`. Every individual symbol was defensible —
the span was not. He caught it by ear before the tool existed.

Two tolerances in that script were each paid for once, and both are in its
comments: `abc2midi` staggers a chord's notes by ~0.021 beat each, so a
four-note chord spans 0.065 and a narrow window silently drops its last note;
and a note ending exactly on the beat belongs to the previous chord.

## Look at the score. Actually look at it.

```bash
abcm2ps -g -O score.svg piece.abc
rsvg-convert -w 1400 -b white score*.svg -o score.png     # then read the PNG
```

Reading SVG source tells you nothing about broken beams, collapsed staves, a clef
flipping mid-bar or sixteen stray rests. The picture tells you all four in one
glance. **Every engraving defect ever found here was found this way.**

## Five silent traps in the ABC toolchain

None raises an error. All five produce a valid file that is wrong.

| trap | what happens | guard |
|---|---|---|
| beaming | decided by **spaces in the source**; dynamics force a space before every note and unbeam the piece | write `CG, CG,` not `C G, C G,` |
| `%%score` | parentheses mean *same staff*; the brace also swaps voice names in pairs (Gerico1007/jamai-melody#2) | `%%score [1 \| 2 \| 3 \| 4]` |
| chord symbols | abc2midi *plays* them: 96 notes instead of 64 | `%%MIDI gchordoff` |
| `gchordoff` itself | it is **per voice**. In the header it only covers the first one, so moving chord symbols to another voice silently restores the accompaniment — 105 notes instead of 70, with thirds appearing on chords that deliberately had none | repeat it inside the voice that carries the symbols |
| chords | unequal durations inside `[...]` are refused, the short note vanishes | give it its own voice |

Plus: FluidSynth reverberates by default and the publisher passes no `-R 0` — cut
it from the ABC with `%%MIDI control 91 0` and `93 0` per voice. And force
`clef=treble` / `clef=bass`, or abcm2ps flips clefs mid-bar.

A canvas with all of these disarmed is proposed in Gerico1007/jamai-melody#4.

## Publish and deliver

```bash
jamai-publish-melody --slug <slug> --note "..." piece.abc    # ABC → MIDI → MP3 + SVG
```

Always give Jerry the listenable link. Then put it where he will find it again:

```bash
episode image <op>  --file score.svg --width 1400 --label "🎼 …"
episode video <op>  --image score.svg --audio piece.mp3 --label "🎬 …"
episode text  <op>  --file analysis.md --lang fr --label "…" --source <clip>
episode note  <op>  --text "quoi / pourquoi / quoi ensuite"   # under 1000 chars
```

`notes` is orientation only. Evidence goes in a section — see
`episode-voice-channel/references/composition-sections.md`.

**Label clips by the role they played, never by their date.** `🔬 PIÈCE À
CONVICTION — le rendu de Jerry sur un autre appareil, il a décidé 6 corrections`
survives a week; `rendu 4 voix, 112 BPM` does not.

## Never lose a source

`~/compositions-jamai` is a git repo (`Gerico1007/assembly-jamai`).

- **Commit after every write** of `composition.json` or a `.abc`. Message = piece
  title + what changes. Stage files **by name** — never `git add -A`.
- **R11: never republish a source without first attaching the outgoing version's
  rendering.** That rendering is its last backup. This rule exists because a
  source was overwritten in place and republished over itself; only its attached
  audio survived, and the version had to be reconstructed from a transcript and
  verified spectrally against it.
- Once a version is committed, pushed, and its rendering attached, editing in
  place is safe. The discipline is what buys that freedom.

## Watching for new drops

```bash
episode watch jamai              # "unchanged 7f3a1c" — 16 bytes when nothing moved
episode watch jamai --interval   # how long to wait before asking again
```

Fingerprint, not inventory; the delay doubles on every quiet round up to an hour
and resets to five minutes the moment something moves. State lives on disk, so a
compacted or replaced agent resumes the loop exactly where it was. **Never
re-list whole directories in a loop** — a previous watch spent eleven hours doing
that: 38 rounds, 27 byte-identical (Gerico1007/dotagents#5).

## Where things are

| path | what |
|---|---|
| `~/Recordings-jamai/` | what Jerry drops — audio **and** MIDI |
| `~/compositions-jamai/` | the atelier; git repo, one folder per composition |
| `~/workspace/jamai-melody/` | tooling; `bin/jamai-publish-melody` |
| `~/workspace/gmusic/.jamai/` | the knowledge — `LEITMOTIF_LIBRARY.md` above all |

Read the leitmotif library before composing. It is the continuity between
sessions, and it now carries motifs Jerry played himself.

## How he works with you

He listens while you build, and interrupts mid-turn with one sentence — *"mets
un G7 à la dernière mesure"*, *"ajoute un tique à la percussion"*. Those are
complete instructions, not sketches: act on them, verify, publish, tell him what
you measured. He will tell you when it is wrong.

Answer in French unless he writes in English. Personas carry fixed languages and
`jamai` is English-only — if the content is French, say so and use a French voice
(Gerico1007/jamai-melody#3).

## What was learned building this

`references/lecons-260802.md` — the session that produced this skill, written for
someone who was not there. Read it if you want to know why any rule above exists.
