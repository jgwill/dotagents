---
name: relational-workspace-honcho
description: Access Honcho relational memory across workspaces, peers, and agent sessions. Use when asked what other agents or humans understand, what a workspace remembers, where a cross-agent effort stands, to search relational memory, or when the user mentions Honcho, workspace memory, peer context, representations, or session context. Uses a local CLI adapter because Pi has no built-in MCP client.
compatibility: Requires curl, jq, Python, Tailnet access to Honcho, and HONCHO_MCP_BEARER_TOKEN supplied by sourcing ~/.env.
metadata:
  author: Guillaume D. Isabelle
  version: "1.0.0"
  issue: jgwill/dotagents#26
---

# Relational Workspace — Honcho

Honcho remembers **who participated, what each understood, corrections, tensions, and unresolved choices**. It does not replace authoritative repositories, Chronicle vessels, service state, or source recordings.

Pi intentionally has no built-in MCP client. This skill therefore uses the bundled Streamable HTTP MCP adapter:

```bash
scripts/honcho-mcp.sh <command>
```

Resolve `scripts/` relative to this `SKILL.md` directory.

## Credential law

- Source `~/.env`; never read, grep, print, log, or summarize it.
- Never print `HONCHO_MCP_BEARER_TOKEN`.
- The helper sources the file silently and sends authorization through a mode-0600 temporary header file.
- Do not copy the token into Pi settings, skill files, issue bodies, command literals, or session artifacts.

## Grounding sequence

Start broad, then narrow:

```bash
scripts/honcho-mcp.sh health
scripts/honcho-mcp.sh workspaces
scripts/honcho-mcp.sh peers <workspace-id>
scripts/honcho-mcp.sh sessions <workspace-id>
```

Then use the least invasive read that answers the question:

```bash
scripts/honcho-mcp.sh search "<question or grounded terms>" [workspace-id] [limit]
scripts/honcho-mcp.sh session-context <workspace-id> <session-id> [search-query] [tokens]
scripts/honcho-mcp.sh messages <workspace-id> <session-id> [page] [size]
scripts/honcho-mcp.sh peer-context <workspace-id> <peer-id> [target-peer] [search-query] [top-k]
scripts/honcho-mcp.sh representation <workspace-id> <peer-id> [target-peer] [session-id] [search-query] [max-conclusions]
scripts/honcho-mcp.sh chat <workspace-id> <peer-id> "<question>" [target-peer] [session-id]
```

Use `messages` only when summaries/search are insufficient; raw session rows may be larger and more private.

## Read Honcho relationally

1. List workspaces rather than guessing their IDs.
2. Read workspace metadata for purpose and authority boundaries.
3. List peers and sessions before asking what a named peer knows.
4. Use `search` for remembered material, `session-context` for one conversation, and `peer-context`/`representation` for standing understanding.
5. Treat `chat` as a dialectic answer from accumulated memory, not a stored-row citation.
6. Attribute memory to the workspace/peer/session that returned it.
7. Verify operational claims against Git, Chronicle, files, or live services before acting on them.

For music and film work, the currently observed workspace is `gmusic-composition`; always list workspaces again because Honcho is live memory and may have changed.

## Mutation boundary

The helper permits only known read tools by default. Unknown or mutating `tools/call` requests fail closed.

Use raw calls only when a convenience command is insufficient:

```bash
scripts/honcho-mcp.sh call <read-tool-name> '<arguments-json>'
```

Mutation requires both:

1. an explicit user request naming the memory write; and
2. the visible `--allow-mutation` flag:

```bash
scripts/honcho-mcp.sh --allow-mutation call <tool-name> '<arguments-json>'
```

Never infer permission to create workspaces/peers/sessions, alter observation settings, append messages, or replace metadata from a request to “look”, “search”, “connect”, or “remember what they said”. Honcho metadata replacement is not a merge.

## Reporting

Keep answers compact:

```text
- Workspace / peer / session
- What Honcho remembers
- What remains unverified
- One next safe move
```

Do not dump raw memory unless asked. Separate relational memory from authoritative proof.
