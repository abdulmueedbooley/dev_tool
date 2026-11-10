# test_scoring.py
from datetime import datetime, timedelta, timezone
from scoring import score_package


def test_healthy_pack():
    recent_date = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()

    mock_info = {
        "name" : "fastlib",
        "last_release" : recent_date,
        "license" : "MIT"
    }

    result = score_package(mock_info, "saas",vul=0)

    assert result["name"] == "fastlib"
    assert result["grade"] == "A"
    assert result["license_risk"] == "Low"
    assert result["score"] >= 90

def test_abandoned_pack():
    recent_date  = (datetime.now(timezone.utc) - timedelta(days=1000)).isoformat()

    mock_info = {
        "name" : "oldlib",
        "last_release" : recent_date,
        "license" : "MIT"
    }

    result = score_package(mock_info, "saas",vul=0)

    assert result["name"] == "oldlib"
    assert result["grade"] == "D"
    assert result["license_risk"] == "Low"
    assert result["score"] <= 40

def test_license_risk():
    recent_date = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()

    mock_info  = {
        "name" : "tinytool",
        "last_release" : recent_date,
        "license" : "AGPL"
    }

    result = score_package(mock_info, "saas",vul=0)

    assert result["name"] == "tinytool"
    assert result["grade"] == "A"
    assert result["license_risk"] == "High"
    assert result["score"] >= 90

    