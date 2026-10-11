#!/usr/bin/env python3
"""
session-to-smdf.py — the MECHANICS layer of a Claude Code session, as a state machine.

Reads one or more .jsonl transcripts and emits an .smdf.json of the agent loop:
the operating modes it passed through, the tool calls and hook fires that moved
it, and every observed transition, each carrying its count.

    ./session-to-smdf.py TRANSCRIPT.jsonl [MORE.jsonl ...] \
        --name AtelierJamaiDemain --namespace Miadi.SessionMechanics \
        -o <episode>/salix/<name>-mechanics.smdf.json

═══ READ THIS BEFORE USING THE OUTPUT ═══════════════════════════════════════

**This is one of two layers, and it is the instrument, not the account.**

    MECHANICS (this script)      MEANING (hand-authored, or LLM-read)
    ─────────────────────────    ────────────────────────────────────
    Executing, Reading,          CURRENT REALITY → action steps →
    Constrained, Delegating        DESIRED OUTCOME
    Call_Bash, HookFired,        tension_established, owner_consented,
    ToolReturned                   moment_of_truth
    forensics: what the loop     conversation: what the work was
    did, where the hooks bit       becoming, and what moved it

The mechanics layer is genuinely useful — every hook fire, every tool call,
every retry is in the JSONL and nowhere else, and counting them reveals things
no one remembers accurately. It is NOT a description of the creative work, and
an agent handed it as if it were will be confused about what happened.

**Never present a mechanics board as "what the session did."** Say what it is:
the instrument reading. Keep the two documents separately named, and relate them
rather than merging them — `*-mechanics.smdf.json` beside the meaning board.

Nothing here is invented: every state, event and transition was observed.
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
    prev_src = None

    def go(event, nxt):
        nonlocal current
        events[event] += 1
        transitions[(current, event, nxt)] += 1
        if nxt != current:
            states[nxt] += 1
        current = nxt

    for rec, src in walk(args.transcripts):
        lines += 1
        rtype = rec.get("type")

        # A new transcript is a SEAM, not a continuation. Without this the last
        # state of file N flows into the first event of file N+1 and the board
        # shows transitions that never happened — the exact thing the word
        # "lineage" claims to model and cannot.
        if src != prev_src:
            if prev_src is not None:
                go("TranscriptBoundary", "AwaitingHuman")
            prev_src = src

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
            kinds = {b.get("type") for b in blocks if isinstance(b, dict)}
            used_tool = False
            for b in blocks:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    used_tool = True
                    name = b.get("name", "unknown")
                    tools_seen[name] += 1
                    go(ident("Call_" + name), family_of(name))
            if used_tool:
                pass
            elif kinds and kinds <= {"thinking", "redacted_thinking"}:
                # Thinking is not answering, and it is emphatically not waiting
                # for a human. Counting it as either was what made AwaitingHuman
                # the largest state on the board while the agent was working.
                go("Thought", "Deliberating")
            elif blocks:
                go("Answered", "Composing")

        elif rtype == "system":
            sub = (rec.get("subtype") or rec.get("level") or "notice")
            if rec.get("hookErrors") or rec.get("preventedContinuation"):
                # ONLY a hook that actually errored or stopped the turn is
                # friction. A routine stop-hook summary fires once per turn and
                # means nothing happened — reading it as constraint turns the
                # turn count into a false finding about struggle.
                go("HookBlocked", "Constrained")
            elif sub == "stop_hook_summary":
                # The reliable end-of-turn marker: exactly one per assistant turn.
                go("TurnEnded", "AwaitingHuman")
            elif sub == "turn_duration":
                continue  # the same boundary, counted twice
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
                    "layer": "mechanics",
                    "isNot": "This board is the agent loop's instrument reading — operating "
                             "modes and tool calls, counted. It is NOT an account of what the "
                             "work was or what it was becoming, and every state name here is "
                             "an inference this script makes, not a label the transcript "
                             "carries. For the account, read a MEANING board: the house "
                             "pattern is /data/ep333/pane-capture-witnessed.smdf.json "
                             "(CURRENT REALITY -> action steps -> DESIRED OUTCOME). This "
                             "board also names only the lane whose transcripts it read; it "
                             "says nothing about any repository it does not list under "
                             "'transcripts'.",
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
