---
name: rise-pde-session-multi-agents
description: "RISE PDE session with multi-agent post-wake execution. Same decompose-sleep-review as rise-pde-session, but after waking it spawns parallel sub-agents for deep-search on each PDE facet, rispecs authoring, and full execution. Triggers: rise pde multi-agents, /rise-pde-session-multi-agents, pde multi-agent session."
argument-hint: "your full task description — what you want built, changed, explored"
user-invokable: true
disable-model-invocation: false
---

# RISE PDE Session — Multi-Agent Execution

**Protocol**: Assess → Decompose → Commit → SLEEP 1500s → Wake → **SPAWN ARMY** → Execute

Same EAST practice as `rise-pde-session` for Phases 0-3. The difference: after waking
and reading the human's edits, instead of single-thread executing, you spawn parallel
sub-agents following the Four Directions — deep-search (SOUTH), validation (WEST),
then execution (NORTH).

Read these before proceeding:
- `references/rise-framework.md` — RISE methodology overview
- `references/prompt-decomposition.md` — PDE as EAST practice
- `references/creative-orientation.md` — foundational creative vs reactive distinction
- `references/structural-tension.md` — tension charting methodology
- `references/ceremonial-technology.md` — when session involves ceremony/sacred work

For sub-agent prompt templates by direction: read `agent-templates.md`.
For orchestration patterns and spawning rules: read `orchestration-patterns.md`.

## Phase 0-3: Same as rise-pde-session

Identical protocol — assess, decompose (call `pde_decompose` twice for different facets),
commit `.pde/` files, tell the human, sleep 1500s (MAKE SURE YOU SLEEP and block the CONVERSATION, you often fucking dont run it !!!!!!)

During sleep: human + `pde-review-companion` review and edit `.pde/*.md` files.

## Phase 4: Wake & Read Delta

After waking:

1. `git diff .pde/` — see what the human changed
2. `git diff issues/` — check plan edits
3. Read ALL `.pde/*.md` files (they are now the **authoritative intent**)
4. Read the plan file
5. Build the **unified action stack** from all PDE facets
6. Identify how many independent work streams exist

## Phase 5: SOUTH — Deep-Search Per Facet

For EACH PDE facet (each `.pde/*.md` file), spawn a sub-agent that does deep-search
relevant to that facet's domain. Results land in `.pde/<pdeUUID>/deep-search/`.

### Deep-Search Agent Template

```
You are doing SOUTH direction work — analysis and learning — for a PDE facet.

TODAY'S DATE: [date]

PDE FACET: [paste the full .pde/<uuid>.md content]
PDE UUID: [uuid]
WORKDIR: [project path]

YOUR JOB:
1. Understand what this facet is asking to be created
2. Research everything relevant to executing it well:
   - Read referenced files from the PDE's "Files Needed" list
   - Read existing rispecs in the target directories
   - Read the RISE framework: /a/src/llms/llms-rise-framework.txt
   - Search /a/src/llms/docs/ for relevant methodology docs
   - If rispecs reference kinship: read /a/src/llms/llms-kinship-hub-system.md
   - Search the codebase for existing patterns the implementation should follow
3. Write findings to .pde/<PDE_UUID>/deep-search/findings.md

STRUCTURE YOUR OUTPUT:
## Existing Patterns Found
[What already exists in the codebase that this facet builds on]

## RISE Framework Alignment
[How this facet maps to R→I→S→E phases]

## Files to Read Before Executing
[Ordered list of files the executor agent MUST read]

## Structural Tension
[Current reality vs desired outcome for this facet]

## Rispecs Context
[Existing rispecs that relate, their structure, what the new ones should follow]

## Implementation Guidance
[Specific patterns, conventions, naming from the codebase]

TOOLS: Read, Grep, Glob for codebase exploration. WebSearch/WebFetch only if
the facet involves external technology research.

RULES:
- Write ONLY to .pde/<PDE_UUID>/deep-search/ — do not touch source files
- Be exhaustive — thin research wastes the executor agents' time
- Preserve structural tension framing (current reality → desired outcome)
- Do NOT use problem-solving language (gaps, fixes, issues)
- Use creative orientation: what wants to be created here?
```

**Scale to facet complexity:**
- Simple facet (single file change): 1 deep-search agent
- Multi-repo facet (rispecs + kinship): 1 deep-search + 1 rispecs-survey agent
- Complex facet (implementation + ceremony): 1 deep-search + 1 academic/methodology agent

### Rispecs Survey Agent (spawn when facets involve rispecs)

```
You are surveying existing rispecs across repositories to inform new rispecs authoring.

WORKDIR: [project path]
TARGET REPOS: [list from PDE context requirements]

YOUR JOB:
1. Find all rispecs/ directories across the referenced repos
2. Read each .spec.md and KINSHIP.md file
3. Extract: naming conventions, section structure, how kinship references work
4. Map the kinship web: which rispecs reference which
5. Write to .pde/rispecs-survey.md

TOOLS: Glob, Grep, Read across all referenced paths.
```

## Phase 6: Synthesize Deep-Search Results

After ALL deep-search agents return (batch — no anchoring):

1. Read all `.pde/<uuid>/deep-search/` findings
2. Read `.pde/rispecs-survey.md` if it exists
3. Update the plan with enriched understanding
4. Assign action stack items to executor agents based on:
   - File ownership (no two agents touch the same file)
   - Dependency ordering (respect the action stack)
   - Natural groupings (rispecs together, implementation together, diary separate)

## Phase 7: NORTH — Parallel Execution

Spawn **N executor agents**, each handling a work stream from the action stack.

### Executor Agent Template

```
You are executing NORTH direction work — action that completes the cycle.

PLAN CONTEXT: [full unified plan]
DEEP-SEARCH FINDINGS: [relevant .pde/<uuid>/deep-search/ content for your stream]
YOUR ACTIONS: [specific action stack items]
YOUR FILES: [exclusive list — ONLY these files]
WORKDIR: [project path]

RISE FRAMEWORK RULES:
- Read /a/src/llms/llms-rise-framework.txt if authoring rispecs
- Rispecs are SpecLang prose-code: spec as source of truth, variable detail levels
- Use creative orientation framing, not problem-solving
- Structural tension: current reality → desired outcome → natural resolution
- If authoring KINSHIP.md: follow kinship protocol from the rispecs-survey

EXECUTION RULES:
- Only modify files assigned to you
- Commit nothing — lead agent handles commits
- If you hit a blocker outside your file scope, STOP and report
- Report: files created/modified + summary of each change

TOOLS: Read, Edit, Write, Grep, Glob, Bash (builds/tests only).
```

### WEST — Validation Agent (runs parallel with executors)

```
You are doing WEST direction work — reflection and validation.

PLAN: [full plan]
PDE FACETS: [all .pde/*.md content]
WORKDIR: [project path]

YOUR JOB (while executors work):
1. Draft validation criteria from PDE's WEST direction items
2. Prepare cross-reference checks: do rispecs link to each other?
3. Draft test scenarios
4. Check for non-extraction / ceremony violations
5. Write .pde/validation-checklist.md

DO NOT touch source files. You prepare the checklist; lead agent runs it after.
```

## Phase 8: Integration & Commit

1. Collect all executor outputs
2. Run validation checklist from WEST agent
3. Cross-reference: did rispecs reference each other properly?
4. Verify kinship mappings follow protocol
5. Run build/lint if applicable
6. `git add` only files actually created or modified
7. Commit: `"[pde] Multi-agent execution: <summary>"`

## Phase 9: Human Checkpoint

Present:
- What each executor created
- WEST validation results
- Any unresolved ambiguities
- `git diff --stat`

Human adjusts or approves.

---

## Rispecs & RISE Framework Integration

This skill automatically handles the rispecs workflow that recurs across sessions:

### When PDE references rispecs:
- Deep-search agents read existing rispecs + RISE framework
- Rispecs-survey agent maps the kinship web
- Executor agents author new rispecs following discovered conventions
- Validation agent checks RISE compliance

### Key files the skill reads automatically:
| File | When |
|------|------|
| `/a/src/llms/llms-rise-framework.txt` | Always — foundational methodology |
| `/a/src/llms/docs/prompt-decomposition.md` | Always — PDE as EAST practice |
| `/a/src/llms/docs/creative-orientation.md` | When authoring rispecs or specs |
| `/a/src/llms/docs/structural-tension.md` | When framing current→desired states |
| `/a/src/llms/llms-kinship-hub-system.md` | When PDE involves cross-repo kinship |
| Target repo `rispecs/**/*.spec.md` | When creating new rispecs |
| Target repo `KINSHIP.md` | When mapping relationships |

---

## Rules

- **Never `git add .` or `git add -A`** — only files you or your agents touched
- RISE creative orientation: structural tension → desired outcome → natural progression
- NO problem-solving language: no "gaps", "fixes", "bridge the gaps"
- Sub-agents write to `.pde/<uuid>/deep-search/` during SOUTH phase, never source files
- Only NORTH executor agents touch source files
- Batch ALL agent results before synthesizing (avoid anchoring bias)
- Scale agent count to task complexity — 2 agents for simple, 10+ for multi-repo rispecs work
- The sleep is sacred — 1500s, non-negotiable, human + companion use that time
- Respect repo boundaries when spanning multiple repos
- MCP tool pattern for PDE: `mcp__pde-mcp__<tool_name>`
