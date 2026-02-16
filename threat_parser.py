import json

json_path = "week 4/threats.json"

with open(json_path, "r") as f:
    data = json.load(f)

threats = data.get("threats", [])

severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
for threat in threats:
    sev = threat.get("severity", "").capitalize()
    if sev in severity_counts:
        severity_counts[sev] += 1

malicious_ips = []
for threat in threats:
    ips = threat.get("indicators", {}).get("ips", [])
    malicious_ips.extend(ips)

active_exploit_threats = [t for t in threats if t.get("active_exploit") is True]

total_threats = len(threats)
critical_count = severity_counts["Critical"]
critical_percentage = (critical_count / total_threats * 100) if total_threats else 0

print("Threats by severity:", severity_counts)
print("Malicious IPs:", malicious_ips)
print("Active Exploit Threats:")
for t in active_exploit_threats:
    print(f"- {t['id']}: {t['description']}")
print(f"Percentage of Critical threats: {critical_percentage:.2f}%")