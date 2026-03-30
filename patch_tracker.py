# patch_tracker.py
# Clean, management-friendly Patch Tracker
import json
import os
from datetime import datetime

def load_inventory(filepath):
    """Load JSON, return list of host dicts."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_days_since_patch(host):
    """Parse date, calculate days."""
    last_patch_date = host.get('last_patch_date')
    if not last_patch_date:
        return None
    try:
        patch_date = datetime.strptime(last_patch_date, '%Y-%m-%d').date()
        return (datetime.now().date() - patch_date).days
    except Exception:
        return None

def filter_by_os(hosts, os_type):
    """Filter by OS (partial match)."""
    return [h for h in hosts if 'os' in h and os_type.lower() in h['os'].lower()]

def filter_by_criticality(hosts, level):
    """Filter by criticality."""
    return [h for h in hosts if h.get('criticality', '').lower() == level.lower()]

def filter_by_environment(hosts, env):
    """Filter by environment."""
    return [h for h in hosts if h.get('environment', '').lower() == env.lower()]

def calculate_risk_score(host):
    """Multi-factor scoring (0-100)."""
    patch_age = host.get('days_since_patch', 0)
    missing_patches = len(host.get('missing_patches', []))
    score = 0
    if patch_age is not None:
        if patch_age > 90:
            score += 50
        elif patch_age > 30:
            score += 35
        elif patch_age > 7:
            score += 20
        else:
            score += 5
    score += min(missing_patches * 10, 40)
    crit_map = {"low": 0, "medium": 3, "high": 7, "critical": 10}
    score += crit_map.get(host.get("criticality", "low"), 0)
    return min(score, 100)

def get_risk_level(score):
    """Convert score to level string."""
    if score >= 70:
        return "critical"
    elif score >= 50:
        return "high"
    elif score >= 25:
        return "medium"
    else:
        return "low"

def get_high_risk_hosts(hosts, threshold=50):
    """Filter and sort."""
    high_risk = [h for h in hosts if h.get('risk_score', 0) >= threshold]
    return sorted(high_risk, key=lambda h: h['risk_score'], reverse=True)

def cis_recommendation(days_since_patch):
    """Provide CIS Control 7 recommendation based on patch age."""
    if days_since_patch is None:
        return "Patch age unknown. Review immediately."
    if days_since_patch > 30:
        return "Patch immediately (overdue per CIS Control 7)."
    elif days_since_patch > 14:
        return "Patch soon (approaching CIS Control 7 deadline)."
    else:
        return "Compliant with CIS Control 7."

def analyze_inventory(hosts):
    """Main pipeline."""
    for host in hosts:
        host['days_since_patch'] = calculate_days_since_patch(host)
        host['risk_score'] = calculate_risk_score(host)
        host['risk_level'] = get_risk_level(host['risk_score'])
        host['cis_recommendation'] = cis_recommendation(host['days_since_patch'])
    high_risk_hosts = get_high_risk_hosts(hosts)
    return hosts, high_risk_hosts

def generate_json_report(high_risk_hosts, out_high='high_risk_report.json'):
    """JSON output for high-risk hosts only."""
    with open(out_high, 'w', encoding='utf-8') as f:
        json.dump(high_risk_hosts, f, indent=2)

def generate_text_summary(high_risk_hosts, out_high='patch_summary.txt'):
    """Management-friendly text summary for high-risk hosts."""
    if not high_risk_hosts:
        summary = "Patch Management Summary Report\nDate: {}\n\nNo high-risk hosts identified.\n".format(datetime.now().strftime('%Y-%m-%d'))
        with open(out_high, 'w', encoding='utf-8') as f:
            f.write(summary)
        return
    avg_score = sum(h['risk_score'] for h in high_risk_hosts) / len(high_risk_hosts)
    summary = [
        "Patch Management Summary Report",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        f"\nHigh-Risk Hosts Identified: {len(high_risk_hosts)}",
        f"Average Risk Score: {round(avg_score)}",
        "\n------------------------------------------------------------"
    ]
    for host in high_risk_hosts:
        summary.append(f"Host: {host.get('hostname', 'unknown')}")
        summary.append(f"  - Operating System: {host.get('os', 'N/A')}")
        summary.append(f"  - Risk Score: {host.get('risk_score', 'N/A')} ({host.get('risk_level', 'N/A').capitalize()})")
        summary.append(f"  - Days Since Last Patch: {host.get('days_since_patch', 'N/A')}")
        summary.append(f"  - Missing Patches: {', '.join(host.get('missing_patches', [])) or 'None'}")
        summary.append(f"  - Recommendation: {host.get('cis_recommendation', '')}")
        summary.append("")
    summary.append("------------------------------------------------------------")
    summary.append("Key:")
    summary.append("- 'Risk Score' is on a 0-100 scale (Critical: 70+, High: 50-69, Medium: 25-49, Low: <25).")
    summary.append("- 'Days Since Last Patch' shows how long the system has gone without updates.")
    summary.append("- 'Recommendation' is based on CIS Control 7 patch timelines.\n")
    with open(out_high, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary))



if __name__ == "__main__":
    inventory_path = os.path.join(os.path.dirname(__file__), 'host_inventory.json')
    hosts = load_inventory(inventory_path)
    hosts, high_risk_hosts = analyze_inventory(hosts)
    generate_json_report(high_risk_hosts)
    generate_text_summary(high_risk_hosts)
