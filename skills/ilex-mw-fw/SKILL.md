---
name: ilex-mw-fw
description: Upgrade, rebuild, restart, verify, or diagnose Medicine Wheel on port 8040 and Forgewright on port 8031 on William's Android/Termux Ilex host. Use when asked to update the local Medicine Wheel app or MCP, update Forgewright, run the Ilex workbench upgrader, inspect an upgrade failure, or find the self-service maintenance command.
compatibility: William's Android/Termux Ilex host with tmux, npm, Git, and ~/scripts/mw-fw-upgrade.sh.
---

# Ilex Medicine Wheel + Forgewright Upgrade

The canonical self-service command on Ilex is:

```bash
~/scripts/mw-fw-upgrade.sh
```

It pulls, rebuilds, restarts, and verifies the two production services managed by `~/bin/ensure-miadi-workbench.sh`:

- Medicine Wheel app + HTTP MCP: `http://127.0.0.1:8040`
- Forgewright: `http://127.0.0.1:8031`

The upgrader reads `~/.config/miadi-workbench/env`. Treat its configured `MEDICINE_WHEEL_ROOT` and `FORGEWRIGHT_ROOT` as authoritative; do not substitute a similarly named clone.

## Before an agent operates it

Read the Ilex continuity contract and live state first:

```text
~/.agents/skills/william-android-successor-handoff/SKILL.md
~/.agents/skills/william-android-successor-handoff/STATE.md
```

Then inspect without deploying:

```bash
~/scripts/mw-fw-upgrade.sh --dry-run
```

The script permits unrelated untracked material but refuses tracked local changes, detached HEADs, missing upstreams, concurrent upgrades, and non-fast-forward pulls. Never stash, reset, clean, force-pull, or switch the live gmtermux branch to bypass those gates.

## Upgrade

For the normal complete operation, run exactly:

```bash
~/scripts/mw-fw-upgrade.sh
```

The script:

1. takes a host-local upgrade lock;
2. fast-forward-pulls each configured production branch;
3. skips dependency installation when the lockfile is unchanged and dependencies exist;
4. rebuilds only stale production artifacts;
5. installs the exact released global `@medicine-wheel/app` and `@medicine-wheel/mcp` versions;
6. restarts the exact tmux workbench session;
7. validates both HTTP services plus global and HTTP MCP tool discovery.

Useful bounded variants:

```bash
~/scripts/mw-fw-upgrade.sh --skip-forgewright
~/scripts/mw-fw-upgrade.sh --skip-global
~/scripts/mw-fw-upgrade.sh --help
```

## Android/Termux boundary

Ilex is tmux-managed, not systemd-managed. Do not translate this workflow into `systemctl` commands.

Node may report `os.cpus().length === 0` on this host. `kuzu@0.11.x` turns that into `NUM_THREADS=0` and attempts a large, unnecessary C++ source build. **Do not manually run `npm ci`, `npm rebuild kuzu`, CMake, or a Kuzu source compile for this deployed read-only Forgewright surface.** The upgrader avoids dependency installation when the lockfile is unchanged and suppresses native lifecycle scripts if a Kuzu lockfile genuinely requires reinstallation on Android. Let the subsequent Next.js production build be the deployment gate.

## Verification

A successful upgrader already runs the canonical checks. For an independent read-back:

```bash
~/bin/ensure-miadi-workbench.sh status
curl -fsS http://127.0.0.1:8040/api/health
curl -fsS http://127.0.0.1:8031/api/health
npm list -g --depth=0 @medicine-wheel/app @medicine-wheel/mcp
```

Success means both tmux panes are live, both ports respond healthy, Medicine Wheel reports JSONL storage, HTTP MCP is available, the Chronicle root node is registered, and Forgewright reports its Medicine Wheel dependency healthy.

## Failure handoff

Every invocation appends to:

```text
~/.cache/miadi-workbench/mw-fw-upgrade.log
```

On failure, the script prints the failed phase and that log path. Do not rerun broad install/build commands by hand. Give the next agent:

1. the printed phase;
2. `~/.cache/miadi-workbench/mw-fw-upgrade.log`;
3. the output of `~/bin/ensure-miadi-workbench.sh status`;
4. only the npm debug-log path named in the canonical log, if npm failed.

A suitable request is: “Read the Ilex MW/FW skill and diagnose the last failed phase from `~/.cache/miadi-workbench/mw-fw-upgrade.log`; preserve live work and finish only the bounded upgrade.”

After a successful repair or version change, append a concise dated entry to the successor `STATE.md` with found, changed, verified, deferred, and next-safe-move facts. Never place credentials or giant command output there.
