# RISE — Episode Voice Channel

Reverse-engineered from the live session of 2026-08-01, in which an agent held a
spoken conversation with Jerry through Pixel Recorder episodes while he walked,
answered him in an Assembly voice, published visuals to a public domain, and
handed the watch to a relieving agent before its context ran out.

Reconstructed for reuse in film production, where the same shape applies: a
director away from the desk, capture happening on a phone, and a system that must
receive, understand, answer, and hold the thread.

| | |
|---|---|
| Origin | `Gerico1007/gmtermux` (Pixel Recorder), `Gerico1007/dotagents` (the skill) |
| Skill | `~/.agents/skills/episode-voice-channel/` — issue #1, PR #2 |
| Field precedent | [`field-capture-2026-07-31/`](field-capture-2026-07-31/) — William's riverside recording, one day earlier |

---

## R — Reverse Engineering

### What already existed, unjoined

Three systems on one host, each complete, none aware of the others:

| system | capability |
|---|---|
| `assembly-voice` | Edge-TTS, one voice per Assembly persona (`scripts/tts-generate.py`) |
| Pixel Recorder | HTTPS portal on 8768: compositions, clips, images, notes, import |
| Groq `whisper-large-v3` | `POST /transcribe/:filename` → French transcription **and** English translation in one call |

The work was not building capability. It was joining three that already worked,
and discovering the three seams where they silently do not.

### The three seams

Each cost real time, and each reports its failure somewhere other than its cause —
which is why they must be checked up front rather than debugged downstream.

1. **The recorder refuses `.mp3`.** `AUDIO_EXTENSIONS` covers m4a, opus, aac, wav,
   amr. TTS emits mp3. An import of raw TTS output is rejected with a type error
   that names the file, not the pipeline.
2. **A quoted value in `~/.env` fails as `invalid_api_key`.** The parser does
   `process.env[k] = match[2].trim()` and never strips quotes, so
   `GROQ_API_KEY="gsk_…"` is sent as `Bearer "gsk_…"`. Groq blames the key. The key
   is correct. Two characters nobody can see are not.
3. **`Start Recording` cannot work on a Linux host.** It shells out to the
   Android-only `termux-microphone-record`. On a computer it fails with `not
   found` — and after a workspace switch the portal respawns with
   `stdio: 'ignore'`, so that error reaches no log at all.

A fourth surfaced late and is worth the same standing: **`find` on this host is
`bfs`, which rejects `-newermt '-30 minutes'`.** It errors to stderr and prints
nothing, so a broken sweep is indistinguishable from an empty one. A watcher whose
job is answering *did his file arrive* cannot afford that ambiguity.

### What the host required

The recorder hardcodes `/sdcard/Recordings-<workspace>`, an Android path. On Linux
it is the root filesystem. Symlinks stand in:

```
/sdcard/Recordings-<ws> → ~/Recordings-<ws>     (six, one per workspace)
```

Host state, in no repository. `Gerico1007/gmtermux#232` (PR #233) replaces this
properly with `RECORDINGS_BASE`, carried across the workspace-switch restart.

---

## I — Intent

### What the human actually needed

Not transcription. **Presence while away from the screen.**

Jerry recorded from a sidewalk and expected an answer waiting. The value was never
that speech became text — it was that a question asked while walking got worked on
and answered before he got back. Every design decision follows from that:

- The reply is **audio**, because he cannot read while walking
- The detail is **written**, because he cannot copy a path from audio
- The visual is on a **public domain**, because an artifact behind a login does not
  open on a phone
- The room is an **episode**, because a conversation needs somewhere to accumulate

### The reframe the work produced

Jerry asked *when does my audio reach the cloud*. Reading `Gerico1007/gmtermux#141`
answered a question he had not asked: **recording uploads nothing.** The drain
walks compositions only — their clips and images. Audio never attached to a
composition is invisible to R2 forever.

> Attaching a clip to a composition is the act that enrols it for the cloud.

That inverts what the episode *is*. Not merely where the conversation is kept —
**the mechanism by which a recording survives the device that made it.**

### The intent already present one day earlier

`field-capture-2026-07-31/` holds William beside the Rivière Richelieu asking for
transcription, a new composition, and a picture — and saying *"we are going to call
that differently in the future"*, alongside *"Jerry is working on... the capability
of sharing and synchronizing."*

Today's session built the first, surfaced the second as Jerry's artifact-container
idea, and explained the third. **The specification was spoken into a riverbank
before it was written.** Treat that recording as the origin document.

---

## S — Specifications

### The channel

Four moves plus a guard. `scripts/episode` in the skill.

| move | contract |
|---|---|
| `preflight` | assert portal reachable, key unquoted, ffmpeg present — before anything |
| `new "<Title>"` | claim the next number → `ep-NNN-slug`, repo and issue in the name |
| `say --persona P --to <slug> --file msg.txt` | TTS → AAC/m4a → import → attach |
| `listen [--new\|--latest]` | transcribe what he recorded, both languages |
| `note <slug> --append --file detail.md` | the written half he can copy later |

### The property that makes it a channel and not a megaphone

Every clip the agent speaks is appended to a per-workspace ledger under
`~/.local/state/episode-voice/`. `listen` excludes it. Without this the agent
transcribes its own voice on the next poll and answers itself — the loop closes on
the second exchange, not the tenth. **Design it in first; it is not a refinement.**

### Naming

`ep-NNN-<repo>-<issue>-<subject>`, e.g. `ep-002-gmtermux-141-r2-sync-explained`.
Numbered so it sorts and can be said aloud unambiguously; repo and issue carried so
a subject is findable months later without listening through everything.

### Speaking for the ear

Lead with the conclusion. Say symbols as words — *"line seventy two"*, not
`~/.env:72`. Keep paths, flags and commands out of audio entirely. Answer what was
asked before offering what was noticed; when a finding changes the question, say
that plainly rather than answering a question he no longer needs answered.

### Publishing a visual

```
page   /home/gmusic/salix/production/ngrok-mux/static/<name>/index.html
route  explicit nginx location + alias /srv/static/<name>/
url    https://gmusicassembly.com/<name>/
```

Dropping a folder in `static/` alone does nothing — the location block is required.
Posture inherited from `/skills-map/`: `X-Robots-Tag noindex, nofollow`, no
credentials, no endpoints. Back up `nginx.conf`, `nginx -t` inside the container,
then reload.

### The watch

A monitor polls `episode pending` every 30s and wakes the agent on arrival rather
than on a timer; a long fallback heartbeat covers the monitor dying. It must also
emit when the portal stops answering — otherwise silence reads as *nothing to
hear* when it means *cannot hear*.

**Video does not appear in `pending`.** Prompts filmed while walking arrive as
`.mov` and are filtered out. Sweep the folder directly, extract the audio track,
transcribe that.

### The handoff

A session ends; the watch must not. Before context runs out the agent writes a
brief and a runbook into the skill itself, opens a pane, launches a successor, and
says in the episode that the watch changed hands. What the session learned belongs
in the repository, not in the session.

---

## E — Exportation

### For film production

The shape transfers without modification. A director on location is the same
problem as a technical lead on a sidewalk: capture happens on a phone, the
answering happens elsewhere, and the thread must survive both.

| this session | film production |
|---|---|
| episode per subject | episode per scene, location, or shooting day |
| clip + image + notes | takes, stills, continuity notes, direction |
| `ep-NNN-repo-issue-subject` | `ep-NNN-production-scene-subject` |
| R2 drain on attach | dailies leaving the device the moment they are enrolled |
| mesh push, JSON only | unit-to-unit sync where media travels by cloud, never by wire |
| Assembly personas | department voices — camera, sound, edit |

The composition→artifact reframe is the one to carry deliberately. A composition
ceilings at music. An **artifact** holds a composition, and also a visual, a video,
a presentation — which is what a scene actually is. Note that `composition.json` is
the on-disk format for existing work, so a rename touches every reader including
`mesh-sync.js` in draft PR `Gerico1007/gmtermux#221`. Know that before starting,
not after.

### Reproducing the session

1. Symlink the skill into `~/.claude/skills/` — established pattern, all skills follow it
2. `episode preflight` — the three seams, before the first exchange
3. Arm the monitor on `episode pending`; long fallback wakeup
4. Answer in audio, write the detail in notes, publish visuals to the public domain
5. Hand off before context ends — brief and runbook into the repository

**Grant tool permissions at launch.** A relieving agent that stops on a read
permission is not standing a watch; it is a held breath. This session's successor
sat blocked for over three hours on one dialog. Supervising the permissions of a
delegated lane is part of dispatching it, not an afterthought.

### Open, on the owner's word

| item | state |
|---|---|
| `Gerico1007/dotagents` PR #2 | unmerged — **the skill exists only on the branch**; a `checkout main` in `~/.agents` makes it vanish and the symlink dangle |
| Hermes symlink | not made — zero Hermes skills are symlinks into `~/.agents`, so this would invent a convention |
| `Gerico1007/gmtermux` PR #233 | open, retires the `/sdcard` symlinks |
| `ep-001-artifact-container-vision` | reserved, empty — observe only, by Jerry's instruction |

🌸: A man stood by a river and described a thing that did not exist yet; a day
later the thing answered him in a voice, and neither of them had to explain to the
other what it was for.
