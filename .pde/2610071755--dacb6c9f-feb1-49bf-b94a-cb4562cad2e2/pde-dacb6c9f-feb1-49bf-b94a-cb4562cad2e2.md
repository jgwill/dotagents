# Prompt Decomposition

> Engine: **claude** (opus)

## Four Directions

### 🌅 EAST — Vision

- Installing the plugin recreates the experience of Jerry's origin session [85%]
- Music prerequisites go into Miadi's distribution system and install alongside miadi [80%]
- Packaging works for album work and for film/TV scoring [45%] _(implicit)_
- Define what 'exact experience' means in checkable terms [60%] _(implicit)_

### 🔥 SOUTH — Analysis

- Read the origin session and list every tool, script, skill, agent, path and service it used [85%] _(implicit)_
- Inventory what plugin 0.1.1 and the four apt packages carry [80%] _(implicit)_
- Collect findings already made in earlier sessions [55%] _(implicit)_
- Check rubberband and other host tools against package dependencies [50%] _(implicit)_

### 🌊 WEST — Validation

- Fresh install of the plugin and packages on gaia [65%] _(implicit)_
- Replay one origin-session piece and check it against the criteria with the verificateur [60%] _(implicit)_
- Regenerate renders, because 03-rendered/ was not synced, and compare MIDI and measurements [50%] _(implicit)_

### ❄️ NORTH — Action

- Finish the installation contribution on jgwill/miadi-orchestration-kit#44 [80%]
- Add the missing parts to the plugin [75%]
- Work in phases and report status per phase [75%]
- Push to Gerico1007:feat/atelier-jerry-plugin and update the PR [60%] _(implicit)_

## Original Prompt

> # Input prompt — William, 2026-10-07, session "miadi-music-session-observability-marketplace-install"
> 
> ## Context the prompt answers
> 
> - `atelier-jerry` plugin: jgwill/miadi-orchestration-kit#44, branch `Gerico1007:feat/atelier-jerry-plugin`, now carrying upstream main and commit `c8dd45b` (four apt packages `miadi-music`, `-render`, `-measure`, `-video` in `packages/miadi/deb`, plugin 0.1.1).
> - The home folders of gmusic were synced from eury to gaia (`.agents/gmusic-sync-to-gaia.sh`), including `atelier-jerry-origin-1937aa47` (Jerry's creation session, minus `03-rendered/`), the compositions and recordings.
> - Earlier user message: "miadi will produce episode for interactive TV Series and in them, there's music and the whole body of work here is part of what would make this working even though there might be part of it relating just to a musical album and not musical scoring for film or something like it... Organize that the best flexible ways so that when we propose our PR with all that part installable, it distribute and is all these musical prereq are installable alongside miadi"
> 
> ## The prompt
> 
> That's good work. Uh, what I'm getting on one side is we are going to have a full installation and potential contribution for our delivery systems or distribution systems would be more accurate. After that, why I synchronized, it's important that you know it's because I'm pretty sure that inside of the actual version of the plugin, there are some missing parts. And it is one of your mission, if you had not done it, to actually find out what would make the plugin not being capable of reproducing what we did. So we expect by using that plugin that it's going to be capable of recreating the exact experience that I gave you context before. It might be hard to study and to ensure that we are there, and maybe you have already found out a lot of things and a lot of elements. Therefore, I'll let you advance in phases. And obviously, one of them will, will be to ensure that the contribution that we are making regarding the whole installation and deployment is made, as well as maybe the current version of the plugin. And you will work on it a little bit more to ensure that we are reaching that goal.
> 

## Primary Intent

**Action:** find and add
**Target:** the parts missing from the atelier-jerry plugin (jgwill/miadi-orchestration-kit#44, plugin 0.1.1) that stop it from recreating the experience of Jerry's origin session atelier-jerry-origin-1937aa47
**Urgency:** session
**Confidence:** 85%

## Secondary Intents

1. **complete** — installation and distribution contribution in jgwill/miadi-orchestration-kit#44: the four apt packages miadi-music, miadi-music-render, miadi-music-measure, miadi-music-video in packages/miadi/deb (commit c8dd45b) _(explicit)_
2. **study** — atelier-jerry-origin-1937aa47 plus the compositions and recordings synced from eury to gaia, used as the reference for what the plugin must reproduce _(implicit)_
3. **gather** — missing-part findings already made in earlier work on this plugin _(implicit)_
4. **define** — checkable criteria for 'recreating the exact experience' _(implicit)_
   - depends on: study atelier-jerry-origin-1937aa47
5. **plan** — phased execution: installation contribution, then plugin completion, then reproduction check _(explicit)_
   - depends on: find and add the missing parts
6. **extend** — atelier-jerry plugin beyond 0.1.1 with the missing skills, agents, hooks, scripts or dependencies _(explicit)_
   - depends on: find and add the missing parts
7. **validate** — that a fresh install of the plugin and apt packages can replay a piece from the origin session _(implicit)_
   - depends on: extend atelier-jerry plugin
8. **check** — rubberband, reported missing by the SessionStart hook on this host, against the apt package dependencies _(implicit)_
9. **keep** — a package layout that serves both album work and film/TV scoring and installs alongside miadi (from the earlier message) _(implicit)_

## Context Requirements

### Files Needed
- jgwill/miadi-orchestration-kit PR #44, branch Gerico1007:feat/atelier-jerry-plugin
- commit c8dd45b
- packages/miadi/deb (miadi-music, miadi-music-render, miadi-music-measure, miadi-music-video control and install files)
- atelier-jerry plugin manifest (plugin 0.1.1) with its skills, agents and hooks
- atelier-jerry-origin-1937aa47 session transcript and working folders (synced to gaia, without 03-rendered/)
- synced compositions and recordings folders on gaia
- .agents/gmusic-sync-to-gaia.sh
- .pde/input-prompt.pending.md

### Tools Required
- git
- gh
- dpkg-deb / apt
- claude plugin marketplace install
- abc2midi
- abcm2ps
- rubberband
- ffmpeg
- atelier-jerry:verificateur agent
- atelier-jerry:mesureur agent

### Assumptions
- The current plugin version lacks parts needed to reproduce the origin session ('I'm pretty sure').
- The synced folders on gaia are a sufficient reference even without 03-rendered/.
- A completed plugin can recreate the exact experience of the origin session.
- Earlier work may already have found many of the missing elements.
- The apt packages at c8dd45b are the right vehicle for the installation side.
- PR jgwill/miadi-orchestration-kit#44 is where both the installation work and the plugin work land.

## Expected Outputs

### Artifacts
- Inventory of missing parts: origin session versus plugin 0.1.1 and the apt packages
- Reproduction criteria for one or two pieces from the origin session
- Phase plan with an exit condition per phase

### Updates
- atelier-jerry plugin skills, agents, hooks and manifest (version bump past 0.1.1)
- packages/miadi/deb control files (dependencies such as rubberband if missing)
- PR jgwill/miadi-orchestration-kit#44 description

### Communications
- Commits pushed to Gerico1007:feat/atelier-jerry-plugin
- Phase status update on jgwill/miadi-orchestration-kit#44

## Action Stack

- [ ] Read the origin session atelier-jerry-origin-1937aa47 and list every tool, script, skill, agent, file path and service it used
- [ ] Inventory what atelier-jerry plugin 0.1.1 and the four apt packages at commit c8dd45b carry
- [ ] Collect the missing-part findings already made in earlier sessions and on jgwill/miadi-orchestration-kit#44
- [ ] Define what reproducing the exact experience means as checkable criteria (depends on: Read the origin session atelier-jerry-origin-1937aa47 and list every tool, script, skill, agent, file path and service it used)
- [ ] Check whether rubberband, reported missing by the SessionStart hook, is declared by the apt packages (depends on: Inventory what atelier-jerry plugin 0.1.1 and the four apt packages at commit c8dd45b carry)
- [ ] Compare the origin session inventory against the plugin and package inventory and list the missing parts (depends on: Inventory what atelier-jerry plugin 0.1.1 and the four apt packages at commit c8dd45b carry)
- [ ] Split the work into phases with an exit condition for each (depends on: Compare the origin session inventory against the plugin and package inventory and list the missing parts)
- [ ] Finish the installation and distribution contribution on jgwill/miadi-orchestration-kit#44 (depends on: Split the work into phases with an exit condition for each)
- [ ] Add the missing parts to the plugin and bump its version (depends on: Split the work into phases with an exit condition for each)
- [ ] Install the plugin through the marketplace and the apt packages from scratch on gaia (depends on: Add the missing parts to the plugin and bump its version)
- [ ] Replay one piece from the origin session with the installed plugin and check it against the reproduction criteria (depends on: Install the plugin through the marketplace and the apt packages from scratch on gaia)
- [ ] Push the commits to Gerico1007:feat/atelier-jerry-plugin and update the PR description with each phase's status (depends on: Replay one piece from the origin session with the installed plugin and check it against the reproduction criteria)

## Ambiguity Flags

- **"'recreating the exact experience' does not say whether it means the same agent behavior, the same outputs, or the same renders"**
  - Suggestion: Pick one or two pieces from the origin session. Pass when the same ABC gives the same MIDI and the same measurement figures, and the same loop states are followed.
- **"03-rendered/ was left out of the sync, so the reference renders are absent"**
  - Suggestion: Regenerate the renders from the synced ABC and compare MIDI and measurements, or sync one rendered sample as a reference.
- **"'maybe you have already found out a lot' does not say where earlier findings are recorded"**
  - Suggestion: Search earlier session transcripts, PR #44 comments and the held-gate ledger before starting a new study.
- **"'delivery systems or distribution systems' does not name the channel"**
  - Suggestion: Name the targets: an apt repository, the Claude plugin marketplace, the miadi installer, or all three.
- **"'as well as maybe the current version of the plugin' leaves open whether the plugin changes ship in PR #44 or in a follow-up"**
  - Suggestion: Default to PR #44 because it is the plugin PR. Split only if the installation half is ready to merge first.
- **"Pushing to Gerico1007:feat/atelier-jerry-plugin needs write access to Jerry's fork"**
  - Suggestion: Check push rights. If they are missing, push to a jgwill branch and point the PR at it.
- **"The compositions and recordings hold Jerry's own voice and takes"**
  - Suggestion: The plugin reproduces the process and does not bundle his material. Test material stays on gaia under the studio-portal consent rules.
- **"The number of phases and what closes each one are not stated"**
  - Suggestion: Three phases: installation contribution, missing parts added, reproduction verified. Each closes with a pushed commit and a PR status line.
- **"The flexible album versus scoring layout comes from an earlier message and may not apply to this round"**
  - Suggestion: Keep the current four-package split and record the album/scoring question as a held item unless the inventory shows a need now.
