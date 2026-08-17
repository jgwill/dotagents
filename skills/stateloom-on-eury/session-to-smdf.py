#!/usr/bin/env python3
"""
session-to-smdf.py — turn a Claude Code session transcript into a state machine.

Reads one or more .jsonl transcripts and emits an .smdf.json describing what the
session ACTUALLY did: the operating states the agent passed through, the events
that moved it, and every observed transition between them.

Nothing here is invented. Every state, event and transition in the output was
observed in the transcript; counts are carried into descriptions so the board
shows weight, not just shape.

    ./session-to-smdf.py TRANSCRIPT.jsonl [MORE.jsonl ...] \
        --name AtelierJamaiDemain --namespace Miadi.Session \
        -o /home/gmusic/salix/repos/stateloom-surface/looms/<name>.smdf.json

Then open the board, or point an agent at it with set_project_file /data/<name>.
"""
import argparse
import collections
import json
import pathlib
import sys

# Tool name -> the operating state the agent is in while calling it.
# Anything unmatched becomes a state of its own, so a new tool is never silently
# folded into a bucket that hides it.
FAMILY = {
    "Bash": "Executing",
    "BashOutput": "Executing",
    "KillShell": "Executing",
    "Read": "Reading",
    "Grep": "Reading",
    "Glob": "Reading",
    "NotebookRead": "Reading",
    "Write": "Writing",
    "Edit": "Writing",
    "MultiEdit": "Writing",
    "NotebookEdit": "Writing",
    "Agent": "Delegating",
    "Task": "Delegating",
    "TaskOutput": "Delegating",
    "TaskStop": "Delegating",
    "SendMessage": "Delegating",
    "WebFetch": "Researching",
    "WebSearch": "Researching",
    "ToolSearch": "Researching",
    "Skill": "LoadingSkill",
    "TodoWrite": "Planning",
    "ExitPlanMode": "Planning",
    "EnterPlanMode": "Planning",
    "AskUserQuestion": "AwaitingHuman",
    "Artifact": "Publishing",
}


def family_of(tool_name):
    if tool_name in FAMILY:
        return FAMILY[tool_name]
    if tool_name.startswith("mcp__"):
        # mcp__<server>__<tool> — the server is the meaningful grouping
        parts = tool_name.split("__")
        server = parts[1] if len(parts) > 1 else "unknown"
        return "MCP_" + "".join(w.capitalize() for w in server.replace("-", "_").split("_"))[:38]
    return "Tool_" + "".join(c for c in tool_name if c.isalnum())[:38]


def ident(s):
    """A state/event name safe for code generation: alnum, unique across the tree."""
    out = "".join(c if c.isalnum() else "_" for c in str(s))
    out = "_".join(p for p in out.split("_") if p)
    return out or "Unknown"


def walk(paths):
    """Yield (record, source_path) for every parseable JSONL line, in file order."""
    for p in paths:
        with open(p, "r", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line), p
                except json.JSONDecodeError:
                    continue


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcripts", nargs="+")
    ap.add_argument("--name", default="Session")
    ap.add_argument("--namespace", default="Miadi.Session")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()

    states = collections.Counter()          # state -> times entered
    events = collections.Counter()          # event -> times raised
    transitions = collections.Counter()     # (from, event, to) -> count
    tools_seen = collections.Counter()      # raw tool name -> count, for descriptions
    lines = 0

    current = "AwaitingHuman"
    states[current] += 1

    def go(event, nxt):
        nonlocal current
        events[event] += 1
        transitions[(current, event, nxt)] += 1
        if nxt != current:
            states[nxt] += 1
        current = nxt

    for rec, _src in walk(args.transcripts):
        lines += 1
        rtype = rec.get("type")

        if rtype == "user":
            msg = rec.get("message") or {}
            content = msg.get("content")
            # A tool_result arriving is not a human speaking.
            is_result = isinstance(content, list) and any(
                isinstance(b, dict) and b.get("type") == "tool_result" for b in content
            )
            if is_result:
                go("ToolReturned", current)
            else:
                go("HumanSpoke", "Interpreting")

        elif rtype == "assistant":
            msg = rec.get("message") or {}
            content = msg.get("content")
            blocks = content if isinstance(content, list) else []
            used_tool = False
            for b in blocks:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    used_tool = True
                    name = b.get("name", "unknown")
                    tools_seen[name] += 1
                    go(ident("Call_" + name), family_of(name))
            if not used_tool and blocks:
                go("Answered", "AwaitingHuman")

        elif rtype == "system":
            sub = (rec.get("subtype") or rec.get("level") or "notice")
            if "hook" in json.dumps(rec)[:2000].lower():
                go("HookFired", "Constrained")
            else:
                go(ident("System_" + str(sub)), current)

        elif rtype in ("mode", "permission-mode"):
            go("ModeChanged", current)

        elif rtype == "file-history-snapshot":
            go("SnapshotTaken", current)

        elif rtype in ("custom-title", "ai-title", "agent-name",
                       "last-prompt", "bridge-session", "attachment"):
            continue  # metadata, not motion

    if not transitions:
        sys.exit("no events found — is that a Claude Code transcript?")

    # ── assemble the SMDF ────────────────────────────────────────────────────
    by_state = collections.defaultdict(list)
    for (src, ev, dst), n in transitions.items():
        by_state[src].append({
            "event": ev,
            "nextState": dst,
            "description": f"observed {n}×",
        })

    state_nodes = []
    for name, entered in states.most_common():
        node = {
            "name": ident(name),
            "kind": "normal",
            "description": f"entered {entered}×",
        }
        if by_state.get(name):
            node["transitions"] = sorted(
                by_state[name], key=lambda t: t["event"]
            )
        state_nodes.append(node)

    event_defs = [
        {"id": ident(e), "description": f"raised {n}×"}
        for e, n in sorted(events.items(), key=lambda kv: -kv[1])
    ]

    doc = {
        "stateMachine": {
            "settings": {
                "namespace": args.namespace,
                "name": ident(args.name),
                "asynchronous": False,
                "_source": {
                    "kind": "claude-code-transcript",
                    "engine": "session-to-smdf.py",
                    "transcripts": [str(pathlib.Path(t).resolve()) for t in args.transcripts],
                    "lines": lines,
                    "tools": dict(tools_seen.most_common()),
                },
            },
            "events": [{
                "name": "SessionEvents",
                "feeder": "SessionFeeder",
                "events": event_defs,
            }],
            "state": {"name": "Root", "states": state_nodes},
        }
    }

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2) + "\n")

    print(f"{out}")
    print(f"  {lines} lines  →  {len(state_nodes)} states, "
          f"{len(event_defs)} events, {len(transitions)} transitions")


if __name__ == "__main__":
    main()
