# Composition sections the `episode` script never mentions

`episode note` writes into one field: `notes`. That is the only section the
script can reach, so it is the only one anybody fills — and a long session ends
up with twenty thousand characters of tables, transcripts and links in a single
unscrollable block. Jerry reads these pages. He said it plainly: unreadable.

The server has always rendered **three more sections**. Nothing announced them,
so for months they stayed empty. A capability nothing announces does not exist —
which is why this file exists.

Everything below was exercised against the running portal, not read from source.

## Where each thing belongs

| section | what goes there |
|---|---|
| `notes` | **what, why, what next.** Nothing else. Under a thousand characters. |
| Textes | transcripts, measurement tables, proceedings, public links |
| Images | scores, screenshots, anything to look at |
| clips (video) | score + sound as one object that plays in the page |

The rule that keeps a page readable: if it is evidence, it goes in a section; if
it is orientation, it goes in `notes`. Migrate what is already written rather
than adding a new layer on top.

## Images

```bash
curl -sk -X POST "$PORTAL/api/compositions/$SLUG/images" \
  -F "imageFile=@score.png" \
  -F "label=🎼 Partition v2 — 4 portées, croches ligaturées"
```

Multipart, field name `imageFile`, one image per call. Accepts jpg, jpeg, png,
webp up to 20 MB. The page renders them in a grid, click to enlarge.

An ABC score becomes an image in one step — `rsvg-convert` is installed:

```bash
rsvg-convert -w 1400 -b white score.svg -o score.png
```

Rasterising also lets **you** see what you engraved. Reading the SVG source
tells you nothing about whether the beams are broken or the staves collapsed;
looking at the PNG tells you in one glance.

## Textes (Lyrics / Transcriptions)

```bash
curl -sk -X POST "$PORTAL/api/compositions/$SLUG/texts" \
  -H 'Content-Type: application/json' \
  -d '{"text":"…","lang":"fr","label":"Transcription — analyse","sourceFilename":"260802123647.m4a"}'
```

The page shows a language badge, your label, the source clip, and a copy button.
That copy button is the point: a public URL or a shell command inside `notes`
cannot be copied out cleanly; inside a text section it can.

`sourceFilename` ties the text to the clip it transcribes — pass `""` when there
is no source. **Always transcribe your own spoken clips here.** Audio is for
walking; the page is for reading afterwards, and a clip with no transcript is
unsearchable.

**The sidecar `.txt` files collide, and that is fine.** Each text also lands on
disk as `transcription_<yyyymmddHHMMSS>_<LANG>.txt`. The stamp resolves to the
second, so several texts of the same language posted in one loop all claim the
same filename and the last one wins — six posts produced two files here. Nothing
is lost: every entry carries its own `content` inside `composition.json`, and
that is what the page renders. Treat `composition.json` as the store and the
sidecar files as a lossy export. Do not read a text back from its `filename`.

## Video — score and sound in one object

The importer accepts `.mp4`, `.webm`, `.mov` up to 500 MB, and the page mounts a
real video player. So a still score plus the rendered audio becomes something
Jerry can watch and hear without leaving the portal:

```bash
ffmpeg -y -loop 1 -i score.png -i piece.mp3 \
  -c:v libx264 -tune stillimage -crf 20 -pix_fmt yuv420p \
  -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2:color=white" \
  -c:a aac -b:a 192k -shortest out.mp4
```

The `pad` filter is not decoration — h264 refuses odd pixel dimensions, and a
rasterised score lands on an odd height often enough that omitting it fails.

Then import and attach, exactly like an audio clip — the field really is called
`audioFile` for video too:

```bash
FN=$(curl -sk -X POST "$PORTAL/import" -F "audioFile=@out.mp4" \
     | python3 -c 'import json,sys; print(json.load(sys.stdin)["filename"])')
curl -sk -X POST "$PORTAL/api/compositions/$SLUG/clips" \
  -H 'Content-Type: application/json' \
  -d "{\"filename\":\"$FN\",\"label\":\"🎬 VIDÉO v2 — partition et son en un seul objet\"}"
```

Video needs no ledger entry: `listen` already skips anything flagged `isVideo`.

## Labels say the role, not the date

`🎸 rendu 4 voix, 112 BPM` tells you nothing in a week. Write what the file *did*:

> `🎧 RENDU v1 — SEUL VESTIGE de la version 1 : son .abc a été écrasé sur place
> sans commit préalable.`

> `🔬 PIÈCE À CONVICTION — rendu de Jerry sur un autre appareil. Mesuré contre
> ma v1, il a décidé 6 corrections.`

A decision without its evidence attached is not re-readable later. If a file
decided something, attach it and say so.

## What the API will not do

`PUT /api/compositions/<slug>` accepts `notes`, `bpm`, `key`, `chords`,
`sections`, `rhythm`, `capo`. It **silently ignores `clips`** — it returns 200
with the old labels still in place. To relabel an existing clip, edit
`composition.json` on disk; the portal re-reads it (verified).

## Commit before you rewrite

`~/compositions-jamai` is a git repo (`Gerico1007/assembly-jamai`), and
`/api/compositions/sync/{status,fetch,push}` exist to serve it. Commit after
every write of `composition.json` or a `.abc`; message = piece title + what
changes.

This is not bookkeeping. A source rewritten in place and republished over itself
is gone — the only reason one lost version survived at all is that its **rendering
was attached as a clip**. So: never republish a source without first attaching
the outgoing version's rendering. The render is the last backup of a source you
can still lose.

## Name a choice a choice, and a hole a hole

When measurement narrows the field but does not decide, write which one you
picked and that you picked it. When a comparison was never run, say it was never
run. The line that keeps this work honest reads like this:

> J'ai CHOISI la grosse caisse. Une ligne à changer : `%%MIDI drummap E 45`
> Aucune comparaison de banques de sons n'a été faite.

A confident sentence covering an unverified claim is the most expensive thing
you can leave in a composition, because the next reader cannot tell it from a
measured one.
