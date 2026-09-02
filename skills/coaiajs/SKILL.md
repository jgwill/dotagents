---
name: coaiajs
version: "2.0.0"
tags:
  - langfuse
  - prompts
  - tracing
  - observations
  - coaia
  - stc
  - pipeline
description: >
  Interface to the current coaiajs CLI for Langfuse v4/OpenTelemetry tracing,
  prompt management, STC narrative operations, and pipeline orchestration.
  Supports project-scoped credential routing, immutable root/child observations,
  prompt versioning, datasets, scores, comments, and media workflows.
---

# CoAIA.js Skill — Langfuse, Narrative, and Pipeline Bridge

## Purpose

Use `coaia` to connect composition and ceremony work with Langfuse prompts and
observation traces, while retaining structural-tension and pipeline operations.
The current trace model is a group of immutable OpenTelemetry observations that
share one `traceId`; the root observation is the trace container.

## Runtime and freshness

```bash
command -v coaia
coaia --version
npm view coaiajs version
```

The current tested release is `coaiajs 0.4.2`. Upgrade only when the registry is
newer:

```bash
npm install -g coaiajs@latest
coaia --version
```

Global options must precede the command: `--env <path>`, `--json`, `--no-color`,
`-M/--memory-path <path>`, and `-V/--version`.

## Credential and project routing

Configuration priority is process environment > dotenv file > `coaia.json` >
defaults. Langfuse reads only the unprefixed names:

- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_BASE_URL` (or `LANGFUSE_HOST`)

`~/.coaia/.env` also carries named project profiles such as `ENG_LANGFUSE_*`,
`CEREMONY_LANGFUSE_*`, and `STORY_LANGFUSE_*`. Those prefixes are not selected
automatically; remap the intended profile into the standard names inside a
subshell. Never print credentials or put them in command arguments.

```bash
(
  set -a
  . ~/.coaia/.env
  set +a
  export LANGFUSE_PUBLIC_KEY="$CEREMONY_LANGFUSE_PUBLIC_KEY"
  export LANGFUSE_SECRET_KEY="$CEREMONY_LANGFUSE_SECRET_KEY"
  export LANGFUSE_BASE_URL="$CEREMONY_LANGFUSE_BASE_URL"
  coaia --json fuse projects
)
```

Always verify the returned project before writing. Ceremony project ID:
`cmkgk10zy009tad077uc42ixf`.

## Prompt management

```bash
coaia fuse prompts list [--page N] [--limit N]
coaia fuse prompts get <name> [--version N] [--label LABEL]
coaia --json fuse prompts get <name>
coaia fuse prompts create \
  --name <name> --prompt <text> --type text \
  --labels production,latest --tags ceremony \
  --commit-message "why this version exists" [--config '<json>']
```

Prompt retrieval supports both text and chat prompts. Markdown is the default
for `get`; use global `--json` when machine-readable output is required. Reusing
a prompt name creates a new version.

## Langfuse v4 trace and observation workflow

`coaiajs` uses the scoped Langfuse JS SDK v5 and exports Langfuse-v4-compatible
OpenTelemetry spans. Writes go to `/api/public/otel/v1/traces`; reads use
Observations API v2. Legacy mutable trace output patching is not supported.

### 1. Create the root observation container

```bash
coaia --json fuse traces create \
  --name <trace-name> \
  [--trace-id <32-hex-or-uuid>] \
  [--session-id <session>] [--user-id <user>] \
  [--input '<json-or-text>'] [--output '<json-or-text>'] \
  [--metadata '<json-object>'] [--tags tag-a,tag-b] \
  [--version <version>] [--environment <environment>]
```

Preserve both returned values:

- `traceId`: reused by every observation in the trace
- `rootObservationId`: passed as `--parent-id` for direct children

### 2. Append a child observation container

```bash
coaia --json fuse traces add-observation \
  --trace-id <trace-id> \
  --parent-id <root-or-parent-observation-id> \
  --name <observation-name> \
  --type event \
  [--input '<json-or-text>'] [--output '<json-or-text>'] \
  [--metadata '<json-object>'] \
  [--trace-name <trace-name>] [--session-id <session>] \
  [--user-id <user>] [--tags tag-a,tag-b] [--model <model>]
```

Allowed types are `span`, `event`, and `generation`. Each export creates a new,
complete, immutable observation. To correct or extend an observation, append a
new child rather than retrying an existing ID. Propagate trace name, session,
user, and tags on children when available.

For a batch, provide a JSON array to:

```bash
coaia --json fuse traces add-observations --trace-id <trace-id> --file observations.json
```

### 3. Verify the hierarchy

```bash
coaia fuse traces trace-view <trace-id>
coaia --json fuse traces get-observation <observation-id>
coaia fuse traces list [--session-id ID] [--name NAME] [--tags a,b]
coaia fuse traces session-view <session-id>
```

OpenTelemetry writes are flushed immediately by the CLI, but reads can be
eventually consistent; retry verification briefly before treating a missing
observation as a failure.

## Other operations

```bash
coaia fuse datasets
coaia fuse dataset-items
coaia fuse scores
coaia fuse score-configs
coaia fuse comments
coaia fuse media
coaia narrative
coaia pde
coaia plan
coaia pipeline
coaia gh
```

The MCP server is `coaiajs-mcp`. Standard mode exposes Langfuse tracing plus
narrative, PDE, and planning tools. The repository also provides focused Custom
GPT OpenAPI actions for root/child observation export and a companion media
proxy for complete file upload workflows.

## Relational operating rules

- Verify the Langfuse project before every write.
- Record prompt URLs, prompt names, and relationship semantics in structured
  input/metadata rather than relying on prose alone.
- Make lineage explicit: parent prompt, dependent prompt, and relation (`uses`,
  `revises`, `derived-from`, and so on).
- Treat trace and observation IDs as receipts; return them after verification.
- Never expose API keys, Basic Authorization values, or dotenv contents.
