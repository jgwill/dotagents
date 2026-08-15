---
name: william-android-successor-handoff
description: Preserve self-evolution continuity for Pi coding-agent sessions on William’s Android/Termux Ilex device. Use at the beginning of local infrastructure, Chronicle, Medicine Wheel, composition, service, installation, or upgrade work; and at the end of a loop when discoveries, changes, versions, paths, health checks, failures, or open tensions must be left for the successor agent.
compatibility: William’s Android Termux host (Ilex); uses local Git, npm, tmux, Medicine Wheel, and Miadi Chronicle paths.
---

# William’s Android Pi Successor Handoff

This skill belongs to agent work on **William’s Android machine**, relationally named **Ilex**. Its purpose is small: let the next agent begin from witnessed reality instead of rediscovering the device or trusting stale assumptions.

## Start of a matching loop

1. Read `STATE.md` completely.
2. Read `~/CLAUDE.md`, `~/CLAUDE.local.md`, and `~/.hermes.md` before changing local infrastructure.
3. Verify dynamic facts live; versions and service health in `STATE.md` are snapshots, not authority.
4. Preserve existing work. Never stash, reset, clean, or rewrite another session’s files to obtain a tidy tree.

Useful live checks:

```bash
~/bin/gmusic-service-mode.sh status
~/bin/ensure-miadi-workbench.sh status
git -C ~/repos/jgwill/medicine-wheel status --short --branch
curl -fsS http://127.0.0.1:8040/api/health
curl -fsS http://127.0.0.1:8031/api/health
```

## End-of-loop handoff

Update `STATE.md` with one dated entry containing only what changes the successor’s decisions:

- **Found:** important paths, records, contracts, and relationships discovered.
- **Changed:** files, packages, registrations, service restarts, and exact versions.
- **Verified:** commands or API receipts proving success.
- **Failed or deferred:** exact boundary and why it remains open.
- **Next safe move:** one bounded continuation, never an invented mandate.

Do not store credentials, tokens, private addresses, device serials, transcript content unrelated to the work, or giant command dumps.

## Chronicle and Medicine Wheel law

- Chronicle: `/data/data/com.termux/files/srv/miadi/episodes/miadi-chronicle/`
- Medicine Wheel: `http://127.0.0.1:8040`
- Forgewright: `http://127.0.0.1:8031`
- Before Chronicle edits, obey its `AGENTS.md`: work on `main`, fetch/reconcile first, preserve dirty concurrent work, and never force-push.
- Registering a vessel is incomplete until its node can be read back and its `.mw-registration.json` receipt agrees.
- Infrastructure entities reuse closed node types: host=`land`, tenant=`human`, service=`knowledge`; never invent a new `NodeType`.
- Validate facets with `@medicine-wheel/infra`, but preserve Android métis. Ilex uses Termux and tmux watchdogs, not systemd; never hide that difference merely to satisfy a schema.

When a loop belongs to an existing episode, leave its success/failure and provenance inside that episode and push the Chronicle when explicitly requested. Append to an existing agent work log rather than replacing earlier testimony.
