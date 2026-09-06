---
name: mino-new-session
description: Import a GitHub Gist into mino-mcp, add rich metadata, and locally generate all three perspectives (mia_miette, tushell_journal, the_council). Expects a gist URL as argument.
argument-hint: "<gist_url>"
user-invokable: true
disable-model-invocation: false
allowed-tools: Agent, Bash, Read, Glob, Grep, WebFetch, mcp__mino-mcp__create_gist, mcp__mino-mcp__get_gist, mcp__mino-mcp__list_templates, mcp__mino-mcp__update_gist_metadata, mcp__mino-mcp__generate_perspective, mcp__mino-mcp__update_perspective, mcp__mino-mcp__get_perspectives, mcp__mino-mcp__summarize_gist, mcp__mino-mcp__update_gist_title
---

# Skill: Mino New Session — Gist Import + Local Perspectives

Import a Copilot CLI session gist into mino-mcp and locally generate all perspectives + metadata in one shot.

## Input

`$ARGUMENTS` = a GitHub Gist URL (e.g. `https://gist.github.com/miadisabelle/abc123...`)

If no URL is provided, stop and ask the user for one.

## Process

### Phase 1: Import & Discover

1. **Fetch gist content** — Use an Agent (subagent_type: general-purpose) with WebFetch to retrieve the gist's raw content via GitHub API (`https://api.github.com/gists/<gist_id>`). Extract:
   - Title / description
   - Session ID, duration, timestamps
   - File content (the session transcript)
   - What was worked on: repos, tools, skills used, missions accomplished
   - AI entities involved, hostname, agent model

2. **Import into mino-mcp** — Call `mcp__mino-mcp__create_gist` with the URL. Capture the returned `gist.id` (UUID) — this is used for all subsequent calls.

3. **Fetch perspective templates** — Call `mcp__mino-mcp__list_templates` to load the voice/structure expectations for each perspective type.

### Phase 2: Metadata

4. **Update metadata** — Call `mcp__mino-mcp__update_gist_metadata` with rich metadata derived from Phase 1 analysis. Use these reserved keys where applicable:
   - `tags` (string[]): descriptive tags for the session's domain, tools, patterns
   - `repository` (string): primary GitHub repo involved
   - `agent` (string): AI agent used (e.g. `fable-6`)
   - `agent_model` (string): model ID
   - `source_type` (string): typically `copilot-session`

   Plus custom keys as relevant:
   - `skill`: the slash-command/skill that drove the session
   - `missions`: array of mission descriptions
   - `session_duration`: human-readable duration
   - `runtime_platform_hostname`: host where session ran
   - `pde_workdir`: PDE working directory if applicable

### Phase 3: Perspectives (all local mode)

Generate all perspectives using `mode="local"` — YOU write the content, never delegate to server AI.

5. **`mia_miette` perspective** — Follow the template voice:
   - Start with `🧠 Mia:` — structural analysis (2-3 sentences): what existed at session start vs end, architectural decisions, velocity
   - Then `🌸 Miette:` — human translation (2-4 sentences): the *why*, warmth, connect the dots for the reader
   - Keep it grounded in what actually happened. No fluff. Fun to read for an advanced 12-year-old.
   - Do NOT use the phrase "structural tension" — instead describe the before/after states directly.

6. **`tushell_journal` perspective** — Follow the template voice:
   - Start with `Journal Entry:` + an evocative title
   - 4-8 sentences in first person as Tushell, the data diver in the Azure Lake
   - Transform technical work into lived narrative using metaphor/analogy. Avoid raw file names — paint pictures instead.
   - End with `Synopsis:` — 1-2 plain sentences of what actually happened technically.
   - Use 🌊 glyph.
   - Expand acronyms (YAML, JSON, MCP, PDE) meaningfully when used.

7. **`the_council` perspective** — Follow the template voice:
   - Dialogue between 🧠 Mia, 🌸 Miette, and 🌊 Tushell
   - They discuss the session — building on each other, finding shared insight
   - 2-3 exchanges, then a `◈ Shared insight:` line synthesizing what none could reach alone
   - Must reference the actual content of the mia_miette and tushell_journal perspectives you just wrote
   - Do NOT mention MCP tools used during the session — focus on what was *created*

**Parallelism**: Steps 5 and 6 can run in parallel. Step 7 (the_council) MUST wait for both 5 and 6 to complete, as it references their content.

### Phase 4: Confirm

8. **Output a summary table** to the user showing what was created:
   - Gist UUID and title
   - Metadata tags
   - Each perspective type with a one-line description of what was written

## Voice & Quality

- Write perspectives that are *fun to read* — adapted for an engaged, curious audience
- Ground every metaphor in something real from the session
- No passive descriptions of facts — find the story, the movement, the transformation
- No "comprehensive" anything
- Use glyphs: 🧠 Mia, 🌸 Miette, 🌊 Tushell

## Error Handling

- If gist import fails → check if the gist already exists via `mcp__mino-mcp__list_gists` and offer to update instead
- If a perspective already exists → use `mcp__mino-mcp__update_perspective` instead of `generate_perspective`
- If gist content is empty or unreadable → report to user, do not generate empty perspectives
