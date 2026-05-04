
import pytest
from vulnerablity_prioritizer import risk_score, load_json, Asset, CVE, VulnerabilityMatch

def match_assets_to_cves(assets, cves):
    matches = []
    for asset in assets:
        for cve in cves:
            if any(soft in asset.software for soft in cve.affected_software):
                matches.append((asset, cve))
    return matches

def score_vulnerabilities(matches, exploited_cves):
    scored = []
    for asset, cve in matches:
        exploited = cve.cve_id in exploited_cves
        score = risk_score(cve.cvss_score, asset.criticality, exploited)
        scored.append(VulnerabilityMatch(asset, cve, score))
    return scored

def test_match_assets_to_cves_typical():
    asset = Asset("A1", "host1", ["nginx"], "high")
    cve = CVE("CVE-1", "desc", 9.0, ["nginx"], "2024-01-01")
    matches = match_assets_to_cves([asset], [cve])
    assert len(matches) == 1
    assert matches[0][0] == asset
    assert matches[0][1] == cve

def test_score_vulnerabilities_exploited():
    asset = Asset("A2", "host2", ["openssl"], "medium")
    cve = CVE("CVE-2", "desc", 7.5, ["openssl"], "2024-01-01")
    matches = match_assets_to_cves([asset], [cve])
    exploited_cves = {"CVE-2"}
    scored = score_vulnerabilities(matches, exploited_cves)
    assert len(scored) == 1
    assert scored[0].risk_score == 15.0

def test_match_assets_to_cves_no_match():
    asset = Asset("A3", "host3", ["apache"], "medium")
    cve = CVE("CVE-3", "desc", 8.0, ["nginx"], "2024-01-01")
    matches = match_assets_to_cves([asset], [cve])
    assert matches == []

def test_match_assets_to_cves_empty_assets():
    assets = []
    cves = [CVE("CVE-4", "desc", 7.0, ["nginx"], "2024-01-01")]
    matches = match_assets_to_cves(assets, cves)
    assert matches == []

def test_risk_score_normal():
    assert risk_score(9.0, 'critical', True) == 9.0 * 2 * 2
    assert risk_score(5.0, 'medium', False) == 5.0 * 1 * 1

def test_risk_score_edge():
    assert risk_score(10.0, 'unknown', False) == 10.0 * 1 * 1
    assert risk_score(0.0, 'critical', True) == 0.0

def test_load_json_valid(tmp_path):
    file = tmp_path / "test.json"
    file.write_text('{"a": 1}')
    data = load_json(str(file))
    assert data == {"a": 1}

def test_load_json_invalid(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text('{bad json}')
    data = load_json(str(file))
    assert data is None

def test_load_json_missing():
    data = load_json("nonexistent.json")
    assert data is None
