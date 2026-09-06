---
name: rise-pde-multi-agent
description: "Multi-agent PDE companion using mcp-miadi-code-pde. Runs alongside rise-pde-session during sleep window OR standalone. Spawns parallel sub-agents for decomposition, execution, review prep. Triggers: rise pde multi, multi-agent pde, parallel pde, spawn pde agents, /rise-pde-multi-agent."
argument-hint: "your full task description — or 'companion' to activate during a sleep window"
user-invokable: true
disable-model-invocation: false
---

# RISE PDE Multi-Agent Session

Two modes of operation:

## Mode A: Sleep-Window Companion

When a `rise-pde-session` agent is sleeping (1500s), the human opens a second
session and invokes this skill. Sub-agents fan out to do productive work so
that when the sleeping agent wakes, the `.pde/` directory and plan are richer.

```
Terminal 1: rise-pde-session  ──decompose──commit──[SLEEP 1500s]──wake──revise──execute
                                                       │
Terminal 2: rise-pde-multi-agent ──────────────────── ACTIVATES HERE
                                                       │
            ├── Agent A1: deeper structural decomposition
            ├── Agent A2: dependency tracing across codebase
            ├── Agent A3: implicit intent + edge case analysis
            ├── Agent A4: pre-execution scaffolding (tests, types)
            └── Lead: synthesize all into revised plan.md + .pde/ edits
                                                       │
Terminal 1: ──────────────────────────────────────── WAKES, sees git diff
```

## Mode B: Standalone Parallel PDE

Full multi-agent PDE session without the sleep pattern. Decomposes, executes,
and integrates — all via parallel sub-agents.

---

## Companion Mode (A) — During Sleep Window

### Step 1: Detect Context

1. Check `.pde/` for existing decomposition files from the sleeping agent
2. Read ALL `.pde/*.md` and `.pde/*.json` files
3. Read `issues/<N>/plan.md` if it exists
4. Run `git log --oneline -5` to see the sleeping agent's commit
5. Understand what was decomposed and what the original prompt was

### Step 2: Spawn Enrichment Agents (parallel)

Spawn **3-5 sub-agents** using the Task tool. Each deepens a different facet.

#### Agent A1: Structural Depth
```
You are deepening a PDE decomposition's STRUCTURAL analysis.

EXISTING PDE OUTPUT: [paste .pde/*.md content]
ORIGINAL TASK: [extracted from PDE files]
WORKDIR: [project path]

YOUR JOB:
- Read the code files referenced in the PDE output
- Verify the decomposition's assumptions against actual code
- Find structural patterns the initial decomposition missed
- Identify files that SHOULD be in scope but weren't listed
- Call mcp__mcp-miadi-code-pde__pde_decompose for a second-pass decomposition
  focused on what was missed

TOOLS: Read, Grep, Glob to explore codebase. mcp-miadi-code-pde for decomposition.

OUTPUT: Additional decomposition ID + findings report.
```

#### Agent A2: Dependency Tracing
```
You are tracing dependencies across the codebase for a PDE decomposition.

EXISTING PDE OUTPUT: [paste .pde/*.md content]
WORKDIR: [project path]

YOUR JOB:
- Grep imports/requires for every file in the PDE action stack
- Map what depends on what — build the actual dependency graph
- Identify ripple effects: if file X changes, what else breaks?
- Flag ordering constraints the initial decomposition missed
- Write findings to .pde/dependencies.md

TOOLS: Grep, Read, Glob for codebase exploration.

OUTPUT: Dependency graph + critical path + risk zones.
```

#### Agent A3: Implicit Intent + Edge Cases
```
You are the edge-case finder for a PDE decomposition.

EXISTING PDE OUTPUT: [paste .pde/*.md content]
ORIGINAL TASK: [extracted from PDE files]
WORKDIR: [project path]

YOUR JOB:
- Re-read the original task with fresh eyes
- What did the user imply but not state?
- What edge cases exist in the target code?
- What tests should exist but don't?
- What could go wrong during execution?
- Call mcp__mcp-miadi-code-pde__pde_decompose with extractImplicit: true

TOOLS: Read, Grep to check existing tests. mcp-miadi-code-pde for decomposition.

OUTPUT: Implicit intents found + edge case list + test gap analysis.
```

#### Agent A4: Pre-Execution Scaffolding
```
You are preparing scaffolding so the executor (sleeping agent) can move fast on wake.

EXISTING PDE OUTPUT: [paste .pde/*.md content]
WORKDIR: [project path]

YOUR JOB:
- Draft test skeletons for planned changes (write to .pde/test-scaffolds/)
- Draft type definitions if new types are needed (write to .pde/type-drafts/)
- Create a checklist the executor can follow step-by-step
- Write .pde/execution-checklist.md

RULES:
- Do NOT modify source files — only write to .pde/
- The sleeping agent will decide what to use when it wakes

TOOLS: Read, Write (only to .pde/ directory), Grep, Glob.

OUTPUT: Scaffold files created + execution checklist.
```

### Step 3: Synthesize & Update Plan

After all enrichment agents return:

1. Read all new `.pde/` content they generated
2. Cross-reference findings: did agents agree or contradict?
3. Update `issues/<N>/plan.md` (or `.pde/plan.md`) with enriched understanding
4. Add a `## Multi-Agent Enrichment` section to the plan showing what was found
5. `git add` only `.pde/` files and plan updates
6. Commit: `"[pde-companion] Enriched decomposition: <summary>"`

The sleeping agent will see this via `git diff .pde/` when it wakes.

### Step 4: Brief the Human

Present a summary:
- What each agent found
- Key disagreements or new insights vs original decomposition
- Recommended edits to `.pde/*.md` files (human can edit before wake)
- Things that need human judgment (ambiguities only a human can resolve)

---

## Standalone Mode (B) — Full Parallel PDE

### Phase 0: Assess
1. Read input, identify scope, read referenced files
2. Determine parallelization: how many independent work streams?

### Phase 1: Parallel Decomposition (2-3 agents)

Spawn decomposition agents — each with a different lens:

| Agent | Lens | Focus |
|-------|------|-------|
| D1 | Structural | Code changes, files, APIs, configs |
| D2 | Relational | Dependencies, ordering, ripple effects |
| D3 | Implicit | Unstated assumptions, edge cases, ambiguities |

Each calls `mcp__mcp-miadi-code-pde__pde_decompose` → reasons through it →
calls `mcp__mcp-miadi-code-pde__pde_parse_response` to store.

Scale: 2 agents for small tasks, 3 for medium, 3+ for large.

### Phase 2: Synthesize Plan

After ALL return (batch — no anchoring bias):
1. Read all `.pde/*.md` outputs
2. Cross-reference D1 structure × D2 dependencies × D3 implicit intents
3. Build unified ordered action stack
4. Write plan, commit `.pde/` + plan

### Phase 3: Parallel Execution (N agents)

Assign action stack items to executor agents with **strict file ownership**:
- No two executors touch the same file
- Each gets: its actions, the full plan context, its file list
- A review-prep agent (R1) runs in parallel drafting the review doc

#### Executor Template
```
PLAN CONTEXT: [full plan]
YOUR ACTIONS: [assigned items]
YOUR FILES: [exclusive file list]
WORKDIR: [path]

RULES: Only modify your files. Commit nothing. Report blockers.
TOOLS: Read, Edit, Write, Grep, Glob, Bash (builds/tests only).
OUTPUT: Files modified + summary of each change.
```

#### Review-Prep Agent (R1)
```
PLAN: [full plan]
WORKDIR: [path]

Prepare: expected diff summary, key review points, test scenarios, risk assessment.
```

### Phase 4: Integration
1. Collect all outputs, verify completion
2. Build/lint/test
3. Resolve cross-file integration
4. `git add` only modified files
5. Commit: `"[pde] Execute: <summary>"`

### Phase 5: Human Checkpoint
Present R1's review summary + `git diff --stat`. Human adjusts or approves.

---

## Webhook Integration

When `PDE_MIADI_WEBHOOK` env is set, pass `send_to_miadi: true` on all
`pde_parse_response` calls. This feeds the Miadi event hub for dashboard tracking.

## Rules

- **Never `git add .` or `git add -A`** — only files you or your agents touched
- RISE creative orientation: structural tension → desired outcome → natural progression
- Sub-agents use `model: "opus"` for quality
- Decomposition agents call `mcp-miadi-code-pde` tools; executors use file tools
- Respect repo boundaries
- Scale agent count to task complexity
- Batch ALL results before synthesizing
- MCP tool pattern: `mcp__mcp-miadi-code-pde__<tool_name>`
- In companion mode: write ONLY to `.pde/` — never touch source files
