# Missing pieces and dependencies

**Status:** measured 2026-08-19, from the recreate question.
**Disc:** `GUILLAUME.md`
**Sisters:** [this time](HOW-WE-DID-IT-THIS-TIME-260819.md) ·
[recreate](RECREATE-THE-WORK-260819.md) ·
[next time](DRAFT-PI-MONO-EXTENSIONS-260819.md)

An LLM handed only `.agents` still cannot do what they did.
This file is the drawing of **why**, and of **what must exist where**.

William is done for today. What follows is left for Jerry.

---

## Jerry — these are yours :)

Not a punch list. Five tensions. The measured map is below if you want
the bones. The creative move is picking **which tension to inhabit**,
not closing all five.

1. **The ear is not in the house.**
   `jamai-midi` / `measure` / `chords` live in `jamai-core` and only
   visit `.agents` as symlinks. You already asked this in GUILLAUME.md.
   Publish? Vendor? A tiny package both `.agents` and the kit can eat?
   Until that choice, a clone of this repo cannot hear.

2. **The method is two Python files on another floor.**
   `gen013.py` (you) and `gen018.py` (William) *are* the work.
   They still point at `/tmp/claude-*`, which dies in 30 days.
   How do those fossils travel without becoming a museum — and without
   bringing `04-captures` (voice, body) into git?

3. **The phone is a tray. Next time it is a worker.**
   Today eury pulls, watches, composes, renders. William's draft says
   watch / voice / songbird / movement / abc / falsify / return live on
   Android, and only render stays here. `extensions/pi/` is zero bytes.
   Which door moves first, and what is allowed to stay stupid on eury?

4. **Two crafts, one number.**
   Your morning method and his park-voice method are not the same
   machine. Both rooms called something opus 018 on the same day.
   The next pack has to know **who is in the room** before it writes a
   bar, or it will remake the wrong lightning.

5. **Something has to stay awake that is not Claude-code.**
   The great results needed a session that stayed open for days.
   Two watches already escaped into systemd. `abies-watch` did not.
   Next time a `pi -e` extension is supposed to be that attention.
   It does not exist yet. What is the smallest thing that can stay
   awake on a phone without becoming another session we nurse?

Issue #32 is the ticket. The four sister files are the brief.
Have fun. :)

Legend: `[in]` inside `.agents` · `[out]` lives elsewhere on eury ·
`[gap]` named, not built · `[android?]` must survive without eury.

---

## The machine, drawn as dependencies

```
                    ┌─ who is in the room ─────────────────┐
                    │  Jerry  → jamai-morning        [in]  │
                    │  William → composing-with-william [in]│
                    └──────────────────┬───────────────────┘
                                       │
 Android drop ──► watch ──► on-drop ──► generator ──► ABC ──► 4 tools ──► hear it
    [out]         [in]       [in]         [gap]       [in*]    [out]       [out]
                   │           │            │                    │
                   │           │            │                    ├ abc2midi      [out]
                   │           │            │                    ├ abcm2ps+rsvg  [out]
                   │           │            │                    ├ fluidsynth    [out]
                   │           │            │                    └ ffmpeg        [out]
                   │           │            │
                   │           │            └ fossils live in the two DROPS [out]
                   │           │              gen013.py / gen018.py
                   │           │              not copied, not path-cleaned
                   │           │
                   │           └ jamai-midi/measure/chords  [out] jamai-core
                   │             (symlinks only inside .agents)
                   │             scipy = /opt/anaconda3 only   [out]
                   │
                   └ episode watch + state
                     scripts/episode                       [in]
                     ~/.local/state/episode-voice          [out]
                     systemd jamai-watch + william-watch   [out]
                     abies-watch = hand-started orphan     [gap]
```

`[in*]` ABC itself is a format, not a file we ship. The **contract** for
writing it is in `RECREATE-THE-WORK-260819.md`. The **examples** are not.

---

## Four layers. What each one needs.

### 1. Watch — file arrives

| piece | where | state |
|---|---|---|
| `jamai-watch` / `ilex-watch` / `abies-watch` | `skills/jamai-morning/scripts/` | `[in]` |
| `episode` | `skills/episode-voice-channel/scripts/` | `[in]` |
| state dir `~/.local/state/episode-voice/` | disk | `[out]` living |
| `jamai-watch.service` / `william-watch.service` | `~/.config/systemd/user/` | `[out]` enabled |
| `abies-watch.service` | — | `[gap]` orphan, ppid 1 |
| leftover `~/.local/state/ilex-watch/` loop | Claude-code tool call | `[gap]` do not restart |
| `atelier-veille/` | skill exists, state empty | not the loop that ran |

Android next time: this whole layer must run **on the phone**.
Today it rsyncs the phone onto eury. `[android?]`

### 2. Measure — what the file is

| piece | where | state |
|---|---|---|
| `jamai-on-drop` | `.agents` script | `[in]` |
| `jamai-midi.py` `jamai-measure.py` `jamai-chords.py` | **symlinks → jamai-core** | `[out]` |
| `jamai-chords-audio.py` | same | `[out]` |
| numpy / scipy | `/opt/anaconda3` only | `[out]` `/usr/bin/python3` has no scipy |
| Groq Whisper | `$GROQ_API_KEY` | `[out]` set on eury; optional |
| `melodie.py` (Jerry pitch track) | only in Jerry's drop | `[out]` not in `.agents` |

GUILLAUME.md already asked: *what is in jamai-core that `.agents` needs?*
Answer, measured: the four `listen/` tools. Without that repo the hook
cannot classify MIDI or audio. They are not published. `[gap]` to
vendor or publish.

Android next time: no anaconda, no scipy, no Groq required.
`jamai-songbird` must bundle its own parser. `[android?]` `[gap]`

### 3. Compose — the work they loved

| piece | where | state |
|---|---|---|
| craft, Jerry | `skills/jamai-morning` | `[in]` |
| craft, William | `skills/composing-with-william` + 3 refs | `[in]` |
| entry that binds them | `RECREATE-THE-WORK-260819.md` | `[in]` now |
| worked example, Jerry | `/home/gmusic/atelier-jerry-origin-1937aa47` | `[out]` |
| worked example, William | `…/songbird-71bbe83b` | `[out]` |
| `gen013.py` / `gen018.py` fossils | those drops `01-generators/` | `[out]` irreplaceable |
| path-cleaned generators in `.agents` | `extensions/pi/jamai-abc/generators/` | `[gap]` folder does not exist |
| header contract (MESURÉ / DONNÉ / CHOISI / REFUSÉ) | recreate file | `[in]` now |
| hardcoded `/tmp/claude-*` in fossils | drops | broken in 30 days |

An LLM that cannot **read the two drops** cannot see the method as
practiced. `.agents` points at them. It does not contain them. That is
deliberate (`04-captures` is voice). The **pointer is the dependency**.

### 4. Render and return — he hears it

| piece | where | state |
|---|---|---|
| `abc2midi` `abcm2ps` `rsvg-convert` `fluidsynth` `ffmpeg` | `/usr/bin` | `[out]` on eury |
| `jamai-publish-melody` | `~/.local/bin` | `[out]` |
| `jamai-score-video.py` `jamai-scroll.py` `jamai-tab.py` | symlinks → jamai-core | `[out]` |
| `jamai-clip.py` `jamai-deglisse.py` | `.agents` files | `[in]` |
| `jamai-defile.py` | named in skills; lives with publish | `[out]` |
| portal `https://localhost:8828` | eury unit pins this | `[out]` |
| `compositions-jamai` git | `~/compositions-jamai` | `[out]` 1.5 G, no remote HEAD |
| SoundFont for fluidsynth | host | `[out]` not named in `.agents` |

These four binaries **are** the list GUILLAUME.md left as
`{{ Jerry list scripts here }}`:

1. `abc2midi`
2. `abcm2ps` + `rsvg-convert`
3. `fluidsynth` (reverb off)
4. `ffmpeg` (via `jamai-defile` / `jamai-clip` / `jamai-publish-melody`)

Android next time: this whole layer stays on eury. That is
`jamai-render`. Silent on the phone. `[android?]` by design.

---

## Next-time tree — named, not built

William's layout, still zero bytes on disk:

```
.agents/extensions/pi/     [gap]
         jamai-watch/      [gap]   [android?]
         jamai-voice/      [gap]   [android?]
         jamai-songbird/   [gap]   [android?]
         jamai-movement/   [gap]   [android?]
         jamai-abc/        [gap]   [android?]
         jamai-falsify/    [gap]   [android?]
         jamai-render/     [gap]   desktop only
         jamai-return/     [gap]   [android?] files-only fallback
.agents/lib/               [gap]
.agents/tests/             [gap]
miadi-orchestration-kit/pi/jamai-extensions   [gap] copy later, not the working tree
termux-docker proof        [gap]   GUILLAUME.md asked; nothing runs it
```

Issue [Gerico1007/dotagents#32](https://github.com/Gerico1007/dotagents/issues/32)
is the ticket. The draft is the spec. No `index.ts` exists.

---

## What an LLM still cannot do

Even with the three docs + the skills, these block "the same work":

| # | missing | blocks | fix, when someone wants it |
|---|---|---|---|
| 1 | jamai-core only as symlinks | measure + some render, if that repo moves | vendor `listen/` into `.agents` or publish the package |
| 2 | fossils not path-cleaned | new generator copies `/tmp/claude-*` | copy `gen013.py` + `gen018.py` into a future `jamai-abc/generators/`, rewrite paths |
| 3 | drops live outside `.agents` | no worked example on a fresh clone | keep the pointers; do not import `04-captures` |
| 4 | `/usr/bin/python3` has no scipy | hook dies under systemd unless PATH is pinned | already pinned in the unit; any new launcher must copy that PATH |
| 5 | SoundFont unnamed | fluidsynth render is host-magic | name the `.sf2` in `jamai-render` README |
| 6 | no local STT for Android | `jamai-voice` without Groq | accept a sidecar `.txt` (draft already says this) |
| 7 | `extensions/pi/` absent | nothing `pi -e` can load | build, one extension at a time, starting with watch |
| 8 | `abies-watch` not a unit | Jerry's phone watch dies with the box | a unit, or it becomes `jamai-watch` on the phone |
| 9 | two opus 018 | a lane remakes the wrong piece | already warned in `composing-with-william`; qualify the room |
| 10 | open Claude-code session | this time the model *was* the orchestrator | next time a pi extension is the orchestrator; not built |

1–4 are why **this time** is not portable.
7–8 and 10 are why **next time** has not started.
5–6 and 9 are traps, not architecture.

---

## What is enough, today, on this machine

On eury, with the two drops readable and jamai-core present:

```
RECREATE-THE-WORK-260819.md
  + skills/jamai-morning | composing-with-william
  + one generator from the matching drop
  + the four host binaries
  + anaconda python
```

That is enough to write the next piece **here**.
It is not enough to write it on ilex, abies, or a clone of `.agents` alone.

The next honest move is not another document. It is either
**vendor `listen/`** (unblocks measure without jamai-core) or
**one `extensions/pi/jamai-watch/index.ts`** (starts next time).
