# DESIGN — Episode as a first-class mode in gmtermux

**Status: observation only.** Jerry asked explicitly that no refactor be done yet. Nothing here
has been implemented; no file outside this one was modified. Every claim carries a file path and
line number so it can be checked before anything is built.

| | |
|---|---|
| Repo | `Gerico1007/gmtermux` — worktree `/home/gmusic/salix/repos/gmtermux-193`, branch `main` at `05bd8c3` |
| Primary subject | `/home/gmusic/salix/repos/gmtermux-193/web/pixel-recorder.js` (9,246 lines) |
| Cross-checked branch | `141-r2-integration` — worktree `/home/gmusic/salix/repos/gmtermux-141-r2-integration`, draft PR `Gerico1007/gmtermux#221` |
| Spoken origin | William, Rivière Richelieu, 2026-07-31 — `field-capture-2026-07-31/transcription_20260731142235_land-capture_EN.txt` |
| Written origin | `compositions-nyro/111-pi-coding-agent-ilex-mut4ep099-075/EP111_ARTIFACT_MANIFEST.md`, committed 2026-07-04 |
| Spoken intent | Jerry, 2026-08-01 — artifact ⊃ composition ⊃ melody, plus per-room behaviour |
| Related open issues | `Gerico1007/gmtermux#224`, `#227`, `#230`, `#204`, `#209` |

---

## 0. Three sources that already say this

**William, spoken beside a river on 2026-07-31**, one day before the idea was named — he named
the fact that it needed naming:

> *"What I would want after that is a transcription, a new composition, **even though we are
> going to call that differently in the future**. And I would want a picture also of that new
> composition."*

**Jerry, spoken 2026-08-01** — the word and the shape. The JSON file is currently called a
*composition*; the outer container should become an **artifact**. An artifact holds a
composition, a composition holds melodies, and an artifact can also hold a link to a visual, a
video, or a presentation. Second axis: the room should behave differently per workspace — a
worktree/survey episode wants links, diagrams and read-only references; the JamAI room should
give the agent read-only access to the artifact but let it add a melody.

**The repository, written on 2026-07-04 and committed** — four weeks before either statement.
`compositions-nyro/111-pi-coding-agent-ilex-mut4ep099-075/EP111_ARTIFACT_MANIFEST.md` opens:

> `# Épisode 111 — Manifeste des artefacts`
>
> `## Fichiers de source`
> `- 260704152457.m4a — Enregistrement audio source…`
> `- transcription_20260704195933_FR.txt — Transcription française complète…`
> `- composition.json — Métadonnées de composition qui relient audio, transcription, label et épisode.`

Read that third bullet carefully. **A hand-written artifact manifest, inside a composition
folder, lists `composition.json` as one of the things it contains.** The containment Jerry
described was already inverted on disk, in French, by an agent that had no lane to put it in.
The same file goes on to list eleven transformation documents and three GitHub issue URLs —
precisely the `documents` and `links` lanes the schema does not have.

The reframe is not a decision waiting to be made. It is a recognition waiting to be written down.

---

## 1. What the platform already expresses, and where "episode" currently lives

### 1.1 Eight portals, four competing container nouns, and no shared renderer

Each portal is a standalone Node/Express (or raw `http`) process serving its own HTML from
template literals.

| Portal | Actual port(s) | Container noun it establishes | Declared at |
|---|---|---|---|
| Ritual Console | 8769 / **HTTPS 8443** | *recording*, *plan*, *rite* | `web/ritual-console.js:24-25` |
| Pixel Recorder | 8767 / **HTTPS 8768** | *recording*, *composition*, *workspace* | `web/pixel-recorder.js:52-53` |
| Clipboard QR Gallery | 8766 | *capture*, *gallery*, **session** | `web/clipboard-qr-gallery.js:24` |
| Clipboard Session View | 8767 | **session** (archived, TLID-named) | `web/clipboard-session-view.js:24` |
| Workspace Portal | 8770 | **session** (GMDAY day-folder) | `web/workspace-portal.js:19` |
| ABC Player | **8771** | **melody** | `web/abc-player.js:24` |
| Forest Conductor | 8769 / **HTTPS 8770** | **session**, **take** | `web/forest-conductor.js:45-46` |
| Forest Web Terminal | 8771 / **HTTPS 8772** | **session** (tmux PTY) | `web/forest-web-terminal.js:31-32` |

Two header comments are stale and will mislead anyone reading before running: `web/abc-player.js:7`
says `Port: 8770` (actual 8771), and `web/ritual-console.js:7` says `Port: 8769` when users
actually reach 8443.

Four port collisions exist — 8767, 8769, 8770, 8771 each appear twice — tolerable today only
because the colliding pairs run on different hosts (Forest Conductor and Forest Terminal are
Eury-side per `web/forest-conductor.js:6-7`; the rest are Termux-side). **Free in the range:
8773-8790.**

### 1.2 The vocabulary already in the codebase

A whole-word scan of user-visible strings across all eight portals:

- **`artifact` — zero occurrences in any portal's code.** The word exists in this repository
  only in hand-written markdown inside composition folders: `EP111_ARTIFACT_MANIFEST.md` and
  `compositions-nyro/ep097-ceremony-agent-skills/EXTENSION_SPEC_2026-07-04_ARTIFACT_OUTPUT_DESCRIPTIONS.md`.
- **`episode` — zero occurrences in any portal's user-visible text.** In `pixel-recorder.js` it
  appears three times, all as a *workspace identifier* (`:34` comment, `:41` the `WORKSPACE_INFO`
  entry, `:47` nav ordering), plus twice in the launcher `.shortcuts/web-portals.sh:14,45`.
- **`session` is the most overloaded noun in the platform**, meaning four different things:
  a clipboard capture-run (`web/clipboard-qr-gallery.js:580` — `📋 Current Session`), a GMDAY
  day-folder (`web/workspace-portal.js:772` — `<h2>Recent Sessions (Top 20)</h2>`), a Forest
  recording pullback (`web/forest-conductor.js:532` — `<h2>🎧 Forest Session Pullback</h2>`),
  and a tmux PTY (`web/forest-web-terminal.js:173` — `<button id="new-session">New Session</button>`).
- **`take` already exists and is already film-shaped.** `web/forest-conductor.js:533` —
  `<div class="panel-kicker">Auto-pulled takes on STOP</div>`; take-cards at `:637`, `:650`;
  `lastTake` at `:527`. Also `lastCompletedForestTake` / `getLatestForestTakeFromDisk()` in
  `web/pixel-recorder.js:160`, `:274`, `:302`.
- **Unclaimed in every user-visible string:** *artifact*, *episode*, *board*, *room*, *deck*,
  *thread*.

**"Compositions" is already ambiguous in the wild.** It is the nav label pointing at ABC Player
(port 8771) in three portals — `web/abc-player.js:459`, `web/clipboard-qr-gallery.js:561-571`,
`web/ritual-console.js:1580-1586` — while in Pixel Recorder the same label points at
`/compositions` (`web/pixel-recorder.js:1795`). And ABC Player's label disagrees with its own
data: it calls itself "Compositions" but scans `~/gmday-plans` for `.abc` files
(`web/abc-player.js:26-33`, `:104`).

### 1.3 Where "episode" lives today — three implicit homes, none of them a type

**(a) As a workspace name.** `web/pixel-recorder.js:39-46`:

```js
const WORKSPACE_INFO = {
  '':         { label: 'Main',     emoji: '📂', color: '#6b7280' },
  'episodes': { label: 'Episodes', emoji: '🎙️', color: '#ec4899' },
  ...
```

The only declaration of the word. `WORKSPACE_INFO` is purely cosmetic — label, emoji, colour.
It carries no behaviour. The switch endpoint validates membership (`:3376-3378`) and throws the
name into an env var (`:99`) before restarting. **Nothing downstream ever branches on which
workspace it is** — verified: zero per-workspace or per-persona branching exists in any of the
other seven portals.

**(b) As a slug convention invented outside the repo.** The `episode-voice-channel` skill mints
`ep-NNN-<repo>-<issue>-<subject>`. On disk right now:

```
~/compositions-episodes/ep-001-artifact-container-vision/
~/compositions-episodes/ep-002-gmtermux-141-r2-sync-explained/
~/compositions-episodes/ep-003-dotagents-1-episode-voice-channel-skill/
~/compositions-episodes/worktree-territory-map/
```

The convention is load-bearing and entirely invisible to the code. `slugify()`
(`web/pixel-recorder.js:819-824`) has no notion of it; the list page sorts by `updated` (`:850`),
so the numbering that makes episodes sayable aloud does not survive into the UI.

**(c) As a composition that uses almost none of the schema.** This is the sharpest evidence, and
it is empirical rather than argued.

| workspace | compositions | using `chords` or `sections` |
|---|---|---|
| `~/compositions` (Main) | 23 | **14** |
| `~/compositions-episodes` | 4 | **0** |
| `<repo>/compositions-nyro` (committed) | 2 | **0** |

Every episode on disk uses exactly three of thirteen schema fields — `clips`, `images`, `notes` —
leaving `chords`, `sections`, `rhythm`, `bpm`, `bpmDetected`, `key`, `capo` at their created
defaults from `web/pixel-recorder.js:875-879`. Meanwhile `ep-002` carries 2,499 characters of
notes and `worktree-territory-map` carries 3,690: **the notes field is doing the work of a
document lane it was never designed for.**

The leak runs both ways. `~/compositions/gmtermux-cloudflare-r2-ep128/` is an episode by every
structural measure (0 chords, 3 clips, 2 images, 1 text) sitting in the music workspace, captured
before the Episodes room existed.

### 1.4 The manifest is already blind to most of what an episode contains

The two committed compositions under `compositions-nyro/` make this quantitative:

| folder | files on disk | files the manifest knows about |
|---|---|---|
| `111-pi-coding-agent-ilex-mut4ep099-075/` | 20 | 2 clips |
| `ep097-ceremony-agent-skills/` | 33 (plus `scripts/`, `skills/`) | 2 clips, 218 chars of notes |

`ep097-ceremony-agent-skills/composition.json` describes itself in its notes as *"reusable agent
skills for API-triggered ceremony actions… and **film-production ceremony support**"* — William's
context exactly — while declaring two audio files and nothing else. Thirty-one markdown documents,
a `pending_actions.json`, a `relational_narrative_engine_sketch.json`, a `scripts/` tree and a
`skills/` tree are on disk, in git, and invisible to every reader of the manifest.

### 1.5 The composition detail page is already an episode screen wearing music clothes

`GET /compositions/:slug` (`web/pixel-recorder.js:4506-7142`) renders, in order:

| region | lines | serves an episode? |
|---|---|---|
| back-link "← All Compositions" | `:5124` | yes |
| title + workspace badge + slug | `:5126-5134` | yes |
| record bar (Record / Pause / Stop) | `:5137-5145` | yes |
| **Details** — Sections, Key/Tonality, Capo, Rhythm, BPM | `:5147-5197` | **no — dead weight** |
| Details — Notes textarea | `:5198-5201` | yes, and overloaded |
| **Clips (N)** — play/watch/crop/delete | `:5207-5273` | yes — this is the audio thread |
| **Images (N)** | `:5274-5301` | yes |
| **Lyrics / Transcriptions (N)** | `:5302-5328` | yes, misnamed |
| Save / Share JSON / Delete | `:5329-5331` | yes |

Four of five sections already serve an episode. What is missing is not a page — it is (i) lanes
for links and documents, and (ii) permission to hide the tonality controls.

### 1.6 The storage lane that already exists but is undeclared

`GET /api/compositions/:slug/images/:filename` (`web/pixel-recorder.js:4056-4063`) joins the slug
directory and streams **any file it finds** — no extension filter. This is why
`Gerico1007/gmtermux#224` reports `The_Visual_Bouquet.pptx` returning HTTP 200 from a route named
`/images/` while being invisible in the UI. The storage lane is already open; the metadata and
the renderer are what is missing.

`MIME_TYPES` (`:132-138`) covers audio, video, MIDI and images. `.pdf` and `.pptx` fall through
`getMimeType()` (`:140-143`) to `application/octet-stream`.

### 1.7 Melodies are the one piece genuinely elsewhere

"Melody" has two disconnected homes:

1. **`.abc` files** — scanned by `web/abc-player.js:104` from `~/gmday-plans`
   (`:26-33`), a tree with no relationship to `~/compositions*`. That portal exposes
   `GET /api/melodies` (`:817`) and renders `${melodies.length} melodies from GMDAY Agent`
   (`:465`). It has **no write path** and no knowledge of compositions.
2. **`.mid` files** — parsed by `addMidiToComposition()` (`web/pixel-recorder.js:1013-1115`),
   stored at `data.sections[i].midi` (`:1101`) or `data.midi[]` (`:1107-1108`).

The innermost noun of Jerry's model is the one currently split across two processes, two ports and
two storage roots. That is the strongest sign the model describes something real: it names a
containment the filesystem does not yet have.

---

## 2. Artifact ⊃ Composition ⊃ Melody — a model that preserves `composition.json`

### 2.1 The reframe stated structurally

Today the folder *is* the composition and `composition.json` *is* its manifest. Jerry's model
inserts a level above and formalises a level below:

```
ARTIFACT           the room / the episode — what a capture session produces
├── composition    the musical reading of the material (chords, sections, key, bpm)
│   └── melody     an .abc tune or a parsed .mid line
├── clips          audio + video takes
├── images         stills, screenshots, diagrams
├── documents      pdf, pptx, md — the deck lane #224 asks for
├── links          URLs to published visuals, videos, presentations, issues
└── notes          the written half
```

The key observation: **artifact and composition already share one directory and one manifest, and
they should keep sharing them.** This is not a data move. It is a declaration of *kind* plus two
new lanes.

### 2.2 The additive changes

**(1) A `kind` discriminator at the top level.**

```json
{ "kind": "episode", "kindVersion": 1 }
```

Absent means `"composition"` — so all 29 files on disk today are already valid without being
touched. `kind` selects which lanes render and which room capabilities apply (§3). Proposed
values: `composition` (music, the current default), `episode` (a capture session), `survey` (a
worktree/reference room), `production` (a film scene or shooting day, for William).

**(2) A `links[]` lane** — the piece with no existing home at all. Verified: zero occurrences of
`data.links`, `publishedUrl`, or any URL-valued composition field anywhere in `pixel-recorder.js`.

```json
"links": [
  { "url": "https://gmusicassembly.com/worktree-map/",
    "title": "Worktree territory map",
    "rel": "visual",
    "addedAt": "2026-08-01T…" }
]
```

`rel` ∈ `visual | video | presentation | reference | issue | commit`. This carries "a link to a
visual, a video, or a presentation" without pulling bytes onto the phone. It is also what
`EP111_ARTIFACT_MANIFEST.md` was hand-rolling: three GitHub issue URLs written into prose because
there was nowhere structured to put them.

**(3) A `documents[]` lane** — already specified in detail by `Gerico1007/gmtermux#224`, which
proposes the field name `files[]` with `{filename, label, kind, mime, previewFilename, addedAt}`
and a PDF-preview path for PPTX decks. **Adopt #224's shape verbatim rather than inventing a
parallel one.** Reconcile the *name* once, in that issue, before either lands: `#224` says
`files`, this document says `documents`. One of the two, chosen deliberately.

Note the relationship: `#224` solves the same tension one level down — a lane *inside* the
composition. Jerry's reframe adds a container *outside* it. They are compatible and should ship
as one change, with `kind` deciding whether the deck lane renders at all.

**(4) `melodies[]` — deferred, deliberately.** `sections[i].midi` and `data.midi[]` already work
and are exercised by real data. A unified `melodies[]` covering `.abc` and `.mid` is the correct
end state, but it is the **only** part of this model that would touch existing populated fields.
Do it last, additively (write `melodies[]` alongside, keep `sections[i].midi` authoritative until
the ABC portal can write), and never as part of the rename.

### 2.3 Why the migration is non-destructive — exactly

**The filename `composition.json` does not change. The directory layout does not change. No
existing key is removed, renamed, or re-typed.** "Artifact" is a *kind* the manifest declares, not
a new file. The entire migration:

| step | action | risk |
|---|---|---|
| 1 | Read `kind` with `kind ?? 'composition'` as fallback | none — no write |
| 2 | Add `links` / `documents` to the `updateComposition` allowlist (`:889`) | see §2.4(b) |
| 3 | Render new lanes only when present and non-empty | none |
| 4 | Backfill `kind: "episode"` on the four `~/compositions-episodes/*` files | one-line write, reversible |

Step 4 is the only write, touches four files, and is reversible by deleting one key. There is no
rewrite pass, no migration script, and no moment at which old and new readers disagree about where
data lives.

**Why unknown keys survive today** — verified across both branches:

- `getComposition()` (`web/pixel-recorder.js:858-864`) does a whole-object `JSON.parse` and
  returns it — no projection.
- `GET /api/compositions/:slug` (`:3920-3924`) returns that object raw.
- Every mutator — `addClipToComposition` (`:912-931`), `addTextToComposition` (`:934-958`),
  `addImageToComposition` (`:1118-1137`), `removeImageFromComposition` (`:1140-1157`) — is
  read-modify-write on the fully parsed object and re-serialises **all** of it.
- On `141-r2-integration`, the mesh push sends the whole parsed object as the wire payload
  (`web/pixel-recorder.js:4230`) and the receiver writes it verbatim (`:4271`) — no pick, no
  allowlist.

A new top-level key, once on disk, round-trips through the UI, the REST API, the R2 drain and a
device-to-device mesh sync without loss.

### 2.4 The one path that destroys it, and the one that silently swallows it

Both are pre-existing defects, not consequences of the reframe.

**(a) `POST /api/forest/compositions/:slug` — total replace.** `web/pixel-recorder.js:732-757`:

```js
const data = req.body;                                        // :740
data.updated = new Date().toISOString();                      // :741
fs.writeFileSync(jsonPath, JSON.stringify(data, null, 2));    // :744
```

Unauthenticated, no merge, no allowlist, no backup, non-atomic. Any caller PUTting a partial body
erases every key it did not send — including `kind`, `links`, `documents`, and today's `images`.
On `141-r2-integration` this is `:891-915`, and it is the one composition writer that did **not**
get `writeJsonAtomic` or a `.sync-backups` copy.

**(b) `PUT /api/compositions/:slug` — the allowlist swallows new keys.**
`web/pixel-recorder.js:885-901`:

```js
const allowed = ['title','chords','sections','rhythm','bpm','bpmDetected','key','capo','notes'];
```

It iterates the allowlist and merges *into* the parsed object, so keys already on disk survive —
but a new key sent through this endpoint is dropped silently with a 200 response. Adding `kind`,
`links` or `documents` requires editing line 889, or the REST edit path will appear to work and
persist nothing. Same line, `:1049`, on the R2 branch.

**(c) `getCompositions()` projection — invisible, not destroyed.** `:826-851` picks exactly eight
fields (`:837-846`). It never writes, so it destroys nothing — but any new top-level field is
invisible to the `/compositions` list page. An episode badge on the card requires adding `kind` to
that projection.

### 2.5 Naming: what the UI calls it vs. what the file is called

- **On disk, `composition.json` keeps its name forever.** Every reader on every branch depends on
  that string, including the `@miadi/composition` package referenced in
  `Gerico1007/gmtermux#227`, which "can read gmtermux composition folders, classify them, observe
  their artifacts."
- **In the UI, the noun follows `kind`** — "Episode" when `kind === 'episode'`, "Composition"
  otherwise.
- **In the API, add aliases rather than replacing routes.** `/api/artifacts/*` may forward to
  `/api/compositions/*`; the old paths never go away.

This keeps the rename a UI change rather than a distributed-systems change.

---

## 3. Per-workspace capability — the smallest mechanism

### 3.1 What the switcher already knows

Room identity is already one global, derived once at boot from one env var:

```js
const WORKSPACE = (process.env.WORKSPACE || '').toLowerCase().trim();   // :37
```

The switch is a validated name (`:3376-3378`), a 409 interlock while recording (`:3382-3384`), and
a restart carrying only that variable (`:99` — `export WORKSPACE='<name>'`, via `tmux
respawn-pane` at `:103` or a detached spawn at `:110`). `WORKSPACE_META` (`:48`) fans that name out
to label, emoji and colour, and `workspaceBadgeHTML()` (`:80-89`) renders it into every page header.

The room is already computed, already global, already visible, and already survives the restart.
Nothing new needs plumbing.

### 3.2 The proposal: extend `WORKSPACE_INFO`, add one helper, and nothing else

```js
const WORKSPACE_INFO = {
  '':         { label: 'Main',     emoji: '📂', color: '#6b7280',
                kind: 'composition', can: ['record','edit','melody','image','link','doc','delete'] },
  'episodes': { label: 'Episodes', emoji: '🎙️', color: '#ec4899',
                kind: 'episode',     can: ['record','edit','image','link','doc','text'] },
  'nyro':     { label: 'Nyro',     emoji: '♠️', color: '#a855f7',
                kind: 'survey',      can: ['link','doc','image','note'] },
  'jamai':    { label: 'JamAI',    emoji: '🎸', color: '#f59e0b',
                kind: 'composition', can: ['melody'] },
  ...
};
const CAN = (c) => (WORKSPACE_META.can || []).includes(c);
```

One derived helper. Every render site and every mutating route consults `CAN(...)`. That is the
whole mechanism — no permissions file, no role table, no token, no per-user state. **The room is
the role.**

This answers Jerry's two examples exactly:

- **Nyro / survey room** — `can: ['link','doc','image','note']`. No `record`, no `edit` of the
  artifact body, no `delete`. Links, diagrams and read-only references, which is what he described
  for a worktree survey.
- **JamAI room** — `can: ['melody']` only. The agent sees the whole artifact and can add a melody;
  it cannot edit notes, delete a clip, or touch the artifact body. Read-only access to the
  artifact, writable only in the melody lane.

### 3.3 Three properties this must have to be honest

**Enforce server-side, not by hiding buttons.** The agent's path into this system is `curl`, not
the DOM — the entire episode voice channel is REST calls (`skills/episode-voice-channel/SKILL.md`).
A hidden button is not a boundary. `CAN(...)` must gate the route handlers (`:3926`, `:3932`,
`:3938`, `:3947`, `:4013`, `:4036`, `:4049`) and return `403` naming the room, so an agent that
hits the wall learns *which room said no* rather than getting a silent no-op.

**Make read-only visible, and reuse the precedent that exists.** `web/clipboard-session-view.js`
is the only portal in the platform with an explicit read-only contract, and it states it three
ways at `:305-307`:

```html
<strong>🔒 Read-Only Archive</strong>
<div class="readonly-badge">ARCHIVED SESSION</div>
<p …>This is a historical session. Changes are not saved.</p>
```

with `.readonly-badge` styled at `:143`. That is the pattern — lock glyph, pill, and one plain
sentence. Copy it rather than inventing a fourth affordance.

The `workspace-isolation` foundations packet in this repo
(`foundations/workspace-isolation/synthesis.md`, Field 5) grounds why: Norman on mode errors —
*"result from inadequate feedback and indication of the state of the system"* — and Sellen,
Kurtenbach & Buxton measuring that a visible mode indicator significantly reduced mode errors
(novices 4.4 → 2.6, experts 6.3 → 3.9). The badge already distinguishes on three channels (colour
+ emoji + name), which the same packet argues is the requirement against Norman's row-of-lights
warning.

**Do not add a confirmation dialog.** The same packet, citing Böhme & Köpsell's 80,000-user field
experiment and Norman's *"Yes, yes, yes, yes. Oh dear!"*, establishes that the `confirm()` already
in `workspaceBadgeHTML()` (`:88`) is habituated through and is not protection. The real interlock
is structural — the 409 at `:3382-3384`. Enforce, show, and make it reversible.

### 3.4 What this deliberately does not do

`Gerico1007/gmtermux#226`'s design — one process, one workspace, restart to switch — already makes
the capability set a boot-time constant, which is the cheapest correct form. The cost, named
honestly by the same foundations packet quoting Krebs et al., is that this is a **multi-instance**
design: no cross-room query, no cross-room capability. That is the right trade when chosen
deliberately and a defect when discovered later. It is chosen here.

---

## 4. The Android episode screen

An episode is a conversation that accumulates. The current detail page is a form with collapsible
sections — right for a song, wrong for a thread, because it puts the newest thing furthest down
four collapsed regions.

### 4.1 Episode list

```
┌────────────────────────────────────────────────┐
│ ☰                        🎙️ Episodes ▾  ABIES ▾│
├────────────────────────────────────────────────┤
│  🎙️ Episodes                                   │
│  [ + New Episode ]                             │
│                                                │
│ ┌────────────────────────────────────────────┐ │
│ │ ep-003 · dotagents #1 episode-voice-chan…  │ │
│ │ 🔊 4  🖼 0  🔗 2  📄 0        2h ago  ☁︎ │ │
│ │ ▸ "the watch changed hands…"                │ │
│ └────────────────────────────────────────────┘ │
│ ┌────────────────────────────────────────────┐ │
│ │ ep-002 · gmtermux #141 r2-sync-explained   │ │
│ │ 🔊 1  🖼 0  🔗 1  📄 0        1d ago  ☁︎ │ │
│ └────────────────────────────────────────────┘ │
│ ┌────────────────────────────────────────────┐ │
│ │ worktree-territory-map          SURVEY     │ │
│ │ 🔊 6  🖼 1  🔗 3  📄 0        1d ago  ⏳ │ │
│ └────────────────────────────────────────────┘ │
└────────────────────────────────────────────────┘
```

Changes from the card at `web/pixel-recorder.js:4384-4389`: sort by episode number when the slug
carries one, not by `updated` (`:850`) — the numbering exists so episodes can be said aloud in
order, and today the sort discards that. Chord and section badges (`:4387-4388`) are replaced by
lane counts. `☁︎` / `⏳` is the R2 cloud/pending badge that already exists on `141-r2-integration`.

### 4.2 Episode detail — the thread

```
┌────────────────────────────────────────────────┐
│ ← Episodes               🎙️ Episodes ▾  ABIES ▾│
├────────────────────────────────────────────────┤
│ ep-003 · episode-voice-channel skill           │
│ ep-003-dotagents-1-episode-voice-channel-skill │
│                                                │
│ ┌── AUDIO THREAD ──────────────── newest ▲ ──┐ │
│ │ ● 🧵 Synth · agent          14:32   1:04  │ │
│ │   ▶ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ☁︎  │ │
│ │   "The transcription failure was two…"     │ │
│ │                                     [more] │ │
│ ├────────────────────────────────────────────┤ │
│ │ ○ Jerry · recorded          14:19   0:47  │ │
│ │   ▶ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ☁︎  │ │
│ │   FR "…ça devrait s'appeler un artifact"   │ │
│ │   EN "…it should be called an artifact"    │ │
│ ├────────────────────────────────────────────┤ │
│ │ ○ Jerry · recorded          13:58   2:11  │ │
│ │   ▶ ━━━━━━━━━━━━━━━━━━━━━━━━━━━  ⏳ pending│ │
│ │   [ Transcribe ]                           │ │
│ └────────────────────────────────────────────┘ │
│                                                │
│ ┌── VISUALS ─────────────────────────── 3 ──┐ │
│ │ ┌──────┐ ┌──────┐ ┌──────┐                │ │
│ │ │ img  │ │ 🔗   │ │ 📄   │                │ │
│ │ │      │ │ map  │ │ deck │                │ │
│ │ └──────┘ └──────┘ └──────┘                │ │
│ │  still    published    The_Visual_        │ │
│ │           visual ↗     Bouquet.pdf ↓      │ │
│ └────────────────────────────────────────────┘ │
│                                                │
│ ┌── NOTES ───────────────────────── 6.9k ──┐  │
│ │ ## What breaks, and why it is not obvious │  │
│ │ The recorder rejects `.mp3`. Its          │  │
│ │ AUDIO_EXTENSIONS list covers m4a, opus…   │  │
│ │                              [ Expand ]   │  │
│ └────────────────────────────────────────────┘ │
│                                                │
│ ┌────────────────────────────────────────────┐ │
│ │  ●  RECORD REPLY          ⏸    ⏹          │ │
│ └────────────────────────────────────────────┘ │
└────────────────────────────────────────────────┘
```

Design decisions and their grounding:

- **The audio thread is one merged, newest-first list**, not the flat `Clips (N)` section at
  `:5207`. Each entry pairs the clip with its transcription. Today `clips[]` and `texts[]` are
  separate arrays (`:912-931`, `:934-958`) — but `texts[i].source` (`:949`) already carries the
  originating filename, so **the join is computable with no schema change at all.**
- **Speaker attribution.** `● agent` vs `○ recorded` is exactly the distinction the voice
  channel's anti-loop ledger under `~/.local/state/episode-voice/` already maintains (`SKILL.md`,
  "Listening to Jerry"). Today that knowledge lives in host state outside any repository. Moving
  it into the clip entry — `"by": "synth"` / `"by": "jerry"` — makes the thread legible and removes
  the channel's dependence on a file no repo owns.
- **Both languages inline.** `texts[]` already stores `lang` (`:946`) and Groq returns FR + EN in
  one call. The page currently renders them as two undifferentiated entries under "Lyrics /
  Transcriptions".
- **`⏳ pending` + `[ Transcribe ]` inline.** `POST /transcribe/:filename` (`:3569`) exists; the
  episode page has no button for it, so the human on a phone cannot trigger the thing the page is
  entirely about.
- **VISUALS is one row, three kinds** — local image (served by `:4056`), external link (new
  `links[]`), document card (`#224`'s lane). One row because on a phone the question is "what can
  I look at", not "what is the storage class".
- **Record Reply is pinned to the bottom.** The record bar is currently at the *top*
  (`:5137-5145`), above four collapsed sections. In a thread the reply belongs where the thread
  ends. Honest constraint from the skill: this button shells out to `termux-microphone-record` and
  works only on Android — on Eury the equivalent is Import.
- **What is gone.** Key/Tonality, Capo, Rhythm, BPM (`:5157-5197`). Zero of four episodes use any
  of them. `CAN('melody')` is false in the Episodes room, so they do not render — the same
  mechanism as §3, not a special case.

### 4.3 Survey / worktree room — same page, different lanes

```
┌────────────────────────────────────────────────┐
│ ← Surveys      ♠️ Nyro ▾  READ-ONLY   ABIES ▾ │
├────────────────────────────────────────────────┤
│ worktree-territory-map                 SURVEY  │
│                                                │
│ ┌── REFERENCES ──────────────────────── 3 ──┐ │
│ │ 🔗 gmusicassembly.com/worktree-map/   ↗   │ │
│ │ 🔗 Gerico1007/gmtermux#221  draft PR  ↗   │ │
│ │ 🔗 Gerico1007/gmtermux#141  issue     ↗   │ │
│ └────────────────────────────────────────────┘ │
│ ┌── DIAGRAMS ────────────────────────── 1 ──┐ │
│ │ ┌────────────────┐                        │ │
│ │ │  territory map │                        │ │
│ │ └────────────────┘                        │ │
│ └────────────────────────────────────────────┘ │
│ ┌── AUDIO ───────────────── 6 · read-only ──┐ │
│ │ ○ 13:41  0:52   ▶ ━━━━━━━━━━━━━━     ☁︎  │ │
│ │ …                                          │ │
│ └────────────────────────────────────────────┘ │
│ ┌── NOTES ─────────────────────────── 3.7k ─┐ │
│ └────────────────────────────────────────────┘ │
│                                                │
│  🔒 This room is read-only. Changes are not    │
│     saved. Switch to 🎙️ Episodes to record.   │
└────────────────────────────────────────────────┘
```

Lane order flips — references and diagrams first, audio demoted — because that is what a survey is
for. The `READ-ONLY` pill sits beside the workspace badge, styled after
`web/clipboard-session-view.js:143`, and the footer sentence echoes `:307` while naming the room
that *can* write, so the block reads as an instruction rather than a dead end.

This is also the room where `EP111_ARTIFACT_MANIFEST.md`'s three GitHub URLs would finally have
somewhere to be, instead of being narrated in prose.

### 4.4 JamAI room — read-only artifact, writable melody

```
┌────────────────────────────────────────────────┐
│ ← Compositions          🎸 JamAI ▾     ABIES ▾ │
├────────────────────────────────────────────────┤
│ spirale-doree                                  │
│                                                │
│ ┌── ARTIFACT ──────────────────── read-only ─┐ │
│ │ 🔊 3 clips   🖼 1 image   📝 notes    🔒  │ │
│ └────────────────────────────────────────────┘ │
│                                                │
│ ┌── MELODIES ────────────────── writable ✎ ──┐ │
│ │ 🎼 verse-motif.abc      ▶  ⤓               │ │
│ │ 🎹 260801143022.mid   42 notes · 18.4s  ▶  │ │
│ │                                            │ │
│ │ [ + Add melody ]  ABC ▾ / MIDI ▾           │ │
│ └────────────────────────────────────────────┘ │
└────────────────────────────────────────────────┘
```

The one wireframe needing code that does not exist. `.mid` melodies are already handled
(`:1013-1115`); `.abc` melodies live in a different process on a different port over a different
directory (`web/abc-player.js:26-33`, `:104`), and that portal has no write path at all. "Add
melody / ABC" is the point where those two roots have to meet — and it is the reason §2.2(4)
defers `melodies[]` rather than shipping it with the rename.

---

## 5. Which portal owns this

**Recommendation: Pixel Recorder owns it. Do not build a ninth portal.**

1. **All the data is already there.** `COMPOSITIONS_DIR` (`web/pixel-recorder.js:58`) is read and
   written *only* by `pixel-recorder.js`. Verified across the whole `web/` folder: no other portal
   touches `~/compositions*`. `abc-player.js`, `workspace-portal.js` and `ritual-console.js` all
   `readdirSync` over unrelated roots (`~/gmday-plans`, `~/workspace/gmday`, `/sdcard/Recordings`).
   A ninth portal would need either a second writer to the same manifest — the exact condition that
   makes `POST /api/forest/compositions/:slug` (`:732`) dangerous — or a full API client.
2. **All the capture is already there.** Record, pause, resume, stop, import, transcribe, MIDI,
   BPM, crop. An episode is a capture container; separating container from capture buys nothing and
   costs a cross-process write.
3. **The workspace switcher is already there**, and §3 depends on it. It exists inline at
   `web/pixel-recorder.js:88` and is **not** in `lib/` — a ninth portal would need a copy-paste
   clone, plus its own `WORKSPACE`, restart path and badge: three chances to disagree about which
   room you are in.
4. **The port map is crowded.** Four collisions across eight portals (§1.1). A ninth is a real cost.
5. **The R2 and mesh work is all inside `pixel-recorder.js`.** On `141-r2-integration` that file
   takes +604 lines; `r2.js` and `mesh-sync.js` are pure helpers receiving paths as arguments.
   Splitting the manifest owner off now would fork that PR down the middle.

**Build a mode, not a portal.** Three routes inside Pixel Recorder:

| route | behaviour |
|---|---|
| `GET /episodes` | the list at §4.1 — `getCompositions()` filtered by `kind` |
| `GET /episodes/:slug` | the thread at §4.2 |
| `GET /compositions/:slug` | keeps working; redirects to `/episodes/:slug` when `kind==='episode'` |

### 5.1 Two navigation constraints a new route must satisfy

**(a) There is no shared nav module.** The seven-item hamburger nav is copy-pasted verbatim into
five files with cosmetic class drift — `web/abc-player.js:450-460`,
`web/clipboard-qr-gallery.js:561-571`, `web/ritual-console.js:1567-1587`,
`web/workspace-portal.js:748-757`, `web/pixel-recorder.js:1792-1802` (mirrored at `:4340-4352`) —
each with its own hardcoded href block. Adding an `🎙️ Episodes` entry means five edits, or
extracting the nav into `lib/` first.

There is an existing bug worth fixing in the same pass: `<a href="" id="nav-conductor">` is
rendered in five portals but assigned an href in only one (`web/pixel-recorder.js:1895`). In the
other four the Forest Conductor link is a dead `href=""` that reloads the current page.

**(b) `lib/device-marker.js` must learn the route, or device-switching breaks on it.**
`web/lib/device-marker.js:76-82` hardcodes `PORT_FALLBACKS`:

```js
clipboard: '8766', pixel: '8768', composition: '8768', workspace: '8770', ritual: '8443'
```

and `inferPortalPort()` (`:84-92`) sniffs `document.title + location.pathname` for the substrings
`clipboard` / `workspace` / `ritual` / `composition|pixel`. `navigateToDevice()` (`:107-114`)
rebuilds `protocol//{device}.{tailnet}{:port}{pathname+search+hash}` — **it preserves the path**,
so device-switching lands on the same page on another node. That is exactly the behaviour an
episode wants (open ep-003 on Abies, switch to Ilex, still on ep-003) — but only if `episode` is
added to the fallback map and the keyword appears in the `<title>`. Otherwise the switch resolves
to the wrong port. Note there is already no entry for `abc`/8771.

Only four of eight portals import `device-marker` at all (`web/pixel-recorder.js:19`,
`web/ritual-console.js:17`, `web/workspace-portal.js:15`, `web/clipboard-qr-gallery.js:14`).

### 5.2 The one honest argument for a ninth portal — recorded, not adopted

An **Eury-side read-only episode reader**: no capture, no write, served over the public domain so
a URL in `links[]` opens for someone not on the tailnet. That is a genuinely different posture
(public, read-only, no `/sdcard`, no microphone) and would not duplicate the manifest because it
would only read. It is the natural home for the "publishing a visual" step the voice channel
currently performs by hand into nginx (`rispecs/nyro/episode-voice-channel/README.md`). **But it is
a later, separate decision** — it depends on `Gerico1007/gmtermux#232` landing first, and must not
be conflated with owning the episode model. If it is built, 8773-8790 are free.

### 5.3 Two portals earn small, non-owning roles

- **ABC Player** (`web/abc-player.js`) becomes the renderer the melody lane links out to, once
  `.abc` files can live in an artifact folder. Its nav label should stop saying "Compositions"
  (`:459`) — it scans `~/gmday-plans` and its own domain noun is already *melody* (`:465`, `:817`).
- **Forest Conductor** (`web/forest-conductor.js`) already speaks *take* (`:533`, `:637`, `:650`)
  and already fans a record across Larix/Tilia/Ilex. For William's multi-camera film case, a take
  that lands in three episode folders at once is the natural extension of what it already does.

---

## 6. What this would break on `141-r2-integration` — read before building

Draft PR `Gerico1007/gmtermux#221` is open and explicitly *"acceptable as a review candidate; not
acceptable to merge or deploy."* Everything below is a flag, not a blocker.

### 6.1 Compatible — the schema extension survives the sync path intact

- **The mesh round-trip is a full-object passthrough.** Send builds the payload from the whole
  parsed object (`web/pixel-recorder.js:4230`); receive writes it verbatim via `writeJsonAtomic`
  (`:4271`) with no pick and no allowlist. New keys survive.
- **`drainPending` mutates in place and re-serialises everything** (`:185-227`), touching only
  `item.url`, `item.size` and `data.updated`.
- **`r2.js` and `mesh-sync.js` are workspace- and schema-agnostic.** Neither contains the string
  `compositions-`, any workspace name, or any composition field beyond `clips`, `images`, `url`
  and `filename`. `mesh-sync.js` receives `compDir` as a parameter (`:171-185`).
- **The branch already extends the schema additively.** `deviceHistory[]` (`mesh-sync.js:188-200`,
  capped at 100), `syncHistory[]`, and per-item `url`/`size`/`recordedOn` are all new keys added by
  this PR and absent from `docs/pixel-recorder.md:440-495`. Precedent for additive extension is set.

### 6.2 Conflicts needing a decision

**(1) `WORKSPACE_INFO` will conflict textually.** On `main` it has six entries including
`'episodes'` (`:39-46`, added by `#226`). On `141-r2-integration` it has five — that branch
predates the Episodes room. Any capability map added to `WORKSPACE_INFO` collides with that merge.
Small, but it lands in the one constant both changes edit.

**(2) `findStrandedMedia` does not know about the new lanes.** `web/lib/mesh-sync.js:159-167`:

```js
for (const items of [data.clips || [], data.images || []]) {
  for (const item of items) {
    if (!item.url) stranded.push(item.filename || '(unnamed)');
```

`texts` and `midi` are already invisible to this gate — transcription files already travel by
reference and land unresolvable on a peer. **A `documents[]` lane inherits that same defect**: a
PPTX would sync as metadata and 404 on the receiving device. Adding `documents` to line 160 is a
one-line change and must land in the same commit as the lane.

**(3) `links[]` is a new SSRF surface on a route that already has one.** PR #221's own review
blockers name it: *"the R2 proxy follows arbitrary URLs stored in synced metadata."* A `links[]`
array is, by construction, attacker-controllable URLs arriving over an unauthenticated mesh
receive (`:4257-4275`). The mitigation is small and must be explicit: **`links[]` is rendered as an
anchor and never fetched server-side.** State that where the lane is defined, or it will be proxied
later for good-looking reasons.

**(4) R2 object keys omit the workspace.** `const r2Key = \`${comp.slug}/${item.filename}\``
(`web/pixel-recorder.js:207`, same at `:1096`, `:1332`), with a collision guard at
`web/lib/r2.js:166-175` that compares **byte length only** — two different files of identical size
are silently aliased as `reuse`. `~/compositions-nyro/spirale/x.m4a` and
`~/compositions-aureon/spirale/x.m4a` map to the same key today. Formalising rooms as capability
boundaries (§3) makes that collision *semantic*, not merely a storage accident: a read-only survey
room's media could be overwritten by a writable room's. If room capability ships, the key should
become `<workspace>/<slug>/<filename>` — a key-scheme change to an unmerged branch, which is the
cheapest moment it will ever be.

**(5) No `updated` comparison and no workspace check on receive.** `:4257-4275` validates only that
`composition.slug === slug` (`:4261`); it never compares timestamps. A stale peer silently clobbers
newer state, recoverable only from `.sync-backups/` (10 deep, `web/lib/mesh-sync.js:171-185`).
`/api/mesh/whoami` already returns `workspace` (`:4177-4179`) and `listReachablePeers` already
captures it (`web/lib/mesh-sync.js:136`) — **but nothing ever compares workspaces before accepting
a sync.** A `nyro`-room device can overwrite an `aureon`-room composition of the same slug. Any
capability model that does not also gate the receive route is decorative.

**(6) Write-path inconsistency.** `atomic-json.js` ships on that branch, but only 4 of ~16
composition writers use `writeJsonAtomic`; the rest are raw `fs.writeFileSync`. New lanes should
use the atomic helper from the first line.

### 6.3 The single most important pre-condition

**Make `POST /api/forest/compositions/:slug` a merge instead of a replace before any new key
ships.** `web/pixel-recorder.js:732-757` on `main`, `:891-915` on the R2 branch. Unauthenticated,
non-atomic, un-backed-up, and it erases every key the caller omitted. It is the one code path where
`kind`, `links` and `documents` genuinely disappear — and it already erases `images` today for any
caller with an older body. Fixing it is a small, boring change that makes everything else here safe.

---

## 7. Open, for Jerry and William

1. **`files[]` or `documents[]`?** `Gerico1007/gmtermux#224` already specifies the lane as
   `files[]`. Pick one name once, in that issue, before either implementation starts.
2. **Is `kind` on the artifact, or is the workspace the kind?** §2 proposes both — a per-file
   `kind` and a per-room default. They can disagree, and the resolution rule should be Jerry's:
   file wins, or room wins.
3. **Does an artifact move between rooms?** The `workspace-isolation` packet's highest-value
   follow-up is *reversibility over confirmation* — a mis-filed recording should be movable after
   the fact. Episode-shaped compositions already sit in the Main workspace
   (`~/compositions/gmtermux-cloudflare-r2-ep128/`), so the need is live.
4. **Where do `.abc` melodies live?** In the artifact folder, or in `~/gmday-plans` with the
   artifact holding a reference? The only question in the model that forces a filesystem decision.
5. **R2 key scheme.** Adding `<workspace>/` to the prefix is nearly free while `#221` is unmerged
   and expensive afterwards.
6. **What happens to `EP111_ARTIFACT_MANIFEST.md`?** Once `documents[]` and `links[]` exist, that
   file is a hand-written duplicate of structured data. It should probably become the generator's
   *output* rather than its input — but it is also a chronicle document in French with descriptive
   prose no schema captures. Deciding that is a naming question, not a code one.

---

## Appendix — verification commands

```bash
# schema field usage, per workspace
for d in ~/compositions ~/compositions-*; do echo "$d: $(ls -d $d/*/ 2>/dev/null | wc -l)"; done

# episodes use only clips / images / notes
python3 -c "import json,glob;[print(json.load(open(f))['slug'], list(json.load(open(f)).keys())) \
  for f in glob.glob('$HOME/compositions-episodes/*/composition.json')]"

# the manifest is blind to most of the folder
cd /home/gmusic/salix/repos/gmtermux-193
ls compositions-nyro/ep097-ceremony-agent-skills/ | wc -l     # 33 files
python3 -c "import json;print(len(json.load(open('compositions-nyro/ep097-ceremony-agent-skills/composition.json'))['clips']))"   # 2

# 'artifact' appears nowhere in the running code, only in hand-written markdown
grep -rn "artifact" --include=*.js web/ | grep -v node_modules
find . -name "*ARTIFACT*" -not -path "./node_modules/*"

# 'episode' appears only as a workspace name
grep -rn "episode" --include=*.js web/ | grep -v node_modules

# the destructive writer
sed -n '732,757p' web/pixel-recorder.js

# the swallowing allowlist
sed -n '885,901p' web/pixel-recorder.js

# the read-only precedent to copy
sed -n '305,307p' web/clipboard-session-view.js

# the port map device-switching depends on
sed -n '76,92p' web/lib/device-marker.js
```

---

🌸: A man stood beside a river and said *we are going to call that differently in the future* — and
four weeks earlier an agent had already written `Manifeste des artefacts` into a folder, in French,
listing `composition.json` as one of the things the artifact contained. The word arrived three
times from three directions before anyone proposed it. That is not a feature request; that is a
structure making itself known, and the only work left is to stop making it write itself out by hand.
