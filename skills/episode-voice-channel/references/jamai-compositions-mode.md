# JamAI compositions mode

The same channel, pointed at music instead of episodes. Nothing about the
transport changes — `say`, `listen`, `note`, `open` all behave as documented in
`SKILL.md`. What changes is the **atelier** the recorder is pointed at, the
material that lands in it, and the tooling you reach for.

Read this when Jerry wants to make music with you rather than talk about work.

## Two things are called "workspace" — they are not the same

Jerry named this ambiguity himself. Keep them apart in what you say to him:

| term | what it is | where it lives |
|---|---|---|
| **atelier** (*dossier de travail*) | a folder pair the Pixel Recorder writes into | `~/compositions-<atelier>/` + `~/Recordings-<atelier>/` |
| **espace de travail** | a herdr workspace — tabs and panes | `herdr workspace list` |

The atelier is set by the `WORKSPACE` env var on the recorder process. The
ateliers that exist: `''` (Main), `episodes`, `aureon`, `nyro`, `jamai`, `synth`.
Every folder pair is already created on disk.

**`jamai` is the musical atelier** — 🎸, amber. Its material lands in
`~/compositions-jamai/` and `~/Recordings-jamai/`.

## Switching the atelier

The badge in the Pixel Recorder header does it, and so does the API:

```bash
curl -sk -X POST https://localhost:8768/api/workspace/switch \
  -H 'Content-Type: application/json' -d '{"workspace":"jamai"}'
```

This **restarts the recorder server** — it re-execs with `WORKSPACE=jamai`. Two
consequences worth knowing before you press it:

- It refuses while a recording is active (`409`). Stop the take first.
- After the restart the process respawns with `stdio: 'ignore'`, so its errors go
  nowhere. If something fails silently afterwards, that is why.
- **It moves the channel.** Clips you spoke into `episodes` are not visible from
  `jamai`. Switch back the same way when the subject returns to work.

Always run `scripts/episode preflight` after a switch — it reports the active
atelier and catches the two failures that cost the most time to diagnose.

## Where the music actually lives

Three places, and they answer different questions:

| path | what it holds |
|---|---|
| `~/compositions-jamai/` | the compositions themselves — clips, notes, what Jerry hears |
| `~/workspace/jamai-melody/` | the tooling. `bin/jamai-publish-melody` renders ABC → MIDI → MP3 and publishes to `gmusicassembly.com/jamai/melody/`. Git repo. |
| `~/workspace/gmusic/.jamai/` | the knowledge — `ABC_TECHNIQUES.md`, `LEITMOTIF_LIBRARY.md`, `MUSICAL_PATTERNS.md`, `templates/`, `skills/jamai-melody/`. Git repo, `main`. |

Read the knowledge repo before composing anything substantial. The leitmotif
library in particular is the continuity between sessions — Jerry recognises a
returning theme, and inventing a fresh one each time throws that away.

## Two ways to deliver music, and they are not interchangeable

**Publish to the melody portal** — for a finished piece Jerry should be able to
open, keep, and share:

```bash
jamai-publish-melody --note "session note" melody.abc
echo "<ABC text>" | jamai-publish-melody -
```

Renders ABC → MIDI → MP3 with FluidSynth, updates the manifest, regenerates the
index, prints the public URL. Always give Jerry that link.

**Speak it into the composition** — for something in the moment: humming a shape,
explaining a chord move, reacting to a take he just recorded. Use `episode say`
with the `jamai` persona, which carries JamAI's voice.

```bash
scripts/episode say --persona jamai --to <composition-slug> --file take-notes.txt
```

A melody worth keeping deserves the portal. A thought about a melody belongs in
the composition beside the audio it refers to.

## Listening to what he plays

`scripts/episode listen` transcribes his recordings the same way it does in
`episodes`. For music this is often not a transcript of words but a description
of what he sang or played — treat it as a musical prompt, not a command, and
answer with sound where sound is the better answer.

## What to say and how

Same rule as `SKILL.md`: write for the ear. But for music, one addition — name
what you hear before proposing anything. "You landed on the flat sixth and left
it hanging" tells him you listened. Jumping straight to a suggestion tells him
you did not.

Personas: `jamai` for anything musical, `aureon` when the moment is about how the
piece feels rather than how it is built. Both speak; `aureon` is in French.
