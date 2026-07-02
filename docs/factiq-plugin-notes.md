# FactIQ Plugin Notes

Source explored: `defog-ai/factiq-plugin`, version `0.11.1` in the Codex
manifest at the time of cloning.

## What It Is

FactIQ is a Codex/Claude plugin that exposes an authenticated MCP server for
economic and financial data analysis. The agent does the analysis work. FactIQ
provides the tools:

- `get_data_catalog` for available schemas and dataset coverage
- `search_datasets`, `describe_dataset`, and `search_series` for discovery
- `run_sql` for read-only SQL against normalized source schemas
- `get_series` for known time series
- `get_market_data` for current market, FX, commodity, and fundamentals data
- `search_earnings` for earnings-call intelligence
- `share_chart` and `share_report` for publishable outputs

The normalized data model is the key abstraction:

- `series` is the catalog
- `data_points` holds `(series_id, time, value)`
- `dimensions` stores faceted metadata such as geography, partner, commodity,
  flow, industry, or category

That uniform shape is what makes a "curiosity studio" plausible. A playbook can
teach the agent the shape of a domain once, then reuse it across essays.

## Useful Output Modes For This Project

### Quick Chart

Best for a single claim that needs one chart. Example: "US housing completions
lagged household formation by X after Y." The output can become one figure in a
visual essay.

### Detailed Report

Best for scouting a whole essay. It can produce a multi-section report with 2-5
charts and methodology notes. Treat this as the research memo before writing the
public-facing essay.

### Bespoke Local Viz

Best match for the RentControl reference. FactIQ can fetch and save raw results,
then a local HTML page can assemble custom interaction, chapter rhythm, and
visual polish.

## Why It Matters Here

The plugin can shorten the path from "I wonder whether..." to "here is the
chart, source, and lineage." That matters because visual essays fail when the
data layer is too expensive to repeat. FactIQ makes repeatability the default.

## Constraints

- It requires a FactIQ account and OAuth login.
- The MCP tools were not available in this thread, so no live FactIQ query was
  run here.
- Row-returning tools cap results at 50 rows, so the agent must aggregate in SQL
  or window series carefully.
- It is strongest for official economic, financial, trade, labor, market, and
  earnings data. It is not a general academic literature database.
- Web/literature claims still need a separate source workflow.

## Where To Extend It

The plugin explicitly invites "domain playbooks." For this project, playbooks
are the highest leverage contribution:

- housing scarcity and affordability
- patient capital and market time horizons
- regulation and industry structure
- consumer value propositions and scale economies shared
- rates, inflation, and asset duration

