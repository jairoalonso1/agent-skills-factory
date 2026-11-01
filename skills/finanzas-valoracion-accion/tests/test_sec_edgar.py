import json
import pytest
from scripts.sec_edgar import extract_company_fact, fetch_sec_company_facts


def test_company_fact_filter_uses_filed_date_and_keeps_accession():
    data={"facts":{"us-gaap":{"Revenues":{"units":{"USD":[
      {"form":"10-K","filed":"2025-02-01","end":"2024-12-31","val":100,"accn":"a"},
      {"form":"10-K","filed":"2026-02-01","end":"2024-12-31","val":90,"accn":"b"},
      {"form":"8-K","filed":"2025-01-01","end":"2024-12-31","val":110,"accn":"c"}
    ]}}}}}
    rows=extract_company_fact(data,"us-gaap","Revenues","USD","2025-12-31")
    assert len(rows)==1 and rows[0]["accn"]=="a" and rows[0]["val"]==100


def test_sec_requires_truthful_configured_user_agent():
    with pytest.raises(ValueError, match="SEC_USER_AGENT"):
        fetch_sec_company_facts("0000320193", user_agent=None)


def test_sec_rejects_malformed_cik_and_date():
    with pytest.raises(ValueError, match="CIK"):
        fetch_sec_company_facts("abc123", user_agent="Research App contact@example.com")
    with pytest.raises(ValueError, match="as_of_date"):
        extract_company_fact({"facts":{}}, "us-gaap", "Revenues", "USD", "bad-date")
