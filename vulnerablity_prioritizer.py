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

	assets_data = load_json(args.assets)
	cves_data = load_json(args.cves)
	threats_data = load_json(args.threats)
	if assets_data is None or cves_data is None or threats_data is None:
		logging.error("Missing or invalid input files. Exiting.")
		return

	exploited_cves = set(threats_data.get('actively_exploited', []))

	assets = [Asset(a['asset_id'], a['hostname'], a['software'], a['criticality']) for a in assets_data]

	cves = [CVE(c['cve_id'], c['description'], c['cvss_score'], c['affected_software'], c['published_date']) for c in cves_data]

	# match and score
	matches = []
	for asset in assets:
		for cve in cves:
			if any(soft in asset.software for soft in cve.affected_software):
				exploited = cve.cve_id in exploited_cves
				score = risk_score(cve.cvss_score, asset.criticality, exploited)
				matches.append(VulnerabilityMatch(asset, cve, score))

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

	try:
		with open(args.output, 'w') as f:
			json.dump(output, f, indent=2)
		logging.info(f"Wrote prioritized vulnerabilities to {args.output}")
	except Exception as e:
		logging.error(f"Failed to write output: {e}")

if __name__ == '__main__':
	main()
