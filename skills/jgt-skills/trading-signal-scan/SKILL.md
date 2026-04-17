---
name: trading-signal-scan
description: "Scans for active FDB/Williams trading signals across instruments using the jgt-data-mcp pipeline. Use when you want to discover what's trading, identify FDB candidates, or get a market-wide signal overview."
metadata: { "avaclaw": { "emoji": "📡", "requires": { "env": ["JGT_DATA_MCP_URL"] } } }
---

# Trading Signal Scan

Discover active FDB and Williams Method signals across the instrument universe. This skill surfaces what the market is offering right now.

## Workflow

### Step 1 — Gather the Instrument Universe

Call `get_instrument_list` via jgt-data-mcp to retrieve all tracked instruments.
If the user specified a single instrument, use only that one.

### Step 2 — Retrieve CDS Signal Data

For each instrument (or the specified one), call:

```
get_market_data({ instrument: "<INST>", timeframe: "<TF>", data_type: "cds" })
```

Focus on the CDS (Candidate Data Series) layer — this is where signal detection lives.
If no timeframe is specified, scan these by default: **H4, D1, H1**.

### Step 3 — Check Williams Dimensions

For instruments showing CDS activity, call:

```
get_williams_dimensions({ instrument: "<INST>", timeframe: "<TF>" })
```

Extract: Alligator state, AO value/trend, AC value, fractal levels, FDB presence.

### Step 4 — Identify FDB Candidates

A **Fractal Divergent Bar (FDB)** is the primary entry signal. Flag instruments where:

- A fractal signal exists on CDS
- AO confirms momentum direction
- Alligator is not sleeping (teeth/lips/jaw are spread)

### Step 5 — Render Signal Table

Present results as a markdown table:

| Instrument | Timeframe | Signal Type | AO  | Alligator State | Strength | Notes     |
| ---------- | --------- | ----------- | --- | --------------- | -------- | --------- |
| EURUSD     | H4        | FDB Long    | +ve | Feeding         | Strong   | Above jaw |
| ...        | ...       | ...         | ... | ...             | ...      | ...       |

**Signal Types**: `FDB Long`, `FDB Short`, `Fractal Only`, `AO Divergence`, `No Signal`
**Alligator States**: `Sleeping` (converged), `Awakening` (opening), `Feeding` (spread/trending)
**Strength**: `Strong` (all 5 dimensions aligned), `Moderate` (3-4), `Weak` (1-2)

## Examples

**User**: "scan for signals"
→ Run full scan on all instruments, H4 and D1 timeframes, return table.

**User**: "what's trading on EURUSD?"
→ Scan EURUSD across M15, H1, H4, D1; report signal status per timeframe.

**User**: "signal scan H1"
→ Scan all instruments on H1 timeframe only.

**User**: "FDB candidates today"
→ Scan all instruments on D1; filter to FDB-only results.

## Notes

- CDS data requires the pipeline to have run (PDS→IDS→CDS); if data seems stale, suggest running `trading-data-refresh`.
- Always note the data timestamp so the user knows signal freshness.
- If `get_instrument_list` returns an empty list, report this clearly and suggest checking jgt-data-mcp status.
