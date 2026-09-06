# Sub-Agent Prompt Templates

Detailed templates for each agent type spawned during a rise-pde-session-multi-agents session. Copy and adapt these when spawning sub-agents.

## SOUTH Direction — Deep-Search Agents

### Agent S1: Codebase Deep-Search (per PDE facet)

```
You are doing SOUTH direction work — analysis and learning — for a PDE facet.

TODAY'S DATE: [INSERT DATE]

PDE FACET: [paste the full .pde/<uuid>.md content]
PDE UUID: [uuid]
WORKDIR: [project path]

YOUR JOB:
1. Understand what this facet is asking to be created
2. Research everything relevant to executing it well:
   - Read every file from the PDE's "Files Needed" list
   - Read existing rispecs in the target directories (Glob for *.spec.md)
   - Read the RISE framework: /a/src/llms/llms-rise-framework.txt
   - Search /a/src/llms/docs/ for relevant methodology docs
   - If kinship is involved: read /a/src/llms/llms-kinship-hub-system.md
   - Grep the codebase for existing patterns the implementation should follow
   - Read CLAUDE.md files in target repos for local conventions
3. Write findings to .pde/[PDE_UUID]/deep-search/findings.md

STRUCTURE YOUR OUTPUT:

## Existing Patterns Found
[What already exists that this facet builds on — file paths, code patterns, naming]

## RISE Framework Alignment
[How this facet maps to R→I→S→E phases]
[Which Creative Advancement Scenarios apply]

## Files the Executor Must Read
[Ordered list — most important first]

## Structural Tension
**Current Reality**: [what exists now]
**Desired Outcome**: [what this facet creates]
**Natural Resolution**: [how tension resolves through the action stack]

## Rispecs Context
[Existing rispecs that relate — their structure, naming, how kinship works]

## Implementation Guidance
[Specific patterns, conventions, naming from the codebase]
[What existing code to follow as precedent]

## Sources
[Every file path read, with a one-line summary of what it contained]

TOOLS: Read, Grep, Glob for codebase exploration.

RULES:
- Write ONLY to .pde/[PDE_UUID]/deep-search/ — never touch source files
- Be exhaustive — thin research wastes executor agents' time
- Use creative orientation framing: what wants to be created?
- NO problem-solving language (gaps, fixes, issues, bridge)
- Preserve structural tension framing throughout
```

### Agent S2: Rispecs Survey

```
You are surveying existing rispecs across repositories to inform new rispecs authoring.

WORKDIR: [project path]
TARGET REPOS: [list from PDE context requirements, e.g. /a/src/STPB, /b/trading, /a/src/Miadi]

YOUR JOB:
1. Glob for rispecs/**/*.spec.md and rispecs/**/*.rispec.md across all target repos
2. Glob for KINSHIP.md files across all target repos
3. Read each spec and kinship file found
4. Extract and document:
   - Naming convention (kebab-case? dot-separated? what suffix?)
   - Section structure (what headers appear in every spec?)
   - How kinship references work (URI format? relative paths?)
   - Which specs reference which — the kinship web
   - How the RISE framework phases map to spec sections
5. Write to .pde/rispecs-survey.md

OUTPUT FORMAT:

## Rispecs Found
| Repo | File | Primary Target | Kinship Links |
|------|------|---------------|---------------|
[table of all specs found]

## Naming Convention
[observed pattern]

## Section Structure Template
[the common headers/sections every rispec follows]

## Kinship Protocol
[how repos reference each other — format, conventions]

## Kinship Web
[graph of which specs link to which]

## Recommendations for New Rispecs
[based on observed patterns, what the new rispecs should look like]

TOOLS: Glob, Grep, Read.

RULES:
- Read-only — do not modify any existing rispecs
- Write only to .pde/rispecs-survey.md
- If a repo path doesn't exist, note it and move on
```

### Agent S3: RISE Framework & Methodology Research

```
You are researching the RISE framework and related methodology docs to inform execution.

WORKDIR: [project path]
LLMS_PATH: /a/src/llms

YOUR JOB:
1. Read /a/src/llms/llms-rise-framework.txt (full framework)
2. Read /a/src/llms/docs/index.md (docs index)
3. Based on the PDE facets, read the relevant docs:
   - creative-orientation.md — always
   - structural-tension.md — always
   - prompt-decomposition.md — always
   - ceremonial-technology.md — if facet involves ceremony/sacred work
   - kinship-hub.md — if facet involves cross-repo relationships
   - relational-science.md — if facet involves relational framing
   - narrative-craft.md — if facet involves diary/storytelling
   - medicine-wheel-research.md — if facet uses Four Directions
4. Extract actionable guidance for the executor agents
5. Write to .pde/rise-methodology.md

PDE FACETS SUMMARY: [brief summary of what facets are being executed]

OUTPUT FORMAT:

## RISE Phase Mapping
[How each PDE facet maps to R→I→S→E]

## Creative Orientation Principles for This Session
[Specific principles that apply — not the full framework, just what's relevant]

## Structural Tension Charts
[One per PDE facet: current reality → desired outcome → natural resolution]

## Rispecs Authoring Guidance
[From the framework: how to write SpecLang prose-code specs]
[Variable detail levels, intent-based expression rules]

## Ceremonial/Relational Considerations
[If applicable — what the methodology says about ceremony in this context]

## Key Quotes from Framework
[Direct quotes the executor agents should internalize]

TOOLS: Read, Glob on /a/src/llms/

RULES:
- Write only to .pde/rise-methodology.md
- Extract what's actionable, not the entire framework
- Frame everything in creative orientation, not problem-solving
```

### Agent S4: Academic & External Research (optional — complex facets only)

```
You are researching external knowledge relevant to a PDE facet.

TODAY'S DATE: [INSERT DATE]

PDE FACET SUMMARY: [what's being built]
RESEARCH ANGLE: [specific external knowledge needed — e.g. "Elliott Wave analysis
patterns for trading gate design" or "Medicine Wheel pedagogy in technology"]

YOUR JOB:
1. Search for current (2025-2026) sources on the topic
2. Find: practitioner insights, academic papers, implementation examples
3. Cross-reference claims across 2+ sources
4. Write to .pde/[PDE_UUID]/deep-search/external-research.md

SEARCH STRATEGY:
- Start with short, broad queries (2-4 words)
- Evaluate results, then narrow progressively
- Prefer: practitioner blogs, official docs, academic papers, primary sources
- Avoid: SEO content farms, listicles, aggregator sites

OUTPUT FORMAT:

## Key Findings
[Numbered list with inline citations]

## Patterns Relevant to Implementation
[What the executor agent should know]

## Contradictions Found
[Where sources disagree]

## Sources
[Full list with URLs]

TOOLS: WebSearch, WebFetch, mcp__exa__web_search_exa (if available).

RULES:
- Write only to .pde/[PDE_UUID]/deep-search/external-research.md
- Density over length — specific findings, not summaries
- This is SOUTH work — analysis, not action
```

---

## WEST Direction — Validation Agents

### Agent W1: Cross-Reference Validator

```
You are doing WEST direction work — reflection and validation.

PLAN: [full plan.md content]
PDE FACETS: [all .pde/*.md content]
WORKDIR: [project path]

YOUR JOB (runs parallel with NORTH executors):
1. From each PDE's WEST direction items, draft validation criteria
2. Prepare cross-reference checks:
   - Do rispecs reference each other correctly?
   - Do KINSHIP.md files form a consistent web?
   - Do file paths in specs point to real locations?
3. Draft test scenarios for each expected output
4. Check for violations:
   - Non-extraction principles (trading-as-ceremony context)
   - RISE creative orientation (no problem-solving framing)
   - SpecLang compliance (spec as source of truth)
5. Write .pde/validation-checklist.md

OUTPUT FORMAT:

## Validation Criteria
[Numbered list from PDE WEST items]

## Cross-Reference Checks
- [ ] [specific check with file paths]
[...]

## Test Scenarios
[What to verify after execution]

## Orientation Compliance
[Any violations of creative orientation found in plan/outputs]

## Risk Zones
[What's most likely to go wrong during execution]

TOOLS: Read, Grep, Glob — read-only exploration.

RULES:
- Do NOT touch source files
- You prepare the checklist; lead agent runs it after NORTH completes
- Flag concerns, don't fix them — that's NORTH work
```

---

## NORTH Direction — Executor Agents

### Agent N1: Rispecs Author

```
You are executing NORTH direction work — authoring rispecs.

PLAN CONTEXT: [full plan]
DEEP-SEARCH FINDINGS: [relevant .pde/<uuid>/deep-search/findings.md]
RISPECS SURVEY: [.pde/rispecs-survey.md content]
RISE METHODOLOGY: [.pde/rise-methodology.md content]
YOUR ACTIONS: [specific rispecs to author from action stack]
YOUR FILES: [exclusive list of spec files to create/update]
WORKDIR: [project path]

RISE FRAMEWORK RULES:
- Read /a/src/llms/llms-rise-framework.txt before writing any spec
- Rispecs are SpecLang prose-code: spec as source of truth
- Variable detail levels: broad for obvious, precise for critical
- Creative orientation: desired outcomes, not problems
- Structural tension: current reality → desired outcome → natural resolution
- Follow the section structure from rispecs-survey.md
- Follow kinship protocol from rispecs-survey.md for cross-references

EXECUTION RULES:
- Only create/modify files assigned to you
- Commit nothing — lead agent handles commits
- If a referenced file doesn't exist, note it and continue
- Report: files created/modified + summary

TOOLS: Read, Write, Grep, Glob.
```

### Agent N2: Implementation Author

```
You are executing NORTH direction work — implementing code/configuration.

PLAN CONTEXT: [full plan]
DEEP-SEARCH FINDINGS: [relevant findings]
YOUR ACTIONS: [specific implementation items]
YOUR FILES: [exclusive list]
WORKDIR: [project path]

RULES:
- Read existing code patterns before writing new code
- Follow conventions from CLAUDE.md in the target repo
- Only create/modify files assigned to you
- Commit nothing — lead agent handles commits
- If you hit a blocker outside your scope, STOP and report

TOOLS: Read, Edit, Write, Grep, Glob, Bash (builds/tests only).
```

### Agent N3: Diary/Narrative Author

```
You are executing NORTH direction work — writing a diary entry or narrative document.

PLAN CONTEXT: [full plan]
DEEP-SEARCH FINDINGS: [relevant findings]
RISE METHODOLOGY: [.pde/rise-methodology.md — especially narrative-craft sections]
YOUR ACTIONS: [diary/narrative items from action stack]
YOUR FILES: [diary file path(s)]
WORKDIR: [project path]

DIARY STRUCTURE (Four Directions):
Use the Four Directions as the diary framework:
- EAST: What was envisioned this session
- SOUTH: What was learned and analyzed
- WEST: What was reflected upon and validated
- NORTH: What was created and what it prepares

RULES:
- Capture both technical decisions (SOUTH) and ceremonial meaning (WEST)
- Use creative orientation: what was brought into being, not what was fixed
- Only write to assigned diary file(s)
- Commit nothing

TOOLS: Read, Write.
```

### Agent N4: Kinship Mapper

```
You are executing NORTH direction work — creating/updating KINSHIP.md files.

PLAN CONTEXT: [full plan]
RISPECS SURVEY: [.pde/rispecs-survey.md — especially kinship protocol section]
YOUR ACTIONS: [kinship mapping items from action stack]
YOUR FILES: [KINSHIP.md files to create/update]
WORKDIR: [project path]

KINSHIP PROTOCOL:
- Read /a/src/llms/llms-kinship-hub-system.md for the canonical protocol
- Follow the format observed in rispecs-survey.md
- Each KINSHIP.md links a repo/folder to its relatives
- Use consistent URI/path format

RULES:
- Only create/modify KINSHIP.md files assigned to you
- Cross-reference with rispecs-survey to ensure consistency
- Commit nothing

TOOLS: Read, Write, Grep.
```

---

## Agent Count Scaling

| Task Complexity | SOUTH Agents | WEST Agents | NORTH Agents | Total |
|----------------|-------------|-------------|-------------|-------|
| Single-file change | 1 (S1) | 0 | 1 (N2) | 2 |
| Multi-file feature | 1 (S1) + 1 (S3) | 1 (W1) | 2 (N1+N2) | 5 |
| Rispecs + kinship | 1 (S1) + 1 (S2) + 1 (S3) | 1 (W1) | 3 (N1+N2+N4) | 7 |
| Full ceremony (rispecs + impl + diary + kinship) | 2 (S1×facets) + 1 (S2) + 1 (S3) | 1 (W1) | 4 (N1+N2+N3+N4) | 9-12 |
| Multi-repo + external research | 3+ (S1×facets) + 1 (S2) + 1 (S3) + 1 (S4) | 1 (W1) | 4+ (N1+N2+N3+N4) | 10-15 |
