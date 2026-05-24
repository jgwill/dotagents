---
name: deep-research
description: >
  This skill should be used when the user asks for "deep research", "thorough research",
  "research everything about", "cover every angle", "comprehensive research on",
  "spawn research agents", "/deep-research", or wants multi-agent parallel research
  on any topic. Also triggers when user says "research this for me", "find everything
  about", "I need a research doc on", or describes needing exhaustive coverage of a
  subject. NOT for quick lookups or single questions — this is for producing
  comprehensive research documents saved to the appropriate project/workspace location.
version: 0.2.0
---

# Deep Research

Multi-agent parallel research orchestrator. Decomposes any research topic into 3-6 specialized angles using MECE principles, spawns Opus sub-agents to cover each angle simultaneously, runs gap analysis, then synthesizes findings into one comprehensive research document.

Anthropic's own multi-agent research system outperforms single-agent by **90.2%**. This skill applies those same proven patterns.

For detailed sub-agent prompt templates by research type: read `agent-templates.md`.
For the full research on multi-agent orchestration patterns: read `orchestration-patterns.md`.

## Who This Is For

A generic deep-research workflow. Inject the active requester/project context from the user brief, durable preferences/memory, repository guidance, and any supplied notes. Do not hard-code a creator profile, social handle, vault path, or niche unless the current task provides it.

## The Research Diamond

Every research session follows this shape:

```
         [Broad: Decompose question]
              /        \
    [Narrow: 3-5 parallel agents]     ← Wave 1
              \        /
         [Evaluate: Gap analysis]
              /        \
    [Deep: 1-2 targeted agents]       ← Wave 2 (if needed)
              \        /
         [Synthesize: Final report]
```

Start wide, go narrow in parallel, identify gaps, go deep on gaps, synthesize.

## Research Orchestration Process

### Phase 0: Establish Date Context

Before anything else, note today's date. You can get it from the system prompt or by running `date`. Inject this date into every sub-agent prompt so they search for current information and properly date the final document. This is critical — sub-agents without date context will search for and cite outdated information.

### Phase 1: Gather Context

Before spawning any agents:

1. **Read the user brief and project guidance** — AGENTS.md/CLAUDE.md, README, issue/spec links, or supplied notes
2. **Search prior context** — use memory/session search/local notes when available; build on existing knowledge, never start from scratch
3. **Clarify purpose only if unclear** — e.g. issue work, decision brief, spec, research artifact, content, or personal learning
4. **Ask about sources when it changes quality** — use the available clarification tool to ask:
   - "Are there specific sources you want me to prioritize?" with options like:
     - "No, use defaults" — proceed with standard source strategy
     - "Specific people/accounts" — X accounts, bloggers, researchers to focus on
     - "Specific sites/communities" — subreddits, forums, documentation sites, YouTube channels
     - "I'll paste links" — user provides specific URLs to anchor the research around
   - This is what separates surface-level research from alpha insights. Default web search scrapes the obvious — user-directed sources find the unusual.
   - If the user provides specific sources, inject them into the relevant sub-agent prompts in Phase 3 (add to SEARCH STRATEGY and SOURCE QUALITY sections).

### Phase 2: MECE Decomposition

Break the topic into **Mutually Exclusive, Collectively Exhaustive** angles. Each angle:
- Does NOT overlap with any other (prevents duplicate work)
- Together they cover everything relevant (no gaps)
- Is specific enough for one agent to investigate thoroughly

**Common decomposition patterns:**

| Research Type | Typical Angles |
|--------------|----------------|
| Content/Platform | General best practices, domain-specific strategy, real examples with metrics, psychology/copywriting, existing knowledge, social discourse |
| Technology | Current state/ecosystem, real shipped code, community sentiment, comparisons/alternatives, existing knowledge, implementation patterns |
| Business | Market data/benchmarks, domain-specific practices, strategy frameworks, existing knowledge, practitioner discourse |

**Scale effort to complexity:**
- Simple factual topic: 3 agents
- Multi-faceted topic: 4-5 agents
- Complex strategic topic: 5-6 agents

### Phase 3: Spawn Parallel Sub-Agents

Spawn **minimum 3, ideally 4-5** sub-agents in parallel using the available delegation tool. Use the strongest practical model for substantive research/synthesis; cheap models are acceptable only for smoke tests or decomposition.

Every sub-agent prompt MUST include these 6 elements:

1. **WHO** — "This research is for [requester/project]. Relevant context: [stable preferences, domain, project goals, constraints]."

2. **WHY** — The specific purpose, e.g. decision support, issue planning, spec drafting, artifact creation, or reusable knowledge. Agents that know WHY produce dramatically better results.

3. **WHAT ANGLE** — Specific scope AND explicit boundaries: "Cover X. Do NOT cover Y — another agent handles that."

4. **HOW** — Which tools to use (see Tools Reference below)

5. **SEARCH STRATEGY** — "Start with SHORT, BROAD queries (2-4 words). Evaluate results. Then progressively narrow focus. Do NOT start with long, specific queries — they return poor results."

6. **SOURCE QUALITY** — "Prefer: practitioner blogs, official docs, academic papers, primary sources. Avoid: SEO content farms, listicles, aggregator sites."

#### Sub-Agent Prompt Template

```
You are researching [ANGLE] for [REQUESTER/PROJECT].
Relevant context: [stable preferences, domain, project goals, constraints, and intended audience].

TODAY'S DATE: [INSERT CURRENT DATE, e.g. 2026-02-10]

PURPOSE: [WHY this research matters — how the requester/project will use it]

YOUR ANGLE: [SPECIFIC SCOPE — what you cover]
BOUNDARIES: [What you do NOT cover — other agents handle those angles]

SEARCH STRATEGY:
- Start with short, broad queries (2-4 words)
- Evaluate what's available, then progressively narrow
- Cross-reference claims across multiple sources
- Aim for 2+ independent sources per key finding

SOURCE QUALITY: Prefer practitioner blogs, official docs, engineering posts, primary
sources. Avoid SEO content farms and listicles.

TOOLS TO USE: [SPECIFIC tools for this angle]

QUALITY BAR: Be exhaustive. Extract every actionable insight, specific number, concrete
example, framework, and contrarian take. Density matters — thin research is useless.
Include sources/URLs for everything. If you find only 3 bullet points, you failed.

OUTPUT FORMAT:
## Key Findings
[Numbered list with inline source citations]

## Evidence Quality
[Which findings are well-sourced vs. speculative]

## Contradictions Found
[Any conflicting information between sources]

## Notable Quotes
[Direct quotes from authoritative sources with attribution]

## Sources
[Full list with URLs]
```

#### Agent Type Selection

| Angle Type | subagent_type | model | Tools |
|-----------|---------------|-------|-------|
| Web research | `delegate_task` | strong | web_search, web_extract, browser when needed |
| Existing knowledge | `delegate_task` | strong | session_search, search_files, read_file on relevant paths |
| Code examples | `delegate_task` | strong | GitHub/code search tools available in the environment |
| Social discourse | `delegate_task` | strong | xurl/xitter or configured social/search tools |

**Social/X research:** use the configured social-search skill/CLI if available; otherwise use web search and clearly label coverage limits.

### Phase 4: Gap Analysis

After ALL sub-agents return (batch — do not process one-at-a-time to avoid anchoring bias):

1. Review all findings together
2. Check: Does each MECE angle have 2+ independent sources?
3. Identify contradictions between agent findings
4. Identify coverage gaps — topics no agent covered adequately
5. **If significant gaps exist**: Spawn 1-2 targeted follow-up agents (Wave 2)

### Phase 5: Synthesize Into Document

Cross-reference all findings and produce ONE comprehensive document. Do NOT simply concatenate agent outputs — synthesize them into something greater than the sum of parts.

**File location**: use the user-specified destination. If absent, save a dated Markdown artifact in the current project/workspace notes or research folder; do not assume a personal vault path.

**Topic folder organization**: Group all research outputs into a topic subfolder within the chosen research/notes location. If a research session produces multiple files (master synthesis + companion documents from sub-agents), they ALL go in the same topic folder. Create the folder if it does not exist.

| Research Topic | Folder |
|---------------|--------|
| Existing project topic | reuse the matching research/notes folder |
| New durable topic | `Research/[Topic Name]/` or project equivalent |
| One-off research | `Research/Other/` or a clearly named dated note |

**Rules:**
- ALWAYS check existing folders first — use an existing folder if the topic fits
- If 3+ files exist on a topic, they deserve their own folder
- Sub-agent companion files go in the SAME folder as the master synthesis
- When maintaining an index, group entries under clear `Research/[Folder]/` headers

**Document structure**:
```markdown
# [Topic Name] [Year]

Research compiled for [requester/project context]. [N] parallel research tracks synthesized.

**Purpose**: [What this research will be used for]
**Date**: [Current date]
**Sources**: [N] web sources, [N] social posts, [N] existing-knowledge references, [N] code examples

---

## Executive Summary

[3-5 bullet points — the most important findings]

---

## Part N: [Angle Name]

### [Sub-topic]

[Dense, actionable content with specific numbers and examples]

---

## Domain-Specific Applications

[How findings apply to the requester/project domain specifically]

---

## Contradictions & Open Questions

[Where sources disagreed, what remains unresolved]

---

## Key Takeaways

[Numbered list of the most actionable insights]

---

## Sources

[All sources cited, organized by section]
```

**Quality gate — do NOT save until ALL pass:**
- Document exceeds 2,000 words (minimum for "comprehensive")
- Specific numbers present, not just generalities
- Concrete examples from real creators/companies included
- Target domain/project context addressed specifically
- Sources attributed throughout
- Contradictions flagged (not hidden)
- The requester/project would gain something genuinely useful or new

### Phase 6: Knowledge Housekeeping

After saving, update the relevant index/README if a new file was created in a location not yet indexed.

## Tools Reference

| Tool | Use For | Notes |
|------|---------|-------|
| web_search / web_extract | Current web information and deep-dive URLs | Prefer primary/current sources |
| browser | Dynamic pages or pages web_extract cannot read | Use sparingly |
| GitHub/code search | Real code patterns | Search actual APIs/config, not vague keywords |
| xurl/xitter/social tools | X/Twitter or social discourse | Use only when configured |
| session_search/search_files/read_file | Existing knowledge | Always check first |

## Important Principles

- **Currency**: Fast-moving topics change quickly. Emphasize current information and date-sensitive claims. Stale advice is dangerous.
- **Density over length**: 3,000 words with specific numbers > 10,000 words of generic advice.
- **Build on existing knowledge**: Check memory, prior sessions, project files, and notes first. Extend them, don't repeat them.
- **WHY multiplier**: Sub-agents knowing WHY produces dramatically better results. Never skip context injection.
- **MECE or bust**: Overlapping agents waste tokens and produce duplicate content. Boundaries matter.
- **Batch synthesis**: Collect ALL findings before synthesizing. Processing one-at-a-time creates anchoring bias.
- **Start broad**: Agents default to overly-specific queries. Explicitly instruct broad-first search strategy.
