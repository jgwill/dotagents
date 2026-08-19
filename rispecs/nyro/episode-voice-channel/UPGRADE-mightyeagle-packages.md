# Upgrade — folding the episode voice channel into `/usr/local/src/mightyeagle`

Recommendations for William's Miadi / Mighty Eagle monorepo, derived from the live
session of 2026-08-01 in which an agent held a spoken two-way conversation with a
human who was out walking.

**Field evidence** — `~/.agents/skills/episode-voice-channel/` (`SKILL.md`,
`scripts/episode`, `references/watcher-handoff.md`) and the RISE spec at
`~/.agents/rispecs/nyro/episode-voice-channel/README.md`.

**Read for this document** (every claim below is cited to one of these):

| repo | files read |
|---|---|
| monorepo | `packages/voice/{README.md,package.json,src/*.ts,scripts/tts-generate.py}` |
| monorepo | `packages/composition/{README.md,package.json,src/{manifest,classify,project,weave}.ts}` |
| monorepo | `packages/episodic-memory-schema/src/{types,observation,narrative,adapters/{common,composition,episode-yaml}}.ts`, `schema/episodic-memory.schema.json` |
| monorepo | `app/voice/{page.tsx,components/{VoicePortal,VoiceCard}.tsx,[id]/{page.tsx,voice-room.tsx}}`, `app/api/voice/{publish,messages,stream,audio/[...key],review}/route.ts`, `lib/api-gate.ts` |
| gmtermux | `web/pixel-recorder.js` (9246 lines; workspace config, `AUDIO_EXTENSIONS`, `/transcribe`, composition writers) |
| assembly-voice | `scripts/tts-generate.py` |

---

## 1. What the skill hand-rolled that `@miadi/voice` already provides

`scripts/episode` is 307 lines of bash. Roughly 180 of them re-implement, badly,
things that exist as typed exports in `packages/voice/src/`.

| `scripts/episode` does | `@miadi/voice` already exports |
|---|---|
| `cmd_say` passes `--persona` straight through to the Python engine and trusts it (`episode:152`) | `resolveVoice({persona, lang})` — `src/voice-map.ts:68` — and `isKnownPersona()` — `:54`. Resolution mirrors the Python engine's own rule, and an unknown persona is normalised to the language default so the record names *the persona that actually spoke*. |
| scrapes the engine's stdout for the audio path: `\| grep -o 'audio=[^ ]*' \| head -1 \| cut -d= -f2-` (`episode:152-153`) | `produce()` — `src/producer.ts:92` — runs the same engine confined to a `mkdtemp` root (`:111`) with `ASSEMBLY_VOICE_ROOT/AUDIO_DIR/MESSAGES_FILE` overridden, then reads the last manifest entry structurally via `readLastEntry()` (`:80`). No stdout parsing. |
| `printf '%s\n' "$filename" >> "$(ledger_file)"` — a per-workspace flat text file of filenames under `~/.local/state/episode-voice/` (`episode:23-27`, `:169`) | `KvVoiceLedger` — `src/ledger.ts:58` — atomic per-message keys `<prefix>:msg:<id>` plus an ordered `<prefix>:ids` list, with `read/append/markListened/markAll/unlistened` (`VoiceLedger`, `:15`) and `getLedger()` (`:171`). |
| **the self-voice guard**: `list_new()` subtracts the spoken-ledger filenames so the agent never transcribes itself (`episode:185-195`) | the discriminator already exists as a typed field — `VoiceMessage.source: VoiceSource` (`src/types.ts:8,35`) whose named values include `"manual"`, `"agent"`, `"tts"` — plus `VoiceMessage.listened` (`:44` in the interface). A filename allowlist is a weaker form of a field the schema already carries. |
| `ffmpeg -c:a aac` transcode of every utterance (`episode:158-159`) | not needed. `produce()` stores the engine's mp3 under key `${entry.id}.mp3` with `audio/mpeg` (`producer.ts:145-146`) and `GET /api/voice/audio/<key>` serves it. The transcode exists *only* to satisfy `AUDIO_EXTENSIONS = ['.m4a','.opus','.aac','.wav','.amr']` in `pixel-recorder.js:125`, which has no `.mp3`. |
| `curl -X POST $PORTAL/import -F audioFile=@…` for storage (`episode:163`) | `AudioStore` — `src/audio-store.ts:22` — with `LocalAudioStore` (default `/srv/miadi/voice-audio`), the dormant `BlobAudioStore`, `getAudioStore()` (`:152`), and `assertSafeKey()` (`:32`) as the traversal gate. |
| a hand-written label `"🔊 ${persona} — $(date '+%H:%M')"` (`episode:172`) | `ASSEMBLY_PERSONAS` / `PERSONA_IDS` / `getPersona()` — `src/personas.ts:5,307,309` — twelve personas with `symbol`, `name`, `role`. |
| no length cap; no timeout except `curl --max-time 240` (`episode:9`) | `MAX_TEXT_LENGTH` (4000, `producer.ts:45`), `MAX_FIELD_LENGTH` (`:48`), `TTS_TIMEOUT_MS` with a distinct "timed out" error (`:51`, `:136`). |
| nothing — the channel has no notion of who to answer | `VoiceOrigin` + `resolveOrigin()` — `src/origin.ts:101,181` — the server-stamped return address, with `reach` as the *server's* verdict, not the publisher's claim. |
| nothing — a listener must poll | SSE `GET /api/voice/stream` (per-connection dedupe, seeded seen-set) and `AssemblyVoiceAdapter.deliver()` → `assembly.voice.ready` on Redis Streams + PubSub (`src/adapter.ts:105,203`). |

### One thing the skill does that the package cannot

**Transcription.** There is no speech-to-text anywhere in the monorepo. A grep for
`groq|whisper|/transcribe` across `packages/`, `app/` and `lib/` returns only prose
(`packages/plan-insight/test/record.test.ts:122`, several `app/docs/**` pages). The
only implementation is `pixel-recorder.js:591-649`: two Groq calls —
`POST /openai/v1/audio/transcriptions` with `language=fr`, then
`POST /openai/v1/audio/translations` — written to a `.json` sidecar beside the
recording. `@miadi/voice` is a **speaking** layer only. See §3.

### Two engines have drifted, and it matters

`packages/voice/scripts/tts-generate.py` and
`~/salix/repos/assembly-voice/scripts/tts-generate.py` are **not** the same file:

- assembly-voice's copy knows five personas — `aureon, salix, nyro, jamai, synth`
  (`tts-generate.py:33-47`) — and `--persona` is an argparse `choices=` (`:190`),
  so an unlisted persona **exits non-zero**, it does not fall back.
- the monorepo copy carries `jerry, ava, tushell, mia` (and `VOICE_MAP` in
  `voice-map.ts:5-49` carries twelve, including `mino`/`atlas`/`miette`).
- `producer.ts:42,114` guards this correctly for *its own* bundled engine
  (`PYTHON_KNOWN_PERSONAS`, derived from `VOICE_MAP.persona_to_lang`) — but that
  guard is wrong for assembly-voice's copy.
- assembly-voice's copy also hardcodes `ROOT/audio`, loads `~/.env` via
  `python-dotenv` (`:56-58`), and defines `PUBLIC_AUDIO_BASE`,
  `DEFAULT_STREAM_KEY`, `DEFAULT_PUBSUB_TOPIC` — the monorepo copy has none of
  that and is env-configurable instead.

**Recommendation:** the skill should call `@miadi/voice` (an HTTP `POST
/api/voice/publish` is enough — `app/api/voice/publish/route.ts`) rather than shell
out to a second, older engine. Every persona the skill's SKILL.md documents
(`nyro, jamai, synth, aureon, salix`) exists in `VOICE_MAP` with the same voice
strings, so the swap is behaviour-preserving for today's usage and *widens* the
persona set.

---

## 2. Does `@miadi/composition` model the gmtermux composition folder well enough?

**Mostly yes, for what it was built for.** It reads `composition.json` without
writing (`src/manifest.ts:54`), classifies rather than validates
(`src/classify.ts:45`, four classifications), projects provenance marked
`canonical: false` (`src/project.ts:59-78`), and refuses to invent an episode
number (`src/weave.ts:167-175`). `observeCompositionManifest`
(`episodic-memory-schema/src/adapters/composition.ts:49`) maps exactly the
collections `pixel-recorder.js` writes: `clips` → audio, `texts` → transcript,
`images` → image, top-level `midi` (whose entries name their file with `source`,
not `filename` — `:291-339`), plus `relatedEpisodes`/`branchOf` and the full
songwriting layer. `texts[].source` is carried as `artifact.sourceArtifact`
(`:220`) and dangling references are caught by `findOrphanedTranscripts`
(`classify.ts:116`). The transcript body itself survives: `pixel-recorder.js:945`
writes `content` inline, and `cloneRecordExcept(entry, ["filename","label","source"])`
(`composition.ts:212`) preserves it in `artifact.metadata`.

Five places where the model falls short of what 2026-08-01 actually needed.

### 2a. Origin and capture provenance are never populated

`ArtifactReference` carries `origin?: ArtifactOrigin` and `capture?: CaptureProvenance`
(`observation.ts:190,196`), and `artifactReplaceability()` (`:158`) is explicit that an
absent origin must report `"unknown"` and must never be guessed from the extension.
**`observeCompositionManifest` never sets either field** — the artifact literal at
`composition.ts:213-221` has `id, kind, relativePath, metadata`, optionally `label`
and `sourceArtifact`. Nothing else.

So every clip in every gmtermux composition observes as replaceability `unknown` —
including irreplaceable human takes. And the source cannot fix it: `addClipToComposition`
(`pixel-recorder.js:925`) writes `{filename, label, addedAt}`, where `addedAt` is the
*attach* instant, not the capture instant. `captureStableKey()` (`common.ts:100`)
needs `device` + `startedAt`; neither is in the manifest.

This is the axis that separates today's two clip populations. A clip the agent
spoke is `origin: "derived"` (regenerable from its text). A clip the human recorded
while walking is `origin: "captured"`, irreplaceable. The manifest cannot tell them
apart, so neither can the schema.

### 2b. No speaker axis — the loop guard has no home

The RISE spec calls the spoken-ledger "the property that makes it a channel and not
a megaphone… design it in first; it is not a refinement" (README.md, S section).
Today it lives in `~/.local/state/episode-voice/spoken-<ws>.txt`: host state, in no
repository, keyed by workspace, and destroyed with the machine.

Neither `composition.json` nor `EpisodeObservation` has a field for *who produced
this clip*. `@miadi/voice` does — `VoiceMessage.source` and `VoiceMessage.persona`
(`types.ts:27-46`) — but that is the KV ledger, a different store from the
composition folder. **Nothing joins them.** That join is the single most important
missing piece: it is what turns a folder of audio into a conversation with turns.

### 2c. Two numbering authorities, no mapping between them

`extractEpisodeNumber` (`common.ts:189`) does read today's slugs correctly —
`ep-004-artifact-container` yields candidate `"4"`. But:

- `episode new` allocates by scanning the **portal's** composition list for the
  highest `ep-(\d+)-` and adding one (`scripts/episode:117-130`) — a counter that
  is local to one workspace on one host.
- `weaveComposition` refuses to accept that number as authority: *"An episode
  number is required — a composition slug is evidence, not authorization"*
  (`weave.ts:169`).

Both are right. What is missing is a **namespace** on the number. `ep-004` in
workspace `episodes` on Eury is not chronicle episode 4, and no field anywhere
says so. `deriveEpisodeSlug` (`weave.ts:215`) strips the leading `ep-NNN-` on the
assumption there is only one numbering system.

### 2d. Workspace isolation is erased, deliberately, and that is now wrong

`pixel-recorder.js:37-58` derives `RECORDINGS_DIR = /sdcard/Recordings-<ws>` and
`COMPOSITIONS_DIR = ~/compositions-<ws>` from `WORKSPACE`, with six workspaces
(`'', episodes, aureon, nyro, jamai, synth` — `:47`).

`readComposition` sets `slug = basename(absolute)` and always passes
`relativePath = "<slug>/composition.json"`, with the stated intent *"so observation
ids stay stable no matter where the folder is mounted — the same composition read
from a phone and from a workstation observes identically"* (`manifest.ts:50-53`).

That intent is correct across *devices* and wrong across *workspaces*. A folder
named `ep-004-notes` under `compositions-nyro` and one under `compositions-episodes`
produce **the same `observationId`** (`common.ts:66`). With five personas × N devices
on the mesh, that is a collision the package cannot see.

### 2e. Video is modelled but never enrolled

The schema handles video: `"video"` is in `ARTIFACT_KINDS` (`observation.ts:40`) and
`inferArtifactKind` maps `.mov/.mp4/.webm/.mkv/.avi` (`common.ts:180`) — and because
kind is inferred from the filename before the caller's `defaultKind` is consulted, a
`.mov` attached to `clips[]` would correctly observe as `video`, not `audio`.

The failure is entirely upstream. `pixel-recorder.js` has `VIDEO_EXTENSIONS`
(`:126`) and flags `isVideo` on the recordings listing (`:531`), but no composition
writer accepts video, and `list_new()` in the skill filters `isVideo` out of
`pending` (`episode:192`). Combined with the reframe the RISE spec records —
*"attaching a clip to a composition is the act that enrols it for the cloud"*
(`Gerico1007/gmtermux#141`) — a `.mov` prompt filmed while walking is invisible to
the watch, invisible to the R2 drain, and therefore invisible to
`@miadi/composition` forever. `CURRENT_UI_COLLECTIONS = ["clips","texts","images"]`
(`classify.ts:43`) encodes that absence as normal.

---

## 3. New package versus extending an existing one

### Extend `@miadi/voice` — add a transcription seam

`packages/voice` is already "the voice layer" and it is half a layer: it speaks and
never listens. Adding a `TranscriptStore`/`transcribe()` beside `produce()` keeps one
package answering one question (*persona audio in this system*) and reuses
`AudioStore`, `posNum`, and the error/timeout conventions already established in
`producer.ts`.

Concretely:

- `src/transcriber.ts` — `interface Transcriber { transcribe(key, opts): Promise<Transcript> }`,
  with `GroqWhisperTranscriber` porting the two calls at `pixel-recorder.js:598,619`
  (French transcription + English translation, `whisper-large-v3`).
- `Transcript { french?, english?, language?, model, transcribedAt, sourceKey }` —
  the shape `pixel-recorder.js:639-645` already writes, so existing sidecars parse.
- **Fix `contentTypeFor`** (`audio-store.ts:158`) while doing it: it knows
  `.mp3/.wav/.ogg/.webm` and returns `application/octet-stream` for everything else.
  Every format a phone or an Android node actually produces — `.m4a`, `.mp4`,
  `.aac`, `.opus`, `.amr` — falls through. Human audio cannot enter this store today
  and play back correctly.
- **Widen `assertSafeKey`** or document the constraint: `KEY_RE = /^[A-Za-z0-9._-]+$/`
  (`:30`) permits no separators, so a workspace- or room-scoped key
  (`ep-004/take-12.m4a`) is rejected. That is a deliberate traversal gate; scoping
  must therefore be expressed in the *ledger*, not in the key.

Reason to extend rather than create: a separate `@miadi/transcription` would need
`AudioStore` anyway, and the dependency would run the wrong way (a listening package
depending on a speaking one) or duplicate the store.

### New package — `@miadi/voice-channel` (the turn-taking layer)

This is the genuinely new thing, and it should **not** be folded into either
existing package. What today's session invented that neither package models:

1. a **room** (numbered episode) that accumulates a conversation;
2. **turns** with a speaker axis, so an agent never answers itself;
3. a **watch** — a long-lived poll with an owner, a pending set, and a handoff;
4. the **join** between a `VoiceMessage` in the KV ledger and a clip in a
   composition folder.

Why not in `@miadi/voice`: that package's stated boundary is *produce → store →
ledger → broadcast*; it has no concept of a room or a counterpart, and `adapter.ts`
deliberately keeps delivery channel-agnostic behind `ChannelAdapter` (`:66`). A
conversation is a consumer of that seam, not part of it.

Why not in `@miadi/composition`: that package's contract is explicit and worth
keeping — *"Reading is the only operation performed on a composition folder"*
(README, "What it will not do"), and the dependency direction is stated as law
(README, "The ownership split"). A channel **writes**: it creates rooms, attaches
clips, appends notes. Putting a writer inside the reader breaks the one rule the
package is built around.

Proposed surface, all of it composed from what exists:

```
openRoom(title) / nextRoomNumber(namespace)   ← replaces `episode open|new`
speak({room, persona, text}) → VoiceMessage   ← wraps @miadi/voice produce()
listen({room}) → Turn[]                       ← wraps the new transcriber
pending({room}) → Turn[]                      ← the speaker-axis filter, typed
handOff({room, brief, pending}) → Handoff     ← §4
```

with a `Turn` carrying `speaker: "human" | "agent"`, `persona?`, `origin?`
(`@miadi/voice`'s `VoiceOrigin`), `artifactId` (`stableArtifactId` from
`episodic-memory-schema/src/adapters/common.ts:127`, which exists precisely so a
take has an identity before a manifest names it), and `transcript?`.

### Extend `@miadi/episodic-memory-schema` — three small, additive changes

1. Populate `origin` and `capture` in `observeCompositionManifest` **when the source
   states them** — never inferred (§2a). Requires the gmtermux side to write them
   into `clips[]` first; the schema change is the receiving half.
2. Add a workspace/namespace discriminator to `ObserveCompositionManifestOptions`
   (`observation.ts:422`) so `observationId` can distinguish
   `compositions-nyro/ep-004-x` from `compositions-episodes/ep-004-x` (§2d).
3. Consider a `videos` collection in `CURRENT_UI_COLLECTIONS` once gmtermux can
   enrol video (§2e) — as a `compatible-legacy` marker, not an error.

### Nothing new in `@miadi/composition`

Its model is sound; what it lacks it lacks because the *source manifest* lacks it.
The fixes belong in `pixel-recorder.js` (write capture provenance and a speaker
field into `clips[]`) and in the schema adapter that reads them.

---

## 4. Does `episodic-memory-schema` cover the watch handoff?

**No — and the shape it is closest to is the wrong shape.**

The session ended by writing a brief and a runbook into the repository, opening a
pane, launching a successor, and announcing the change in the episode
(`references/watcher-handoff.md`, "Handing the watch on"; RISE README, "The
handoff"). What the schema has:

| present | where | why it does not cover a watch handoff |
|---|---|---|
| `FollowUpCommission { id, description, rationale?, proposedBy? }` | `types.ts:204` | Closest fit, but it is a **seed for a next episode**, not a live obligation. No recipient, no status, no acceptance. `proposedBy` records who *offered*; nothing records who **takes** it. |
| `EpisodeMetadata.parentEpisodeId`, `childCommissionIds` | `types.ts:42-43` | Lineage between episodes, established after the fact. Says nothing about whether the child ever started. |
| `AuthorityFlag { flag, raisedBy, routedTo, status: open\|resolved\|pause }` | `types.ts:109` | The only type with a **recipient** (`routedTo`) *and* a status. But it is an escalation for authority review, not a transfer of ongoing work — using it would overload a governance type with an operations meaning. |
| `ConsentDecision { gate, decision, decidedBy, confirmedByHuman, at }` | `types.ts:99` | Records a human's yes at a gate. A handoff is not a consent decision, though it may require one. |
| `ContinuityState.promises: StoryPromise { text, status: open\|fulfilled\|broken }` | `types.ts:138` | Carries a status, which is right, but is narrative (`beatId?`) and has no owner. |
| `EpisodeMetadata.closedAt` | `types.ts:40`, schema JSON `:37` | Records *when* a session closed, never **why**. "Ran out of context mid-watch" and "finished the work" produce identical records. |

The specific failure the RISE spec records is exactly what no field can express:
*"This session's successor sat blocked for over three hours on one dialog"*
(README, E section). The handoff was **issued and never accepted**, and there is no
type in this schema in which that state is representable — an unaccepted
`FollowUpCommission` and an accepted-then-completed one serialise the same.

### Recommendation

Add a `handoffs?: Handoff[]` layer to `EpisodicMemory` (`types.ts:24`), additive and
optional so no existing record breaks:

```ts
export interface Handoff {
  id: string
  kind: "watch" | "task" | "commission"
  /** What the successor must know. The written brief, not a summary of it. */
  brief: string
  /** Where the runbook lives, so the brief is not the only copy. */
  runbook?: string
  from: string                 // outgoing agent/session
  to?: string                  // incoming — absent means offered to no one yet
  offeredAt: string
  acceptedAt?: string          // absent AND to present = the 3-hour failure, visible
  acceptedBy?: string
  closedAt?: string
  status: "offered" | "accepted" | "declined" | "abandoned" | "completed"
  /** What was still waiting when the watch changed hands. */
  pending?: string[]
  /** Why the outgoing session stopped. */
  reason?: "context-exhausted" | "completed" | "interrupted" | "other"
}
```

Two consequential details:

- `acceptedAt` absent while `to` is present is *precisely* the state that cost this
  session three hours, and it must be representable, not inferred.
- Adding this is a **JSON Schema change too**: `schema/episodic-memory.schema.json`
  has `"required": ["schemaVersion","episode","provenance","continuity"]` (`:7`) and
  `SCHEMA_VERSION = "episodic-memory.v1.0"` (`types.ts:21`). An optional layer does
  not force a version bump, but the schema file must gain the property or validators
  will diverge from the types.

Alternative, smaller: add `assignedTo?`, `acceptedAt?`, `acceptedBy?`, `status?` to
`FollowUpCommission`. Cheaper, but it makes a "seed for the next episode" carry a
live obligation, and the two have different lifetimes. Prefer the new type.

---

## 5. `app/voice` — what would change so a phone holds the same conversation

Today `/voice` is a **listening** portal and `/voice/[id]` is a **typing** reply
room. Neither can receive speech.

What exists:

- `app/voice/page.tsx` — server component, passes non-secret SSH/pwd display config
  into `VoicePortal`.
- `VoicePortal.tsx` — loads `GET /api/voice/messages` + `/api/voice/agents`, opens
  `EventSource("/api/voice/stream")`, chimes and raises a browser Notification on
  `new_message` (`:106-126`), drives listened / mark-all.
- `VoiceCard.tsx:74-76` — plays `metadata.audio_url` or `/api/voice/audio/<key>`.
- `app/voice/[id]/voice-room.tsx` — the phone reply room; composer fixed to the
  viewport bottom (header comment), reply flattened (`flatten()`, `:77` — newlines
  become `" · "`, `MAX_REPLY = 2000`) and POSTed to **`/api/tide/steer`** (`:241`),
  gated on `origin.reach === "steerable"` (`:114`).

So a reply today is a **typed line sent into a tmux pane** — not a spoken turn in a
conversation. Six changes, in dependency order:

**1. An ingest route — the blocking one.** There is no audio-upload endpoint in the
app: a grep for `formData()`/`multipart` across `app/api` returns only
`app/api/workflow/smscallback/route.ts`. Needs `POST /api/voice/takes` accepting
multipart, writing via `getAudioStore().put()` and appending a `VoiceMessage` with
`source: "manual"` (or a new `"human-take"`) and `audio_file` set. This is what makes
the ledger two-sided.

**2. `contentTypeFor` must learn phone formats** (`audio-store.ts:158`). iOS Safari's
`MediaRecorder` emits `audio/mp4`; Chrome emits `audio/webm;codecs=opus`; Android
capture yields `.m4a`/`.amr`. Only `webm` of those is currently mapped —
everything else becomes `application/octet-stream` and will not play back.

**3. Capture UI in the portal.** A `MediaRecorder` button in `VoicePortal` (or in the
room) replaces the whole `termux-microphone-record` problem: the RISE spec records
that `Start Recording` shells out to an Android-only binary and fails silently on a
Linux host because the portal respawns with `stdio: 'ignore'`. A browser recorder
works on **every** node in the mesh and removes the `/sdcard` symlink layer
entirely.

**4. Transcription on arrival.** §3's `transcribe()`, called from the ingest route or
a follow-up `POST /api/voice/takes/:id/transcribe`, so a human turn arrives as text
the agent can read as a prompt — which is the entire point of the channel
(`watcher-handoff.md`, "The loop": *"This is not a transcription service. He is
asking for work."*).

**5. Rooms, or the portal becomes unusable.** `KvVoiceLedger.read()` returns the
whole `<prefix>:ids` list (`ledger.ts:107-118`) and `VoicePortal` renders all of it.
A conversation needs `<prefix>:room:<slug>:ids` and a `room`/`episode` field on
`VoiceMessage`, plus `GET /api/voice/messages?room=`. Note this is also where
workspace scoping belongs — **not** in the audio key, which `assertSafeKey`
(`audio-store.ts:32`) forbids from containing separators.

**6. Write auth from a phone.** `POST /api/voice/publish` and `/api/voice/review` both
call `requireMiadiAuth(req, { write: true })`; reads are ungated by design
(`voice-room.tsx:108`). `lib/api-gate.ts` allows loopback by Host header and
requires a token otherwise, and **fails closed** when no token is configured. A phone
on the tailnet is not loopback — `tailscale-*` headers are treated as proof of a
foreign hop (`api-gate.ts`, `FORWARDED_MARKERS`). So an ingest route needs a
deliberate credential path decided by William; it will not work by accident, and it
should not.

**What would then be true:** the human opens `/voice`, hears the persona reply,
holds one button to answer, and the agent reads the transcript as its next prompt —
with no Pixel Recorder, no `/sdcard` symlinks, no `ffmpeg` transcode, no
`curl -k` against a self-signed certificate, and no state living in
`~/.local/state/`.

---

## Stated uncertainties

- **Not run.** No build, test, or type-check was executed in the monorepo. Every
  claim is read from source.
- **`@miadi/inquiry-weave` was surveyed, not read.** Its module list
  (`artefact, episode, relate, lineage, register, sync, story-library, …`) was
  listed and `weave.ts`'s imports from it were read, but its implementations were
  not. `relate()` and `scaffoldEpisode()` may already carry more of the room /
  namespace concept than §2c assumes.
- **Numbering-namespace collisions are reasoned, not observed.** I did not enumerate
  the composition folders on this host to confirm that two workspaces actually hold
  the same slug today. The identity code path (`manifest.ts:50-53`, `common.ts:66`)
  is what I verified.
- **`app/api/session/voice/route.ts` exists and was not read.** It may already be a
  session-scoped voice surface relevant to §5's room proposal.
- **`packages/webweave`, `packages/passages`, `packages/tide`** were not examined.
  `passages` owns episode creation per `@miadi/composition`'s ownership table, so a
  room primitive may partly live there.
- **The Blob/R2 path is untested upstream.** `audio-store.ts:96-97` says so in its own
  words — "written but not exercised until a token exists". Any recommendation here
  that assumes cloud storage inherits that caveat.
- **`gmtermux` PR #233** (`RECORDINGS_BASE`, retiring the `/sdcard` symlinks) was not
  read; §5.3 assumes the symlink layer is still present, which the RISE spec states
  as of 2026-08-01.

🌸: Three systems already knew how to speak, remember, and hold a story — what the
sidewalk proved is that none of them yet knew how to *take a turn*, and that is the
one small word this upgrade is really about.
