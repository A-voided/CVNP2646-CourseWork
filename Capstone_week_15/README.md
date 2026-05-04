
# Vulnerability Prioritizer

## Overview
This tool analyzes asset, vulnerability (CVE), and threat intelligence data to produce a prioritized list of vulnerabilities and a management summary report. It helps organizations focus on the most urgent security risks.

## Quick Start

### 1. Clone the Repository
Clone or download this project folder to your local machine.

### 2. Install Python
Ensure you have Python 3.7 or newer installed. You can check with:
```
python --version
```

### 3. Install Dependencies
Install pytest for running tests:
```
pip install pytest
```

### 4. Prepare Input Files
Make sure these files are in the same directory as the script:
- `asset_inventory.json`
- `cve_feed.json`
- `threat_intel.json`

Sample data is already provided. You can edit or expand these files as needed.

### 5. Run the Tool
From the project directory, run:
```
python vulnerablity_prioritizer.py --assets asset_inventory.json --cves cve_feed.json --threats threat_intel.json --output priority_list.json
```

- This will generate:
  - `priority_list.json` (detailed, technical output)
  - `manager_output.txt` (plain-language management summary)

### 6. Run the Tests
To verify the tool works as expected, run:
```
python -m pytest tests
```

All tests should pass. If not, check your Python version and dependencies.

## File Descriptions
- `vulnerablity_prioritizer.py`: Main script for analysis and reporting
- `asset_inventory.json`: List of assets, their software, and criticality
- `cve_feed.json`: List of CVEs with details and affected software
- `threat_intel.json`: List of actively exploited CVEs
- `priority_list.json`: Output file with prioritized vulnerabilities
- `manager_output.txt`: Management summary report
- `tests/`: Directory containing automated tests

## Troubleshooting
- If you see errors about missing files, ensure your input JSON files are present and valid.
- If you see `pip` or `pytest` not found, ensure Python and pip are installed and in your PATH.
- For any issues, check the log output in your terminal for details.

## Contact
For questions or improvements, please contact the project maintainer.
