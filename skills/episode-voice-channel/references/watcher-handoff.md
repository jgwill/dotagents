# Running as the episode watcher

How to be the agent that stays awake on the channel: watch for what Jerry
records, transcribe it, act on it, and answer by voice. Read this when you are
taking over the watch from another session, or starting it fresh.

The point of the watch is continuity. Jerry records while he is walking and
expects an answer to be waiting when he checks. A session that ends takes the
watch with it, so handing it off cleanly matters more than any single reply.

## What you are watching

`episode pending` prints the filenames waiting on you — Jerry recorded them, you
did not, and they have no transcription yet. That single command is the whole
filter. It reads `GET /recordings` and removes three classes:

- anything already transcribed
- anything in the spoken ledger (`~/.local/state/episode-voice/spoken-<ws>.txt`) —
  this is how the channel avoids transcribing its own voice and talking in a loop
- MIDI and video

**Video is excluded, and that has bitten us.** Jerry sends `.mov` prompts filmed
while walking. They never appear in `pending`, so the watch stays silent on them.
Until that changes, sweep the folder directly when he says he posted something
and nothing arrived:

```bash
touch -d '30 minutes ago' /tmp/ref30
find ~/Recordings-episodes -type f -newer /tmp/ref30 -printf '%TH:%TM %10s %p\n' | sort
```

Use the reference-file form, not `-newermt '-30 minutes'`. On this host `find` is
**bfs**, which rejects relative timestamps — and it fails in the worst possible
way for a watcher: the error goes to stderr and the command yields no rows, so a
sweep that is actually broken looks exactly like a sweep that found nothing. That
mistake cost this session a wrong conclusion about whether a file had arrived.
When a sweep returns empty, confirm the method works by checking it can still see
a file you know exists.

For a video prompt, the words are in the audio track. Pull it and send that:

```bash
ffmpeg -y -loglevel error -i <file>.mov -map 0:a:0 -c:a aac -b:a 128k /tmp/vp.m4a
# then transcribe /tmp/vp.m4a with the Groq key from ~/.env
```

Frames are usually just Jerry outdoors — worth a glance to confirm it is not a
screen recording, but the substance is nearly always the narration.

## The loop

Poll roughly every 30 seconds. When something lands:

1. `episode listen --new` — prints French and English
2. Read the English as a prompt addressed to you, and **act on it**. This is not
   a transcription service. He is asking for work.
3. Answer with `episode say` into the right episode, and put the detail he cannot
   copy from audio into `episode note`.

If a monitor tool is available, prefer polling `episode pending` in it over a
timer — it wakes you the moment something lands instead of on a schedule. Also
emit a line when the portal stops answering, or silence will read as "nothing to
hear" when it actually means "cannot hear."

## Which room to answer in

Episodes are numbered and carry the repo and issue when the subject has one:

```
ep-002-gmtermux-141-r2-sync-explained
ep-003-dotagents-1-episode-voice-channel-skill
```

`episode new "<Title>"` claims the next number. Jerry asked for repo and issue in
the name so he can find a subject later without listening through everything.
Start a new episode when the subject changes rather than letting one room
accumulate — he scrolls these afterward.

## Speaking so it lands

He is walking. Lead with the conclusion, then the reason. Say symbols as words —
"line seventy two", not `~/.env:72`. Keep paths, flags and commands out of the
audio entirely and put them in the note, where he can copy them later.

Answer what he asked before offering what you noticed. If you found something
that changes his question, say so plainly rather than answering the question he
no longer needs answered.

## Publishing a visual

When a visual explains better than words, build a standalone page and put it on
his public domain — he opens it on the phone, so an artifact URL behind a login
does not work.

```
page:   /home/gmusic/salix/production/ngrok-mux/static/<name>/index.html
route:  nginx.conf in /home/gmusic/salix/production/ngrok-mux
url:    https://gmusicassembly.com/<name>/
```

Each path needs an explicit `location` block with `alias /srv/static/<name>/` —
dropping a folder in `static/` alone does nothing. Copy the `/skills-map/` block
and keep its posture: `X-Robots-Tag noindex, nofollow`, no credentials, no
endpoints, nothing that would matter if a stranger found it. Back up `nginx.conf`
before editing, run `nginx -t` inside the container before reloading.

Pages written for the Artifact mechanism have no `<head>` — they rely on a
wrapper. Wrap them before serving standalone or they render unstyled.

## State that outlives you

| what | where |
|---|---|
| the skill | `~/.agents/skills/episode-voice-channel/` (repo `Gerico1007/dotagents`) |
| spoken ledger | `~/.local/state/episode-voice/spoken-<workspace>.txt` |
| recordings | `~/Recordings-<workspace>/`, reached as `/sdcard/Recordings-<workspace>/` |
| compositions | `~/compositions-<workspace>/` |

The `/sdcard` paths are symlinks standing in for an Android layout the recorder
hardcodes. They are host state, not in any repo, so a fresh machine will not have
them. `Gerico1007/gmtermux#232` replaces them properly.

## Handing the watch on

Before your session ends, say so in the episode rather than going quiet — an
unanswered recording is worse than a late answer. Tell Jerry the watch is
stopping and what is still pending, so he knows whether to expect a reply.
