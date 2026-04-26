# AI_USAGE.md

## Use of AI Assistance in This Project

This project was developed with the assistance of GitHub Copilot (AI programming assistant, powered by GPT-4.1). The AI was used in the following ways:

- **Project Planning & Structure:**
	- Outlined the overall architecture and file/module structure for the vulnerability prioritizer.
	- Suggested input and output file formats and naming conventions.

- **Code Generation:**
	- Generated the initial MVP script, including class definitions (`Asset`, `CVE`, `VulnerabilityMatch`).
	- Provided code for argument parsing, JSON file reading/writing, and error handling.
	- Implemented the risk scoring algorithm and asset–CVE matching logic.
	- Added logging and diagnostics for easier debugging and transparency.

- **Testing & Documentation Guidance:**
	- Suggested testing strategies (unit, integration, edge case testing).
	- Provided sample data file formats and output examples.

- **Iterative Support:**
	- Answered questions about algorithms, logic, and best practices.
	- Explained code structure and class usage for better understanding.
	- Offered advice on expanding the MVP into a more advanced tool.

All code and documentation were reviewed and approved by the project author. The AI was used as a productivity and learning tool, not as a replacement for human judgment or final review.

## User Approval and Decision-Making

- The user actively reviewed all AI-generated suggestions and code.
- Approved:
	- The overall file/module structure and naming conventions.
	- The use of classes (`Asset`, `CVE`, `VulnerabilityMatch`) for code organization.
	- The risk scoring formula and logic for matching vulnerabilities to assets.
	- The approach to argument parsing, error handling, and logging.
	- The MVP script’s end-to-end workflow and output format.
- Denied or Modified:
	- Deferred or skipped advanced features (e.g., patch planning, management reports) for the MVP phase.
	- Chose not to implement a user interface or automation at this stage.
	- Requested explanations and examples before accepting class-based designs.
	- Opted for a simple, clear MVP rather than a complex or feature-rich tool initially.

The user’s feedback and decisions directly shaped the final implementation, ensuring the project met their goals and understanding at every step.
