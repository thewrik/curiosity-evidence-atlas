# Essay Pipeline

## 0. Capture The Curiosity

Write the question in one sentence. Then write the honest reason it matters.

Example:

> Do patient investors win because they are smarter, or because institutions
> force everyone else to care about the next quarter?

## 1. Build The Claim Ledger

Every essay starts with claims, not charts.

Claim fields:

- `claim`
- `type`: mechanism, empirical, definition, historical, anecdotal, normative
- `status`: untested, supported, mixed, contradicted, source-needed
- `evidence_needed`
- `source_candidates`
- `factiq_dataset_candidates`
- `notes`

## 2. Use FactIQ For The Data Scout

For economic or financial claims:

1. call `get_data_catalog`
2. search likely datasets
3. describe chosen datasets
4. search series or inspect dimensions
5. query with `run_sql`
6. compute derived metrics locally
7. publish quick charts or a detailed report
8. save ChartSpecs and report links into the essay manifest

## 3. Write The Mechanism Toy

Before the empirical sections, create one small interactive model. It can be:

- a slider
- a two-state simulation
- an annotated diagram
- a sortable table
- a before/after toggle

Its job is to teach the causal mechanism, not prove the whole essay.

## 4. Draft The Essay

Use this chapter shape:

1. Hook: why the question is tempting
2. Mechanism: the simple model
3. First test: the cleanest data
4. Complication: where the model breaks or needs nuance
5. Case: one concrete story
6. Synthesis: what changed
7. Sources: how to audit the work

## 5. Verify

Before publishing:

- every chart title states a numerical finding
- every chart has source and lineage
- every strong factual sentence appears in the claim ledger
- every caveat that affects interpretation is visible in the prose
- the page works on mobile
- the source trail can be followed by a skeptical reader

