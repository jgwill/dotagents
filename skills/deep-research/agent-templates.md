# Sub-Agent Prompt Templates

Detailed templates for common research decompositions. Copy and adapt these when spawning sub-agents.

## Content Platform Research (YouTube, TikTok, Shorts)

### Agent 1: General Best Practices & Algorithm

\`\`\`
You are researching [PLATFORM] [SPECIFIC ASPECT] best practices and current algorithm
behavior for [REQUESTER/PROJECT]. Relevant context: [domain, audience, goals, constraints].

PURPOSE: The requester will use this research to generate optimized
[titles/descriptions/hooks/etc.] for maximum engagement, viewers, and growth. The research
needs to be exhaustive enough to serve as the knowledge base behind that prompt.

YOUR ANGLE: General best practices and algorithm mechanics for [PLATFORM] [ASPECT].
Cover: character limits, algorithm ranking signals, what the platform rewards/penalizes,
formatting rules, proven formulas, A/B test data, engagement metrics that matter.
DO NOT cover: domain-specific advice (another agent handles that), social discourse, or existing internal knowledge.

TOOLS: Use available web search/extract tools to find the most current information.
Prioritize sources from the current and prior year. Deep-dive particularly rich articles
with the best available page extraction tool.

QUALITY BAR: Be exhaustive. I need specific numbers (character counts, engagement
percentages, algorithm thresholds), not generalities. If a source says "keep titles short,"
I need to know EXACTLY how short and why. Include every framework, formula, and data point
you find. Sources for everything.
\`\`\`

### Agent 2: Niche-Specific Strategies

\`\`\`
You are researching [PLATFORM] [SPECIFIC ASPECT] strategies specifically for [DOMAIN/AUDIENCE], for [REQUESTER/PROJECT].

PURPOSE: [Same as above — what the research will be used for]

YOUR ANGLE: How [ASPECT] works differently in [DOMAIN/AUDIENCE] compared to
general content. Cover: what practitioners specifically do, what hooks/formats work for
this domain, how to translate complex topics into engaging [titles/descriptions/etc.],
examples from successful comparable creators/teams, and what the target audience responds to.
DO NOT cover: general best practices (another agent handles that) or existing internal knowledge.

TOOLS: Use web search to find domain-specific advice. Search for comparable practitioners, teams, or creators and analyze their patterns.

QUALITY BAR: I need SPECIFIC examples from real comparable practitioners with actual metrics where
possible. "Tech content should be educational" is useless. "Fireship's Shorts averaging 500K
views use [specific pattern]" is gold.
\`\`\`

### Agent 3: Real Examples & Pattern Analysis

\`\`\`
You are analyzing real-world examples of high-performing [PLATFORM] [ASPECT] to extract
patterns, for [REQUESTER/PROJECT].

PURPOSE: [What the research will be used for]

YOUR ANGLE: Find and analyze 15-30 real examples of high-performing [titles/descriptions/hooks]
on [PLATFORM]. Extract patterns: word choice, structure, length, emotional triggers, formatting.
Focus on both general high-performing content AND domain-specific content.
DO NOT cover: theory or general advice (other agents handle that).

TOOLS: Use web search and code/GitHub search if applicable. Look for case studies, creator breakdowns,
and analysis posts that include actual performance data.

QUALITY BAR: I need REAL examples with REAL numbers. Not hypothetical titles — actual titles
from actual [videos/shorts] with actual view counts. The more examples the better. Organize
by pattern type.
\`\`\`

### Agent 4: Psychology & Copywriting

\`\`\`
You are researching the psychological and copywriting principles behind high-engagement
[PLATFORM] [ASPECT], for [REQUESTER/PROJECT].

PURPOSE: [What the research will be used for]

YOUR ANGLE: The WHY behind what works. Cover: cognitive biases exploited by viral content
(curiosity gap, loss aversion, social proof, pattern interrupt), copywriting frameworks
adapted for short-form, attention psychology, the neuroscience of scrolling behavior,
power words and trigger words with data on their effectiveness.
DO NOT cover: platform-specific algorithm mechanics (another agent handles that).

TOOLS: Use web search. Look for research papers, marketing studies, copywriting resources,
and behavioral psychology applied to short-form content.

QUALITY BAR: I need frameworks I can codify into rules, not vague psychology. "Curiosity
works" is useless. "Open loops increase watch time by 47% (Source: [study])" is gold.
Specific power words, specific emotional triggers, specific formulas.
\`\`\`

### Agent 5: X/Twitter Discourse

\`\`\`
You are searching X/Twitter for current creator discourse about [PLATFORM] [ASPECT],
for [REQUESTER/PROJECT].

PURPOSE: [What the research will be used for]. X discourse captures what creators are
ACTUALLY experiencing right now vs. what blog posts from 6 months ago say.

YOUR ANGLE: What are creators saying RIGHT NOW about [ASPECT] on [PLATFORM]? Recent
algorithm changes, what's working this month, creator tips that haven't made it to blog
posts yet, contrarian takes, pain points, and wins.
DO NOT cover: general best practices from web search (other agents handle that).

TOOLS: Use the x-research CLI:
Use the configured X/social research tool or CLI for this environment. Run 3-5 different queries to cover the topic from multiple angles.

Include actual posts with engagement metrics when available.

QUALITY BAR: I need actual tweets from actual creators with actual engagement numbers.
Filter for signal — a tweet with 500 likes from a known creator matters more than 50
tweets with 2 likes each.
\`\`\`

### Agent 6: Existing Knowledge

\`\`\`
You are searching existing project/user knowledge about [TOPIC]. Use supplied paths, repository notes, memory/session search, or the configured notes vault/research store.

PURPOSE: [What the research will be used for]. Existing notes and prior work should
inform the research — not be duplicated.

YOUR ANGLE: Find EVERYTHING the existing knowledge base already knows about [TOPIC]. Check:
- supplied project/research folders
- README/AGENTS/CLAUDE guidance
- prior session notes or indexed knowledge
- relevant issue/spec/design documents

DO NOT do web research — other agents handle that. Your job is internal knowledge only.

TOOLS: Use search_files to find relevant files and read_file to extract insights.

QUALITY BAR: Report everything found, organized by source file. Note what seems current
vs. potentially outdated. Flag any contradictions with what other agents might find.
\`\`\`

## Technology Research

### Agent 1: Current State & Ecosystem

\`\`\`
[Same WHO/WHY preamble, adapted]

YOUR ANGLE: Current state of [TECHNOLOGY] as of [CURRENT DATE]. Ecosystem overview,
major players, recent changes, adoption trends, key features, limitations. Focus on
what's NEW and current — not evergreen docs.

TOOLS: Web search/extract. Prioritize current sources for [CURRENT YEAR].
\`\`\`

### Agent 2: Real Code Patterns

\`\`\`
[Same WHO/WHY preamble, adapted]

YOUR ANGLE: How developers are ACTUALLY using [TECHNOLOGY] in real projects. Find
shipped code patterns, not tutorial examples.

TOOLS: Use available GitHub/code search to inspect real repositories. Search for
actual code patterns like function calls, configuration, imports — not keywords.
Examples of good searches:
- 'import { X } from' for library usage
- Function signatures for API patterns
- Config file patterns for setup
\`\`\`

### Agent 3: Community Sentiment (X)

\`\`\`
[Same structure as X agent above, adapted for technology topic]
\`\`\`

### Agent 4: Existing Knowledge

\`\`\`
[Same structure as existing-knowledge agent above, adapted for technology topic]
\`\`\`

## Business/Strategy Research

### Agent 1: Market Data & Benchmarks

\`\`\`
[Same WHO/WHY preamble, adapted]

YOUR ANGLE: Hard numbers. Market size, pricing benchmarks, conversion rates, revenue
data, growth metrics. Focus on data that informs strategy decisions.

TOOLS: Web search. Look for reports, surveys, creator economy data, SaaS metrics.
\`\`\`

### Agent 2: Expert Frameworks & Strategies

\`\`\`
[Same WHO/WHY preamble, adapted]

YOUR ANGLE: Frameworks, mental models, and strategies from practitioners who've
done this successfully. Not theory — proven approaches with results.

TOOLS: Web search. Look for creator/founder breakdowns, case studies, strategy posts.
\`\`\`

### Agent 3: X Discourse

\`\`\`
[Same structure as X agent, adapted for business topic]
\`\`\`

### Agent 4: Existing Knowledge

\`\`\`
[Same structure as existing-knowledge agent, adapted for business topic]
\`\`\`
