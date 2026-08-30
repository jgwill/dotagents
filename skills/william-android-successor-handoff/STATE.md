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

## 2026-08-15 — Honcho relational workspace access

- **Found:** Pi has no built-in MCP client, but Honcho's Streamable HTTP endpoint accepts MCP 2025-06-18 and identifies as `honcho-v3` 1.29.0. The `gmusic-composition` workspace holds six peers and one active `composition-toolchain` session; its current tension is packaging scattered JamAI composition/score/video tooling so William can run it beyond Eury.
- **Changed:** created and closed `jgwill/dotagents#26`; added `skills/relational-workspace-honcho/` with a credential-safe MCP CLI adapter and pushed dotagents `main` at `650b256`.
- **Verified:** upstream health is OK; workspace, peer, session, semantic search, and session-context reads succeed. The helper's unknown/mutating tool path fails closed without explicit `--allow-mutation`.
- **Failed or deferred:** no Honcho memory was created or changed. Honcho testimony about remote files remains relational memory until verified on the owning host/repository.
- **Next safe move:** use the `gmusic-composition` workspace to coordinate the package name and owning organization, then verify the remembered Eury tool inventory at source before implementation.

## 2026-08-15 — gmtermux endpoint/deprecation fast-forward

- **Found:** fork branch `origin/refactor/cross-importing-modules-260805` had advanced four documentation/specification and Gaia endpoint-script commits beyond the live current branch; none touched portal or workbench runtime paths or overlapped preserved local composition work.
- **Changed:** fast-forwarded the current home branch `refactor/cross-importing-modules-260805-ep083-rispecs-260815` from `21b60d7` to `8f50940`; no services were restarted and no local composition material was altered.
- **Verified:** the full service profile and both watchdogs remained running; Ritual, both Pixel Recorders, Clipboard, Workspace, Medicine Wheel, and Forgewright each returned HTTP 200 after the merge.
- **Failed or deferred:** the current branch is now four commits ahead of its own fork remote branch; it was not pushed because no push was requested.
- **Next safe move:** continue running normally; push the current branch only when William explicitly asks to publish this fast-forward.

## 2026-08-15 — five fixed composition workspace services

- **Found:** `~/compositions-episodes` was already managed on `:9768`; William clarified the final topology as Aureon `:8768`, Nyro `:9768`, JamAI `:4768`, Synth `:5768`, and Episodes `:3768`. The former workspace menu restarted the process on its current port, so a click could silently replace a fixed service identity. A six-pane full-profile window also exceeds Ilex's mobile tmux geometry and initially prevented Workspace `:8770` from starting.
- **Changed:** on gmtermux branch `refactor/cross-importing-modules-260805`, opened and expanded fork issue `#61`; updated the uncommitted launcher, watchdog, mode manager, Pixel workspace/navigation modules, compatibility route, tests, setup text, and portal documentation. The original five-pane `portals` window stays bounded while Nyro, JamAI, and Synth use separate windows in the same supervised session. The menu now links to each fixed HTTPS port on the current hostname; it never restarts the current process, and Main/shared is omitted because it has no managed service. Starting Synth created its empty expected composition and recording directories.
- **Verified:** all 118 Node tests pass. The managed `full` profile and both watchdogs are running. All five `/compositions` pages return HTTP 200 with the correct workspace marker and all five fixed menu destinations. The legacy switch POST returns Synth `:5768` navigation metadata with `restarting:false`. Ritual `:8443`, Clipboard `:8766`, Workspace `:8770`, Medicine Wheel `:8040`, and Forgewright `:8031` are listening; both workbench health checks pass.
- **Failed or deferred:** the first six-pane startup failed honestly at Workspace `:8770`; the multi-window correction passed. No real-browser click was observable from the shell, though generated links and live pages were verified. The gmtermux changes remain uncommitted; preserved local composition and PDE material remains untouched.
- **Next safe move:** perform one human menu click between workspaces, capture any further operating limitation under issue `#61`, then stage only the implementation/documentation files and commit with a `[#61]` subject when William asks to publish.

## 2026-08-15 — capture-service consumer UI issue and RISE export

- **Found:** the capture-service backend and first real Episode 320 take are proven, but no browser UI consumes the service; Pixel Recorder/Songbird still own their prototype write path. Workspace Portal owns IPv4 `:8770`, while the bounded capture-service proof uses IPv6 loopback.
- **Changed:** opened `miadisabelle/gmtermux#62` to make Pixel/Songbird human-facing clients of `@miadi/capture-service`; created `rispecs/capture-service-consumer-ui.spec.md`, upgraded `capture-vocabulary-deprecation.spec.md` from future-service language to the witnessed transition, and indexed the new surface in `rispecs/README.md`.
- **Verified:** issue #62 reads back open at `https://github.com/miadisabelle/gmtermux/issues/62`; targeted specs pass whitespace/diff checks and cover the RISE desired outcome, API lifecycle, existing consumer roles, port tension, transition law, and acceptance flow.
- **Failed or deferred:** the three rispec changes remain local and uncommitted because the live home branch carries substantial unrelated tracked work and no commit/push was requested. No implementation or service files changed.
- **Next safe move:** review the RISE wording, then stage only the three rispec files and commit with `[#62]` when William asks to publish; implementation begins with the server-side `CAPTURE_SERVICE_URL` adapter, not a second recording engine.

## 2026-08-16 — ep083 Movement Studio local UI witnessed

- **Found:** the ep083 packages were developed from a separate `/a/...` worktree, but the prototype UI is also present and running directly on Ilex from `~/gmtermux-ep083` as `node web/movement-studio.mjs`. That worktree is detached at `7251386` with a pre-existing modified `package-lock.json`.
- **Changed:** no runtime or source was changed; this entry records the witnessed boundary only.
- **Verified:** `http://127.0.0.1:8790/`, `/api/status`, `/api/takes`, and the Socket.IO browser client all return HTTP 200. The studio is idle and lists two recorded movement takes.
- **Failed or deferred:** the process is an unsupervised child of PID 1, not integrated into Ilex's managed gmtermux home checkout, so reboot/process death may remove the UI. Port 8790 is plain HTTP, not HTTPS.
- **Next safe move:** browse `http://127.0.0.1:8790/` on Ilex now; only if persistence is desired, integrate it into the managed gmtermux service profile without disturbing concurrent home-worktree changes.

## 2026-08-17 — Chronicle main synchronized with Gaia

- **Found:** Ilex `main` was four commits ahead and six behind Gaia; 59 incoming paths overlapped untracked files, all byte-identical to their `origin/main` blobs.
- **Changed:** activated the tracked non-rewind hooks, preserved the overlapping files through a verified backup, merged Gaia without rebasing or stashing, and pushed merge commit `d85201d66d6e4d6bc146780dbaaa56b8a20ca2bd`.
- **Verified:** local `main`, `origin/main`, and `ls-remote origin main` agree at `d85201d`; ahead and behind are both zero. Existing non-overlapping untracked work remains untouched.
- **Failed or deferred:** none for synchronization; untracked Chronicle work still belongs to its existing lanes.
- **Next safe move:** preserve those untracked lanes and fetch again before the next Chronicle commit or push.

## 2026-08-18 — Chronicle manual-sync collision reconciled

- **Found:** Chronicle `main` was four commits behind Gaia because 101 incoming Episode 333 paths already existed untracked after a manual folder synchronization. Every collision was byte-identical to its incoming blob; Episode 333 held 149 media files, including 96 media paths not targeted by the incoming commits.
- **Changed:** moved only the 101 proven-identical blockers into `/data/data/com.termux/files/srv/miadi/episodes-sync-preservation/20260818T173054-0400-d85201d-to-776110c`, fast-forwarded to `776110c`, then committed Episode 327's `composition.json` alone as `4ad5af3e46303524784f2b7f415fb76a595646af` and pushed `main`.
- **Verified:** a before/after manifest proves all 190 protected local files unchanged; the backup retains all 101 original blockers. Local `main`, `origin/main`, and `ls-remote origin main` agree at `4ad5af3`; Episode 333 still has 149 media files, and Episode 327's raw M4A remains present and ignored.
- **Failed or deferred:** Android denied the first attempted hard link before any blocker moved or Git state changed; the manifest-and-move path then succeeded. Root `.miette/` remains untracked tool residue and was deliberately not committed.
- **Next safe move:** retain the preservation directory until William confirms the synchronized folder is satisfactory; fetch again before the next Chronicle write and never remove raw media as repository cleanup.

## 2026-08-20 — interrupted Chronicle rebase repaired

- **Found:** `git pull --rebase` replayed Ilex's four local commits onto Gaia `main` at `246023c`, but the shared-tree reference hook correctly refused the final sideways move from the old local tip `f07a1f6` to rebased tip `250575f`, leaving `HEAD` detached with completed rebase metadata.
- **Changed:** after proving Gaia had not advanced and that `250575f` contained `origin/main`, completed only the interrupted `git rebase --continue` with the hook's explicit one-command `MINO_ALLOW_REWIND=1` escape hatch. No reset, stash, clean, or content edit occurred; both untracked Miette paths remain preserved.
- **Verified:** `main` is attached at `250575f`, the rebase metadata is gone, divergence is `0 behind / 4 ahead`, and `git push --dry-run origin main` reports the expected fast-forward `246023c..250575f`.
- **Failed or deferred:** the real push remains deliberately deferred because the first rejected push is a report-and-stop boundary in the shared-tree operating law.
- **Next safe move:** after acknowledging Gaia's intervening Episode 338/545 commits, recheck `ls-remote`; if it is still `246023c`, an ordinary `git push origin main` can publish the already-reconciled four-commit fast-forward.

## 2026-08-21 — upstream PR 260 merged without crossing the Episode boundary

- **Found:** upstream PR 260's head `16858c7` is contained in `Gerico1007/gmtermux` `main` at `4707e0f`. The live branch's port `3768` surface is a dedicated Chronicle Episode Recorder, not a fifth musical composition workspace. `compositions-nyro` and `compositions-aureon` are authoritative symlinks into Miadi Studio and must not regain tracked children.
- **Changed:** merged upstream `main` into current gmtermux branch `refactor/cross-importing-modules-260805` as `f934c342fdc88a4af8c8746e42ab71b7d2dcbcd6`; resolved launcher language in favor of Episode semantics while adding Movement Studio `:8776`; kept both composition symlinks unchanged and removed upstream's two attempted `compositions-nyro` index entries. Reconciled npm dependencies and restarted the full portal profile. No push occurred.
- **Verified:** 167/167 Node tests pass; the focused Episode/portal boundary suite passes 40/40. Live Episode Recorder `:3768` returns 200, withholds `/compositions` (404), and has no composition import control; Nyro composition `ep083` exposes PR 260's import control; Movement `:8776/api/status` returns 200. No tracked Git path exists beneath either composition symlink.
- **Failed or deferred:** Medicine Wheel `:8040` and Forgewright `:8031` were already down. Restart refused because the Medicine Wheel build predates package files, and the canonical upgrader safely refuses the pre-existing tracked `llms` submodule change. No reset, stash, manual build, or submodule mutation was attempted. The two excluded upstream documents remain preserved at `~/tmp/gmtermux-upstream-merge-20260821T154126/`.
- **Next safe move:** reconcile the Medicine Wheel `llms` submodule change with its owning lane, then run `~/scripts/mw-fw-upgrade.sh`; push gmtermux commit `f934c34` only if William explicitly requests publication.

## 2026-08-21 — composition transcription fix sent upstream

- **Found:** fork branch `71-composition-transcribe-upstream-ready` is a clean one-commit branch based on upstream `main` at `4707e0f`; the earlier fork PR 72 was closed as the wrong destination.
- **Changed:** under William's explicit upstream exception, opened `Gerico1007/gmtermux#263` from `miadisabelle:71-composition-transcribe-upstream-ready` to upstream `main`.
- **Verified:** PR 263 is open and mergeable with commit `4994b8d`, two changed files, and 18 additions; its recorded targeted test result is 15/15 passing.
- **Failed or deferred:** no checks are currently reported by GitHub; upstream review and merge remain pending.
- **Next safe move:** await upstream review at `https://github.com/Gerico1007/gmtermux/pull/263` and keep the fork branch available until resolution.

## 2026-08-21 — upstream PR 262 integrated; ep083 worktree retired

- **Found:** upstream PR 262 is merge commit `cdc1fdf` and adds Movement capture/attachment inside compositions. The old detached `~/gmtermux-ep083` service on `:8790` was already dead; managed home already served Movement Studio on `:8776` against the durable `movement-scores` symlink. Upstream still treated `compositions-episodes` as a musical target, conflicting with Ilex's dedicated Chronicle Episode Recorder boundary.
- **Changed:** merged upstream `main` into current `refactor/cross-importing-modules-260805` as `4883aaa`, then excluded Chronicle vessels from Movement composition targets with regression commit `f545a4c`. Restarted the full managed portal profile and watchdog. Preserved the legacy worktree's one-line lockfile drift and stale runtime receipts under `~/tmp/gmtermux-ep083-retirement-20260821T221139-0400/`, then removed the detached worktree and stale `:8790` PID/log files; the score symlink and captures remain.
- **Verified:** 170/170 Node tests pass; changed JavaScript syntax and whitespace checks pass. All nine full-profile ports listen. Movement `:8776` returns idle status, 14 standalone takes, and 94 targets across main/Aureon/Nyro/JamAI/Synth with zero Episode targets. Nyro `ep083` renders Movement and transcription controls; its Movement proxy is healthy. Episode Recorder `:3768/compositions` remains 404. Medicine Wheel and Forgewright health remain HTTP 200; `:8790` is stopped.
- **Failed or deferred:** no real sensor capture was performed to avoid creating or mutating composition material without human acceptance. The two gmtermux commits are local and unpushed; the current branch is 12 commits ahead of its fork remote because it now contains PR 262's ten upstream commits plus the merge and boundary commit.
- **Next safe move:** human-test Start Movement → Stop + Attach from a disposable composition, then push `refactor/cross-importing-modules-260805` to the fork only when William explicitly requests publication.

## 2026-08-22 — Episode 333 movement captures associated locally

- **Found:** Episode 333’s transcript names two movement captures after Songbird take `260816160542`; its composition notes identify `260816160613` as Opus 017’s timing/dynamics source and `260816160647` as its ending gesture. The movement evidence belongs directly to Opus 017, while Opus 018 is grounded in the later park transcription.
- **Changed:** copied those two capture triplets from `miadi-studio/movement/` into `miadi-studio/jamai/op003-la-bifurcation-ep333/` using the current `_movement` naming convention; added both records to `composition.json`; committed exactly those seven paths as `2151f219bcbbcbd8e6d948148cebc354711e57c9` and pushed Chronicle/episodes `main`. Standalone originals remain intact.
- **Verified:** composition JSON parses; both records resolve to JSONL, provenance, and summary files; copied JSONL and summaries are byte-identical to their originals; `git diff --check` passes. Local `HEAD`, `origin/main`, and `ls-remote origin main` all equal `2151f219bcbbcbd8e6d948148cebc354711e57c9`, with zero divergence; the Episode 333 path is clean.
- **Failed or deferred:** none for this association and publication.
- **Next safe move:** the other computer can pull episodes `main` and classify its remaining exported creative and agent artifacts without recreating Episode 333’s movement association.

## 2026-08-22 — Aureon ava002 movement captures associated and pushed

- **Found:** `ava002` carries grounded evidence for five movement takes: `260816133652` (Opus 018 rotations), `260816164326` (Opus 019 gesture), `260816164423` (paired with the prior take for Opus 020), `260816171428` (explicit 100 Hz Opus 022 capture), and `260816173315` (explicit Opus 023 transition source).
- **Changed:** copied those five capture triplets from `miadi-studio/movement/` into `miadi-studio/aureon/ava002/` with `_movement` names, registered all five in `composition.json`, committed exactly those 16 paths as `60c8d53f423823a612ce26097d2a4a4a13e20089`, and pushed episodes `main`.
- **Verified:** all metadata and provenance JSON parses; all five copied JSONL and summary files are byte-identical to their standalone originals; local `HEAD`, `origin/main`, and `ls-remote origin main` agree at `60c8d53f423823a612ce26097d2a4a4a13e20089`; `ava002` is clean.
- **Failed or deferred:** none.
- **Next safe move:** the other computer can pull episodes `main`; no further `ava002` movement migration is needed unless new evidence identifies another capture.

## 2026-08-22 — Medicine Wheel 0.6.3 upgrade restart loop repaired

- **Found:** the release upgrade had completed source/build/global-package work, but Medicine Wheel 0.6.3's bare `GET /api/nodes` returns the provider's first 100 nodes. The workbench manager searched only that page for `chronicle:miadi-chronicle`, falsely declared the existing root missing, and made the watchdog repeatedly restart healthy services while holding the launcher lock.
- **Changed:** updated `~/bin/ensure-miadi-workbench.sh` to verify the root through direct `GET /api/nodes/chronicle%3Amiadi-chronicle`; reloaded only the stale watchdog wrapper; ran the full canonical `~/scripts/mw-fw-upgrade.sh`; restored the tmux watchdog. The manager fix remains an uncommitted tracked change in the live gmtermux worktree.
- **Verified:** the full upgrader completed at 23:22 with Medicine Wheel app/MCP `0.6.3` at `21635d8`, Forgewright `0.2.0` at `554b175`, 81 global and HTTP MCP tools, both health endpoints healthy, and the Chronicle root registered. One 60-second watchdog cycle left both service pane PIDs unchanged, logged `OK required workbench services healthy`, and released the launcher lock.
- **Failed or deferred:** Recharts deprecation and npm `allow-scripts` notices for Sharp are non-fatal release-package warnings; Sharp's install check ran successfully. No dependency/source mutation was made for those upstream warnings, and the local manager fix was not committed or pushed.
- **Next safe move:** use `~/scripts/mw-fw-upgrade.sh` normally; when publication is requested, review and commit only the direct root-node check under the existing gmtermux issue-12 lineage.

## 2026-08-25 — Episode Recorder fullscreen ceremony notes

- **Found:** the live gmtermux branch already contains and has pushed the prior Episode creation work (`0533e20`, `c296b03`), including create-before-recording and first-take vessel-text publication.
- **Changed:** opened and closed fork issue `miadisabelle/gmtermux#79`; added reusable `/lib/fullscreen-editor.{js,css}` and mounted it around each ceremony's existing Working notes textarea and Save notes action. Committed and pushed `8848479` on `refactor/cross-importing-modules-260805`, then respawned only the exact Episode Recorder tmux pane on `:3768`.
- **Verified:** focused tests pass 15/15; local and fork branch heads agree. Live Episode 339 renders three ceremony cards with the fullscreen toggle and Save notes, and `:3768` serves byte-identical component assets over HTTP 200.
- **Failed or deferred:** the broad suite passed 187/188; its unrelated inert-import port probe failed because the managed Movement Studio already owns live port `8776`. No physical browser tap/save was performed against William's notes.
- **Next safe move:** human-tap one Working notes fullscreen icon and save a deliberate note; no source change is expected unless that tactile acceptance exposes an Android-specific issue.

## 2026-08-25 — fullscreen ceremony-note deep links

- **Found:** the shared fullscreen editor can carry navigation generically whenever its host gives the editor an HTML id; no Episode-specific URL logic is needed inside the controller.
- **Changed:** opened and closed fork issue `miadisabelle/gmtermux#80`; ceremony note editors now use `#ceremony-<UUID>-note`, while the shared component synchronizes, restores, and reacts to that hash. Committed and pushed `b224a4a`, then respawned only the exact Episode Recorder pane on `:3768`.
- **Verified:** focused tests pass 16/16 and local/fork heads agree. The live Episode 339 page exposes a verified `#ceremony-78f215e9-eee5-4ac2-88e8-544cf54f9cf2-note` target and serves the exact updated controller; `:3768` remains enabled and listening.
- **Failed or deferred:** no physical browser reload/copy gesture was performed; component routing and the live destination were verified independently.
- **Next safe move:** copy or reload one live note URL on Ilex and confirm the addressed editor opens without summoning the keyboard unexpectedly.

## 2026-08-25 — Episode Recorder transcription lifecycle refresh

- **Found:** the `:3768` stop handler did not refresh the Episode inbox until the Groq transcription request completed, so the durable recording remained invisible during the longest stage; manual transcription also left the take header stale.
- **Changed:** gmtermux commit `72fb79fa82ee7f9c9c37c1df39ab061026de3ad1` on `refactor/cross-importing-modules-260805` refreshes immediately after stop, shows a bounded transcribing state, disables premature transcript/store gestures, and refreshes again on completion or retry. The canonical full portal profile was restarted; the commit remains local and unpushed as requested.
- **Verified:** Episode Recorder tests pass 13/13; JavaScript syntax and whitespace checks pass. The broad suite passes 189/190, with only the known live Movement Studio `:8776` inert-import probe conflict. Live `https://127.0.0.1:3768/` returns HTTP 200 with the new lifecycle UI, Episode and inbox reads are online, `/compositions` remains 404, all portal ports listen, and Medicine Wheel plus Forgewright remain healthy.
- **Failed or deferred:** replaying tmux's quoted `pane_start_command` through `respawn-pane` exited and removed the Episode pane; `~/bin/ensure-portals.sh restart` immediately restored the complete supervised profile. No physical recording or paid transcription was created during shell verification, and no push was requested.
- **Next safe move:** human-test one short inbox take through Stop & Transcribe; it should appear immediately as Transcribing, then open its transcript without another tap. Push the current fork branch only when William requests publication.

## 2026-08-26 — Opus 004 copied to Eury for Abies

- **Found:** Ilex’s stale direct Eury Tailscale name no longer resolves and its ngrok fallback refuses connections; Gaia can still reach Eury through its configured `eury` SSH route.
- **Changed:** streamed the complete current directory `miadi-studio/jamai/op004-la-bifurcation-ep333/` through Gaia without staging it there, creating Eury `/home/mia/compositions-jamai/4abies/`; the Ilex source remains intact.
- **Verified:** all 217 regular-file SHA-256 hashes match, and the complete 236-entry tree structure matches; Eury reports the destination at 50 MB.
- **Failed or deferred:** direct Ilex-to-Eury access remains stale; the successful copy used Gaia as a relay.
- **Next safe move:** JamAI or Abies can continue from Eury `~/compositions-jamai/4abies/`; repair Ilex’s direct Eury alias only in a separate networking task.

## 2026-08-26 — Eury 4abies destination corrected

- **Found:** William intended the `gmusic` account root `/home/gmusic/4abies/`, not Mia’s JamAI composition root.
- **Changed:** streamed the complete Ilex source again through Gaia into `/home/gmusic/4abies/`, owned by `gmusic:gmusic`; the earlier `/home/mia/compositions-jamai/4abies/` copy remains preserved.
- **Verified:** all 217 regular-file SHA-256 hashes and the complete 236-entry tree structure match the Ilex source; Eury reports the corrected destination at 50 MB.
- **Failed or deferred:** the superseded Mia-account copy was not deleted without explicit instruction.
- **Next safe move:** work from `/home/gmusic/4abies/`; remove the earlier Mia-account copy only if William explicitly requests it.

## 2026-08-27 — Episode shelf search refinement deployed

- **Found:** the Episode Recorder shelf indexed numeric `97` but not its padded Chronicle identity `097`, and omitted the canonical folder slug/path from its search corpus.
- **Changed:** opened fork issue `miadisabelle/gmtermux#81`; commit `06919680351eeafc797e1abe4795481b0debbac8` adds padded/unpadded numbers, title, slug, folder path, and goal to each shelf card's search text. The commit is pushed on `refactor/cross-importing-modules-260805`, and the full portal profile was restarted.
- **Verified:** focused Episode Recorder tests pass 14/14; the live selected Episode 097 page returns HTTP 200 and matches `097`, `97`, `ceremony`, `agent`, and `skills`; all managed full-profile ports plus Medicine Wheel and Forgewright listen.
- **Failed or deferred:** the broad suite passes 190/191; only the known unrelated Movement Studio import probe fails because the live supervised service already owns port `8776`. No physical browser typing gesture was observable from the shell.
- **Next safe move:** use the shelf normally; only reopen issue 81 if an Android browser reveals a query-normalization edge not covered by number/title/folder matching.

## 2026-08-27 — Exact Episode ranking and paired embodied capture deployed

- **Found:** entering `140` needed exact identity ranking rather than opaque substring hiding. Independently, Movement `Stop + Attach` scheduled a page reload after 700 ms, destroying an active Songbird MediaRecorder and its minute-long voice-to-MIDI processing chain.
- **Changed:** pushed gmtermux commits `db35055` (`#81`) and `4bfa48c` (`#73`) on the live current branch. Episode filtering now lives in reusable `episode-shelf-filter.js`, ranks exact numbers first, reports counts, and provides explicit home links. Reusable `capture-pair-controller.js` coordinates Songbird + Movement; explicit adapters return start/stop promises; bundle state is persisted and server-verified through `capture-bundles.js`; independent controls remain. The full portal profile was restarted.
- **Verified:** live Episode 140 returns HTTP 200 and the module ranks `140` before `1400` and text mentions. Live JamAI Opus 004 renders the combined bar between Songbird and Movement; its six inline scripts parse, the served controller is byte-identical, and the non-mutating route proof returns the expected 404. Focused paired/composition tests pass 43/43; full suite passes 202/203; every managed port and both workbench health endpoints are healthy. Local and fork branch heads agree at `4bfa48c48dd5899e252b55d2764b11927f3b18c1`.
- **Failed or deferred:** the only suite failure is the known unrelated port-8776 inert-import probe while Movement Studio is intentionally live. No real microphone/sensor take was created; issue `#73` remains open for William's physical Start both → Stop both acceptance and terminal bundle receipt. Issue `#81` is closed.
- **Next safe move:** in one composition, record a short combined take, press only `Stop both`, remain on the page through Songbird processing, then verify the terminal complete/partial message before using Refresh attached takes.

## 2026-08-27 — Aureon pre-fix Songbird loss boundary witnessed

- **Found:** Aureon composition `ava004-sactrda` preserves Movement take `260827111050` (898.706 s, 8,971 packets), but the contemporaneous long Songbird voice never reached disk. The pre-fix composition UI held MediaRecorder output in browser memory until Stop; stopping Movement reloaded the page and destroyed that in-memory recording before `/import`. `260827111035.m4a` is a separate 8.94 s ordinary recording. `260827112601.m4a` is only a later 3.26 s Songbird take, with its MIDI and Nyro sidecar attached.
- **Changed:** no capture, composition, or runtime file was changed; only this successor witness was appended.
- **Verified:** filesystem searches found no matching long audio or temporary browser artefact; `ffprobe`, composition JSON inspection, and hashes prove the surviving identities. Fix commit `4bfa48c` landed at 11:52 local, after the 11:10–11:26 incident.
- **Failed or deferred:** the lost browser-only media cannot be recovered from Ilex storage after the document reload. Movement evidence remains durable.
- **Next safe move:** use the deployed `Start both` → `Stop both` bar and remain on-page through processing; future durability work should stage timesliced Songbird chunks before final Stop so navigation cannot erase a long take.

## 2026-08-28 — Opus 004 paired capture and no-expiry watcher

- **Found:** the old Lightning four-minute clock started at arm and expired before William pressed Start both. The subsequent paired take did survive: Songbird `260828125325.m4a/.mid` and Movement `260828125135_movement.jsonl` plus sidecars. The producer receipt is partial only because Movement Studio timed out answering Stop after attachment.
- **Changed:** explicitly recovered V7, then published the requested shared-seed contrast as V8 movement-neutral and V9 movement-interpreted with the finalized pre-capture direction; both pass 10/10. Watcher v4 now waits indefinitely before producer Start both, begins its duration at declared start, closes on terminal Stop both, and retains the latest pre-arm transcription as direction. Pipeline 2.3.0 supports explicit neutral/interpreted modes.
- **Verified:** 22/22 watcher tests, 23/23 Python tests, Pi extension load, and live V8/V9 MP3/MIDI/score routes pass; MP3 Range is 206.
- **Failed or deferred:** the historical producer receipt remains partial and is not rewritten. The timeout defect itself is corrected and pushed in gmtermux `aa1cf3f`: Movement Stop gets 30 seconds while status/start retain five; 39 focused tests pass and JamAI `:4768` restarted healthy.
- **Next safe move:** William runs `/reload`; then `/lightning-arm 4` must show no deadline until Start both. Use Start both → perform → Stop both; no `/lightning-finish` is required.

## 2026-08-28 — Opus 004 V10 musical-quality mediation

- **Found:** William rejected V9's repeatedly cycling non-guitar accompaniment despite its 10/10 structural ledger. MIDI identifies picked bass as the strongest candidate without claiming perceptual certainty: 136/136 body bass attacks coincided with rhythm guitar, exact guitar/bass bar runs reached five, and drums reached six.
- **Changed:** pipeline 2.4.0 adds `musically-mediated` mode and makes it the default for future automatic captures. Movement is smoothed into four-bar phrase arcs; bass, rhythm guitar, drums, lead, and cadence receive phrase-level arrangement. Three pre-MIDI gates now measure accompaniment repetition, bass independence, and drum phrasing. Episode 333 and the composition each carry a musical-quality witness.
- **Verified:** V10 `a70806438a816e8d563f` attempt 1 stayed unpublished at 12/13 (bass coincidence 0.863636). Attempt 2 published at 13/13 with coincidence 0.681818, 32 drum patterns, and identical-bar runs of one. Current tests pass 22/22 watcher and 25/25 Python; Pi extension load and V10 page/API/media/score routes pass, with audio Range 206.
- **Failed or deferred:** a full mix cannot prove which timbre William perceived, and 13/13 does not establish aesthetic acceptance. William has not yet listened to V10. Watcher v4 runtime acceptance still requires his `/reload`.
- **Next safe move:** listen to V10 first. If the loop remains, preserve it and use private diagnostic stems or William's timbre identification before another revision; do not weaken the new gates or infer perceptual certainty from MIDI alone.
