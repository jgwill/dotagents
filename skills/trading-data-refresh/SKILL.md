---
name: trading-data-refresh
description: "Triggers and monitors the jgt data pipeline refresh (PDS→IDS→CDS→TTF→MLF). Use when market data is stale, before running signal scans, or to check pipeline health."
metadata: { "avaclaw": { "emoji": "🔄", "requires": { "env": ["JGT_DATA_MCP_URL"] } } }
---

# Trading Data Refresh

This skill awakens the data pipeline — moving raw price data through each transformation stage so that indicators, signals, and machine learning features are current and ready.

## Pipeline Stages

```
PDS → IDS → CDS → TTF → MLF
 ↓      ↓      ↓      ↓      ↓
Raw  Indicat  Signal  TF   ML
Price  ors   Detect  Anal  Feat
```

| Stage | Full Name             | What It Contains                                  |
| ----- | --------------------- | ------------------------------------------------- |
| PDS   | Price Data Series     | Raw OHLCV bars                                    |
| IDS   | Indicator Data Series | Williams indicators (Alligator, AO, AC, Fractals) |
| CDS   | Candidate Data Series | Detected signal candidates (FDB, fractal breaks)  |
| TTF   | Trade Timeframe       | Multi-timeframe cross-analysis                    |
| MLF   | ML Features           | Machine learning feature vectors                  |

## Workflow

### Step 1 — Check Scheduler Status

Call via jgt-data-mcp:

```
get_scheduler_status()
```

Display:

- Last run time per stage
- Currently running jobs (if any)
- Next scheduled run
- Any errors from last run

If a refresh is already running, report that and offer to monitor it instead of triggering a new one.

### Step 2 — Determine Scope

- If user said `all`: refresh all instruments, all stages
- If user specified instrument(s): refresh only those
- If user specified stage: refresh from that stage onward (stages are sequential — refreshing IDS requires valid PDS)

Default behavior (no args): Check status first, then offer to refresh all stale instruments.

### Step 3 — Trigger Refresh

Call via jgt-data-mcp:

```
trigger_refresh({
  instrument: "<INST or 'all'>",
  stage: "<stage or 'all'>",
  force: false
})
```

Pass `force: true` only if user explicitly asks to force a re-run despite fresh data.

Report the triggered job IDs or confirmation.

### Step 4 — Monitor Completion

After triggering, poll `get_scheduler_status()` periodically to track progress.

Display a progress view:

```
Data Pipeline Refresh — EURUSD H4
─────────────────────────────────
✅ PDS  — completed  (12:34:01)
✅ IDS  — completed  (12:34:45)
🔄 CDS  — running... (12:35:02)
⏳ TTF  — pending
⏳ MLF  — pending
─────────────────────────────────
Estimated completion: ~3 minutes
```

Continue monitoring until all requested stages complete or an error occurs.

### Step 5 — Report Outcome

On completion:

- List instruments refreshed
- Note any stages that failed (with error detail)
- Suggest next action: "Data is fresh — ready for signal scan" → suggest `trading-signal-scan`

## Status Display (No Refresh)

If user asks for "data pipeline status" without requesting a refresh:

1. Call `get_scheduler_status()`
2. Show last run times per stage per instrument
3. Flag any stages that are more than 1 hour stale (for intraday TFs) or 24 hours stale (for daily+)
4. Recommend which instruments/stages need refreshing

## Examples

**User**: "refresh data"
→ Check status, trigger full refresh for all instruments, monitor.

**User**: "update market data EURUSD"
→ Trigger refresh for EURUSD only, all stages, monitor completion.

**User**: "refresh CDS GBPJPY"
→ Trigger CDS refresh for GBPJPY (IDS must be current first; warn if not).

**User**: "data pipeline status"
→ Show status table — no refresh triggered.

**User**: "is the data fresh?"
→ Call `get_scheduler_status()`, report freshness per stage, flag any stale data.

**User**: "force refresh XAUUSD"
→ Trigger with `force: true` for XAUUSD, monitor.

## Notes

- Never trigger a force refresh for all instruments without user confirmation — it is resource-intensive.
- If `trigger_refresh` returns an error about a running job, do NOT trigger again; monitor the existing job.
- Stale data thresholds: M1-M15 → 15 min; M30-H1 → 1 hour; H4-D1 → 4 hours; W1-MN1 → 24 hours.
- After a successful refresh, CDS data is ready for `trading-signal-scan`.
