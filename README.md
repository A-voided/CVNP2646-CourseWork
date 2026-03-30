README!!!!!!!!!!

OVERVIEW
________________________________________________________
This patch_tracker.py parses host data logs in a JSON format and gives you a comprehensive breakdown detailed with everything you need to know, including 3 forms of output, one of which is a .txt with a key on how to read the information on it. Patch management is important for the fact of needing to make sure your devices are up to date and secure. Devices that fall behind on updates are susceptible to easy exploitation, which in high security environments is very unacceptable.

USAGE
___________________________________________________________
HOW TO USE THIS SCRIPT !!!!! LOOK HERE !!!!!!!!!!!!!!!!!!!!!!!@@@@@@@@@@@@@HEREEEEEEEEEE
In a Python terminal, navigate to the directory of patch_tracker.py.
Once you CD there, enter: python patch_tracker.py
It will output accordingly.
Change the data in host_inventory.json if you need.

Risk Scoring Algorithm 
_______________________________________________
How this functions is it starts at 0, then from there it adds points based on the amount of days passed: 90 = 50 points, 30 = 35 points, 7 or more = 20 points, 7 or less = 5 points. It adds 10 points for each missed patch to a max of 40 and also adds extra points based on the host's criticality: low 0, mid 3, high 7, critical 10. Total is maxed at 100 and this is used to assign a risk level for each host as well.


CIS BENCHMARK ALIGNMENT
______________________________________________
The way I implemented this in my script is it checks how many days have passed since last patch and provides a recommendation accordingly. If the patch is 14 days or less it says compliant with CIS Control 7. If it's unknown it says immediate review. If it's between 15 and 30 days it says patch soon. If it's over 30 it's a patch immediately.

SAMPLE OUTPUTS 
_______________________________________________
High RISK Report json 
  {
    "hostname": "WEB-SRV-001",
    "ip_address": "10.20.10.11",
    "os": "Ubuntu 22.04 LTS",
    "os_version": "22.04.3",
    "last_patch_date": "2024-04-22",
    "criticality": "critical",
    "environment": "production",
    "department": "Engineering",
    "owner": "devops@company.com",
    "tags": [
      "internet-facing",
      "pci-scope"
    ],
    "days_since_patch": 706,
    "risk_score": 60,
    "risk_level": "high",
    "cis_recommendation": "Patch immediately (overdue per CIS Control 7)."
  },
  {
    "hostname": "WEB-SRV-002",
    "ip_address": "10.20.10.12",
    "os": "Ubuntu 22.04 LTS",
    "os_version": "22.04.3",
    "last_patch_date": "2024-09-30",
    "criticality": "critical",
    "environment": "production",
    "department": "Engineering",
    "owner": "devops@company.com",
    "tags": [
      "internet-facing"
    ],
    "days_since_patch": 545,
    "risk_score": 60,
    "risk_level": "high",
    "cis_recommendation": "Patch immediately (overdue per CIS Control 7)."
  },
  
    "hostname": "DB-SRV-001",
    "ip_address": "10.20.20.11",
    "os": "Ubuntu 22.04 LTS",
    "os_version": "22.04.3",
    "last_patch_date": "2024-07-18",
    "criticality": "critical",
    "environment": "production",
    "department": "Engineering",
    "owner": "dba@company.com",
    "tags": [
      "pci-scope",
      "hipaa"
    ],
    "days_since_patch": 619,
    "risk_score": 60,
    "risk_level": "high",
    "cis_recommendation": "Patch immediately (overdue per CIS Control 7)."
    Patch Summary txt atch Management Summary Report
Date: 2026-03-29

High-Risk Hosts Identified: 20
Average Risk Score: 56

------------------------------------------------------------
Host: WEB-SRV-001
  - Operating System: Ubuntu 22.04 LTS
  - Risk Score: 60 (High)
  - Days Since Last Patch: 706
  - Missing Patches: None
  - Recommendation: Patch immediately (overdue per CIS Control 7).

Host: WEB-SRV-002
  - Operating System: Ubuntu 22.04 LTS
  - Risk Score: 60 (High)
  - Days Since Last Patch: 545
  - Missing Patches: None
  - Recommendation: Patch immediately (overdue per CIS Control 7).

Host: DB-SRV-001
  - Operating System: Ubuntu 22.04 LTS
  - Risk Score: 60 (High)
  - Days Since Last Patch: 619
  - Missing Patches: None
  - Recommendation: Patch immediately (overdue per CIS Control 7).
  ------------------------------------------------
  As well as the key for the txt
  Key: - 'Risk Score' is on a 0-100 scale (Critical: 70+, High: 50-69, Medium: 25-49, Low: <25).
- 'Days Since Last Patch' shows how long the system has gone without updates.
- 'Recommendation' is based on CIS Control 7 patch timelines.
----------------------------------------------------------------

Functions Overview 
-----------------------------------------------------
generate_text_summary writes easily readable and understandable reports in a txt file 
as a whole it reads the data analyzes it and generates reports about what it found 
Top to bottom run through
load_inventory loads host JSON
calculate_days_since_patch does as stated
filter_by_os filters for host OS
filter_by_criticality filters for critical level
filter_by_environment filters hosts by environment like "production" "test"
calculate_risk_score calculates risk based on patch age, missing amount, and criticality
get_risk_level converts risk score into level
get_high_risk_hosts filters for high risk hosts
cis_recommendation gives a CIS patching recommendation based on timelines provided
analyze_inventory runs the main analysis pipeline adding info to the host and identifying high-risk hosts
generate_json_report writes high risk host data to the JSON file
generate_text_summary writes easily readable and understandable reports in a txt file
as a whole it reads the data, analyzes it, and generates reports about what it found

TEST RESULTS 
---------------------------------------------------------
20 high risk hosts found
706 days since last patch and 739 days and 684 days were the longest since last patch if that's what you meant by top 3

AI USAGES 
----------------------------------------------------------------
During the duration of this assignment I used AI in a few implementations. Proofreading has easily become one of my favorites on this type of work. Next, I used it for the required web app parts or recommendations, used it to help with getting it to generate a better format on my txt just to see what it would give me and it looked nice. I made the key; it didn't come with one but I figured it would be nice to have anyway. I also used AI to help with getting a better understanding of how the structure and efficiency you can get and use to make it still better to modify in the future.

CHALLENGES 
-----------------------------------------------------------------
I had first run into the issue of getting everything running right again after my reset of my computer, but besides that, getting the output structure proper without having help was a challenge. So was getting my Copilot to work on the proper file at the time I was requesting things—it was just getting confused, and usually it's good about it, but I just started selecting the files I was trying to work on to solve the issue.

