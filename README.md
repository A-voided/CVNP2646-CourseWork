## Denied or Rejected Changes

Throughout the development of this project, some AI-generated or suggested changes were reviewed and intentionally not accepted, including:

- Proposals to add unnecessary complexity to the directory structure (e.g., splitting code into multiple submodules when a single script was sufficient for the project scope).
- Suggestions to add advanced dependency management or CI/CD configuration, which were deemed out of scope for this assignment.
- Automated formatting or refactoring that would have reduced code readability or conflicted with the user’s preferred style.
- Any changes that would have made the tool less accessible to new users or complicated the setup process.

All denied changes were reviewed and rejected by the project author to ensure the final implementation remained clear, maintainable, and aligned with the project’s goals and requirements.

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
If you have a requirements.txt file, install all dependencies with:
```
pip install -r requirements.txt
```
Or, to install pytest only:
```
pip install pytest
```


### 4. Prepare Input Files
Make sure these files are in the project directory:
- `asset_inventory.json`
- `cve_feed.json`
- `threat_intel.json`

Sample data is already provided. You can edit or expand these files as needed.


### 5. Run the Tool
From the project directory, run:
```
python vulnerablity_prioritizer.py --assets asset_inventory.json --cves cve_feed.json --threats threat_intel.json --output outputs/priority_list.json
```

- This will generate:
  - `outputs/priority_list.json` (detailed, technical output)
  - `outputs/manager_output.txt` (plain-language management summary)


### 6. Run the Tests
To verify the tool works as expected, run:
```
python -m pytest tests
```
All tests should pass. If not, check your Python version and dependencies.


## Project Structure
```
Capstone_week_15/
├── outputs/
│   ├── priority_list.json
│   └── manager_output.txt
├── tests/
│   ├── __init__.py
│   ├── test_vulnerablity_prioritizer.py
│   └── test_integration_pipeline.py
├── AI_USAGE.md
├── asset_inventory.json
├── cve_feed.json
│── README.md
├── AI_USAGE.md
├── threat_intel.json
├── vulnerablity_prioritizer.py
```

## File Descriptions
- `vulnerablity_prioritizer.py`: Main script for analysis and reporting
- `asset_inventory.json`: List of assets, their software, and criticality
- `cve_feed.json`: List of CVEs with details and affected software
- `threat_intel.json`: List of actively exploited CVEs
- `outputs/priority_list.json`: Output file with prioritized vulnerabilities
- `outputs/manager_output.txt`: Management summary report
- `tests/`: Directory containing automated tests


## Troubleshooting
- If you see errors about missing files, ensure your input JSON files are present and valid.
- If you see `pip` or `pytest` not found, ensure Python and pip are installed and in your PATH.
- Output files will be found in the outputs/ directory after running the tool.
- For any issues, check the log output in your terminal for details.

## Contact
For questions or improvements, please contact the project maintainer.

all information on this readme was verfied for functionality and authenticty by Me James Goebel