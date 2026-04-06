import os
import json
import csv
from datetime import datetime
from collections import defaultdict

# File Utilities

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_csv(filepath):
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

# Data Helpers

def build_user_lookup(users_data):
    return {user.get('user_id'): user for user in users_data}

def group_roles_by_user(roles_data):
    user_roles = defaultdict(list)
    for role_entry in roles_data:
        user_roles[role_entry.get('user_id')].append(role_entry.get('role'))
    return dict(user_roles)

# Detection Rules

def check_disabled_with_roles(users_dict, roles_by_user):
    violations = []
    for user_id, user in users_dict.items():
        if user.get('status') == 'disabled' and user_id in roles_by_user:
            violations.append({
                'user_id': user_id,
                'username': user.get('username'),
                'roles': roles_by_user.get(user_id, []),
                'severity': 'CRITICAL',
                'type': 'disabled_with_roles',
            })
    return violations


def check_unauthorized_admins(users_dict, roles_data, authorized_depts=None):
    if authorized_depts is None:
        authorized_depts = {'IT', 'Security'}

    violations = []
    for role_entry in roles_data:
        role = role_entry.get('role', '').lower()
        if 'admin' in role:
            user_id = role_entry.get('user_id')
            user = users_dict.get(user_id, {})
            if user.get('department') not in authorized_depts:
                violations.append({
                    'user_id': user_id,
                    'username': user.get('username'),
                    'department': user.get('department'),
                    'role': role_entry.get('role'),
                    'severity': 'HIGH',
                    'type': 'unauthorized_admin',
                })
    return violations


def check_stale_accounts(users_dict, stale_days=90):
    violations = []
    now = datetime.now()

    for user_id, user in users_dict.items():
        if user.get('status') == 'active':
            last_login = user.get('last_login')
            days_stale = None

            if last_login:
                try:
                    last_login_date = datetime.strptime(last_login, '%Y-%m-%d')
                    days_stale = (now - last_login_date).days
                except ValueError:
                    pass

            if days_stale is None or days_stale > stale_days:
                violations.append({
                    'user_id': user_id,
                    'username': user.get('username'),
                    'last_login': last_login,
                    'days_stale': days_stale,
                    'severity': 'MEDIUM',
                    'type': 'stale_account',
                })

    return violations


def check_service_account_pattern(users_dict):
    violations = []
    for user_id, user in users_dict.items():
        username = user.get('username', '')
        if username.startswith('svc_') and user.get('status', '').lower() != 'service':
            violations.append({
                'user_id': user_id,
                'username': username,
                'status': user.get('status'),
                'severity': 'LOW',
                'type': 'service_account_pattern',
            })
    return violations


def check_department_validation(users_dict, approved_departments=None):
    if approved_departments is None:
        approved_departments = {'IT', 'Security', 'Finance', 'HR', 'Marketing'}

    violations = []
    for user_id, user in users_dict.items():
        if user.get('department') not in approved_departments:
            violations.append({
                'user_id': user_id,
                'username': user.get('username'),
                'department': user.get('department'),
                'severity': 'LOW',
                'type': 'department_validation',
            })
    return violations

# Report Generators

def generate_json_report(all_violations, users_dict, roles_data):
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    severity_counts = {}
    type_counts = {}

    for v in all_violations:
        sev = v.get('severity', 'LOW').upper()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

        t = v.get('type', 'unknown')
        type_counts[t] = type_counts.get(t, 0) + 1

    report = {
        "audit_metadata": {
            "timestamp": now,
            "total_users_audited": len(users_dict),
            "total_role_assignments": len(roles_data),
            "total_violations": len(all_violations),
            "auditor": "IAM Audit System v1.0"
        },
        "violation_summary": {
            "by_severity": severity_counts,
            "by_type": type_counts
        },
        "all_violations": all_violations
    }

    return json.dumps(report, indent=2)


def generate_text_report(all_violations, users_dict, roles_data):
    from datetime import datetime
    auditor = "IAM Audit Reporter v1.9102"
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Executive summary counts
    total_users = len(users_dict)
    total_roles = len(roles_data)
    total_violations = len(all_violations)

    # Severity and type breakdowns
    severity_levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    severity_counts = {k: 0 for k in severity_levels}
    type_counts = {}
    for v in all_violations:
        sev = v.get('severity', 'LOW').upper()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        t = v.get('type', 'unknown')
        type_counts[t] = type_counts.get(t, 0) + 1

    # Visual bar helper
    def bar(count, max_count, width=12):
        if max_count == 0:
            return ""
        filled = int((count / max_count) * width)
        empty = width - filled
        return "█" * filled + "░" * empty

    # Sort types by count desc
    sorted_types = sorted(type_counts.items(), key=lambda x: -x[1])

    # Group violations by severity
    violations_by_sev = {k: [] for k in severity_levels}
    for v in all_violations:
        sev = v.get('severity', 'LOW').upper()
        violations_by_sev.setdefault(sev, []).append(v)

    lines = []
    lines.append("=" * 80)
    lines.append("USER ACCOUNT & PERMISSIONS REPORT\n")
    lines.append(f"Generated: {now}")
    lines.append(f"Auditor: {auditor}\n")

    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Total Users Audited: {total_users}")
    lines.append(f"Total Role Assignments: {total_roles}")
    lines.append(f"Total Violations Found: {total_violations}\n")

    lines.append("VIOLATIONS BY SEVERITY")
    lines.append("=+++++++=======+++=======++++==++++===+++===+++===++++==")
    max_sev = max(severity_counts.values()) if severity_counts else 1
    for sev in severity_levels:
        lines.append(f"{sev:<12} [ {severity_counts[sev]:<3} ] {bar(severity_counts[sev], max_sev)}")
    lines.append("")

    lines.append("VIOLATIONS BY TYPE")
    lines.append("-=-=-=-=-==-=-=-=-=-=-=-==-=-=-=-=-=-=-==-=-=--=-=--=-=")
    max_type = max([c for _, c in sorted_types], default=1)
    for t, c in sorted_types:
        lines.append(f"{t:<30} [ {c:<3} ] {bar(c, max_type)}")
    lines.append("")

    lines.append("DETAILED VIOLATIONS")
    lines.append("=" * 28)

    for sev in severity_levels:
        vlist = violations_by_sev.get(sev, [])
        if not vlist:
            continue
        lines.append("")
        lines.append(f"{sev} SEVERITY ({len(vlist)})")
        lines.append("." * 95)
        for idx, v in enumerate(vlist, 1):
            uname = v.get('username', '-')
            uid = v.get('user_id', '-')
            vtype = v.get('type', '-')
            details = ""
            if vtype == 'disabled_with_roles':
                roles = v.get('roles', [])
                details = f"Disabled account has {len(roles)} active role(s): {', '.join(roles)}"
            elif vtype == 'unauthorized_admin':
                details = f"Admin role assigned to unauthorized department: {v.get('department', '-')}, Role: {v.get('role', '-') }"
            elif vtype == 'stale_account':
                days = v.get('days_stale')
                last_login = v.get('last_login', '-')
                details = f"Last login: {last_login}, Days stale: {days if days is not None else 'N/A'}"
            elif vtype == 'service_account_pattern':
                details = f"Username pattern 'svc_' but status is '{v.get('status', '-')}'"
            elif vtype == 'department_validation':
                details = f"Unapproved department: {v.get('department', '-') }"
            else:
                details = str(v)
            lines.append(f"{idx}. User: {uname} (ID: {uid})")
            lines.append(f"   Type: {vtype}")
            lines.append(f"   Details: {details}\n")

    lines.append("=" * 28)
    lines.append("END OF REPORT")
    return "\n".join(lines)

# Main Execution

def main():

    users_file = 'users.json'
    roles_file = 'roles.json'

    users_data = load_json(users_file)
    roles_data = load_json(roles_file)

    users_dict = build_user_lookup(users_data)
    roles_by_user = group_roles_by_user(roles_data)

    all_violations = []
    all_violations.extend(check_disabled_with_roles(users_dict, roles_by_user))
    all_violations.extend(check_unauthorized_admins(users_dict, roles_data))
    all_violations.extend(check_stale_accounts(users_dict))
    all_violations.extend(check_service_account_pattern(users_dict))
    all_violations.extend(check_department_validation(users_dict))

    json_report = generate_json_report(all_violations, users_dict, roles_data)
    text_report = generate_text_report(all_violations, users_dict, roles_data)

    with open('audit_report.json', 'w', encoding='utf-8') as f:
        f.write(json_report)

    with open('audit_report.txt', 'w', encoding='utf-8') as f:
        f.write(text_report)

    print(f"Audit complete! Found {len(all_violations)} violations.")
    print("Reports saved: audit_report.json, audit_report.txt")


if __name__ == '__main__':
    main()