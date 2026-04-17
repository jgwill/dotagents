---
name: trading-gate-assessment
description: "Runs the ARIANE Three Agreements protocol to produce a trade verdict (ALLOW | WAIT | NO_TRADE). Use when evaluating whether to enter a trade. Consults all Four Faces: Alligator Guardian, Fractal Pathfinder, Momentum Witness, Garden Keeper."
metadata:
  {
    "avaclaw":
      { "emoji": "🚦", "requires": { "env": ["JGT_DATA_MCP_URL", "JGT_ANALYSIS_MCP_URL"] } },
  }
---

# Trading Gate Assessment — ARIANE Protocol

This skill channels the ARIANE Four Faces to render a trade verdict. All four Faces must reach agreement before a trade is ALLOWED. One dissent means WAIT; two or more mean NO_TRADE.

## The Four Faces

| Face   | Role               | Primary Tool              | Question Asked                 |
| ------ | ------------------ | ------------------------- | ------------------------------ |
| Face 1 | Alligator Guardian | `get_alligator_alignment` | Is the trend structure sound?  |
| Face 2 | Fractal Pathfinder | `get_market_data(cds)`    | Is there a valid entry signal? |
| Face 3 | Momentum Witness   | `get_williams_dimensions` | Does energy confirm direction? |
| Face 4 | Garden Keeper      | `query_analysis`          | Is risk/capital acceptable?    |

## Workflow

### Step 1 — Parse Intent

Identify: `instrument`, `timeframe`, `direction` (long/short, or undecided).
If direction is not stated, run the assessment for the dominant signal direction found in Face 2.

### Step 2 — Face 1: Alligator Guardian

Call via jgt-data-mcp:

```
get_alligator_alignment({ instrument: "<INST>", timeframe: "<TF>" })
```

Assess:

- **ALLOW**: Alligator is Feeding (spread lines, price outside), direction matches
- **WAIT**: Alligator is Awakening (lines starting to separate)
- **NO_TRADE**: Alligator is Sleeping (lines intertwined/converged)

Record Face 1 verdict + reasoning.

### Step 3 — Face 2: Fractal Pathfinder

Call via jgt-data-mcp:

```
get_market_data({ instrument: "<INST>", timeframe: "<TF>", data_type: "cds" })
```

Assess:

- **ALLOW**: Active FDB or fresh fractal breakout in trade direction
- **WAIT**: Fractal exists but not yet broken / FDB forming
- **NO_TRADE**: No fractal signal, or signal is counter-direction

Record Face 2 verdict + fractal levels found.

### Step 4 — Face 3: Momentum Witness

Call via jgt-data-mcp:

```
get_williams_dimensions({ instrument: "<INST>", timeframe: "<TF>" })
```

Assess AO (Awesome Oscillator) and AC (Acceleration/Deceleration):

- **ALLOW**: AO positive + accelerating in trade direction (AC confirms)
- **WAIT**: AO in transition (crossing zero or diverging)
- **NO_TRADE**: AO opposes trade direction

Record Face 3 verdict + AO/AC values.

### Step 5 — Face 4: Garden Keeper

Call via jgt-analysis-mcp:

```
query_analysis({ instrument: "<INST>", query_type: "risk_assessment" })
```

Also call `get_perspective` if available for regime context.
Assess:

- **ALLOW**: Position size fits capital rules, no excessive exposure, regime supports trade
- **WAIT**: Near exposure limits, or regime is uncertain
- **NO_TRADE**: Over-exposure, adverse regime, or capital rules violated

Record Face 4 verdict + risk details.

### Step 6 — Three Agreements Synthesis

Count verdicts:

- 4× ALLOW → **✅ ALLOW** — proceed to order execution
- 3× ALLOW, 1× WAIT → **⏳ WAIT** — monitor, conditions almost ready
- Any NO_TRADE → **🚫 NO_TRADE** — do not enter
- 2+ WAIT → **⏳ WAIT** — insufficient alignment

### Step 7 — Render Verdict Card

```
═══════════════════════════════════════
ARIANE GATE ASSESSMENT
Instrument : EURUSD | Timeframe: H4 | Direction: Long
───────────────────────────────────────
Face 1 — Alligator Guardian : ALLOW
  Alligator feeding upward, price above jaw
Face 2 — Fractal Pathfinder : ALLOW
  FDB signal active at 1.0850, fractal broken
Face 3 — Momentum Witness   : WAIT
  AO positive but AC decelerating
Face 4 — Garden Keeper      : ALLOW
  Risk within limits, uptrend regime confirmed
───────────────────────────────────────
THREE AGREEMENTS VERDICT: ⏳ WAIT
  Reason: Face 3 dissents — await AC confirmation
═══════════════════════════════════════
```

## Examples

**User**: "assess trade EURUSD H4 long"
→ Run full Four Faces assessment, render verdict card.

**User**: "gate check GBPJPY D1"
→ Run assessment for dominant signal direction on GBPJPY D1.

**User**: "should I trade USDJPY?"
→ Scan H4 and D1, run ARIANE on strongest signal found.

**User**: "ARIANE assessment XAUUSD H1 short"
→ Full assessment for gold short on H1.

## Notes

- If any MCP tool fails, report that Face as INCONCLUSIVE (counts as WAIT).
- Always show the reasoning from each Face, not just the final verdict.
- After an ALLOW verdict, suggest using `trading-order-execution` skill to proceed.
- After a WAIT verdict, suggest re-running after next candle close.
