#!/usr/bin/env python3
"""Build a FactIQ-ready research-question dossier from the Nomad dataset."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = REPO_ROOT / "site" / "data" / "raw" / "research-data.json"
OUT = REPO_ROOT / "site" / "data" / "scale-sharing-rq.json"


TARGETS = ["Costco", "Amazon", "Wal-Mart", "Stagecoach", "Berkshire Hathaway"]


def period_year(value: str) -> int:
    for token in str(value).replace(",", "").split():
        if token.isdigit() and len(token) == 4:
            return int(token)
    if len(str(value)) >= 4 and str(value)[:4].isdigit():
        return int(str(value)[:4])
    return 0


def shorten(text: str, n: int = 260) -> str:
    text = " ".join(str(text).split())
    if len(text) <= n:
        return text
    return text[: n - 1].rsplit(" ", 1)[0] + "..."


def build() -> dict:
    data = json.loads(RAW_DATA.read_text())
    companies = {item["canonical_name"]: item for item in data["companies"]}

    seed_companies = []
    for name in TARGETS:
        company = companies[name]
        mentions = sorted(company["mentions"], key=lambda item: period_year(item.get("period_end", "")))
        years = [period_year(item.get("period_end", "")) for item in mentions if period_year(item.get("period_end", ""))]
        seed_companies.append(
            {
                "name": name,
                "ticker": company.get("ticker_if_known"),
                "sector": company.get("sector"),
                "mention_count": len(mentions),
                "first_mention_year": min(years) if years else None,
                "last_mention_year": max(years) if years else None,
                "nomad_thesis_seed": shorten(company.get("moat_summary", ""), 360),
                "first_context": shorten(mentions[0].get("context", ""), 340) if mentions else "",
            }
        )

    return {
        "title": "The Scale-Sharing Test",
        "subtitle": "Can Nomad's favorite kind of business be measured as customer value plus durable economics?",
        "research_question": (
            "Do companies that Nomad framed as sharing scale economies with customers show a measurable pattern of "
            "lower customer prices or better customer value, rising volume/revenue, and durable economics, without "
            "needing high near-term margins to make the investment work?"
        ),
        "why_this_maps_to_memory": [
            "The local Nomad dataset marks Consumer Value Proposition in 24/24 letters.",
            "Patience & Long-Term Horizon appears in 20/24 letters.",
            "The strongest recurring examples include Costco, Amazon, Wal-Mart, Stagecoach, and Berkshire Hathaway.",
            "The phrase 'scale-economics shared' appears in the Amazon/AirAsia/Costco context extracted from the letters.",
        ],
        "seed_companies": seed_companies,
        "hypotheses": [
            {
                "id": "H1",
                "claim": "Scale-sharing companies should show customer-value pressure before accounting quality is obvious.",
                "observable": "Category prices, retail sales/volume, revenue growth, membership/subscription or unit indicators.",
                "factiq_surfaces": ["BLS CPI/PPI", "Census retail", "company fundamentals", "earnings calls"],
            },
            {
                "id": "H2",
                "claim": "The market underprices these companies when growth spending suppresses near-term margins.",
                "observable": "Drawdowns, valuation multiples, revenue growth, operating margin path, earnings-call language.",
                "factiq_surfaces": ["market data", "fundamentals", "earnings-call search"],
            },
            {
                "id": "H3",
                "claim": "Patience matters most when rates and macro conditions make distant payoff harder to hold.",
                "observable": "Returns from first mention across rate/inflation regimes and drawdown/recovery windows.",
                "factiq_surfaces": ["market data", "BLS CPI", "BEA GDP/income", "rates/monetary-policy datasets"],
            },
        ],
        "factiq_repo_basis": [
            {
                "repo_file": "README.md",
                "used_for": "Confirmed FactIQ supports official statistics, market data, earnings-call intelligence, shareable charts, and reports.",
            },
            {
                "repo_file": "skills/factiq/SKILL.md",
                "used_for": "Confirmed workflow: catalog, dataset search, SQL, market data, earnings search, then chart/report publishing.",
            },
            {
                "repo_file": "references/schemas.md",
                "used_for": "Mapped likely schemas: BLS, Census, BEA, World Bank/IMF, and market/earnings tools.",
            },
            {
                "repo_file": "references/chart-spec.md + report-spec.md",
                "used_for": "Defined output as an evidence report with claim-titled charts and lineage.",
            },
        ],
        "factiq_questions": [
            {
                "question": "From first Nomad mention, did COST/AMZN/WMT outperform while fundamentals compounded?",
                "mode": "Detailed report",
                "tools": ["get_market_data", "search_earnings", "share_report"],
                "charts": ["indexed total return proxy", "revenue and operating margin path", "drawdown and recovery windows"],
            },
            {
                "question": "Did customer-facing price/value indicators move differently for retail/ecommerce categories?",
                "mode": "Bespoke local viz or report",
                "tools": ["search_datasets", "describe_dataset", "run_sql", "share_chart"],
                "charts": ["CPI/PPI retail category index", "Census retail sales", "company revenue overlay"],
            },
            {
                "question": "Does earnings-call language reveal the same tradeoff Nomad cared about: lower prices now, larger ecosystem later?",
                "mode": "Detailed report",
                "tools": ["search_earnings"],
                "charts": ["frequency of price/value/customer terms", "examples table by company and period"],
            },
        ],
        "starter_queries": [
            {
                "label": "Find CPI retail/category data in FactIQ",
                "tool": "search_datasets",
                "query": "CPI retail prices apparel food household ecommerce consumer goods",
            },
            {
                "label": "Find Census retail sales data",
                "tool": "search_datasets",
                "query": "retail sales ecommerce warehouse clubs department stores",
            },
            {
                "label": "Find company market and fundamentals data",
                "tool": "get_market_data",
                "query": "SYMBOL_SEARCH / OVERVIEW / INCOME_STATEMENT / EARNINGS for COST, AMZN, WMT",
            },
            {
                "label": "Search earnings calls for scale-sharing language",
                "tool": "search_earnings",
                "query": "price value customer savings scale efficiency membership flywheel",
            },
        ],
        "first_output": {
            "artifact": "FactIQ detailed report",
            "working_title": "Were Nomad's scale-sharing companies underpriced because margins were the wrong signal?",
            "sections": [
                "Nomad's seed thesis from the letters",
                "Market and fundamentals after first mention",
                "Customer-value indicators and category prices",
                "Earnings-call language: value, price, scale, and reinvestment",
                "What this supports, what remains interpretive",
            ],
        },
    }


def main() -> None:
    OUT.write_text(json.dumps(build(), indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
