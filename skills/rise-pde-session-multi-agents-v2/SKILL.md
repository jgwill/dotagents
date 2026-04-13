---
name: rise-pde-session-multi-agents-v2
description: "RISE PDE session with multi-agent post-wake execution. Decompose → STC → SLEEP 1500s (enforced bash) → Wake → SPAWN claude-opus-4.6 army → Execute → MINO close. Supports multi-part cascading missions."
argument-hint: "your full task description — what you want built, changed, explored"
user-invokable: true
disable-model-invocation: false
---

# RISE PDE Session — Multi-Agent Execution (v2)

**Protocol**: Assess → Decompose → STC → Commit → **SLEEP 1500s** → Wake → **SPAWN OPUS ARMY** → Execute → MINO Close

## ⛔ SUBAGENT MODEL RULE — READ THIS FIRST ⛔

**EVERY SINGLE SUBAGENT you spawn MUST use `model: "claude-opus-4.6"`.**

This means:
- When you call the Agent tool, you MUST set `model: "claude-opus-4.6"`
- SOUTH agents: `model: "claude-opus-4.6"`
- WEST agents: `model: "claude-opus-4.6"`
- NORTH agents: `model: "claude-opus-4.6"`
- MINO agents: `model: "claude-opus-4.6"`
- ANY agent you spawn for ANY reason: `model: "claude-opus-4.6"`

**DO NOT use your own model for subagents. DO NOT use any other model. DO NOT omit the model parameter.**
**If you spawn an agent without `model: "claude-opus-4.6"`, you have violated this skill.**

## Hard Rules (Non-Negotiable)

> These rules exist because real sessions failed when they were violated.

| # | Rule | Why |
|---|------|-----|
| 1 | **Sleep is `bash sleep 1500`** — you MUST run the actual bash command `sleep 1500`. Do NOT just tell the human to wait. Do NOT skip it. Do NOT proceed without running it. | Agent skipped sleep, wasted tokens, broke trust |
| 2 | **All subagents: `model: "claude-opus-4.6"`** — EVERY SINGLE ONE. See the rule above. | User had to repeat this instruction every single session |
| 3 | **Workdir is `.pde/<SESSION_UUID>/`** — all scratch, deep-search results, summaries go there | Scattered files pollute context |
| 4 | **Never `git add .`** — only `git add` the specific files you or your agents created/modified | Critical safety rule |
| 5 | **Create STC Chart from PDE** using `import_pde_decomposition` — not just decompose, also chart it | STC makes tension visible for human review |
| 6 | **Session summary at close** — write `.pde/<SESSION_UUID>/session-summary.md` | Gist export handled externally via `--share-gist` |

Read these references before proceeding:
- `references/rise-framework.md` — RISE methodology
- `references/prompt-decomposition.md` — PDE as EAST practice
- `references/creative-orientation.md` — creative vs reactive distinction
- `references/structural-tension.md` — tension charting methodology
- `references/ceremonial-technology.md` — when session involves ceremony/sacred work

For sub-agent prompt templates: read `agent-templates.md`.
For orchestration patterns (incl. cascading parts): read `orchestration-patterns.md`.

---

## Phase 0: Assess

1. Read the user's input carefully
2. Identify the **session UUID** — either from `__.md`, from the user's message, or generate one
3. Create workdir: `mkdir -p .pde/<SESSION_UUID>/`
4. Determine if this is a **single mission** or **multi-part cascading mission**
   - Multi-part: user says "Part 1... Part 2..." or numbered sections
   - See `orchestration-patterns.md` → Cascading Parts Pattern

## Phase 1: Decompose (EAST 🌅)

1. Call `pde_decompose(prompt)` with the full user input
2. Process the decomposition — generate the JSON yourself
3. Call `pde_parse_response(llm_response, original_prompt, workdir)` — stores to `.pde/`
4. Note the PDE UUID — you'll need it throughout

**For multi-part missions**: decompose the ENTIRE input once, then identify part boundaries in the action stack.

## Phase 2: Create STC Chart

1. Call `import_pde_decomposition(pde_id, workdir)` — creates `.coaia/pde/<session>.jsonl`
2. Present the STC to the human:
   - **Desired Outcome**: what the session creates
   - **Current Reality**: what exists now (including ambiguities)
   - **Action Steps**: the ordered stack with direction tags
3. Note the STC chart ID for progress tracking

## Phase 3: Commit & SLEEP

1. `git add` only the `.pde/<UUID>.md` and `.pde/<UUID>.json` and `.coaia/pde/<session>.jsonl`
2. Commit: `"[pde] Decompose: <summary> — STC chart_<id>"`
3. Tell the human what was decomposed and what the STC shows

**THEN YOU MUST RUN THIS EXACT COMMAND USING THE BASH TOOL:**

```bash
sleep 1500
```

**THIS IS NOT OPTIONAL. THIS IS NOT A SUGGESTION. YOU MUST RUN `sleep 1500` IN BASH RIGHT NOW.**

Do NOT:
- ❌ Skip the sleep
- ❌ Say "I'll wait for you" instead of running the command
- ❌ Say "sleep 1500" in text without actually calling the Bash tool
- ❌ Proceed to Phase 4 without the sleep completing
- ❌ Spawn any agents before the sleep finishes

Do:
- ✅ Call the Bash tool with command `sleep 1500` and timeout `600000`
- ✅ Wait for it to complete (it will take 1500 seconds = 25 minutes)
- ✅ Only AFTER the bash tool returns, proceed to Phase 4

The human + `pde-review-companion` use these 25 minutes to review and edit `.pde/*.md` files.
If you skip this, you waste the human's tokens and break the review window.

## Phase 4: Wake & Read Delta

After waking:

1. `git diff .pde/` — see what the human changed
2. `git diff issues/` — check plan edits
3. Read ALL `.pde/*.md` files (they are now the **authoritative intent**)
4. Read the STC chart file
5. Build the **unified action stack** from all PDE facets
6. Identify how many independent work streams exist
7. For **multi-part missions**: identify which part to execute first

## Phase 5: SOUTH — Deep-Search Per Facet

**Reminder: ALL agents you spawn MUST use `model: "claude-opus-4.6"` in the Agent tool call.**

For EACH PDE facet, spawn a sub-agent (model: "claude-opus-4.6") that does deep-search.
Results land in `.pde/<SESSION_UUID>/deep-search/`.

Use templates from `agent-templates.md` → Agent S1, S2, S3, S4.

**Scale to facet complexity:**
- Simple facet (single file change): 1 deep-search agent (model: "claude-opus-4.6")
- Multi-repo facet (rispecs + kinship): 1 deep-search + 1 rispecs-survey agent (both model: "claude-opus-4.6")
- Complex facet (implementation + ceremony): 1 deep-search + 1 academic/methodology agent (both model: "claude-opus-4.6")

**All SOUTH agents write to `.pde/<SESSION_UUID>/deep-search/` only — never source files.**

## Phase 6: Synthesize Deep-Search Results

After ALL deep-search agents return (**batch — no anchoring**):

1. Read all `.pde/<SESSION_UUID>/deep-search/` findings
2. Read `.pde/rispecs-survey.md` if it exists
3. Update the plan with enriched understanding
4. Assign action stack items to executor agents (model: "claude-opus-4.6") based on:
   - File ownership (no two agents touch the same file)
   - Dependency ordering (respect the action stack)
   - Natural groupings (rispecs together, implementation together, diary separate)

## Phase 7: NORTH — Parallel Execution

**Reminder: ALL agents you spawn MUST use `model: "claude-opus-4.6"` in the Agent tool call.**

Spawn **N executor agents** (each with model: "claude-opus-4.6"), each handling a work stream.

Use templates from `agent-templates.md` → Agent N1, N2, N3, N4, N5.

### WEST — Validation Agent (runs parallel with executors)

Spawn 1 validation agent (model: "claude-opus-4.6") alongside NORTH executors.
Use template from `agent-templates.md` → Agent W1.

## Phase 8: Integration & Commit

1. Collect all executor outputs
2. Run validation checklist from WEST agent
3. Cross-reference: did rispecs reference each other properly?
4. Verify kinship mappings follow protocol
5. Run build/lint if applicable
6. `git add` only files actually created or modified
7. Commit: `"[pde] Multi-agent execution: <summary>"`

### For Multi-Part Cascading Missions

After committing Part N:
1. Present Part N results to human
2. If more parts remain → return to Phase 5 for Part N+1
3. Each part gets its own commit: `"[pde] Part N: <summary>"`
4. See `orchestration-patterns.md` → Cascading Parts Pattern

## Phase 9: Human Checkpoint

Present:
- What each executor created
- WEST validation results
- Any unresolved ambiguities
- `git diff --stat`
- STC progress update (which action steps completed)

Human adjusts or approves.

## Phase 10: Session Close

After human approval:

1. Present final `git diff --stat`
2. Write a brief session summary to `.pde/<SESSION_UUID>/session-summary.md`
3. The session gist export is handled OUTSIDE this skill — the orchestrator launches copilot-cli with `--share-gist` and receives the `gist_url` when the session exits. That gist_url then gets routed to `mino-mcp` by the orchestrator, not by this session.

**You do NOT need to export a gist. The `--share-gist` flag on copilot-cli handles that automatically.**

---

## Rispecs & RISE Framework Integration

Unchanged from v1 — see `agent-templates.md` for rispecs workflow.

### Key files the skill reads automatically:
| File | When |
|------|------|
| `/a/src/llms/llms-rise-framework.txt` | Always |
| `/a/src/llms/docs/prompt-decomposition.md` | Always |
| `/a/src/llms/docs/creative-orientation.md` | When authoring rispecs |
| `/a/src/llms/docs/structural-tension.md` | When framing current→desired states |
| `/a/src/llms/llms-kinship-hub-system.md` | When PDE involves cross-repo kinship |
| Target repo `rispecs/**/*.spec.md` | When creating new rispecs |
| Target repo `KINSHIP.md` | When mapping relationships |

---

## Rules

- **`bash sleep 1500`** — actual command, non-negotiable, 25 minutes for human review
- **All subagents: `model: "claude-opus-4.6"`** — stated here, enforced everywhere
- **Workdir: `.pde/<SESSION_UUID>/`** — all scratch, deep-search, summaries go here
- **Never `git add .` or `git add -A`** — only files you or your agents touched
- RISE creative orientation: structural tension → desired outcome → natural progression
- NO problem-solving language: no "gaps", "fixes", "bridge the gaps"
- Sub-agents write to `.pde/<SESSION_UUID>/deep-search/` during SOUTH, never source files
- Only NORTH executor agents touch source files
- Batch ALL agent results before synthesizing (avoid anchoring bias)
- Scale agent count to task complexity — 2 agents for simple, 10+ for multi-repo
- Respect repo boundaries when spanning multiple repos
- MCP tool pattern: `mcp__mcp-pde__<tool>` for PDE, `mcp__coaia-pde__<tool>` for STC
- Session summary at close — gist export is handled by `--share-gist` at launch, not inside the session
