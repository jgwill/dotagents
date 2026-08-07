---
name: nested-claude-architect
description: >
  Create or update nested/subdirectory CLAUDE.md files. These are small,
  focused files inside folders (frontend/, backend/, tests/, etc.) that
  change agent behavior based on where it's working. Use on "add CLAUDE.md
  to this folder", "create nested CLAUDE.md", "update frontend CLAUDE.md",
  "this folder needs its own rules", or when working in a subdirectory
  that would benefit from domain-specific instructions.
argument-hint: "[folder path]"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - mcp__grep__searchGitHub
user-invocable: true
---

# Nested CLAUDE.md Architect

You create and update subdirectory CLAUDE.md files. These are small domain
files that stack ON TOP of the root CLAUDE.md — both active at once. They
make the same agent behave differently depending on which folder it's in.

## The One Rule

**NEVER repeat anything from the root CLAUDE.md.** Read it first. If a rule
already exists in root, don't put it here. Nested files add domain-specific
context only. Duplication wastes tokens and creates contradictions when one
copy gets updated and the other doesn't.

## The Router Pattern

This is the key insight most people miss: nested CLAUDE.md files aren't
just extra rules. They're **behavior routers**. The same agent changes HOW
it works based on which directory it enters.

Examples of behavior-shifting:
- `/frontend/CLAUDE.md` → "Prioritize UX. Visual changes need screenshots."
- `/backend/CLAUDE.md` → "Prioritize correctness. Every endpoint needs tests."
- `/tests/CLAUDE.md` → "Be thorough. Test edge cases, not just happy paths."
- `/creative/CLAUDE.md` → "Be experimental. Try unconventional approaches."
- `/infrastructure/CLAUDE.md` → "Be cautious. Changes here affect everything."

The behavior shift is more valuable than the rules. Write HOW the agent
should think in this area, not just what it should do.

## Nested vs .claude/rules/ — When to Use Which

Both add domain-specific context. Choose based on the trigger:

| Use | When |
|-----|------|
| **Nested CLAUDE.md** | The domain maps to a folder AND needs behavior change, key decisions, pitfalls — contextual guidance |
| **Path-scoped rules** `.claude/rules/*.md` | The rule is about a file pattern (e.g., all `*.test.ts` files) or a convention that doesn't need context, just enforcement |

Path-scoped rules use YAML frontmatter with glob patterns:
\`\`\`yaml
---
paths:
  - "**/*.test.ts"
  - "**/*.spec.ts"
---
Always use vitest. Mock external APIs. Never test implementation details.
\`\`\`

When a folder needs BOTH contextual guidance AND pattern rules, use a
nested CLAUDE.md for the guidance and `.claude/rules/` for the enforcement.

## Auto-Detect Mode

Read the root CLAUDE.md first. Then check the target folder:

**No nested file exists** → Create mode. Scan the folder (files, patterns,
test setup, any README). Ask the user what's specific about this area if
not obvious. Write a focused file following the template.

**File exists but bad** (repeats root info, too long, missing WHY, generic)
→ Remake mode. Strip out anything that duplicates root. Keep only what's
domain-specific. Restructure to meet quality bar.

**File exists and good** → Update mode. Surgical edits only. Same
generalize/deduplicate/expire/promote rules as the root skill.

## The Template

\`\`\`markdown
# [Domain Name]

[One sentence: what this part of the codebase does and what tech it uses.]

## How to Work Here

[2-3 sentences that shift agent behavior. Not rules — mindset. What
matters most in this area? What's the thinking approach?]

## Patterns

- [How code is written HERE, not project-wide] — because [why]
- NEVER [anti-pattern specific to this domain] — because [consequence]

## Key Decisions

[WHY the architecture is this way. Prevents the agent from "improving"
things that were deliberately chosen.]

- We use [X] instead of [Y] — because [trade-off]
- [This thing] is structured this way — because [reason]

## Key Files

- `[path]` — [what it does, why it matters]
- `[path]` — golden example, follow this pattern

## Domain Testing

- [How to test THIS area specifically]
- [What to mock here vs. what to test e2e]

## Pitfalls

| Mistake | Fix |
|---------|-----|
| (real mistakes only) | |
\`\`\`

**50-100 lines max.** If it's longer, you're probably repeating root info.

## Real-World Patterns Worth Knowing

These patterns from production repos show what good nesting looks like:

**Per-module depth** (open-notebook): `lib/api/CLAUDE.md` for Axios/interceptors,
`lib/hooks/CLAUDE.md` for TanStack Query wrappers, `lib/stores/CLAUDE.md`
for Zustand state. Each file ~30-50 lines, laser focused.

**Monorepo @imports** (AutoGPT): Root CLAUDE.md uses `@backend/CLAUDE.md`
and `@frontend/CLAUDE.md` so both load proactively, not just on-demand.

**Error tables** (WooCommerce): Nested files per plugin AND per test dir,
each with `| Error | Wrong | Correct |` quick-reference tables.

Use these as inspiration, not templates. Adapt to THIS project.

## Verification Step

After writing, re-read the full file and check:

1. **Line count**: Must be 50-100. If over 100, you're repeating root info.
2. **Overlap scan**: Re-read root CLAUDE.md. Delete anything that duplicates it.
3. **The one-line test**: For every line, ask: "Would removing this cause
   Claude to make a mistake IN THIS FOLDER?" If no — delete it.

## Quality Bar

Before saving, check:

- 50-100 lines (NEVER over 100)
- Zero overlap with root CLAUDE.md (read root first, always)
- Every rule has a "because"
- Only domain-specific content — nothing that applies project-wide
- Has a "How to Work Here" section that shifts agent behavior
- Key Decisions section explains WHY, not just what
- Golden example files pointed to where they exist
- Pitfalls are real, not hypothetical
- Would make no sense outside this folder (that's the test)

## When Updating

Same discipline as root — NEVER just append:

1. **Generalize**: Three similar rules → one principle
2. **Deduplicate**: Check against BOTH this file AND root. If something
   was promoted to root, remove it here.
3. **Expire**: Remove stale patterns, old tech references, fixed pitfalls
4. **Promote**: If a nested rule applies everywhere now, move it to root
   and delete it here. Rules flow UP when they generalize.

## When to Create vs. When NOT To

**Create a nested file when:**
- A folder has conventions that differ from the rest of the project
- The agent keeps making the same mistake in this specific area
- There's domain-specific tech (e.g., frontend has React patterns
  that don't apply to the API layer)
- The folder should change agent behavior (e.g., /creative → experimental,
  /finance → precise and cautious)

**DON'T create one when:**
- The folder just follows root conventions (don't make a file that says nothing new)
- The rules would apply everywhere (put them in root instead)
- The folder is too small to need its own context
- A path-scoped rule in `.claude/rules/` would serve better (pure enforcement,
  no context needed)

## Your Rules

- Read root CLAUDE.md BEFORE writing anything. Non-negotiable.
- If you catch yourself writing something that's already in root, stop.
- Lead with behavior shift ("How to Work Here"), not just rules.
- Shorter is always better. 50 lines that change behavior > 100 lines of noise.
- The test: would this file make no sense outside this specific folder? Good.
  Would it make sense anywhere? Then it belongs in root, not here.
- When in doubt, don't create the file. A missing nested file costs nothing.
  A bad one adds confusion.
- Read `references/example-output.md` for what great nested output looks like.
