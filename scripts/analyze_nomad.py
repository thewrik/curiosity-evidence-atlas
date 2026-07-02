#!/usr/bin/env python3
"""Derive a worked-example analysis from the Nomad letters dataset."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "site" / "data" / "raw" / "research-data.json"


def year(value: str) -> int:
    match = re.search(r"(19|20)\d{2}", value or "")
    if not match:
        return 0
    return int(match.group(0))


def pct(part: int, whole: int) -> float:
    return round((part / whole) * 100, 1) if whole else 0.0


def load(source: Path) -> dict:
    return json.loads(source.read_text())


def company_lookup(companies: list[dict]) -> dict[str, dict]:
    lookup = {}
    for company in companies:
        lookup[company["canonical_name"]] = company
        lookup[company["canonical_name"].lower()] = company
    return lookup


def derive(data: dict, source: Path) -> dict:
    letters = sorted(
        data["letters"],
        key=lambda item: (year(item.get("period_end", "")), item.get("period_end", "")),
    )
    companies = data["companies"]
    artifacts = data["artifacts"]
    timeline_items = data["timeline_items"]
    company_by_name = company_lookup(companies)

    theme_counts = Counter()
    mental_model_counts = Counter()
    company_counts = Counter()
    letter_rows = []
    theme_by_year: dict[int, Counter] = defaultdict(Counter)
    company_years: dict[str, set[int]] = defaultdict(set)
    company_letters: dict[str, list[dict]] = defaultdict(list)

    for letter in letters:
        letter_year = year(letter["period_end"] or letter["sort_date"])
        themes = letter.get("themes", [])
        mental_models = letter.get("mental_models", [])
        mentioned_companies = [
            item.get("canonical_name") or item.get("name")
            for item in letter.get("companies", [])
            if item.get("canonical_name") or item.get("name")
        ]

        theme_counts.update(themes)
        mental_model_counts.update(mental_models)
        theme_by_year[letter_year].update(themes)
        company_counts.update(mentioned_companies)

        for name in mentioned_companies:
            company_years[name].add(letter_year)
            company_letters[name].append(
                {
                    "letter_id": letter["id"],
                    "title": letter["title"],
                    "year": letter_year,
                    "period_end": letter["period_end"],
                }
            )

        letter_rows.append(
            {
                "id": letter["id"],
                "title": letter["title"],
                "year": letter_year,
                "letter_type": letter["letter_type"],
                "page_count": letter["end_page"] - letter["start_page"] + 1,
                "theme_count": len(themes),
                "company_count": len(mentioned_companies),
                "claim_count": len(letter.get("claims", [])),
                "artifact_count": sum(1 for item in artifacts if item["letter_id"] == letter["id"]),
                "research_prompt_count": len(letter.get("what_to_research_next", [])),
                "summary": letter.get("summary", ""),
            }
        )

    top_companies = []
    for name, count in company_counts.most_common(12):
        years = sorted(company_years[name])
        company = company_by_name.get(name) or company_by_name.get(name.lower()) or {}
        top_companies.append(
            {
                "name": name,
                "mentions": count,
                "first_year": years[0],
                "last_year": years[-1],
                "span_years": years[-1] - years[0] + 1,
                "ticker": company.get("ticker_if_known"),
                "sector": company.get("sector"),
                "moat_summary": company.get("moat_summary", ""),
                "letters": company_letters[name],
            }
        )

    recurring_companies = [
        item
        for item in top_companies
        if item["mentions"] >= 3 and item["span_years"] >= 3
    ]

    research_rich_letters = sorted(
        letter_rows,
        key=lambda item: (
            item["claim_count"] + item["artifact_count"] + item["company_count"],
            item["page_count"],
        ),
        reverse=True,
    )[:8]

    years = sorted(theme_by_year)
    top_themes = [name for name, _ in theme_counts.most_common(8)]
    theme_year_matrix = [
        {
            "year": item_year,
            **{theme: theme_by_year[item_year].get(theme, 0) for theme in top_themes},
        }
        for item_year in years
    ]

    model_rows = [
        {"name": name, "letters": count, "share": pct(count, len(letters))}
        for name, count in mental_model_counts.most_common(12)
    ]

    event_type_counts = Counter(item.get("event_type", "Unknown") for item in timeline_items)
    artifact_kind_counts = Counter(item.get("kind", "Unknown") for item in artifacts)

    answer_cards = [
        {
            "question": "What is the core philosophy in the letters?",
            "answer": (
                f"Consumer Value Proposition appears in {theme_counts['Consumer Value Proposition']}/"
                f"{len(letters)} letters, Management Alignment in "
                f"{theme_counts['Management Alignment']}/{len(letters)}, and Patience & Long-Term "
                f"Horizon in {theme_counts['Patience & Long-Term Horizon']}/{len(letters)}."
            ),
            "evidence": "Counts from the per-letter `themes` field.",
            "chart": "theme_counts",
        },
        {
            "question": "Which companies carry the recurring examples?",
            "answer": (
                "Costco, Amazon, Stagecoach, Berkshire Hathaway, and Matichon are the top five "
                "recurring company examples in the extracted company mentions."
            ),
            "evidence": "Counts from each letter's extracted company list.",
            "chart": "top_companies",
        },
        {
            "question": "Is this mostly a stock-picking archive or a mental-model archive?",
            "answer": (
                "It is both, but the extracted structure says the mental-model layer is the durable "
                "one: the same themes recur across many different companies and years."
            ),
            "evidence": "Theme recurrence is broader than any single company recurrence.",
            "chart": "models",
        },
        {
            "question": "Which letters deserve a second research pass first?",
            "answer": (
                "The richest starting points are the letters with the highest combined count of "
                "claims, artifacts, and company examples."
            ),
            "evidence": "Ranked from claims + artifacts + company mentions per letter.",
            "chart": "research_rich_letters",
        },
        {
            "question": "What can this dataset not answer by itself?",
            "answer": (
                "It can identify what Nomad claimed and emphasized, but it cannot prove whether "
                "the claims were right without outside market, fundamentals, and macro data."
            ),
            "evidence": "The local dataset contains extracted text structure, not outcome data.",
            "chart": "next_questions",
        },
    ]

    external_questions = [
        {
            "question": "Did the recurring companies outperform after they first appeared?",
            "needs": "Market returns and benchmark data by first-mention date.",
            "factiq_fit": "Use market data and fundamentals for tickers such as COST and AMZN.",
        },
        {
            "question": "Were the letters early to consumer value and scale-economies ideas?",
            "needs": "Company fundamentals, category prices, margins, and earnings-call language.",
            "factiq_fit": "Use fundamentals, CPI/category data, and earnings-call search.",
        },
        {
            "question": "Did patience matter more in low-rate or high-rate regimes?",
            "needs": "Rates, inflation, market drawdowns, and recovery windows.",
            "factiq_fit": "Use official macro data plus market series.",
        },
        {
            "question": "Which claims are falsifiable versus purely interpretive?",
            "needs": "A claim ledger linked to market, accounting, and operating outcomes.",
            "factiq_fit": "Use FactIQ for the data-linked claims; keep interpretive claims separate.",
        },
    ]

    period_years = [row["year"] for row in letter_rows if row["year"]]

    return {
        "meta": {
            **data["meta"],
            "source_data_file": str(source),
            "derived_at": "2026-07-03",
            "note": "Derived only from the local Nomad letters dataset; no external market data used.",
        },
        "summary": {
            "letter_count": len(letters),
            "company_count": len(companies),
            "timeline_item_count": len(timeline_items),
            "artifact_count": len(artifacts),
            "date_span": f"{min(period_years)}-{max(period_years)}",
            "top_theme": theme_counts.most_common(1)[0][0],
            "top_company": top_companies[0]["name"],
        },
        "answer_cards": answer_cards,
        "theme_counts": [
            {"name": name, "letters": count, "share": pct(count, len(letters))}
            for name, count in theme_counts.most_common()
        ],
        "theme_year_matrix": theme_year_matrix,
        "mental_models": model_rows,
        "top_companies": top_companies,
        "recurring_companies": recurring_companies,
        "research_rich_letters": research_rich_letters,
        "letter_rows": letter_rows,
        "event_type_counts": [
            {"name": name, "count": count} for name, count in event_type_counts.most_common()
        ],
        "artifact_kind_counts": [
            {"name": name, "count": count} for name, count in artifact_kind_counts.most_common()
        ],
        "external_questions": external_questions,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    source = Path(args.source)
    data = derive(load(source), source)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
