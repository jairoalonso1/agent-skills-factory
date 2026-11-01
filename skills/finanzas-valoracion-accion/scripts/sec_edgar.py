"""Minimal SEC Company Facts client with configurable identification and PIT filtering.

This module retrieves raw SEC XBRL facts. It is not a universal financial-statement
normalizer: taxonomy mapping, issuer-specific tags and quarterly derivations require
separate reviewed logic.
"""
from __future__ import annotations
import json
import os
import time
import urllib.error
import urllib.request
from typing import Any

SEC_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"


def fetch_sec_company_facts(cik: str, user_agent: str | None = None,
                            timeout: float = 30.0, retries: int = 2) -> dict[str, Any]:
    ua = user_agent or os.environ.get("SEC_USER_AGENT")
    if not ua or len(ua.strip()) < 10 or "@" not in ua:
        raise ValueError("Set SEC_USER_AGENT to a truthful application name and monitored contact email")
    raw_cik = str(cik).strip()
    if not raw_cik.isdigit() or not 1 <= len(raw_cik) <= 10: raise ValueError("CIK must contain 1 to 10 digits")
    if timeout <= 0 or retries < 0: raise ValueError("timeout must be positive and retries cannot be negative")
    cik_digits = raw_cik
    url = SEC_FACTS_URL.format(cik=cik_digits.zfill(10))
    request = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "application/json"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt >= retries: raise
        except (urllib.error.URLError, TimeoutError):
            if attempt >= retries: raise
        time.sleep(min(2 ** attempt, 8))
    raise RuntimeError("SEC request failed after retries")


def extract_company_fact(company_facts: dict[str, Any], taxonomy: str, tag: str,
                         unit: str, as_of_date: str, forms: tuple[str, ...] = ("10-K", "10-Q")) -> list[dict[str, Any]]:
    """Return reported observations filed on/before as_of_date, retaining provenance.

    Values are raw XBRL observations; duration/instant semantics are preserved.
    No quarterly flow derivation or cross-tag normalization is performed.
    """
    from datetime import date
    try: date.fromisoformat(as_of_date)
    except ValueError as exc: raise ValueError("as_of_date must be YYYY-MM-DD") from exc
    try: observations = company_facts["facts"][taxonomy][tag]["units"][unit]
    except KeyError as exc: raise KeyError(f"SEC fact not found: {taxonomy}.{tag} [{unit}]") from exc
    rows = []
    for item in observations:
        filed = item.get("filed")
        if not filed or filed > as_of_date or item.get("form") not in forms: continue
        rows.append({k: item.get(k) for k in ("fy", "fp", "form", "filed", "start", "end", "val", "accn", "frame")})
    return sorted(rows, key=lambda x: (x.get("end") or "", x.get("filed") or "", x.get("accn") or ""))
