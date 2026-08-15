---
name: coaiajs
version: "1.0.0"
tags:
  - langfuse
  - prompts
  - coaia
  - stc
  - pipeline
description: >
  Interface to coaiajs CLI for Langfuse prompt management, STC narrative operations,
  and pipeline orchestration. Enables retrieving, creating, and pushing prompts
  from compositions to Langfuse, and linking prompt URLs back to composition.json.
---

# CoAIA.js Skill — Langfuse Prompt Bridge

## Purpose

Bridge between composition recordings, structural tension charts, and Langfuse prompt management.
Enables a flow where `composition.json` can be pushed as a new Langfuse prompt with its transcriptions,
and the resulting prompt URL is stored back in the composition metadata.

## Tool: `coaia` (v0.1.3+)

Installed at: `$PREFIX/bin/coaia`
Config: `~/.coaia/.env` (Langfuse credentials, Redis, etc.)

## Langfuse Credential Sets

coaiajs loads from `~/.coaia/.env`. Multiple Langfuse projects are configured:

| Label | Env Prefix | Project Use |
|-------|-----------|-------------|
| Ceremony/ilex | `LANGFUSE_` (lines 84-86) | Ceremony prompts, miadi-stcbot |
| Aetherial | `LANGFUSE_` (lines 108-111) | Tracing, aetherial integration |
| Engineering | `ENG_LANGFUSE_` | Engineering world prompts |
| Ceremony alt | `CEREMONY_LANGFUSE_` | Ceremony-specific keys |
| Story | `STORY_LANGFUSE_` | Story world prompts |

**Note:** Last `LANGFUSE_SECRET_KEY`/`LANGFUSE_PUBLIC_KEY` in the file wins for coaia CLI.
The Ceremony/ilex keys (project `cmkgk10zy009tad077uc42ixf`) are overridden by Aetherial keys.
For prompts in the Ceremony project, use direct API calls with Ceremony credentials.

## Core Commands

### Prompt Management
```bash
coaia fuse prompts list                    # List all prompts
coaia fuse prompts get <name>              # Get prompt (text type only — chat type has bug)
coaia fuse prompts get <name> --version N  # Get specific version
coaia fuse prompts create                  # Create new prompt
```

### Other Operations
```bash
coaia fuse sessions          # Session management
coaia fuse traces            # Trace operations
coaia fuse scores            # Score management
coaia fuse datasets          # Dataset management
coaia fuse comments          # Comment operations
coaia narrative              # STC narrative operations
coaia pde                    # Prompt Decomposition Engine
coaia plan                   # Structural tension plans
coaia gh                     # GitHub operations
```

## Known Issues

- `coaia fuse prompts get` fails for `chat`-type prompts with error:
  `Prompt not found with label '[object Object]'`
  **Workaround:** Use direct Langfuse API with node.js:
  ```javascript
  const https = require('https');
  const pk = '<public_key>';
  const sk = '<secret_key>';
  const auth = Buffer.from(pk + ':' + sk).toString('base64');
  https.get({
    hostname: 'cloud.langfuse.com',
    path: '/api/public/v2/prompts/<name>',
    headers: { 'Authorization': 'Basic ' + auth }
  }, handler);
  ```

## Composition-to-Prompt Flow (Planned Integration)

### Vision
1. A `composition.json` from a recording session contains transcription and metadata
2. `coaia fuse prompts create` pushes it as a new Langfuse prompt
3. The returned prompt URL is stored in `composition.json` under `langfuse_prompt_url`
4. This enables relaxed prompt drafting from composition recordings
5. An STC-inspired routing system (like stcbot) can monitor for new compositions
   and auto-create prompts, linking them bidirectionally

### STC Bot Integration
When `@stc`, `@stcgoal`, `@stcissue`, `@stcmastery`, or `@stckin` mentions are detected:
- If tmux session `stcbot` exists, route the mention there
- The bot triages into memory keys for action
- Similar routing could trigger `coaia fuse prompts create` for composition-born prompts

## When to Use

- Retrieving prompts from Langfuse for reuse in agent sessions
- Pushing composition transcriptions as versioned Langfuse prompts
- Linking prompt evolution to chronicle episodes
- Managing STC narrative state through coaia CLI
- Debugging Langfuse credential routing across projects
