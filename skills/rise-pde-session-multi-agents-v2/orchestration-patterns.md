# Four Directions Orchestration Patterns

How multi-agent spawning maps to the Medicine Wheel directions in a PDE session.

## Pattern 1: Standard Four Directions Cycle

```
                    🌅 EAST — VISION
                  PDE Decompose + STC Chart
                  (orchestrator)
                        |
                   COMMIT .pde/ + .coaia/
                        |
                  ██ SLEEP 1500s ██
                  bash sleep 1500
                  human + companion review
                        |
                        v
        ┌───────── WAKE ──────────┐
        |                         |
   🔥 SOUTH                 🌊 WEST
   Deep-Search              Validation
   (opus subagents)         (opus subagent)
   per PDE facet            cross-reference
        |                         |
        └──────── MERGE ──────────┘
                    |
                    v
                ❄️ NORTH
               Execution
           (opus subagents)
           file-ownership
                    |
                    v
              INTEGRATION
              orchestrator
              commit + checkpoint
                    |
                    v
              📋 SESSION CLOSE
              session-summary.md
              (gist via --share-gist at exit)
```

## Pattern 2: Cascading Parts

For multi-part missions (Part 1 → commit → Part 2 → commit → Part 3).

**Evidence**: Session 260313000018.txt — 3-part ceremony work with subagent chains per part.

```
                    🌅 EAST — VISION
                  PDE Decompose ENTIRE input
                  STC Chart (all parts)
                  Identify part boundaries
                        |
                  ██ SLEEP 1500s ██
                        |
                        v
              ┌── PART 1 ──────────┐
              │ SOUTH → NORTH → W  │
              │ commit Part 1      │
              │ present to human   │
              └────────┬───────────┘
                       │
              ┌── PART 2 ──────────┐
              │ SOUTH → NORTH → W  │
              │ commit Part 2      │
              │ present to human   │
              └────────┬───────────┘
                       │
              ┌── PART N ──────────┐
              │ SOUTH → NORTH → W  │
              │ commit Part N      │
              │ present to human   │
              └────────┬───────────┘
                       │
                  📋 SESSION CLOSE
```

### Part Boundary Detection

The orchestrator detects parts from:
1. **Explicit numbering**: "Part 1...", "1.", "First...", "When done with that..."
2. **Commit boundaries**: "commit, then...", "after committing..."
3. **Dependency chains**: Action stack items that form sequential groups

### Part Execution Rules

- Each part gets its own SOUTH → NORTH → WEST cycle
- Each part gets its own git commit
- Human checkpoint between parts (brief — not another sleep)
- Subagents for Part N+1 can reference Part N outputs
- If Part N fails validation, resolve before starting Part N+1

## Pattern 3: Review-Then-Execute (Single Agent Delegation)

For simpler tasks where full SOUTH/WEST/NORTH parallelism is overkill.

```
EAST → SLEEP → WAKE →
  spawn opus subagent 1: deep-search + implement
  spawn opus subagent 2: review what subagent 1 did
  spawn opus subagent 3: correct based on review
→ COMMIT → MINO CLOSE
```

**Evidence**: Session 84a82daa user prompt — "one subagent researches, another reviews, another implements, another reviews all."

## Why Four Directions, Not Pipeline

Traditional CI/CD: build → test → deploy. Sequential. Mechanical.

Four Directions: vision → analysis → reflection → action. Each direction feeds the next.

In multi-agent terms:
- SOUTH and WEST agents can run **in parallel** (different purposes)
- NORTH agents run after SOUTH (they need findings)
- WEST validation runs alongside NORTH (preparing checklist while executors build)

## Agent Spawning Rules

### From Real Sessions: What We Learned

1. **MECE decomposition** — each agent covers a distinct angle with explicit boundaries
2. **"Do NOT cover X"** — every agent prompt states what OTHER agents handle
3. **Batch results before synthesis** — wait for ALL agents, then merge (avoid anchoring bias)
4. **Scale to complexity** — 2 agents for simple, 15 for multi-repo ceremony
5. **File ownership** — no two executor agents touch the same file
6. **Lead agent integrates** — sub-agents report, lead merges and commits
7. **Always `model: "claude-opus-4.6"`** — never downgrade subagent model

### PDE-Specific Additions

8. **Direction-typed agents** — each agent knows its Medicine Wheel direction
9. **`.pde/<SESSION_UUID>/`** — all scratch work goes in session workdir
10. **Rispecs awareness** — agents that author rispecs read the survey first
11. **Creative orientation throughout** — no problem-solving language in any agent output
12. **STC tracking** — action steps marked complete as parts finish

## File Ownership Protocol

```
SOUTH agents  → write to .pde/<SESSION_UUID>/deep-search/ only
WEST agents   → write to .pde/<SESSION_UUID>/ only
NORTH agents  → write to assigned source files only (exclusive ownership)
Lead agent    → reads everything, commits everything, writes session-summary.md
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
6. Update STC            → mark completed action steps
7. Integration test      → build/lint if applicable
8. Commit                → git add only touched files
```

## Error Handling

| Situation | Response |
|-----------|----------|
| SOUTH agent finds referenced file doesn't exist | Note in findings, executor creates it |
| NORTH agent hits blocker outside its file scope | Agent STOPS and reports; lead reassigns |
| WEST validation fails on a NORTH output | Lead spawns a fix agent with the specific file |
| Two agents produce conflicting rispecs references | Lead resolves using kinship protocol |
| Agent times out | Lead reads partial output, spawns replacement for remaining work |
| Multi-part: Part N fails | Resolve before starting Part N+1 |

## Comparison: Single-Agent vs Multi-Agent PDE

| Aspect | rise-pde-session | rise-pde-session-multi-agents (v2) |
|--------|-----------------|-------------------------------|
| Decomposition | 2 PDE calls | Same 2 PDE calls + STC Chart |
| Sleep | 1500s mandatory | 1500s **enforced bash sleep** |
| Post-wake research | Agent reads files inline | SOUTH opus agents research in parallel |
| Rispecs authoring | Agent writes sequentially | Rispecs survey + parallel authoring |
| Validation | Agent self-checks | WEST opus agent prepares checklist |
| Execution | Sequential file-by-file | Parallel by file ownership |
| Multi-part | Not supported | Cascading Parts pattern |
| Session close | None | session-summary.md (gist via `--share-gist`) |
| Cost model | All same model | Haiku orchestrator + opus subagents |
| Diary | Part of sequential work | Dedicated narrative agent |
| Total agent count | 1 | 2-15 depending on complexity |
| Context window pressure | High (everything in one context) | Low (distributed across agents) |
