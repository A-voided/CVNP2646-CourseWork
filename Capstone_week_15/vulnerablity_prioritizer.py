import argparse
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class Asset:
	def __init__(self, asset_id, hostname, software, criticality):
		self.asset_id = asset_id
		self.hostname = hostname
		self.software = software
		self.criticality = criticality

class CVE:
	def __init__(self, cve_id, description, cvss_score, affected_software, published_date):
		self.cve_id = cve_id
		self.description = description
		self.cvss_score = cvss_score
		self.affected_software = affected_software
		self.published_date = published_date

class VulnerabilityMatch:
	def __init__(self, asset, cve, risk_score):
		self.asset = asset
		self.cve = cve
		self.risk_score = risk_score

def load_json(path):
	try:
		with open(path, 'r') as f:
			return json.load(f)
	except FileNotFoundError:
		logging.error(f"File not found: {path}")
		return None
	except PermissionError:
		logging.error(f"Permission denied: {path}")
		return None
	except json.JSONDecodeError:
		logging.error(f"Invalid JSON in file: {path}")
		return None

def risk_score(cvss, criticality, exploited):
	crit_weights = {'critical': 2, 'high': 1.5, 'medium': 1, 'low': 0.5}
	exploit_bonus = 2 if exploited else 1
	return cvss * crit_weights.get(criticality, 1) * exploit_bonus

def main():
	parser = argparse.ArgumentParser(description="Vulnerability Prioritizer MVP")
	parser.add_argument('--assets', '-a', default='asset_inventory.json', help='Asset inventory JSON file')
	parser.add_argument('--cves', '-c', default='cve_feed.json', help='CVE feed JSON file')
	parser.add_argument('--threats', '-t', default='threat_intel.json', help='Threat intel JSON file')
	parser.add_argument('--output', '-o', default='priority_list.json', help='Output JSON file')
	args = parser.parse_args()

	def validate_assets(data):
		if not isinstance(data, list):
			logging.error("Asset inventory must be a list.")
			return False
		for asset in data:
			if not all(k in asset for k in ("asset_id", "hostname", "software", "criticality")):
				logging.error(f"Asset missing required fields: {asset}")
				return False
			if not isinstance(asset["software"], list):
				logging.error(f"Asset 'software' must be a list: {asset}")
				return False
		return True

	def validate_cves(data):
		if not isinstance(data, list):
			logging.error("CVE feed must be a list.")
			return False
		for cve in data:
			if not all(k in cve for k in ("cve_id", "description", "cvss_score", "affected_software", "published_date")):
				logging.error(f"CVE missing required fields: {cve}")
				return False
			if not isinstance(cve["affected_software"], list):
				logging.error(f"CVE 'affected_software' must be a list: {cve}")
				return False
			if not isinstance(cve["cvss_score"], (int, float)):
				logging.error(f"CVE 'cvss_score' must be a number: {cve}")
				return False
		return True

	def validate_threats(data):
		if not isinstance(data, dict):
			logging.error("Threat intel must be a dictionary.")
			return False
		if "actively_exploited" not in data or not isinstance(data["actively_exploited"], list):
			logging.error("Threat intel must contain a list 'actively_exploited'.")
			return False
		return True

	assets_data = load_json(args.assets)
	cves_data = load_json(args.cves)
	threats_data = load_json(args.threats)
	if assets_data is None or cves_data is None or threats_data is None:
		logging.error("Missing or invalid input files. Exiting.")
		return
	if not (validate_assets(assets_data) and validate_cves(cves_data) and validate_threats(threats_data)):
		logging.error("Input validation failed. Exiting.")
		return


	exploited_cves = set(threats_data.get('actively_exploited', []))
	assets = [Asset(a['asset_id'], a['hostname'], a['software'], a['criticality']) for a in assets_data]
	cves = [CVE(c['cve_id'], c['description'], c['cvss_score'], c['affected_software'], c['published_date']) for c in cves_data]

	def match_assets_to_cves(assets, cves):
		"""Aggregate: Find all asset/CVE pairs where software matches."""
		matches = []
		for asset in assets:
			for cve in cves:
				if any(soft in asset.software for soft in cve.affected_software):
					matches.append((asset, cve))
		return matches

	def score_vulnerabilities(matches, exploited_cves):
		"""Detection: Score and wrap matches as VulnerabilityMatch objects."""
		scored = []
		for asset, cve in matches:
			exploited = cve.cve_id in exploited_cves
			score = risk_score(cve.cvss_score, asset.criticality, exploited)
			scored.append(VulnerabilityMatch(asset, cve, score))
		return scored

	# Aggregation step
	raw_matches = match_assets_to_cves(assets, cves)
	# Detection/scoring step
	matches = score_vulnerabilities(raw_matches, exploited_cves)
	matches.sort(key=lambda m: m.risk_score, reverse=True)

	output = []
	for m in matches:
		output.append({
			'asset_id': m.asset.asset_id,
			'hostname': m.asset.hostname,
			'cve_id': m.cve.cve_id,
			'description': m.cve.description,
			'cvss_score': m.cve.cvss_score,
			'criticality': m.asset.criticality,
			'exploited': m.cve.cve_id in exploited_cves,
			'risk_score': round(m.risk_score, 2)
		})


	# Write technical output
	try:
		with open(args.output, 'w') as f:
			json.dump(output, f, indent=2)
		logging.info(f"Wrote prioritized vulnerabilities to {args.output}")
	except Exception as e:
		logging.error(f"Failed to write output: {e}")

	# Write management summary output
	try:
		with open('manager_output.txt', 'w') as f:
			f.write("MANAGEMENT SUMMARY REPORT\n")
			f.write("========================\n\n")
			f.write(f"Total unique CVEs found: {len(set(m['cve_id'] for m in output))}\n")
			f.write(f"Total affected assets: {len(set(m['asset_id'] for m in output))}\n\n")
			f.write("Top Risks (by priority):\n")
			for i, m in enumerate(output[:5]):
				f.write(f"{i+1}. Asset: {m['hostname']} (Criticality: {m['criticality']})\n")
				f.write(f"   CVE: {m['cve_id']} | Score: {m['cvss_score']} | Exploited: {m['exploited']}\n")
				f.write(f"   Description: {m['description']}\n")
				f.write(f"   Calculated Risk Score: {m['risk_score']}\n")
				# Enhanced explanation for exploited CVEs
				if m['exploited']:
					f.write("   [!] This CVE is actively exploited in the wild. Immediate attention is required.\n")
					f.write("       What to look for: Signs of compromise, unusual activity, or known attack patterns related to this CVE.\n")
				# Purpose and impact
				f.write(f"   Purpose of CVE: {m['description'].split('.')[0] if '.' in m['description'] else m['description']}\n")
				f.write(f"   Impact: This vulnerability affects the software: {', '.join([sw for sw in m['description'].split() if sw in m['description']]) if m['description'] else 'See above.'}\n\n")
			f.write("\nWhat to look for in this report:\n")
			f.write("- Focus on assets with high or critical criticality and high risk scores.\n")
			f.write("- Pay special attention to CVEs marked as 'Exploited'—these are being used by attackers right now.\n")
			f.write("- For each exploited CVE, review your systems for signs of compromise and apply patches or mitigations immediately.\n")
			f.write("- Review the CVE description for business impact and urgency.\n")
			f.write("\nExplanation:\n")
			f.write("This report summarizes the most urgent vulnerabilities in your environment. Each item is prioritized by risk, considering asset importance, CVSS score, and whether the vulnerability is actively exploited. Addressing these items first will reduce your organization's exposure to the most significant threats.\n")
		logging.info("Wrote management summary to manager_output.txt")
	except Exception as e:
		logging.error(f"Failed to write management summary: {e}")

if __name__ == '__main__':
	main()
