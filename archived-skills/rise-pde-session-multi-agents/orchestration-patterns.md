# Four Directions Orchestration Pattern

How multi-agent spawning maps to the Medicine Wheel directions in a PDE session.

## The Pattern

```
                    🌅 EAST — VISION
                  PDE Decomposition
                  (rise-pde-session)
                        |
                    SLEEP 1500s
                  human + companion
                        |
                        v
        ┌───────── WAKE ──────────┐
        |                         |
   🔥 SOUTH                 🌊 WEST
   Deep-Search              Validation
   (parallel agents)        (parallel agent)
   per PDE facet            cross-reference
        |                         |
        └──────── MERGE ──────────┘
                    |
                    v
                ❄️ NORTH
               Execution
           (parallel agents)
           file-ownership
                    |
                    v
              INTEGRATION
              lead agent
              commit + checkpoint
```

## Why Four Directions, Not Pipeline

Traditional CI/CD is a pipeline: build → test → deploy. Sequential. Mechanical.

The Four Directions pattern is a **cycle**: vision → analysis → reflection → action.
Each direction feeds the next. SOUTH findings inform WEST validation criteria.
WEST validation shapes NORTH execution constraints. NORTH actions complete what
EAST envisioned.

In multi-agent terms:
- SOUTH and WEST agents can run **in parallel** because they serve different purposes
- NORTH agents run after SOUTH completes (they need the findings)
- WEST validation runs alongside NORTH (preparing the checklist while executors build)

## Agent Spawning Rules

### From deep-research: What We Learned

The deep-research skill proved these orchestration principles:

1. **MECE decomposition** — each agent covers a distinct angle with explicit boundaries
2. **"Do NOT cover X"** — every agent prompt states what OTHER agents handle
3. **Batch results before synthesis** — wait for ALL agents, then merge. Never process one-at-a-time (anchoring bias)
4. **Scale to complexity** — 2 agents for simple, 15 for multi-repo ceremony
5. **File ownership** — no two executor agents touch the same file
6. **Lead agent integrates** — sub-agents report, lead merges and commits

### PDE-Specific Additions

7. **Direction-typed agents** — each agent knows its Medicine Wheel direction
8. **`.pde/` as workspace** — SOUTH agents write to `.pde/<uuid>/deep-search/`, never source
9. **Rispecs awareness** — agents that author rispecs read the survey first
10. **Creative orientation throughout** — no problem-solving language in any agent output

## File Ownership Protocol

```
SOUTH agents  → write to .pde/ only
WEST agents   → write to .pde/ only
NORTH agents  → write to assigned source files only (exclusive ownership)
Lead agent    → reads everything, commits everything
```

When assigning NORTH agents:
1. List all files to be created/modified from the action stack
2. Group by natural clusters (all rispecs together, all implementation together)
3. Verify no file appears in two agents' lists
4. If a file must be touched by two action items, batch those items into one agent

## Synthesis Protocol

After all agents return:

```
1. Read SOUTH findings  → understand what exists, what the framework says
2. Read WEST checklist   → know what to validate
3. Read NORTH outputs    → see what was created
4. Cross-reference       → do NORTH outputs satisfy WEST criteria?
5. Resolve conflicts     → if two agents disagree, structural tension analysis
6. Integration test      → build/lint if applicable
7. Commit                → git add only touched files
```

## Error Handling

| Situation | Response |
|-----------|----------|
| SOUTH agent finds referenced file doesn't exist | Note in findings, executor creates it |
| NORTH agent hits blocker outside its file scope | Agent STOPS and reports; lead reassigns |
| WEST validation fails on a NORTH output | Lead spawns a fix agent with the specific file |
| Two agents produce conflicting rispecs references | Lead resolves using kinship protocol |
| Agent times out | Lead reads partial output, spawns replacement for remaining work |

## Comparison: Single-Agent vs Multi-Agent PDE

| Aspect | rise-pde-session | rise-pde-session-multi-agents |
|--------|-----------------|-------------------------------|
| Decomposition | 2 PDE calls | Same 2 PDE calls |
| Sleep | 1500s mandatory | 1500s mandatory |
| Post-wake research | Agent reads files inline | SOUTH agents research in parallel |
| Rispecs authoring | Agent writes sequentially | Rispecs survey + parallel authoring |
| Validation | Agent self-checks | WEST agent prepares checklist |
| Execution | Sequential file-by-file | Parallel by file ownership |
| Diary | Part of sequential work | Dedicated narrative agent |
| Total agent count | 1 | 2-15 depending on complexity |
| Context window pressure | High (everything in one context) | Low (distributed across agents) |
