# Draft — Pi-mono JamAI extensions

**Status:** draft for review. Not installed. Not a package yet.
**Date:** 2026-08-19
**Opened by:** William
**Issue:** [Gerico1007/dotagents#32](https://github.com/Gerico1007/dotagents/issues/32)
**Disc:** `GUILLAUME.md`
**Source session:** songbird-71bbe83b (episode 333) + the three Android doors Claude-code watched.

These eight extensions replace the Claude-code loop that woke JamAI when William was recording voice, playing Songbird, or writing a movement-score. Each one is meant to run as a single `index.ts` via `pi -e`, with no npm dependency if the work can be done in-process or with a bundled script. Host binaries (`abc2midi`, `fluidsynth`, `ffmpeg`) live only in `jamai-render`.

Existing skills stay in `skills/`. Extensions read them as files. They do not import `jamai-core` or any other repo.

---

## 1. The eight extensions

**jamai-watch**
Wakes JamAI when a drop on the Android node has finished writing. Classifies it as voice transcription, Songbird MIDI-plus-audio, or movement-score. Dispatches the matching door. Carries the 75-second stable-size rule and the own-import filter so the atelier never hears itself.

**jamai-voice**
Turns a finished voice recording into instructions and prohibitions. Reads an existing transcription first. Extracts subject, anchors, and comments without asking him for a key or a tempo. Hands a GATHER brief onward. Groq is optional; a local text file is enough.

**jamai-songbird**
Reads his Songbird MIDI note for note and measures the raw take: ceiling, register, tempo, pitch-class. Names what sounded before anyone writes a bar. Bundles its own parser. No mido, no librosa. Feeds MEASURE HIM into the generator.

**jamai-movement**
Reads a movement-score JSONL. Cuts stations from stillness and rotation the way gen018 cut the belly take. One second of his body becomes one bar. Emits timing and segment bounds only. No audio toolchain.

**jamai-abc**
Writes one self-contained Python generator from the door measurements. Emits ABC. Header order is his: what is his, what the measure imposes, what I chose, what was tried and refused. Hardcoded `/tmp` paths die here.

**jamai-falsify**
Measures every written claim in the MIDI or ABC before he hears it. A failed claim rewrites the score, never the sentence. This is stage 4 of composing-with-william. Runs with a bundled MIDI parser alone.

**jamai-render**
Turns ABC into MIDI, wave, and m4a when `abc2midi`, `fluidsynth`, and `ffmpeg` are on the box. Silent on Android. Never required for the piece to exist. Desktop only.

**jamai-return**
Puts the score, the sound, and the three provenance blocks back in his room, and speaks if a voice channel is open. Degrades to local files when the portal is down.

Android-viable: watch, voice, songbird, movement, abc, falsify, return (files-only).
Desktop-only: render.

---

## 2. Envisioned layout in this repo

Keep each extension a folder that Pi can load alone. One README at the pack root names the chain. No shared `node_modules`. Shared measurement code, if it appears, is copied into the extension that needs it until a second consumer exists.

```
pi-mono/
  README.md                 # chain map, android vs desktop, how to pi -e
  jamai-watch/
    index.ts
    README.md
  jamai-voice/
    index.ts
    README.md
  jamai-songbird/
    index.ts
    README.md
    midi.ts                 # bundled parser, only if songbird needs it
  jamai-movement/
    index.ts
    README.md
  jamai-abc/
    index.ts
    README.md
    generators/             # path-cleaned fossils from songbird 01-generators/
  jamai-falsify/
    index.ts
    README.md
  jamai-render/
    index.ts
    README.md               # names the three host binaries; refuses to start without them
  jamai-return/
    index.ts
    README.md
```

`skills/composing-with-william`, `skills/jamai-morning`, and `skills/episode-voice-channel` stay where they are. The extensions read those files. They do not move them.

A later publish into `miadi-orchestration-kit/pi/jamai-extensions` is a copy, not the working tree. Review happens here first.

Load one extension:

```bash
pi -e /home/gmusic/.agents/pi-mono/jamai-watch/index.ts
```

Do not add a root `package.json` until a second extension actually shares code.
