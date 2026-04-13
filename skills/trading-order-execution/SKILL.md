---
name: trading-order-execution
description: "Places and manages orders through jgt-transact with mandatory human confirmation at every step. Use for opening positions, closing trades, placing limit/stop orders, or cancelling orders. ALWAYS proposes before executing."
metadata: { "avaclaw": { "emoji": "⚡", "requires": { "env": ["JGT_DATA_MCP_URL"] } } }
---

> ⚠️ **MESSAGING CHANNEL SAFETY**: When invoked from WhatsApp, Telegram, Slack, or any non-terminal channel, ALWAYS require the user to confirm with their full name or a configured PIN before executing any order. Terminal/direct sessions follow the standard confirmation flow below.

# Trading Order Execution

This skill executes trades through the jgt-transact API. **Human confirmation is required at every execution step.** No order is placed without explicit user approval.

## ⚠️ SAFETY CONTRACT

> **This skill will NEVER execute an order without showing you the full proposal and receiving your explicit confirmation.**
> Default position size is conservative (0.01 lots) unless user specifies otherwise.
> Maximum single order size is capped at campaign/account risk rules.

## Base URLs

- **jgt-transact**: `http://localhost:8084`
- **jgt-analysis-mcp**: via MCP tools `propose_action`, `acknowledge_action`

## Order Workflow (Mandatory Steps)

### STEP 1 — Propose Action

Before any execution, call via jgt-analysis-mcp:

```
propose_action({
  instrument: "<INST>",
  action: "open|close|cancel",
  direction: "long|short",
  size: <lots>,
  order_type: "market|limit|stop",
  price: <price_if_limit_stop>,
  rationale: "<why this trade>"
})
```

This logs the intent and generates a proposal ID.

### STEP 2 — Display Proposal to Human

Show a clear, formatted proposal card:

```
╔══════════════════════════════════════╗
║         ORDER PROPOSAL               ║
╠══════════════════════════════════════╣
║ Action     : OPEN LONG               ║
║ Instrument : EURUSD                  ║
║ Size       : 0.10 lots               ║
║ Order Type : Market                  ║
║ Est. Price : 1.08450                 ║
║ Stop Loss  : 1.08150 (30 pips)       ║
║ Take Profit: 1.08990 (54 pips)       ║
║ Risk/Reward: 1:1.8                   ║
║ Proposal ID: prop_20250115_001       ║
╠══════════════════════════════════════╣
║ ⚠️  AWAITING YOUR CONFIRMATION       ║
║ Type YES to execute, NO to cancel    ║
╚══════════════════════════════════════╝
```

**STOP HERE. Do not proceed until the user explicitly types YES or confirms.**

### STEP 3 — Human Confirms or Rejects

- If user says **YES / confirm / proceed / execute**: continue to Step 4.
- If user says **NO / cancel / stop / abort**: call `acknowledge_action` with status=rejected, inform user, stop.
- If user modifies parameters (size, price, etc.): return to Step 1 with updated params.

### STEP 4 — Acknowledge Action

Call via jgt-analysis-mcp:

```
acknowledge_action({
  proposal_id: "<prop_id>",
  status: "confirmed",
  confirmed_by: "human"
})
```

### STEP 5 — Execute via jgt-transact

**Open Long/Short (Market)**:

```
POST http://localhost:8084/fxaddorder
{
  "instrument": "EURUSD",
  "direction": "long",
  "size": 0.10,
  "order_type": "market"
}
```

**Open with Limit/Stop**:

```
POST http://localhost:8084/fxaddorder
{
  "instrument": "EURUSD",
  "direction": "long",
  "size": 0.10,
  "order_type": "limit",
  "price": 1.08200
}
```

**Close Position**:

```
POST http://localhost:8084/fxclose
{
  "instrument": "EURUSD",
  "ticket": "<ticket_id>"
}
```

**Remove/Cancel Order**:

```
POST http://localhost:8084/fxrmorder
{
  "ticket": "<ticket_id>"
}
```

**List Open Positions/Orders**:

```
GET http://localhost:8084/fxtr
```

### STEP 6 — Confirm Execution

Report the execution result to the user:

- Order ticket number
- Fill price (if market order)
- Order status
- Any errors clearly highlighted

## Action Reference

| User Intent           | Endpoint           | Notes                             |
| --------------------- | ------------------ | --------------------------------- |
| Open long/short       | `POST /fxaddorder` | Requires confirmation             |
| Close position        | `POST /fxclose`    | Show P&L before confirm           |
| Cancel pending order  | `POST /fxrmorder`  | Show order details before confirm |
| List positions/orders | `GET /fxtr`        | No confirmation needed            |

## Examples

**User**: "place order EURUSD long 0.1"
→ Propose market long 0.1 lots EURUSD, show card, await YES.

**User**: "execute trade"
→ Ask for instrument, direction, size, order type. Then propose.

**User**: "close position EURUSD"
→ List open EURUSD positions, show P&L for each, propose close, await YES.

**User**: "cancel my GBPJPY limit order"
→ List pending GBPJPY orders, show details, propose removal, await YES.

**User**: "order management"
→ Show all open positions and pending orders via `GET /fxtr`.

**User**: "list positions"
→ Call `GET /fxtr`, format open trades table (no confirmation needed).

## Notes

- If ARIANE gate assessment has NOT been run, warn the user and suggest running `trading-gate-assessment` first.
- Never suggest or accept position sizes that exceed 5% of account balance per trade without explicit user instruction.
- If jgt-transact is unreachable (port 8084), report clearly — do NOT attempt workarounds.
- Always log the proposal ID from `propose_action` — it is the audit trail.
- If a market order fails, do NOT retry automatically. Report the error and await user decision.
