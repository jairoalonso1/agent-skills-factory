"""Structural evidence, source-freshness and acceptance checks."""
from __future__ import annotations
from datetime import date, datetime
from math import isfinite
from typing import Any

ALLOWED_EVIDENCE_TYPES = {"reported", "company_guidance", "consensus", "analyst_assumption", "calculated", "market_data"}


def _iso_date(value: Any) -> bool:
    if not isinstance(value, str): return False
    try: date.fromisoformat(value); return True
    except ValueError: return False


def _iso_datetime(value: Any) -> bool:
    if not isinstance(value, str): return False
    try: datetime.fromisoformat(value.replace("Z", "+00:00")); return True
    except ValueError: return False


def validate_source_record(source: dict[str, Any]) -> list[str]:
    issues = []
    for field in ("source_id", "publisher", "title", "url", "published_at", "retrieved_at"):
        if not source.get(field): issues.append(f"missing:{field}")
    if source.get("evidence_type") not in ALLOWED_EVIDENCE_TYPES: issues.append("invalid:evidence_type")
    if source.get("url") and not str(source["url"]).startswith(("https://", "http://")): issues.append("invalid:url")
    if source.get("published_at") and not (_iso_date(source["published_at"]) or _iso_datetime(source["published_at"])): issues.append("invalid:published_at")
    if source.get("retrieved_at") and not _iso_datetime(source["retrieved_at"]): issues.append("invalid:retrieved_at")
    return issues


def validate_research_package(package: dict[str, Any]) -> dict[str, Any]:
    """Report structural issues; never auto-certifies research quality."""
    issues: list[str] = []
    required = ("issuer", "valuation_date", "reporting_currency", "financials", "valuation", "scenarios", "risks", "sources")
    for key in required:
        if package.get(key) in (None, "", [], {}): issues.append(f"missing:{key}")
    if package.get("valuation_date") and not _iso_date(package["valuation_date"]): issues.append("invalid:valuation_date")
    currency = package.get("reporting_currency")
    if currency and (not isinstance(currency, str) or len(currency) != 3 or not currency.isalpha() or currency.upper() != currency):
        issues.append("invalid:reporting_currency")
    price = package.get("current_price")
    if price is not None and (not isinstance(price, (int, float)) or not isfinite(price) or price <= 0):
        issues.append("invalid:current_price")
    sources = package.get("sources", [])
    if not isinstance(sources, list):
        issues.append("invalid:sources")
        sources = []
    if not sources: issues.append("missing:evidence_sources")
    seen_ids = set()
    for idx, source in enumerate(sources):
        if not isinstance(source, dict):
            issues.append(f"source[{idx}]:invalid:record")
            continue
        issues.extend(f"source[{idx}]:{x}" for x in validate_source_record(source))
        source_id = source.get("source_id")
        if source_id and source_id in seen_ids: issues.append(f"source[{idx}]:duplicate:source_id")
        if source_id: seen_ids.add(source_id)
    scenarios = package.get("scenarios", {})
    if not isinstance(scenarios, dict):
        issues.append("invalid:scenarios"); scenarios = {}
    for key in ("bear", "base", "bull"):
        if key not in scenarios: issues.append(f"missing:scenario:{key}")
    if all(k in scenarios for k in ("bear", "base", "bull")):
        vals = [scenarios[k].get("target_price") if isinstance(scenarios[k], dict) else None for k in ("bear", "base", "bull")]
        if any(not isinstance(v, (int, float)) or not isfinite(v) for v in vals): issues.append("invalid:scenario_target_price")
        elif not vals[0] <= vals[1] <= vals[2]: issues.append("invalid:scenario_order")
    return {"passed": not issues, "issues": issues,
            "disclaimer": "Automated structural checks do not replace analyst review, source verification or model validation."}
