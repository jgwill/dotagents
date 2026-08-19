# HOW WE DID IT THIS TIME

**Status:** measured on eury, 2026-08-19. The loop that produced the two
compositions. Do not treat this as the next design.
**Pair:** [recreate](RECREATE-THE-WORK-260819.md) · [missing](MISSING-AND-DEPENDENCIES-260819.md) · [next time](DRAFT-PI-MONO-EXTENSIONS-260819.md)
**Disc:** `GUILLAUME.md`
**Sessions that still hold the room** (`scripts/_env.sh`):

| who | session id | herdr pane | still live |
|---|---|---|---|
| Jerry origin | `1937aa47-767f-4543-8cdc-257364ae2c52` | `w17:p6` ATELIER-jamai-demain | yes |
| William fork (ava002 / songbird) | `71bbe83b-8963-4635-b8a2-40bcffbb3aff` | `w17:p8` | yes |
| observer (opus 003) | `7cd9bb52-eab9-4dfb-861b-680bcfa1df17` | `w17:pA` | yes |

The great results came from **a Claude-code session that stayed open** plus
**bash watches that cost zero tokens**. The session composed. The watches only
said "something landed."

---

## The shape

```
Android drop (Pixel Recorder / Songbird / voice)
        │
        │  THIS TIME the phone is a tray, not a worker.
        ▼
eury pulls or already has the file
        │
        ├─ jamai-watch   Jerry on eury     ~/Recordings-jamai
        ├─ ilex-watch    William on ilex   mirror → ~/Recordings-william
        └─ abies-watch   Jerry on abies    mirror → ~/compositions-abies
                │
                ▼
        jamai-on-drop     measure only (MIDI notes, audio bands, Whisper)
                │         writes ~/.local/state/episode-voice/drops/<name>/
                ▼
        Claude-code session still open in herdr
                │         reads the drop, composes, engraves, publishes
                ▼
        portal return     score / m4a / note back into the room
```

Nothing in that chain ran on the phone except the capture.

---

## What is actually alive right now

Three folders Jerry named. Only one is the living machine.

| folder | role | living? |
|---|---|---|
| `~/.local/state/episode-voice/` | pid, log, ledger, fingerprint, drops for the three bash watches | **yes** |
| `~/.local/state/ilex-watch/` | inline Claude-code loop on ilex portals `8768=aureon` / `4768=jamai` | **yes, leftover** |
| `~/.local/state/atelier-veille/` | empty (`mine.txt` only) | no |

Three bash watches, all `skills/jamai-morning/scripts/`, all zero tokens:

| script | systemd unit | who | what it watches | hook |
|---|---|---|---|---|
| `jamai-watch` | `jamai-watch.service` **enabled** | Jerry | local `~/Recordings-jamai` | `jamai-on-drop` |
| `ilex-watch` | `william-watch.service` **enabled** | William | rsync from `ilex` then `episode watch william` | same hook |
| `abies-watch` | **none** (ppid 1, started by hand) | Jerry phone | rsync from `abies` then `episode watch abies` | same hook |

`atelier-veille` is the later generalization (parametrized watch). It is **not**
what produced the pieces. Do not confuse the skill with the loop that ran.

A fourth loop still sits inside a Claude-code tool call and writes
`~/.local/state/ilex-watch/{aureon,jamai}.{seen,salles,tailles,echec}`. That is
the old shape: the model holds the `while true`. The systemd units already
escaped it for Jerry and William. Abies did not.

---

## Laws this loop paid for (keep them)

These are not style. Each one failed once.

1. **Fingerprint, never inventory.** `episode watch` writes 16 bytes when
   nothing moved. Re-listing directories in a loop burned eleven hours
   (Gerico1007/dotagents#5).
2. **Stable size before "new".** An open `.m4a` has no moov index. Wait until
   the size repeats. The inline ilex loop uses 75 s; `jamai-on-drop` also
   refuses to classify a file still being written.
3. **Own-import filter.** Portal transcriptions of *our* voice come back as
   `.json` next to the `.m4a`. Without `*-mine.txt` / `mien.txt`, the atelier
   hears itself.
4. **Two failures before MUET.** A phone in the woods blinks. One missed probe
   is not a crash.
5. **Never `--delete` on the mirror.** A failed rsync must leave the mirror
   stale, never empty — empty looks like "everything moved."
6. **Local atelier name ≠ remote name.** William's mirror on eury is `william`,
   not `jamai`. `jamai` is already Jerry. Mixing them opened an empty room
   (`william-op001`) inside Jerry's atelier.
7. **`ilex:8768` from eury is eury talking to itself.** Only ssh port 8022 is
   relayed. A 200 without a tunnel is a false positive (`ilex-watch` écart 11).
8. **Identity is `(host, port, code tree)`.** On eury, 8768 and 8828 both
   answer `jamai`. The unit pins `PIXEL_RECORDER_URL=https://localhost:8828`
   and anaconda `PATH` (scipy). Wrong python = healthy watch, dead hook.
9. **Hook stdin is `/dev/null`.** ffmpeg once ate the next filename off the
   pipe. A real drop would have vanished.
10. **Classify by bytes, not extension.** Three of Jerry's MIDI arrived as
    `.m4a` (`MThd` in the first four bytes).

The hook does **not** compose. Verdict only. Composition stays in the open
session. That split is why the results were good: the model woke with a
measured file, not a guess.

---

## Why this cannot be the next time

- The phone is only a tray. Every process after capture needs eury.
- Two Claude-code sessions have to stay up for days. The watches outlived them
  only because someone later wrapped two of them in systemd.
- `abies-watch` is still a hand-started orphan. Kill the box, it dies.
- The leftover `ilex-watch/` loop is still the model holding `while true`.
- Host binaries (`abc2midi`, `fluidsynth`, `ffmpeg`, anaconda scipy) are
  assumed everywhere. Nothing in this loop is Android-viable except the drop.
- Copying `jamai-watch` and renaming `jamai` was the only way to get a second
  atelier. That is how `ilex-watch` and `abies-watch` exist.

Next time the watch, the classify, the ABC, and the falsify have to be able to
live **on the Android**. Eury keeps render. The open Claude-code session is not
part of the machine.

That design is the other file.
