# test_scoring.py
from datetime import datetime, timedelta, timezone
from scoring import score_package


def months_ago(n):
    """Build a PyPI-style date string for n months ago."""
    date = datetime.now(timezone.utc) - timedelta(days=30 * n)
    return date.isoformat()


def test_healthy_package():
    facts = {"name": "fastlib", "license": "MIT", "last_release": months_ago(1)}
    result = score_package(facts, "saas")
    assert result["score"] == 100
    assert result["grade"] == "A"
    assert result["licence_risk"] == "Low"


def test_abandoned_package():
    facts = {"name": "oldlib", "license": "MIT", "last_release": months_ago(26)}
    result = score_package(facts, "saas")
    assert result["score"] == 40
    assert result["grade"] == "D"
    assert "26 months" in result["reason"]


def test_agpl_in_saas_is_high_risk():
    facts = {"name": "tinytool", "license": "AGPL-3.0", "last_release": months_ago(3)}
    result = score_package(facts, "saas")
    assert result["licence_risk"] == "High"


def test_agpl_internal_is_low_risk():
    facts = {"name": "tinytool", "license": "AGPL-3.0", "last_release": months_ago(3)}
    result = score_package(facts, "internal")
    assert result["licence_risk"] == "Low"