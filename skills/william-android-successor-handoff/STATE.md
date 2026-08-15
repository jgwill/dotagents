# Ilex successor state

Last witnessed: 2026-08-05, Pi session `019fcfce-2833-756c-a584-0f05d95ea3a5`.

## Identity and landmarks

- Ilex is William’s Google Pixel 2 running Android 11 and Termux; Android reports hostname `localhost`, while **Ilex** is its relational host name.
- Home/gmtermux: `/data/data/com.termux/files/home/`
- **Repository root:** `../repos/` from home, i.e. `/data/data/com.termux/files/repos/` — **never assume `~/repos/`**, which does not exist on Ilex. Resolve configured roots from `~/.config/miadi-workbench/env` before repository operations.
- Compositions: `~/compositions-nyro/`
- Chronicle: `/data/data/com.termux/files/srv/miadi/episodes/miadi-chronicle/`
- Skills: `~/.agents` → `/data/data/com.termux/files/repos/jgwill/dotagents`
- Medicine Wheel source: `~/repos/jgwill/medicine-wheel`
- Workbench manager: `~/bin/ensure-miadi-workbench.sh`

## Current service snapshot

The active `focus` profile held four observed services:

- Medicine Wheel `:8040` — app `0.5.7`, MCP `4.5.7`, JSONL store.
- Forgewright `:8031` — `0.1.0`, Chronicle read-only.
- Pixel Recorder Nyro `:8768`.
- Pixel Recorder Episodes `:9768`.

Medicine Wheel and Forgewright were restarted and verified healthy. The runtime is sustained by tmux watchdogs, not systemd.

## Package upgrades made in this loop

- `@miadi/inquiry-weave` `0.6.0` → `0.6.3`
- `@miadi/episodic-memory-schema` `0.5.1` → `0.7.0`
- `@miadi/composition` `0.1.1` → `0.1.2`
- `@miadi/hooks-core` `0.4.0` → `0.5.0`

Medicine Wheel app/MCP/storage/ontology were already at current `0.5.7` / `4.5.7` lines.

## Episode 090 anchors

- Composition intake: `~/compositions-nyro/ep090-networking-ceremony/`
- Chronicle vessel: `2026-06-24-episode-090-networking-ceremonies/`
- Wheel node: `chronicle:2026-06-24-episode-090-networking-ceremonies`
- Agent provenance: `agent-work-log.md`
- Registration receipt: `.mw-registration.json`
- Old ceremony ID `ceremony:1782487736071:y380v` is honestly dangling on the current wheel; do not fabricate a replacement.
- The larger composition-to-Chronicle reconciliation is deferred. Carry only the most important source material, with provenance and human validation.

## Infrastructure inventory registered this loop

- Host: `infra:host:ilex-android`
- Tenant: `infra:tenant:ilex:u0_a194`
- Services: `infra:service:ilex:medicine-wheel`, `infra:service:ilex:forgewright`, `infra:service:ilex:nyro-recorder`, `infra:service:ilex:episodes-portal`
- Session opening: `ceremony:ep090:ilex-mobile-successor:20260805:opening`
- Session closing: `ceremony:ep090:ilex-mobile-successor:20260805:closing`
- Initial pushed report commit: `2f0ef2fa3a75b57c51c063cfc3f229e80f30f80a`
- Final pushed Chronicle head after closing and cycle feedback: `974f024ad06bb061602a652346a6326f3508e7f0`
- Narrative cycle: `cycle-ep090-ilex-mobile-networking-adequacy-20260805` with seven registered beats, two ceremonies, ten mapped relations, and a complete East → South → West → North arc
- Chronicle report: `experiments/ilex-android-successor-and-infrastructure-2026-08-05.md`
- Experiment receipt: `experiments/ilex-android-inventory.receipt.json`

All facets passed `@medicine-wheel/infra@0.5.7` Zod validation and the four observed port bindings had no conflict. Important schema feedback: `ServiceFacet.unit` assumes systemd semantics, while Ilex is tmux-managed. The records preserve that mismatch in `metis`; future evolution should add a manager-neutral runtime field or Termux adapter.

## Preserved boundary

At the snapshot, the Chronicle had pre-existing live JSONL store changes and an untracked Episode 300 vessel. They belong to concurrent work and must not be stashed, reset, cleaned, or casually bundled into another commit.

## 2026-08-05 — Plan Perspective collection and Episode 310 relation

- **Found:** `origin/feat/infra-0.1.0-116` was already fully merged into Medicine Wheel `main`. Chronicle Episode 310 arrived at commit `f258fcb`; its PerspectiveRecord existed as `plan-perspective:f2eab200-f324-4a9f-b279-cb7957eaa96b`, but only carried a source-host absolute episode path that Forgewright rejects.
- **Changed:** Medicine Wheel commit `826c422` allows unfiltered `GET /api/plan-perspectives`; it is pushed on `origin/main`. The production build passed and the exact Medicine Wheel + Forgewright workbench was deliberately restarted. The existing PerspectiveRecord was re-registered through the API with canonical relative Episode 310 membership while preserving its absolute provenance path.
- **Verified:** the requested unfiltered curl returns HTTP 200 with 12 records; canonical Episode 310 filtering returns the one perspective; Forgewright `/api/chronicle/perspectives` projects the same record; both services are healthy.
- **Failed or deferred:** Vitest aborts on this Android host with `Illegal instruction`/exit 132 before tests execute; `npm run build` completed successfully. The original plan file remains on its source host, while the Chronicle artifacts and registered perspective narrative are locally readable.
- **Next safe move:** normalize source-host absolute Chronicle paths at the registration boundary so future plan-to-episode relations do not require a corrective re-registration.

## 2026-08-05 — gmtermux cross-import refactor deployed

- **Found:** `refactor/cross-importing-modules-260805` is based directly on the formerly deployed `ep117-ilex-miafork-dev` and splits five portal monoliths into 116 changed files. Static and isolated startup checks exposed seven extracted module-contract defects, including 29 unresolved runtime references; the pre-existing suite alone did not exercise server startup.
- **Changed:** switched the live home worktree to `refactor/cross-importing-modules-260805`; reconciled `node_modules` to the pushed lockfile (`coaia-narrative@0.16.0`, Xterm packages); repaired seven runtime files; restarted the managed `focus` profile. Fix commit `dd78c0fbcddfcf90477f4ed019b7db2e8c1dfc8d` is pushed to `miadisabelle/gmtermux` on the refactor branch.
- **Verified:** 24/24 Node tests pass; 131 JavaScript files pass syntax; all extracted modules pass an ESLint `no-undef` audit; Pixel, Ritual, Clipboard, Workspace, and Forest Conductor passed isolated startup/read smokes. Live Nyro `:8768` and Episodes `:9768` serve roots, composition pages/APIs, playground, recordings, status, Forest reads, static client modules, and correct HTTP redirects. Portal and workbench watchdogs remain stable; Medicine Wheel `:8040` and Forgewright `:8031` remain healthy.
- **Failed or deferred:** `npm audit --omit=dev` reports 12 production findings (1 low, 3 moderate, 8 high); no automatic dependency mutation was attempted. Microphone start/stop, uploads, deletes, and other write-side routes were deliberately not exercised against William's real data. Existing untracked composition material remains untouched.
- **Next safe move:** add a portable server-assembly regression test that exercises route registration/startup contracts, then review the audit findings and perform human UI/write-path acceptance before merging the refactor.

## 2026-08-06 — server-assembly follow-up and full portal profile

- **Found:** refactor branch commit `708fb1558eb399e7376bc3deeebc37047c0af85f` adds the previously recommended portable server-assembly contract and uniform `buildApp()` exports for Pixel, Clipboard, and Workspace. Local `HEAD` and the fork branch agree.
- **Changed:** switched the managed G.Music profile from `focus` to persistent `full`, restarting both Pixel recorders on the new commit and starting Ritual Console `:8443`, Clipboard Gallery `:8766`, and Workspace Portal `:8770`. No source edits or gmtermux commits were needed.
- **Verified:** all 38 Node tests pass, including assembly/route dispatch for all five portal surfaces. Every full-profile service returned HTTP 200 on representative page and JSON reads; HTTP redirects were correct; Workspace listed 20 folders and read one folder successfully. After watchdog reconciliation all five panes and ports remained stable with no captured runtime errors. Medicine Wheel `:8040` and Forgewright `:8031` remained healthy.
- **Failed or deferred:** no write-side portal action was exercised against real data. `full` intentionally consumes more memory than the former `focus` profile.
- **Next safe move:** leave `full` active while Workspace is needed and monitor Android memory pressure; use `gmusic-service-mode.sh focus` if the device needs the lower-memory profile.

## 2026-08-07 — self-service Medicine Wheel + Forgewright upgrade

- **Found:** Node 24 reports `os.cpus().length === 0` on Ilex. The `kuzu@0.11.3` lifecycle installer interprets that as `NUM_THREADS=0` and attempts an unnecessary C++ source build. Forgewright's deployed Chronicle read-only surface builds and runs without that native lifecycle step.
- **Changed:** added `~/scripts/mw-fw-upgrade.sh` (gmtermux `7b3b93e`, pushed on `refactor/cross-importing-modules-260805`) and the discoverable `ilex-mw-fw` skill (dotagents `94d25ad`, pushed on `main`). The upgrader fast-forward-pulls configured roots, preserves tracked work gates, skips unchanged dependencies/fresh builds, suppresses Kuzu lifecycle compilation on Android, synchronizes released global MW packages, restarts the exact tmux workbench, and logs to `~/.cache/miadi-workbench/mw-fw-upgrade.log`.
- **Verified:** the no-argument upgrader completed. Medicine Wheel is app `0.5.9` / MCP `4.5.9` at `15d4cf3`; Forgewright rebuilt at `80875ac` and now identifies as `@miadi/forgewright`; ports `8040` and `8031` are healthy; global and HTTP MCP each expose 81 tools including `register_host` and `list_infra_topology`. Pi discovered `~/.agents/skills/ilex-mw-fw/SKILL.md` without diagnostics.
- **Failed or deferred:** the first proof run safely stopped before restart when Kuzu requested zero build threads; an attempted bounded native retry was human-aborted as unnecessary and no compiler remained. The corrected deployment did not compile Kuzu. The gmtermux commit is pushed on the current refactor branch, not merged to the fork's default branch; issue `miadisabelle/gmtermux#49` remains open for normal integration.
- **Next safe move:** use `~/scripts/mw-fw-upgrade.sh --dry-run` before future upgrades, then the no-argument command; on failure, hand the printed phase and canonical log to an agent rather than running npm/CMake manually.

## 2026-08-08 — workbench LAN exposure and current Forgewright root

- **Found:** `~/bin/ensure-miadi-workbench.sh` already launches both Next.js servers with `-H 0.0.0.0`; the workbench environment still pointed Forgewright at the obsolete `forgewright-plan-episode-4` worktree.
- **Changed:** added a hard prohibition against that legacy worktree to `~/CLAUDE.local.md`; changed `FORGEWRIGHT_ROOT` to `/data/data/com.termux/files/repos/miadisabelle/forgewright`; fast-forwarded current Forgewright `main` to `80875ac`, reconciled its missing dependencies with lifecycle scripts disabled, built it, and restarted the exact workbench. No application package source changes remain.
- **Verified:** launcher gates pass; logs report `Network: http://0.0.0.0:8040` and `Network: http://0.0.0.0:8031`; direct LAN calls to `http://192.168.2.52:8040/` and `:8031/` both return HTTP 200, and both LAN `/api/health` responses are healthy. The active Forgewright root is the current repo at HEAD `80875ac`.
- **Failed or deferred:** reachability from a separate Wi-Fi client was not observable from Ilex; if it still fails there, inspect Wi-Fi client isolation/routing rather than changing application source.
- **Next safe move:** use the current LAN URLs while Ilex remains at `192.168.2.52`; re-read `wlan0` after network changes because DHCP may change the address.

## 2026-08-08 — Songbird sung-capture deployment

- **Found:** `ffmpeg` was already installed at `$PREFIX/bin/ffmpeg`; the live gmtermux worktree remained on `refactor/cross-importing-modules-260805` with concurrent composition files preserved.
- **Changed:** fast-forwarded fork-only `origin/refactor/cross-importing-modules-260805` from `7b3b93e` to `10b8620` and restarted only the Pixel recorder portals with `~/bin/ensure-portals.sh restart`.
- **Verified:** `https://localhost:8768/songbird` returns HTTP 200 and `/echo-trace` returns HTTP 302.
- **Failed or deferred:** none.
- **Next safe move:** perform a human sung-capture acceptance pass when ready, confirming both voice and MIDI land in the intended composition.

## 2026-08-08 — Songbird composition-embed deployment

- **Found:** the live gmtermux worktree remained on `refactor/cross-importing-modules-260805` at `10b8620`.
- **Changed:** fast-forwarded fork-only `origin/refactor/cross-importing-modules-260805` to `ce7df6a` and restarted only the Pixel recorder portals.
- **Verified:** `https://localhost:8768/lib/songbird-capture.js` and `/songbird` both return HTTP 200.
- **Failed or deferred:** none.
- **Next safe move:** perform a human capture from a composition page and confirm the take's voice and MIDI are stored in that same composition.

## 2026-08-08 — Songbird take-card deployment

- **Found:** the live gmtermux worktree was at `ce7df6a` on `refactor/cross-importing-modules-260805`.
- **Changed:** fast-forwarded fork-only `origin/refactor/cross-importing-modules-260805` to `c0451f3` and restarted only the Pixel recorder portals.
- **Verified:** `/lib/songbird-take-card.js`, `/lib/songbird-capture.js`, and `/songbird` on Nyro `:8768` all return HTTP 200.
- **Failed or deferred:** none.
- **Next safe move:** use human acceptance to validate preview, transport, note annotation, and Keep/Retake/Discard behavior against a real take.

## 2026-08-08 — Reusable Songbird Take Card completed

- **Found:** the live fork branch was at `c0451f3`; unrelated staged and untracked device material remained present and preserved.
- **Changed:** fast-forwarded `refactor/cross-importing-modules-260805` to `6e8d55c`, restarted only the Pixel recorder portals, and closed `miadisabelle/gmtermux#53` after green verification.
- **Verified:** `npm test` passes 103/103; Take Card JS/CSS, `/songbird`, and `/compositions/ep250-bridgemind-miadi-workspaces` return HTTP 200. Both pages mount `SongbirdTakeCard`; the studio has no legacy `takePanel`; the composition flow exposes annotation plus Keep, Retake, and Discard.
- **Failed or deferred:** none; no device-only fix was needed.
- **Next safe move:** human-test one real sung take through Keep, Retake, and Discard when write-side acceptance is desired.

## 2026-08-08 — Songbird live-note lane deployment

- **Found:** the live fork branch was at `6e8d55c`; unrelated device material remained preserved.
- **Changed:** fast-forwarded `refactor/cross-importing-modules-260805` to `74ddb70`, restarted only the Pixel recorder portals, and closed `miadisabelle/gmtermux#54` after green verification.
- **Verified:** `npm test` passes 105/105; `/lib/nyro/pitch.js` and a composition detail page return HTTP 200, and the page contains `sbLive`, `sbLiveNotes`, and `NyroPitch.detectPitch`.
- **Failed or deferred:** none.
- **Next safe move:** human-test the live pitch lane with the device microphone when write-side acceptance is desired.

## 2026-08-08 — Songbird composition handed to JamAI on Eury

- **Found:** Eury's JamAI composition root is `~/compositions-jamai/`; the requested `william-op001` destination was absent.
- **Changed:** copied Ilex `~/compositions-jamai/op001-songbird-spark-rel-ep317/` to Eury as `~/compositions-jamai/william-op001/`; the source remains intact.
- **Verified:** the destination contains one file, `composition.json`, whose SHA-256 matches the Ilex source (`d40158eddacee45a0e1beba512d1a3a1b2e4a3df630dc53dbfd8fea1b6398c44`).
- **Failed or deferred:** no commit was requested in Eury's composition repository.
- **Next safe move:** JamAI can continue from Eury's `~/compositions-jamai/william-op001/`.

## 2026-08-12 — Phase 1 capture/recordings redeploy

- **Found:** Ilex repositories live under `../repos/` from home (`/data/data/com.termux/files/repos/`), not `~/repos/`; the workbench config remains authoritative for both production roots. The unrelated untracked `.miette` material in both roots was preserved.
- **Changed:** fast-forwarded Medicine Wheel `main` from `15d4cf3` to `ca48ed8` and Forgewright `main` from `b911e5b` to `cdf5f2b`; rebuilt both production apps, refreshed global MW `0.5.9` packages, and restarted the exact tmux workbench. No gmtermux/home-repo source was changed.
- **Verified:** both branches equal `origin/main`; `:8040` and `:8031` are healthy. `GET :8040/api/captures` is HTTP 200. Episode 316's scoped recordings API is HTTP 200 with `belt-intent-capsule.mp3`; the actual `EpisodeRecordingsSection` renders its heading/count, filename, audio control, and scoped audio URL, whose range smoke returns HTTP 206.
- **Failed or deferred:** the exact requested unfiltered `GET :8031/api/chronicle/recordings` returns HTTP 400 (`episode must be a relative chronicle path`), not the expected 200; the deployed route contract currently requires `?episode=<relative-path>`.
- **Next safe move:** Mia/Forgewright should decide whether the unfiltered endpoint must aggregate/list or whether the acceptance URL should be scoped, then ship that contract correction in a later development phase rather than mutating this deployment.

## 2026-08-12 — Version-release follow-up redeploy

- **Found:** the prior runtime was Medicine Wheel app `0.5.9` and Forgewright `0.1.0`; each production `main` was one commit behind after Mia's release. Forgewright's health route still hardcodes `0.1.0` even at the `v0.1.1` release.
- **Changed:** fast-forwarded Medicine Wheel to `2c6906e` (`0.5.10`) and Forgewright to tagged `69623f9` (`v0.1.1`), reconciled changed lockfiles, rebuilt both, installed global `@medicine-wheel/app@0.5.10` plus independently versioned `@medicine-wheel/mcp@4.5.9`, and restarted the exact tmux workbench.
- **Verified:** both repo HEADs equal `origin/main`; manager status reports app `0.5.10`, MCP `4.5.9`, and Forgewright `0.1.1`; both health endpoints return HTTP 200. Exact `GET :8040/api/captures` returns HTTP 200, and Episode 316's scoped recordings endpoint still returns HTTP 200 with one recording.
- **Failed or deferred:** exact unfiltered `GET :8031/api/chronicle/recordings` still returns HTTP 400 because `episode` is required. `GET :8031/api/health` is healthy but incorrectly self-reports version `0.1.0`; source `package.json`, exact tag, build output, and manager status all prove deployed Forgewright is `0.1.1`.
- **Next safe move:** correct Forgewright's unfiltered recordings acceptance contract and derive health version from package/build metadata in a source-development phase; do not patch the production checkout ad hoc.

## 2026-08-12 — Forgewright v0.1.2 Captures vocabulary redeploy

- **Found:** production Forgewright `main` was two commits behind at `v0.1.1`; its only unrelated local material remained untracked `.miette/` and was preserved. Medicine Wheel was already fresh at app `0.5.10` / MCP `4.5.9`.
- **Changed:** fast-forwarded Forgewright from `69623f9` to exact tag `v0.1.2` (`210fac4`), reconciled its changed lockfile without native lifecycle builds, built production artifacts, and restarted the exact managed tmux workbench; global MW synchronization was deliberately skipped.
- **Verified:** `GET :8031/api/health` returns HTTP 200 and version `0.1.2`; repo HEAD equals `origin/main`. The live Episode 170 payload has zero captures and the actual episode section renders `Captures · 0 none captured yet`. Episode 316 returns one take and renders `Captures · 1`, `belt-intent-capsule.mp3`, its audio control, size, and timestamp; neither rendered section uses the visible word `Recordings`.
- **Failed or deferred:** none in the requested acceptance. The workbench manager restarts the exact two-pane session as one unit, so Medicine Wheel restarted healthy but its current source and fresh build were not changed.
- **Next safe move:** browse normally; if another episode lacks the Captures line, preserve its exact episode path and inspect that path's scoped API response before changing code.

## 2026-08-12 — Phase 2 first real capture-service take on Ilex

- **Found:** the existing `/data/data/com.termux/files/repos/jgwill/Miadi` checkout was 53 commits behind with a tracked lockfile modification, so it was preserved; a clean shallow `main` clone was made at `/data/data/com.termux/files/repos/jgwill/Miadi-capture-service-phase2` (`827886b`). IPv4 `:8770` is already owned by gmtermux Workspace Portal; it was not stopped or changed. Termux:API and `termux-microphone-record` are installed, and GROQ was available from `~/.env` (value never exposed).
- **Changed:** built `node-service-kit`, `capture`, `capture-client`, and `capture-service@0.1.0`; fast-forwarded the Chronicle safely to `3c3a441` to receive Episode 320 while preserving three modified store files byte-for-byte; launched capture-service in tmux `miadi-capture-service-phase2` on IPv6 loopback `[::1]:8770`, with runtime files under `$PREFIX/var/run/miadi-capture-service-phase2`. Captured, registered, and transcribed `260812183252.m4a` directly in Episode 320 with its provenance and transcription sidecars.
- **Verified:** capture-service tests pass 43/43. The real Termux driver reported recording then idle; the take is 5 seconds / 9,945 bytes. Groq `whisper-large-v3` transcription returned HTTP 200 uncached with French + English fields. Medicine Wheel `/api/captures` returns count 1 and the Episode 320 record. Forgewright returns Episode 320 count 1 and renders `Captures · 1`, captured/transcript badges, duration, and audio control; capture-service and Forgewright range reads each return HTTP 206.
- **Failed or deferred:** the first pnpm install failed on unrelated Android `node-pty`/`tree-sitter` native lifecycle builds; the locked install succeeded with scripts suppressed and package build/tests gated it. Two IPv4 launches failed `EADDRINUSE` before the Workspace owner was identified; IPv6 coexistence preserves phase law but the registered URI is device-local, not a LAN capture endpoint. The tmux service has no boot watchdog yet.
- **Next safe move:** keep using `[::1]:8770` for this bounded device proof. Any permanent supervision, LAN exposure, or IPv4 port reassignment must be an explicit later phase coordinated with the existing Workspace Portal.

## 2026-08-12 — Episode 320 first real take pushed

- **Changed:** staged only `260812183252.m4a`, `260812183252.m4a.take.json`, and `260812183252.json` by exact name; committed them on Chronicle `main` as `60c395f4c09686a137537e372eb8200a0f809f5a` (`Episode 320: preserve Ilex's first real capture-service take (Miadi#598)`) and pushed to the local bare `origin`.
- **Verified:** local `main`, `origin/main`, and `ls-remote origin main` all resolve to `60c395f4c09686a137537e372eb8200a0f809f5a`; `git rev-list --count origin/main..main` and the reverse count both return `0`.
- **Preserved:** the pre-existing modified Chronicle `.mw/store/{ceremonies,edges,nodes}.jsonl` files remain unstaged and were not included in the commit.

## 2026-08-13 — Chronicle origin migrated to Gaia SSH

- **Found:** the new SSH tunnel presents the same trusted ED25519 and RSA host-key fingerprints as Gaia. Its Chronicle `main` was five commits ahead of Ilex, with no path overlap against Ilex's four modified Medicine Wheel store files.
- **Changed:** replaced the Chronicle checkout's local-bare `origin` with the new Gaia SSH origin, pinned the exact tunnel endpoint to Gaia's already-trusted ED25519 key, and added the optional `miadi-episodes-gaia` SSH alias with strict host checking and the intended client identity. Fast-forwarded `main` to `065eb694a530010f029c96327a6b4142733e576a`.
- **Verified:** strict read access and a no-mutation push dry run both succeed; local `main` equals `origin/main`. The four pre-existing modified store files were hashed before and after the fast-forward and remained byte-identical. SSH directory/key/config/known-host permissions remain restrictive.
- **Failed or deferred:** the ngrok address is ephemeral. No automatic trust-on-first-use or disabled host-key checking was introduced.
- **Next safe move:** if the tunnel address rotates, compare its presented key fingerprint with Gaia's already-trusted key before updating the remote and alias; preserve the four live store modifications.

## 2026-08-15 — local Chronicle search capability

- **Found:** `~/.hermes.md` names the local Chronicle root. `ava001` is mapped, not expressly born into Episode 317; `ep102-song-heal-caretaker` still has no Episode 102 vessel, while Episodes 100, 103, 120, and 300 provide grounded healing/film/song support.
- **Changed:** created and closed `jgwill/dotagents#25`; added `skills/miadi-chronicle-search/SKILL.md` and pushed dotagents `main` at `8ddfbb9`. Opened `miadisabelle/gmtermux#60` as the read-only Composition UI/runtime companion to Episode 097 routing.
- **Verified:** local and remote dotagents `main` both resolve to `8ddfbb96ad0146b5b9fd82d5a2982a4476c672bb`; gmtermux issue 60 links the shipped capability.
- **Failed or deferred:** no Chronicle, composition, or gmtermux source was changed. Cross-agent workspace memory may still require Honcho rather than filesystem search alone.
- **Next safe move:** connect Honcho when William wants other agents' workspace memory, then use `ava001` as the first human-reviewed fixture for gmtermux issue 60.
