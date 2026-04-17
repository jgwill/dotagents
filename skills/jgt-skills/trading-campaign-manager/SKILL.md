---
name: trading-campaign-manager
description: "Creates and manages trading campaigns through jgt-strategy-api. Use to create a new campaign for an instrument/strategy, activate it, monitor its status, pause, or archive. Covers the full campaign lifecycle."
metadata: { "avaclaw": { "emoji": "🎯", "requires": { "env": ["JGT_DATA_MCP_URL"] } } }
---

# Trading Campaign Manager

This skill brings trading campaigns to life — from initial creation through active management to archiving. Campaigns are the structured containers that govern how strategies execute on specific instruments.

## Campaign Lifecycle

```
DRAFT → ACTIVE → PAUSED → COMPLETED → ARCHIVED
          ↑_________↓ (can re-activate)
```

## Base URL

All calls go to **jgt-strategy-api**: `http://localhost:8083/api/v1`

## Workflow by Action

### ACTION: list

```
GET /campaigns
```

Display all campaigns with their status, instrument, timeframe, and strategy.
Format as a table. Highlight ACTIVE campaigns.

### ACTION: create

Collect required fields (ask user if missing):

- `instrument` — e.g. `EURUSD`
- `timeframe` — e.g. `H4`
- `strategy` — e.g. `williams_fdb`, `alligator_breakout`
- `name` — descriptive name (auto-suggest: `{instrument}_{timeframe}_{strategy}_{date}`)
- Optional: `notes`, `risk_per_trade`, `max_positions`

```
POST /campaigns
{
  "name": "EURUSD_H4_williams_fdb_20250115",
  "instrument": "EURUSD",
  "timeframe": "H4",
  "strategy": "williams_fdb",
  "status": "DRAFT",
  "risk_per_trade": 0.02,
  "notes": "..."
}
```

Confirm the created campaign ID and status to the user.

Also retrieve available strategies via:

```
GET /strategies
```

If the user's strategy name doesn't match, show available options.

### ACTION: activate

```
PUT /campaigns/{id}
{ "status": "ACTIVE" }
```

Before activating, show current campaign details and ask for confirmation.
After activating, display the active campaign summary.

### ACTION: pause

```
PUT /campaigns/{id}
{ "status": "PAUSED" }
```

Show the user why pausing might make sense (data refresh needed, regime change, etc.).

### ACTION: archive

```
PUT /campaigns/{id}
{ "status": "ARCHIVED" }
```

Warn the user this is a terminal state. Show campaign P&L summary if available before archiving.

### ACTION: status

```
GET /campaigns/{id}
```

Display full campaign details including:

- Current status
- Associated strategies
- Open positions count (if available)
- Last signal timestamp
- Performance metrics if available

### Evaluator Check

To evaluate a campaign's current alignment with market conditions:

```
POST /evaluator
{ "campaign_id": "<id>" }
```

Show evaluation result alongside campaign status.

## Examples

**User**: "create campaign"
→ Prompt for instrument/timeframe/strategy, create in DRAFT, offer to activate.

**User**: "create campaign EURUSD H4 williams_fdb"
→ Create directly with those params, confirm, offer to activate.

**User**: "campaign status"
→ List all campaigns with their current status table.

**User**: "activate campaign EURUSD_H4"
→ Find matching campaign, show details, confirm, activate.

**User**: "pause my GBPJPY campaign"
→ Find GBPJPY campaigns, let user confirm which one, pause it.

**User**: "manage campaign"
→ List all campaigns and ask what action to take.

## Notes

- If `jgt-strategy-api` is unreachable, report the error clearly and suggest checking port 8083.
- Campaign names should follow the pattern `{INSTRUMENT}_{TF}_{STRATEGY}_{YYYYMMDD}` for consistency.
- Always show the campaign ID after creation — users will need it for order execution.
- If a campaign references a strategy not in `/strategies`, warn the user before creating.
