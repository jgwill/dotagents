---
name: trading-htf-analysis
description: "Analyzes higher timeframe Alligator state and wave structure (H4/D1/W1) to determine trend alignment, wave position, and optimal entry timeframes. Use before trade assessment or when orienting to the macro market structure."
metadata: { "avaclaw": { "emoji": "📐", "requires": { "env": ["JGT_DATA_MCP_URL"] } } }
---

# Higher Timeframe Analysis

This skill reads the larger wave structures that govern market direction — the Alligator's feeding patterns across H4, D1, and W1 timeframes, revealing where in the wave sequence price currently lives and which entry timeframes are aligned.

## Default Timeframe Stack (HTF → Entry)

| Level        | Timeframe | Role                      |
| ------------ | --------- | ------------------------- |
| Macro        | W1 / MN1  | Dominant trend direction  |
| Intermediate | D1        | Swing structure           |
| Tactical     | H4        | Trade timeframe reference |
| Entry        | H1 / H4   | Signal timeframe          |

Analyze top-down: W1 → D1 → H4. Alignment across all three is the strongest setup.

## Workflow

### Step 1 — Parse Request

Identify `instrument`. Default timeframes: `W1, D1, H4`.
If user specifies timeframes, use those instead.

### Step 2 — Get Alligator Alignment Per Timeframe

For each timeframe, call via jgt-data-mcp:

```
get_alligator_alignment({ instrument: "<INST>", timeframe: "<TF>" })
```

Extract per timeframe:

- Alligator state: `Sleeping` | `Awakening` | `Feeding`
- Direction: `Bullish` | `Bearish` | `Neutral`
- Jaw / Teeth / Lips values and their spread
- Price position relative to Alligator (above / inside / below)

### Step 3 — Get Wave Perspective

Call via jgt-data-mcp:

```
get_perspective({ instrument: "<INST>", analysis_type: "wave_analysis", timeframe: "<HTF>" })
```

Use D1 or W1 as the primary wave analysis timeframe.
Extract:

- Current wave count / position (Elliott or Williams wave labeling)
- Wave direction
- Estimated wave stage (early / mid / mature / exhaustion)

### Step 4 — Get TTF Data

Call via jgt-data-mcp:

```
get_market_data({ instrument: "<INST>", timeframe: "H4", data_type: "ttf" })
```

The TTF (Trade Timeframe) layer provides cross-timeframe signal integration.

### Step 5 — Assess Trend Strength and Alignment

Score the alignment:

- **3/3 aligned** (all HTFs Feeding in same direction): Maximum conviction
- **2/3 aligned**: Moderate — proceed with caution
- **1/3 or 0/3**: No alignment — avoid entries against dominant timeframes

Determine **price zone**:

- Above all Alligator lines → strongly in trend territory
- Inside Alligator → consolidation, uncertain
- Below all lines (for bullish) → potential reversal or counter-trend only

### Step 6 — Render HTF Analysis Report

```
╔═══════════════════════════════════════════════════╗
║    HIGHER TIMEFRAME ANALYSIS — EURUSD             ║
╠═══════════════════════════════════════════════════╣
║ W1   │ Feeding Bullish  │ Price above jaw  │ ✅   ║
║ D1   │ Awakening Bullish│ Price at teeth   │ 🔄   ║
║ H4   │ Sleeping         │ Price inside     │ ⏳   ║
╠═══════════════════════════════════════════════════╣
║ Trend Alignment : 2/3 Bullish                     ║
║ Wave Position   : Wave 3 of D1 impulse (mid)      ║
║ Wave Stage      : Mid-wave, momentum intact        ║
╠═══════════════════════════════════════════════════╣
║ SUGGESTED ENTRY TIMEFRAMES                        ║
║  Primary  : H4 (await Alligator to wake)          ║
║  Secondary: H1 (for early positioning)            ║
╠═══════════════════════════════════════════════════╣
║ TREND BIAS: BULLISH — WAIT for H4 alignment       ║
╚═══════════════════════════════════════════════════╝
```

### Alligator State Legend

| State        | Jaw/Teeth/Lips         | Meaning                         |
| ------------ | ---------------------- | ------------------------------- |
| 🛌 Sleeping  | Intertwined, flat      | No trend, avoid new entries     |
| 👁️ Awakening | Starting to spread     | Trend emerging, prepare         |
| 🐊 Feeding   | Spread, sequential     | Active trend, enter with signal |
| 😴 Sated     | Converging after trend | Trend ending, tighten stops     |

## Timeframe Alignment Rules

- **Long bias**: W1 and D1 both Feeding Bullish → look for long entries on H4/H1
- **Short bias**: W1 and D1 both Feeding Bearish → look for short entries on H4/H1
- **Mixed signals**: D1 Bullish + H4 Bearish → wait for resolution, no new entries
- **All sleeping**: Market in consolidation — wait for breakout

## Suggested Entry Timeframes (by HTF alignment)

| HTF Alignment              | Suggested Entry TF   |
| -------------------------- | -------------------- |
| W1+D1+H4 aligned           | H1 or H4             |
| W1+D1 aligned, H4 sleeping | H4 (await wake)      |
| W1 aligned only            | D1 (await D1 signal) |
| No alignment               | No entry — wait      |

## Examples

**User**: "htf analysis EURUSD"
→ Full W1/D1/H4 analysis, wave structure, trend bias, entry TF suggestion.

**User**: "higher timeframe GBPJPY"
→ Same as above for GBPJPY.

**User**: "wave structure XAUUSD D1"
→ Focus on D1 wave analysis + H4 alignment for gold.

**User**: "Alligator alignment USDJPY"
→ Show Alligator state across W1, D1, H4 in table format.

**User**: "what timeframe should I trade EURUSD?"
→ Run HTF analysis, recommend entry timeframes based on alignment.

## Notes

- HTF analysis is the prerequisite for `trading-gate-assessment`. Always run HTF first for context.
- If W1 data is unavailable (e.g., new instrument), use D1 as the top-level macro timeframe.
- Wave count labels are directional guidance, not strict Elliott labeling — use them as context, not precise targets.
- After identifying the entry timeframe, run `trading-signal-scan` on that timeframe to find specific signals.
