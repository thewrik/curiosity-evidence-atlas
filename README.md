# Nomad Questions

A worked example that uses a real dataset, not a template.

Live site:

https://curiosity-evidence-atlas.surge.sh/

GitHub repo:

https://github.com/thewrik/curiosity-evidence-atlas

## What This Is

This repo takes the local **Nomad Letters Research Site** JSON dataset and asks:

> What questions can this dataset answer by itself, before we bring in external
> market or macro data?

The page answers those questions with data from the dataset:

- what ideas recur most often across the letters
- which companies carry the recurring examples
- which letters are densest in claims, artifacts, and company mentions
- what this dataset can identify now
- what needs FactIQ or another external data source later

## Data

Raw source:

- `site/data/raw/research-data.json`

Derived analysis:

- `site/data/nomad-analysis.json`

The derived file is generated from the raw dataset with:

```bash
python3 scripts/analyze_nomad.py --out site/data/nomad-analysis.json
```

Current dataset summary:

- 24 letters
- 45 companies
- 160 timeline items
- 65 extracted artifacts
- period covered: 2001-2013

## Run Locally

```bash
cd site
python3 -m http.server 8765
```

Then open:

```text
http://127.0.0.1:8765/
```

## Deploy

This site is deployed with Surge:

```bash
surge --project site --domain curiosity-evidence-atlas.surge.sh
```

## Why FactIQ Still Matters

The local dataset tells us what Nomad emphasized and claimed. It does not prove
whether those claims were correct. The natural next layer is to connect first
mentions and thesis passages to outside data:

- stock returns and benchmarks
- fundamentals and margins
- rates and inflation regimes
- earnings-call language
- sector or category-level economic data

That is where FactIQ can become useful: not as the first artifact, but as the
outcome-data layer on top of this extracted reading map.
