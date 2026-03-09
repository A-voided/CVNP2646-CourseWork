README
How to Run
-------------
Open console and run: python backup_planner.py backup_config.json

Structure
-------------
I chose my JSON structure for ease of use and kept it easily modifiable.

Validation Levels
-------------------
Top-level: Checks if the config is a dictionary and checks for load errors.
Plans list validation: Ensures there's a "plans" key and verifies it's a list.
Plan validation: Checks each plan for the required name, sources, and destination fields.
Per-source validation: Checks for a path and ensures it's not empty.