# Your job: stand the episode watch for Jerry

Jerry is out walking. He records audio and video into a Pixel Recorder episode
and expects an answer waiting when he checks his phone. The session that set this
up is running out of context, so you are taking the watch.

Everything below was verified on this machine on 2026-08-01. Where something is
unverified or undecided, it says so.

## Load the skill first

```
episode-voice-channel
```

It is loadable by name (symlinked into `~/.claude/skills/`). Read its `SKILL.md`,
then `references/watcher-handoff.md` — that second file is the actual runbook for
this job. Do not proceed on this brief alone; the runbook has the details.

The program is `~/.agents/skills/episode-voice-channel/scripts/episode`.

## The loop

Poll `episode pending` about every 30 seconds. When a filename appears:

1. `episode listen --new` — prints French and English
2. Treat the English as a prompt **addressed to you** and do the work. He is
   asking for things to be built, checked, explained — not merely transcribed.
3. Reply with `episode say --persona synth --to <slug> --file msg.txt`
4. Put paths, commands and links in `episode note` — he cannot copy them from audio

Prefer a Monitor polling `episode pending` over a bare timer, so you wake when
something lands rather than on a schedule. Emit a line if the portal stops
answering — otherwise silence looks like "nothing to hear" when it means
"cannot hear."

**Video prompts do not appear in `pending`.** He films `.mov` clips while walking.
The runbook explains how to catch and transcribe them. This has already caught us
out once.

## Current state — verified

- Portal: `https://localhost:8768`, self-signed, workspace **episodes**.
  Started detached with `setsid`; its log is a file, not a terminal.
- Recordings: `~/Recordings-episodes/` (reached as `/sdcard/Recordings-episodes/`)
- Episodes so far:
  - `ep-001-artifact-container-vision` — empty; reserved for his artifact-container
    idea (renaming composition → artifact). He explicitly said **do not implement
    it**, only observe. An issue for it is his call, not yours.
  - `ep-002-gmtermux-141-r2-sync-explained` — R2/mesh sync explainer
  - `ep-003-dotagents-1-episode-voice-channel-skill` — this skill, and his video prompt
  - `worktree-territory-map` — the older room, before numbering

## Two published pages

- https://gmusicassembly.com/gmtermux-worktree/ — worktree survey
- https://gmusicassembly.com/gmtermux-r2-sync/ — when audio reaches the cloud

Both are `noindex`, served from `/home/gmusic/salix/production/ngrok-mux/static/`
via explicit nginx `location` blocks. Runbook explains how to add another.

## Open, waiting on Jerry's word — do NOT do these unasked

- **Merge `Gerico1007/dotagents` PR #2** (branch `1-episode-voice-channel`, issue #1).
  He said he would merge once the skill worked well. It works, but he has not said
  go. **The skill only exists on that branch** — if anyone runs `git checkout main`
  in `~/.agents`, the folder vanishes and the symlink dangles. Merging fixes that
  permanently; until then, leave the branch checked out.
- **The Hermes symlink.** Claude is linked. Hermes uses
  `~/.hermes/skills/<category>/<name>/` and **not one Hermes skill is currently a
  symlink into `~/.agents`** — they are all real folders. Adding one would be the
  first of its kind, so it is a decision, not a chore. Likely `media` or
  `creative`. Ask; do not invent the convention.
- **`Gerico1007/gmtermux` PR #233** (branch `232-eury-native-portals`) — teaches the
  portals `RECORDINGS_BASE` and would retire the `/sdcard` symlinks propping this
  machine up. Open, not a draft, 4 commits ahead. His call.

## Things that will waste your time if you rediscover them

- The recorder rejects `.mp3`. TTS emits mp3. Convert to AAC/`.m4a` before import —
  the skill's `say` already does this.
- A **quoted** value in `~/.env` reaches Groq with the quote characters attached and
  fails as `invalid_api_key`, blaming the key rather than the quoting. Fixed today
  for `GROQ_API_KEY`. `~/.config/gbravo/r2.env` is clean — if a quoted value is ever
  added there it will fail the same way.
- **Start Recording cannot work on this Linux host** — it shells out to the
  Android-only `termux-microphone-record`. Import is the path here.
- After a workspace switch the portal respawns with `stdio: 'ignore'`, so its errors
  go nowhere. If something fails invisibly, that is why.

## How to talk to him

He is walking. Lead with the conclusion. Say symbols as words — "line seventy two",
not `~/.env:72`. Answer what he asked before offering what you noticed. If you find
something that changes his question, say that plainly.

When your own context runs low, say so in the episode and name what is still
pending. Going quiet is worse than a late answer.

## First action

Announce yourself in `ep-003-dotagents-1-episode-voice-channel-skill` with a short
`episode say` — tell him the watch has been handed over and you are listening.
Then start the loop.
