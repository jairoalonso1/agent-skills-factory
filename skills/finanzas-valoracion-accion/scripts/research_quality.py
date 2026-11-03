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
    observations = package.get("data_observations")
    if observations is not None:
        if not isinstance(observations, list): issues.append("invalid:data_observations"); observations = []
        observation_ids = set()
        for idx, obs in enumerate(observations):
            if not isinstance(obs, dict): issues.append(f"observation[{idx}]:invalid:record"); continue
            for field in ("observation_id", "field", "unit", "evidence_type"):
                if not obs.get(field): issues.append(f"observation[{idx}]:missing:{field}")
            oid=obs.get("observation_id")
            if oid and oid in observation_ids: issues.append(f"observation[{idx}]:duplicate:observation_id")
            if oid: observation_ids.add(oid)
            et=obs.get("evidence_type")
            if et not in ALLOWED_EVIDENCE_TYPES: issues.append(f"observation[{idx}]:invalid:evidence_type")
            if et in {"reported","company_guidance","consensus","market_data"} and not obs.get("source_ids"): issues.append(f"observation[{idx}]:missing:source_ids")
            if et=="calculated" and (not obs.get("input_observation_ids") or not obs.get("transformation")): issues.append(f"observation[{idx}]:missing:calculation_lineage")
            if et=="analyst_assumption" and not obs.get("rationale"): issues.append(f"observation[{idx}]:missing:rationale")
        source_ids={x.get("source_id") for x in sources if isinstance(x,dict) and x.get("source_id")}
        for idx,obs in enumerate(observations):
            if not isinstance(obs,dict): continue
            for sid in obs.get("source_ids",[]):
                if sid not in source_ids: issues.append(f"observation[{idx}]:unresolved:source_id:{sid}")
            for parent in obs.get("input_observation_ids",[]):
                if parent==obs.get("observation_id") or parent not in observation_ids: issues.append(f"observation[{idx}]:unresolved:input_observation_id:{parent}")
    scenarios = package.get("scenarios", {})
    if not isinstance(scenarios, dict):
        issues.append("invalid:scenarios"); scenarios = {}
    for key in ("bear", "base", "bull"):
        if key not in scenarios: issues.append(f"missing:scenario:{key}")
    if all(k in scenarios for k in ("bear", "base", "bull")):
        vals = []
        allowed_statuses = {"estimated", "reported", "calculated", "not_available", "not_estimated", "not_applicable"}
        for key in ("bear", "base", "bull"):
            item = scenarios[key]
            if not isinstance(item, dict):
                issues.append(f"invalid:scenario:{key}"); vals.append(None); continue
            value = item.get("target_price")
            status = item.get("status", "estimated" if value is not None else None)
            if status not in allowed_statuses:
                issues.append(f"invalid:scenario_status:{key}")
            if value is None:
                if status not in {"not_available", "not_estimated", "not_applicable"}:
                    issues.append(f"missing:scenario_target_price:{key}")
                vals.append(None)
            elif not isinstance(value, (int, float)) or not isfinite(value) or value <= 0:
                issues.append(f"invalid:scenario_target_price:{key}"); vals.append(None)
            else:
                vals.append(float(value))
        numeric_values = [value for value in vals if value is not None]
        if len(numeric_values) == 3 and not vals[0] <= vals[1] <= vals[2]:
            issues.append("invalid:scenario_order")
    warnings=[]
    if "data_observations" not in package: warnings.append("missing:data_observations_ledger")
    fin=package.get("financials",{})
    if isinstance(fin,dict) and fin.get("roic") is not None and not package.get("roic_definition"): warnings.append("missing:roic_methodology_definition")
    return {"passed": not issues, "issues": issues, "warnings": warnings,
            "disclaimer": "Automated structural checks do not replace analyst review, source verification or model validation."}
