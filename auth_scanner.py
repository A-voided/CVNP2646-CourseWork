#!/usr/bin/env python3
"""
Authentication Log Scanner
Analyzes authentication logs for security incidents

Author: [James Goebel Jr.]
Date: 2026-3-1
"""

import json
from collections import Counter
from datetime import datetime


def parse_log_line(line):
    """
    Parse a single authentication log line.
    
    Args:
        line: Raw log line string
    
    Returns:
        dict with parsed fields, or None if malformed
    """
    entries = []

    import re
    parts = re.split(r'(\d{4}-\d{2}-\d{2} [^ ]+)', line)

    i = 1
    while i < len(parts):
        entry = parts[i] + parts[i+1] if i+1 < len(parts) else parts[i]
        entries.append(entry.strip())
        i += 2

    parsed_entries = []
    for entry in entries:
        fields = {}
        try:
            tokens = entry.strip().split()
            if len(tokens) < 3:
                raise ValueError('Too few tokens')
            fields['timestamp'] = tokens[0] + ' ' + tokens[1]
            for token in tokens[2:]:
                if '=' in token:
                    k, v = token.split('=', 1)
                    fields[k.strip()] = v.strip()
            parsed_entries.append(fields)
        except Exception:
            parsed_entries.append(None)

    return parsed_entries


def analyze_logs(filename):
    """
    Analyze authentication logs from a file.
    
    Args:
        filename: Path to log file
    
    Returns:
        dict containing analysis results
    """
    
    failed_by_user = Counter()
    failed_by_ip = Counter()
    total_success = 0
    total_fail = 0
    parse_errors = 0
    total_events = 0
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parsed_entries = parse_log_line(line)
            for entry in parsed_entries:
                if entry is None:
                    parse_errors += 1
                    continue
                total_events += 1
                status = entry.get('status', '').strip().upper()
                user = entry.get('user', 'UNKNOWN')
                ip = entry.get('ip', 'UNKNOWN')
                if status == 'FAIL':
                    total_fail += 1
                    failed_by_user[user] += 1
                    failed_by_ip[ip] += 1
                elif status == 'SUCCESS':
                    total_success += 1
                else:
                    parse_errors += 1
    failure_rate = (total_fail / total_events * 100) if total_events else 0.0
    results = {
        'total_events': total_events,
        'total_success': total_success,
        'total_fail': total_fail,
        'failure_rate': failure_rate,
        'parse_errors': parse_errors,
        'failed_by_user': dict(failed_by_user),
        'failed_by_ip': dict(failed_by_ip)
    }
    return results


def generate_json_report(results):
    """
    Generate JSON report from analysis results.
    
    Args:
        results: dict from analyze_logs()
    
    Returns:
        JSON string
    """
    report = {
        'report_generated': datetime.now().isoformat(),
        'summary': {
            'total_events': results['total_events'],
            'total_success': results['total_success'],
            'total_fail': results['total_fail'],
            'failure_rate': results['failure_rate'],
            'parse_errors': results['parse_errors']
        },
        'top_failed_users': sorted(results['failed_by_user'].items(), key=lambda x: x[1], reverse=True)[:5],
        'top_failed_ips': sorted(results['failed_by_ip'].items(), key=lambda x: x[1], reverse=True)[:5]
    }
    return json.dumps(report, indent=4)


def generate_text_report(results):
    """
    Generate human-readable text report.
    
    Args:
        results: dict from analyze_logs()
    
    Returns:
        Formatted text string
    """
    lines = []
    lines.append('='*70)
    lines.append('        AUTHENTICATION FAILURE ANALYSIS REPORT')
    lines.append(f'        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append('='*70)
    lines.append('')
    lines.append(f'ALERT: High failure rate detected: {results["failure_rate"]:.1f}% (baseline: 2-5%)' if results["failure_rate"] > 5 else 'Failure rate within normal range.')
    if results["failure_rate"] > 20:
        lines.append('Potential BRUTE FORCE ATTACK in progress.')
    lines.append('-'*70)
    lines.append('SUMMARY STATISTICS')
    lines.append('-'*70)
    lines.append(f'Total Events:        {results["total_events"]}')
    lines.append(f'Successful Logins:   {results["total_success"]} ({(results["total_success"]/results["total_events"]*100) if results["total_events"] else 0:.1f}%)')
    lines.append(f'Failed Attempts:     {results["total_fail"]} ({results["failure_rate"]:.1f}%)')
    lines.append(f'Parse Errors:        {results["parse_errors"]}')
    lines.append('-'*70)
    lines.append('TOP 5 TARGETED ACCOUNTS')
    lines.append('-'*70)
    for i, (user, count) in enumerate(sorted(results['failed_by_user'].items(), key=lambda x: x[1], reverse=True)[:5], 1):
        lines.append(f'{i}. {user:<16} {count} failed attempts')
    if not results['failed_by_user']:
        lines.append('No failed login attempts recorded.')
    lines.append('-'*70)
    lines.append('TOP 5 ATTACKING SOURCE IPs')
    lines.append('-'*70)
    for i, (ip, count) in enumerate(sorted(results['failed_by_ip'].items(), key=lambda x: x[1], reverse=True)[:5], 1):
        lines.append(f'{i}. {ip:<16} {count} failed attempts')
    if not results['failed_by_ip']:
        lines.append('No failed login attempts recorded.')
    lines.append('='*70)
    lines.append('Report generated by: SOC Automation Platform')
    lines.append('='*70)
    return '\n'.join(lines)


def main():

    """Main execution function."""

    import os
    import sys
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
        if not os.path.isabs(log_file):
            log_file = os.path.join(os.path.dirname(__file__), log_file)
    else:
        print("Usage: python auth_scanner.py <log_file>")
        sys.exit(1)
    results = analyze_logs(log_file)
    
    json_report = generate_json_report(results)
    with open(os.path.join(os.path.dirname(__file__), 'incident_report.json'), 'w', encoding='utf-8') as jf:
        jf.write(json_report)
    
    text_report = generate_text_report(results)
    with open(os.path.join(os.path.dirname(__file__), 'incident_report.txt'), 'w', encoding='utf-8') as tf:
        tf.write(text_report)
    
    print("Authentication Log Scanner")
    print("=" * 50)
    print(f"Log file analyzed: {log_file}")
    print(f"Total Events: {results['total_events']}")
    print(f"Successes:    {results['total_success']}")
    print(f"Failures:     {results['total_fail']}")
    print(f"Parse Errors: {results['parse_errors']}")
    print(f"Failure Rate: {results['failure_rate']:.1f}%")
    print("Reports saved as incident_report.json and incident_report.txt")

if __name__ == "__main__":
    main()
