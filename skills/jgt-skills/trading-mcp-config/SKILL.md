---
name: trading-mcp-config
description: "Configure and verify jgt trading MCP server connections. Run this first before using any trading skills. Helps set up JGT_DATA_MCP_URL and JGT_ANALYSIS_MCP_URL environment variables."
metadata: { "avaclaw": { "emoji": "⚙️" } }
---

# Trading MCP Configuration

Help the user configure their jgt MCP server endpoints for trading skills.

## Required Services

### 1. jgt-data-mcp (Market Data Pipeline)

- **Default URL**: `http://localhost:8080`
- **Environment variable**: `JGT_DATA_MCP_URL`
- **Provides tools**: `get_instrument_list`, `get_market_data`, `get_williams_dimensions`, `refresh_pipeline`, `get_pipeline_status`
- **Data pipeline**: PDS → IDS → CDS → TTF → MLF

### 2. jgt-analysis-mcp (Trade Analysis Engine)

- **Default URL**: `http://localhost:8085`
- **Environment variable**: `JGT_ANALYSIS_MCP_URL`
- **Provides tools**: `analyze_trade_setup`, `get_gate_assessment`, `get_council_briefing`
- **Runs**: ARIANE Three Agreements evaluation

## Configuration Steps

1. **Check current config**: Look for `JGT_DATA_MCP_URL` and `JGT_ANALYSIS_MCP_URL` in the environment
2. **If not set**: Guide the user to add them to `~/.bashrc`, `~/.zshrc`, or `~/.avaclaw/env`:
   ```bash
   export JGT_DATA_MCP_URL=http://localhost:8080
   export JGT_ANALYSIS_MCP_URL=http://localhost:8085
   ```
3. **Verify connectivity**: Test both endpoints:
   - `curl -s $JGT_DATA_MCP_URL/health` should return 200
   - `curl -s $JGT_ANALYSIS_MCP_URL/health` should return 200
4. **Test tool availability**: Try calling `get_instrument_list` via jgt-data-mcp to confirm tools are accessible

## Verification Report Format

```
🔧 Trading MCP Configuration Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
jgt-data-mcp:     ✅ Connected (http://localhost:8080)
  └─ Tools:       get_instrument_list ✅ | get_market_data ✅ | get_williams_dimensions ✅
  └─ Pipeline:    PDS ✅ → IDS ✅ → CDS ✅ → TTF ✅ → MLF ✅

jgt-analysis-mcp: ✅ Connected (http://localhost:8085)
  └─ Tools:       analyze_trade_setup ✅ | get_gate_assessment ✅ | get_council_briefing ✅

Overall: 2/2 services healthy, 8/8 tools responding
Trading skills: READY ✅
```

## Troubleshooting

- **Connection refused**: Service not running. Start the jgt services first.
- **Timeout**: Service starting up or network issue. Wait 30 seconds and retry.
- **404 on tools**: Service running but version mismatch. Check service version.
- **Partial tools**: Some pipeline stages may be initializing. Run `trading-data-refresh` to trigger a full pipeline build.
