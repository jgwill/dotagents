---
name: rise-pde-session
description: PDE-decomposed development session with mandatory 25-minute human review window. Agent decomposes, commits, SLEEPS 1500 seconds, then revises based on human edits. Requires mcp-pde MCP tool.
argument-hint: "your full task description — what you want built, changed, explored"
user-invokable: true
disable-model-invocation: false
---

# RISE PDE Session

**Protocol**: Assess → Decompose → Commit → **SLEEP 1500s** → Revise → Execute

## Phase 0: Initial Assessment

1. **READ the input carefully** before anything else
2. Identify: file references, implied context, issue numbers, repo boundaries
3. Note what is stated vs what is implied — implied meaning matters
4. If the input references files (e.g., `@smcraft/MMOT.md`), read them NOW
5. Form a mental model of the full scope before decomposing

## Phase 1: Decompose

6. Call `pde_decompose` on the input — **do it TWICE** (the prompt likely has multiple facets: implementation + relationships, code + specs, etc.)
7. Each call creates files in `.pde/` — you should have ~4 files total (2 `.md` + 2 `.json`)
8. Read ALL generated `.pde/*.md` files
9. Cross-reference PDE output against your Phase 0 assessment — did PDE catch everything you noticed? Did it miss implied meaning?
10. Draft `issues/<issue-number>/plan.md` synthesizing the decomposed intent
    - Use the issue number from the input context (look in `__.md`, STCISSUE.md, or ask)
11. `git add` only: `.pde/` output files + `issues/<N>/plan.md`
12. Commit: `"[pde] Decomposition for: <short summary>"`
13. Tell the user: "PDE files committed. Sleeping 25 minutes for your review."

## Phase 2: MANDATORY SLEEP

**THIS IS NON-NEGOTIABLE. DO NOT SKIP.**

14. Run: `sleep 1500`
15. This is 25 minutes. The human will edit `.pde/*.md` during this time. Do not run that in a background process, it should block and make your conversation wait. This is intentional.
16. Do NOT poll. Do NOT check. Do NOT proceed. SLEEP.

## Phase 3: Wake & Revise

17. After waking: run `git diff .pde/` to see what the human changed
18. The human's edits ARE the authoritative intent — they override PDE interpretation
19. Also run `git diff issues/` in case the plan was edited too
20. Revise `issues/<N>/plan.md` based on the delta
21. Commit the revised plan
22. Present the final plan for confirmation before executing

## Phase 4: Execute

23. Build task list from the revised plan
24. Execute incrementally, committing as you go
25. Only `git add` files you actually touched

## Rules

- The user's raw words ARE the input — if file paths are included, preserve them in the PDE call
- Phase 0 catches what PDE might miss — implied context, cross-repo relationships, emotional emphasis
- **sleep 1500 is mandatory** — the human needs this time, skipping it wastes premium tokens
- Use RISE creative orientation: structural tension, desired outcome, natural progression
- Never `git add .` or `git add -A`
- If the input references another repo (e.g., smcraft has its own `.git`), respect repo boundaries
- Do not run that in a background process, it should block and make your conversation wait. This is intentional.