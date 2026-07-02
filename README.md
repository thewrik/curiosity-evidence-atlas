# Curiosity Evidence Atlas

A small repo for turning recurring curiosities into RentControl-style visual
evidence essays: one sharp question, a narrative arc, audited claims, live data
charts, and a source trail a reader can inspect.

This was created after exploring
[defog-ai/factiq-plugin](https://github.com/defog-ai/factiq-plugin/) and the
reference essay
[Rent Control: The Ceiling Trap](https://mason.gmu.edu/~atabarro/RentControl/).

## Working Idea

FactIQ is useful here because it gives an agent a repeatable path from an
economic or financial question to sourced data:

- discover official datasets and series
- query a normalized warehouse with read-only SQL
- compute derived metrics locally
- publish shareable charts or reports with lineage
- build bespoke local HTML visualizations when a fixed chart is not enough

The RentControl page is useful as a product reference because it shows the
reader a claim in layers: story first, interactive theory next, empirical cases
after that, and sources at the end. This repo combines those ideas into a
repeatable essay pipeline.

## Repo Map

- `site/` - a static prototype you can open in a browser
- `docs/factiq-plugin-notes.md` - what the plugin can do and where it is limited
- `docs/rentcontrol-reference-notes.md` - what to borrow from the reference site
- `docs/product-brief.md` - the concept and design principles
- `docs/essay-pipeline.md` - the production workflow
- `docs/curiosity-backlog.md` - candidate topics based on the local trails found
- `docs/factiq-playbooks/` - starter playbooks for repeatable research domains
- `templates/essay-manifest.schema.json` - a schema for future essays

## Open The Prototype

Published site:

https://curiosity-evidence-atlas.surge.sh/

GitHub repo:

https://github.com/thewrik/curiosity-evidence-atlas

The prototype is static. Open:

```bash
open site/index.html
```

Or from this repo:

```bash
python3 -m http.server 8765
```

Then visit `http://localhost:8765/site/`.

## FactIQ Setup

The plugin is not installed in the current Codex environment I inspected. To use
it in a future thread:

```bash
codex plugin marketplace add defog-ai/factiq-plugin
codex plugin add factiq@factiq
codex mcp login factiq
```

After login, a future essay pass can replace the sample data in
`site/data/sample-essay.json` with real FactIQ ChartSpecs, report links, and
lineage.

## First Good Target

The strongest first essay is probably not "rent control again." It should be a
curiosity that naturally joins your local trails with FactIQ's strengths:

> When patient capital says the market is too short-term, where can we actually
> see that in the data?

That can connect the Nomad investor-letter artifact already present in local
Codex outputs to public market data, rates, sector cycles, earnings-call
language, and valuation/composition charts. It also gives you a personal spine:
curiosity first, evidence second, beautiful essay third.
