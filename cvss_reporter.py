#!/usr/bin/env python3

DECIMALS = 1

def validate_score(score):
    try:
        s = float(score)
    except (ValueError, TypeError):
        raise ValueError("Score must be a number between 0.0 and 10.0")
    if s < 0.0 or s > 10.0:
        raise ValueError("Score must be between 0.0 and 10.0")
    return s

def score_to_percentage(score):
    s = validate_score(score)
    return s / 10.0 * 100.0

def categorize_severity(score):
    s = validate_score(score)
    if s >= 9.0:
        return "CRITICAL"
    if s >= 7.0:
        return "HIGH"
    if s >= 4.0:
        return "MEDIUM"
    if s >= 0.1:
        return "LOW"
    return "NONE"

def format_vulnerability(vuln):
    s = validate_score(vuln.get("cvss", 0.0))
    pct = score_to_percentage(s)
    sev = categorize_severity(s)
    return (
        f"{vuln.get('id','UNKNOWN')}: {vuln.get('title','No title')}\n"
        f"  CVSS: {s:.1f}/10.0 ({pct:.1f}%)  Severity: {sev}\n"
        f"  Description: {vuln.get('description','No description')}"
    )

def print_report(vulns):
    print("VULNERABILITY REPORT")
    print("=" * 60)
    for v in vulns:
        print(format_vulnerability(v))
        print("-" * 60)

def main():
    import argparse, json, sys

    parser = argparse.ArgumentParser(description='Print CVSS vulnerability report')
    parser.add_argument('-f', '--file', help='Path to JSON file with list of vulnerabilities')
    parser.add_argument('-j', '--json', help='JSON string representing list of vulnerabilities')
    args = parser.parse_args()

    data = None
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception as e:
            print(f"Failed to read file: {e}", file=sys.stderr)
            sys.exit(2)
    elif args.json:
        try:
            data = json.loads(args.json)
        except Exception as e:
            print(f"Invalid JSON: {e}", file=sys.stderr)
            sys.exit(2)
    else:
        parser.error('Provide --file or --json')

    if not isinstance(data, list):
        print('Input JSON must be a list of vulnerability objects', file=sys.stderr)
        sys.exit(2)

    print_report(data)


if __name__ == '__main__':
    main()
