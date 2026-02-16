import json

def generate_report(data, filename="scan_data.json"):
	with open(filename, "w") as f:
		json.dump(data, f, indent=4)
