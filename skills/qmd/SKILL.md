---
name: qmd
description: Search markdown knowledge bases, notes, and documentation using QMD. Use when users ask to search notes, find documents, or look up information.
license: MIT
compatibility: Requires the `qmd` MCP server to be registered. Local or SSH-remote — the skill does not care which.
metadata:
  author: tobi
  version: "2.1.0"
allowed-tools: mcp__qmd__*
---

# QMD — Hybrid Search over Markdown

Use the `mcp__qmd__*` tools. Whether the index lives on this host or behind an SSH proxy is a deployment detail; the tool surface is identical. If `mcp__qmd__*` tools are not present in your toolset, QMD is not registered on this host — say so and stop. Do not fall back to a `qmd` shell binary.

## MCP: `query`

```json
{
  "searches": [
    { "type": "lex", "query": "CAP theorem consistency" },
    { "type": "vec", "query": "tradeoff between consistency and availability" }
  ],
  "collections": ["docs"],
  "limit": 10
}
```

### Query Types

| Type | Method | Input |
|------|--------|-------|
| `lex` | BM25 | Keywords — exact terms, names, code |
| `vec` | Vector | Question — natural language |
| `hyde` | Vector | Answer — hypothetical result (50-100 words) |

### Writing Good Queries

**lex (keyword)**
- 2-5 terms, no filler words
- Exact phrase: `"connection pool"` (quoted)
- Exclude terms: `performance -sports` (minus prefix)
- Code identifiers work: `handleError async`

**vec (semantic)**
- Full natural language question
- Be specific: `"how does the rate limiter handle burst traffic"`
- Include context: `"in the payment service, how are refunds processed"`

**hyde (hypothetical document)**
- Write 50-100 words of what the *answer* looks like
- Use the vocabulary you expect in the result

**expand (auto-expand)**
- Use a single-line query (implicit) or `expand: question` on its own line
- Lets the local LLM generate lex/vec/hyde variations
- Do not mix `expand:` with other typed lines — it's either a standalone expand query or a full query document

### Intent (Disambiguation)

When a query term is ambiguous, add `intent` to steer results:

```json
{
  "searches": [
    { "type": "lex", "query": "performance" }
  ],
  "intent": "web page load times and Core Web Vitals"
}
```

Intent affects expansion, reranking, chunk selection, and snippet extraction. It does not search on its own — it's a steering signal that disambiguates queries like "performance" (web-perf vs team health vs fitness).

### Combining Types

| Goal | Approach |
|------|----------|
| Know exact terms | `lex` only |
| Don't know vocabulary | Use a single-line query (implicit `expand:`) or `vec` |
| Best recall | `lex` + `vec` |
| Complex topic | `lex` + `vec` + `hyde` |
| Ambiguous query | Add `intent` to any combination above |

First query gets 2x weight in fusion — put your best guess first.

### Lex Query Syntax

| Syntax | Meaning | Example |
|--------|---------|---------|
| `term` | Prefix match | `perf` matches "performance" |
| `"phrase"` | Exact phrase | `"rate limiter"` |
| `-term` | Exclude | `performance -sports` |

Note: `-term` only works in lex queries, not vec/hyde.

### Collection Filtering

```json
{ "collections": ["docs"] }              // Single
{ "collections": ["docs", "notes"] }     // Multiple (OR)
```

Omit to search all collections.

## Other MCP Tools

| Tool | Use |
|------|-----|
| `get` | Retrieve doc by path or `#docid` |
| `multi_get` | Retrieve multiple by glob/list |
| `status` | Collections and health |

## Setup

QMD is registered as an MCP server (`qmd`) in this host's MCP config. No local binary, no HTTP endpoint, no shell fallbacks — every interaction goes through `mcp__qmd__*`. If the tools are missing, ask the host operator to register the `qmd` MCP; do not attempt to install a local CLI.
