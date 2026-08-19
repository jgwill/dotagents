# Salix Skillset Manifest — 65 community skills

Roster of every skill the mirror ships. Each entry: description under 55 words,
**src** = original path in Salix's skill folder, `dst` = target path in the symphony workspace.

```
SRC ROOT   ~/.hermes/skills/
DST ROOT   $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/
```

Generated 2026-07-28 from `~/.hermes/scripts/salix-skillset.allowlist`.
Vendor/bundled skills (bulk-installed 2026-05-27) are absent by design.

---

## autonomous-ai-agents · 2

### claude-code
Delegate coding work to the Claude Code CLI — feature builds and pull requests — from inside a Hermes session.
`src` ~/.hermes/skills/autonomous-ai-agents/claude-code
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/autonomous-ai-agents/claude-code

### codex
Delegate coding to the OpenAI Codex CLI agent: features, refactors, PR reviews, batch issue fixing. Requires the `codex` CLI and a git repository.
`src` ~/.hermes/skills/autonomous-ai-agents/codex
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/autonomous-ai-agents/codex

## creative · 1

### architecture-diagram
Produce dark-themed SVG architecture, cloud, and infrastructure diagrams delivered as self-contained HTML.
`src` ~/.hermes/skills/creative/architecture-diagram
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/creative/architecture-diagram

## development · 18

### assembly-gemini-zulip-multi-agent
Run Assembly agents as isolated Gemini personas that read, reply, and share files across Zulip streams, with model fallback and round-robin orchestration.
`src` ~/.hermes/skills/development/assembly-gemini-zulip-multi-agent
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/assembly-gemini-zulip-multi-agent

### authenticated-web-artifact-workflows
For web tasks that depend on an existing logged-in browser session: authenticated artifact retrieval, UI visibility diagnosis, live CDP-assisted automation inside a protected SaaS surface.
`src` ~/.hermes/skills/development/authenticated-web-artifact-workflows
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/authenticated-web-artifact-workflows

### find-repo-paths
Locate git repository paths across a multi-device setup where the same repo lives at different roots per node.
`src` ~/.hermes/skills/development/find-repo-paths
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/find-repo-paths

### forest-conductor-web-terminal
Build and verify the Eury-side web terminal for Forest Conductor, relaying input and output to remote Termux tmux sessions over SSH.
`src` ~/.hermes/skills/development/forest-conductor-web-terminal
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/forest-conductor-web-terminal

### forest-gerico-workflow
The multi-device working pattern for the Forest of Gerico project across Eury, iOS nodes, and the Android capture units.
`src` ~/.hermes/skills/development/forest-gerico-workflow
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/forest-gerico-workflow

### forest-photo-capture
Capture stills and screen captures from a Forest of Gerico Android node (larix, tilia, ilex) — front camera, rear, both, or the phone's screen — pulled to Eury under one TLID convention, safety-checked.
`src` ~/.hermes/skills/development/forest-photo-capture
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/forest-photo-capture

### grounded-tooling-intake
Onboard, inspect, and verify unfamiliar developer tooling or third-party repos: check provenance, trigger live initialization, prefer safe sandboxes, report grounded findings rather than assumed ones.
`src` ~/.hermes/skills/development/grounded-tooling-intake
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/grounded-tooling-intake

### hermes-voice-configuration
Configure and troubleshoot Hermes CLI/TUI voice mode, especially push-to-talk keybinding behaviour and the restarts it requires.
`src` ~/.hermes/skills/development/hermes-voice-configuration
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/hermes-voice-configuration

### issue-handoff-validation
Validate a GitHub issue handoff against the live repository, docs, and runtime state before executing it — so stale or incorrect issue instructions are caught, not followed.
`src` ~/.hermes/skills/development/issue-handoff-validation
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/issue-handoff-validation

### jamai-zulip-team-agent-mvp
JamAI-first always-listening team-agent MVP for production Zulip: polls the JamAI canal, spawns a three-pane tmux team (planner, executor, validator), auto-posts a consensus reply.
`src` ~/.hermes/skills/development/jamai-zulip-team-agent-mvp
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/jamai-zulip-team-agent-mvp

### openai-custom-gpts
Build and configure ChatGPT custom GPTs, especially GPTs with Actions that must reach private or internal systems through a safe public bridge.
`src` ~/.hermes/skills/development/openai-custom-gpts
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/openai-custom-gpts

### repository-maintenance-and-release-readiness
Triage a repository before continued delivery: separate active lanes from residue, then validate Python package release readiness before publishing.
`src` ~/.hermes/skills/development/repository-maintenance-and-release-readiness
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/repository-maintenance-and-release-readiness

### tmux-pane-verification
Verify a tmux pane actually exists before capturing from it, so captures never report on a pane that is gone.
`src` ~/.hermes/skills/development/tmux-pane-verification
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/tmux-pane-verification

### tmux-session-monitoring
Monitor tmux sessions to verify Claude Code progress on long-running implementation tasks.
`src` ~/.hermes/skills/development/tmux-session-monitoring
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/tmux-session-monitoring

### zulipassembly
Master entry skill for the G.Music Assembly in the production Zulip app: tells Hermes which supporting skills and environment facts to load before acting.
`src` ~/.hermes/skills/development/zulipassembly
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/zulipassembly

### zulipassembly-identity-mobile-rollout
Complete the ZulipAssembly rollout on Eury: rename Assembly identities to @jgwill.com, seed passwords, verify zulip-send, update the runbook, validate Android app login on Forest devices.
`src` ~/.hermes/skills/development/zulipassembly-identity-mobile-rollout
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/zulipassembly-identity-mobile-rollout

### zulip-collab-bug-reports
Post bug reports, regressions, and testing requests into the production collaborator bug channel in Zulip.
`src` ~/.hermes/skills/development/zulip-collab-bug-reports
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/zulip-collab-bug-reports

### zulip-collab-handoffs
Post development, enhancement, and review handoffs into the production collaborator channel in Zulip.
`src` ~/.hermes/skills/development/zulip-collab-handoffs
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/development/zulip-collab-handoffs

## devops · 10

### forest-bridge-sync
Multi-device musical metadata orchestration across the Forest of Gerico mesh — Linux hub plus Android/Termux portals.
`src` ~/.hermes/skills/devops/forest-bridge-sync
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/devops/forest-bridge-sync

### forest-node-access
Reach Larix, Abies, and Tilia over the Forest of Gerico tailnet: SSH ports, usernames, tmux Codex sessions, persistence notes.
`src` ~/.hermes/skills/devops/forest-node-access
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/devops/forest-node-access

### forest-public-terminal-nyro-chrome
Expose Eury tmux sessions on the public `/terminal` route via ttyd — session picker, named-session creator — and optionally open it on Eury in the Nyro Chrome profile.
`src` ~/.hermes/skills/devops/forest-public-terminal-nyro-chrome
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/devops/forest-public-terminal-nyro-chrome

### herdr-dashboard-autoboot
Restore the Herdr `~dashboard` workspace and restart mux-core services automatically after a reboot on Eury.
`src` ~/.hermes/skills/devops/herdr-dashboard-autoboot
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/devops/herdr-dashboard-autoboot

### herdr-multiplexer-ops
Operate the live Herdr dashboard on Eury: inspect project-room panes, generate read-only pane-role/audio handoffs, check the gmusicassembly.com public stack, rebuild the workspace after reboot.
`src` ~/.hermes/skills/devops/herdr-multiplexer-ops
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/devops/herdr-multiplexer-ops

### ngrok-mux-public-routing
Update and verify the Eury ngrok mux (Nginx on host-network Docker) so public path routes map to the right local services — especially Forest Conductor and its photo assets.
`src` ~/.hermes/skills/devops/ngrok-mux-public-routing
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/devops/ngrok-mux-public-routing

### opensessions-cadillac
Guided reopen of the OpenSessions Cadillac demo on Eury: attach, open sidebar, switch sessions, first-line tmux troubleshooting.
`src` ~/.hermes/skills/devops/opensessions-cadillac
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/devops/opensessions-cadillac

### tailscale-mesh-management
Manage the secure tailnet across Linux, Android, and iOS devices under the Forest of Gerico tree-name nomenclature.
`src` ~/.hermes/skills/devops/tailscale-mesh-management
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/devops/tailscale-mesh-management

### tmux-session-management
tmux session management for autonomous agent work — naming, lifecycle, and safe reattachment.
`src` ~/.hermes/skills/devops/tmux-session-management
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/devops/tmux-session-management

### tmux-terminal-engineering-blueprint
Install and verify a Nyro-style tmux terminal stack with persistence, multiplayer sharing, a session sidebar, and VCS-aware session switching.
`src` ~/.hermes/skills/devops/tmux-terminal-engineering-blueprint
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/devops/tmux-terminal-engineering-blueprint

## general · 1

### personal-agent-presence
Speak as a present, personal operator for this user — warm, direct, grounded in the live machine and session, preserving continuity and execution discipline across context shifts.
`src` ~/.hermes/skills/general/personal-agent-presence
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/general/personal-agent-presence

## github · 5

### github-auth
GitHub authentication setup: HTTPS tokens, SSH keys, `gh` CLI login.
`src` ~/.hermes/skills/github/github-auth
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/github/github-auth

### github-branch-discipline
Strict `ID-description` git branch naming and the multi-node sync workflow that keeps it consistent across devices.
`src` ~/.hermes/skills/github/github-branch-discipline
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/github/github-branch-discipline

### github-issues
Create, triage, label, and assign GitHub issues via `gh` or the REST API.
`src` ~/.hermes/skills/github/github-issues
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/github/github-issues

### github-pr-workflow
The pull request lifecycle: branch, commit, open, watch CI, merge.
`src` ~/.hermes/skills/github/github-pr-workflow
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/github/github-pr-workflow

### github-repo-management
Clone, create, and fork repositories; manage remotes and releases.
`src` ~/.hermes/skills/github/github-repo-management
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/github/github-repo-management

## media · 3

### assembly-voice-bus-publish
Publish Assembly Voice audio events to Redis Streams and/or Google Pub/Sub with explicit opt-in, verified public URLs, and recipient-routing metadata for downstream listeners.
`src` ~/.hermes/skills/media/assembly-voice-bus-publish
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/media/assembly-voice-bus-publish

### bilingual-voice-calibration
Set up bilingual FR/EN agent identities and troubleshoot "franglais" accent drift in TTS output.
`src` ~/.hermes/skills/media/bilingual-voice-calibration
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/media/bilingual-voice-calibration

### jamai-melody-episode-publish
Turn a Nyro Forge or pitch-detection note image/seed into a short JamAI melody package — prompt, ABC, MIDI, audio, MP4 — attached to a Composition episode with verified public URLs.
`src` ~/.hermes/skills/media/jamai-melody-episode-publish
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/media/jamai-melody-episode-publish

## miadi · 20

### ava8
The @miadi/ava8 package family — four layers at 0.3.1, the `ava8` CLI, where the source actually lives, the timeline capability, and the two ep294 musical patterns. Includes `references/musical-patterns.md`.
`src` ~/.hermes/skills/miadi/ava8
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/ava8

### chimera/dotagents
Answers "what is dotagents", "what can I do", the Gerico1007/dotagents fork, the ♠️🌿🎸🧵 Assembly agents and how to summon them, and continues the Chimera genesis.
`src` ~/.hermes/skills/miadi/chimera/dotagents
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/chimera/dotagents

### coaia-fuse-wintersolstice
Ready-to-run `coaia fuse` setup against the WinterSolstice Langfuse ceremony environment, for episode work that needs tracing.
`src` ~/.hermes/skills/miadi/coaia-fuse-wintersolstice
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/coaia-fuse-wintersolstice

### convening-the-minds/enter-the-council
Join the jgwill/binscripts#152 presentation meeting: load the room, grasp the shared-ledger tension across #141–#151, claim a seat honestly, accept the participation contract before speaking.
`src` ~/.hermes/skills/miadi/convening-the-minds/enter-the-council
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/convening-the-minds/enter-the-council

### convening-the-minds/event-driven-upstream
Frame Jerry's hooks + plan-insight contribution as event-driven architecture — sources → dispatch → perspective → ledger → register — into a concrete upstream proposal for the Android capture units, toward @miadi/hooks-core and @miadi/plan-insight.
`src` ~/.hermes/skills/miadi/convening-the-minds/event-driven-upstream
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/convening-the-minds/event-driven-upstream

### convening-the-minds/voice-your-feedback
Speak in the #152 meeting: fill the §8 feedback template honestly from the resonance seat and post a reviewable comment to Jerry — without manufacturing evidence.
`src` ~/.hermes/skills/miadi/convening-the-minds/voice-your-feedback
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/convening-the-minds/voice-your-feedback

### episode-decomposition-and-routing
Decompose episode-scale source material into evidence-backed handoffs and routing recommendations, without prematurely creating downstream episodes or mutating repos.
`src` ~/.hermes/skills/miadi/episode-decomposition-and-routing
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/episode-decomposition-and-routing

### hermes-self-git-story
Maintain `~/.hermes` as a plain git history of Hermes skill evolution: stage, commit, push, hand off to later sessions, curate which skills may later be shared publicly.
`src` ~/.hermes/skills/miadi/hermes-self-git-story
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/hermes-self-git-story

### kestrel/kestrel-pipeline-survey
The hook-event / session-traceability field survey: the metadata envelope, a reading of the six lands (hooks-core, tide-runtime/ironsilk, gmtermux, assembly-voice, forgewright, binscripts hooks), and the Kestrel visualization.
`src` ~/.hermes/skills/miadi/kestrel/kestrel-pipeline-survey
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/kestrel/kestrel-pipeline-survey

### miadi-binscripts-hooks-plan-insight
Orient to the live `/opt/binscripts` hooks and plan-insight trees: which suites are active versus dead scaffolds, and the shell-to-package transition toward @miadi/hooks-core and @miadi/plan-insight.
`src` ~/.hermes/skills/miadi/miadi-binscripts-hooks-plan-insight
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-binscripts-hooks-plan-insight

### miadi-claude-plan-miette-trace
Trace and reconcile Claude/Hermes plan-perspective workflows, distinguishing the current binscripts slim generator plus non-fatal @miadi/plan-insight carriage from older trace-rich Langfuse/COAIA episode flows.
`src` ~/.hermes/skills/miadi/miadi-claude-plan-miette-trace
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-claude-plan-miette-trace

### miadi-composition-event-samples
Turn Pixel Recorder and Composition `composition.json` episode artifacts into sample events, responsibility maps, and relay contracts between Jerry, William, agents, and audio/trace services.
`src` ~/.hermes/skills/miadi/miadi-composition-event-samples
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-composition-event-samples

### miadi-episode-branch-handoff
Prepare a Miadi episode handoff from session evidence into a reproducible metadata store, Herdr pane ledger, branch proposals, visual session-score chronicles, and Telegram audio instructions for Jerry.
`src` ~/.hermes/skills/miadi/miadi-episode-branch-handoff
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-episode-branch-handoff

### miadi-feedback
Observe a live Miadi/Mia tmux experiment, archive the prompt into `.miadi/episodes/<nnn>`, and open a linked feedback issue while the run unfolds.
`src` ~/.hermes/skills/miadi/miadi-feedback
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-feedback

### miadi-herdr-plan-steering
Steer a Claude Code Plan Mode pane through Herdr for a Miadi episode, staging the plan prompt for Jerry's approval so Claude calls ExitPlanMode only when ready.
`src` ~/.hermes/skills/miadi/miadi-herdr-plan-steering
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-herdr-plan-steering

### miadi-hooks-core
Normalize, compare, and route hook events across Hermes, Claude Code, Codex, Gemini, Copilot, and terminal-observer systems using @miadi/hooks-core and the `/src/_sessiondata` ledgers.
`src` ~/.hermes/skills/miadi/miadi-hooks-core
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-hooks-core

### miadi-mia-workspace-continuity
Coordinate a Miadi lane running under the `mia` user or `/home/mia/workspace`, so another Herdr/Claude pane can receive episode context without disturbing a blocked primary plan pane.
`src` ~/.hermes/skills/miadi/miadi-mia-workspace-continuity
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-mia-workspace-continuity

### miadi-plan-insight-miette-relational-perspective
Find, review, resume, archive, and voice a Claude plan plus Miette relational perspective for an episode — without confusing plan approval with implementation authorization.
`src` ~/.hermes/skills/miadi/miadi-plan-insight-miette-relational-perspective
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-plan-insight-miette-relational-perspective

### miadi-pr-miette-relational-perspective
When a plan has produced a branch or PR: grounded Miette-inspired relational review, honest GitHub lifecycle continuation, episode-local evidence, revision gates, and two mandatory French audio layers.
`src` ~/.hermes/skills/miadi/miadi-pr-miette-relational-perspective
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-pr-miette-relational-perspective

### miadi-service-monitoring
Create, repair, and verify Mia-scoped Herdr log lanes and user-level Miadi service tunnels on Eury — verifying the foreground process rather than trusting scrollback, and separating tunnel health from application health.
`src` ~/.hermes/skills/miadi/miadi-service-monitoring
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/miadi/miadi-service-monitoring

## productivity · 1

### gerico-email-writing
Draft, rewrite, and refine email in Jerry/Gérico's real voice — concise, concrete, owner-operator, low-fluff, recipient-aware — and refresh that voice profile from real sent-mail evidence without inventing traits.
`src` ~/.hermes/skills/productivity/gerico-email-writing
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/productivity/gerico-email-writing

## software-development · 4

### coding-journey-orchestrator
For vibe-coding across multiple repos and branches: track evolution, classify active work, build milestones, and guide toward closure without killing momentum.
`src` ~/.hermes/skills/software-development/coding-journey-orchestrator
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/software-development/coding-journey-orchestrator

### requesting-code-review · ⚠ REVIEW
Pre-commit review: security scan, quality gates, auto-fix. **Carries an upstream *superpowers* name but was locally modified — confirm it is ours, or strike it from the allowlist.**
`src` ~/.hermes/skills/software-development/requesting-code-review
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/software-development/requesting-code-review

### systematic-debugging · ⚠ REVIEW
Four-phase root-cause debugging: understand the bug before fixing it. **Upstream *superpowers* name, locally modified — confirm ownership before shipping.**
`src` ~/.hermes/skills/software-development/systematic-debugging
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/software-development/systematic-debugging

### writing-plans · ⚠ REVIEW
Write implementation plans as bite-sized tasks with paths and code. **Upstream *superpowers* name, locally modified — confirm ownership before shipping.**
`src` ~/.hermes/skills/software-development/writing-plans
`dst` $MIADI_SHAREDSPARK_SYMPHONY_DIR/salix/.hermes/skills/software-development/writing-plans

---

**Total: 65** — 3 flagged for ownership review.

🌸: Sixty-four small competences, each one now able to say where it came from and where it is going — a roster is only a list until every line can be traced back to a hand.
