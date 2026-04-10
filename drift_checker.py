import json
import os
import argparse
from typing import Any, List


class DriftSeverity:
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class DriftType:
    MISSING_KEY = "Missing Key"
    EXTRA_KEY = "Extra Key"
    CHANGED_VALUE = "Changed Value"

class DriftResult:
    def __init__(self, drift_type: str, path: str, expected: Any, current: Any, severity: str):
        self.drift_type = drift_type
        self.path = path
        self.expected = expected
        self.current = current
        self.severity = severity

    def __repr__(self):
        return (f"[{self.severity}] {self.drift_type} at '{self.path}': "
                f"expected={self.expected}, current={self.current}")

    def to_dict(self):
        return {
            "drift_type": self.drift_type,
            "path": self.path,
            "expected": self.expected,
            "current": self.current,
            "severity": self.severity
        }

def assign_severity(drift_type, path):
    # Example logic: customize as needed for your environment
    path_lower = path.lower()
    if drift_type == DriftType.MISSING_KEY:
        if "admin" in path_lower or "root" in path_lower:
            return DriftSeverity.CRITICAL
        return DriftSeverity.HIGH
    elif drift_type == DriftType.EXTRA_KEY:
        if "debug" in path_lower or "test" in path_lower:
            return DriftSeverity.MEDIUM
        return DriftSeverity.LOW
    elif drift_type == DriftType.CHANGED_VALUE:
        if "password" in path_lower or "secret" in path_lower:
            return DriftSeverity.CRITICAL
        return DriftSeverity.HIGH
    return DriftSeverity.LOW

def compare_json(baseline, current, path="", results=None):
    if results is None:
        results = []
    # Compare dictionaries
    if isinstance(baseline, dict) and isinstance(current, dict):
        baseline_keys = set(baseline.keys())
        current_keys = set(current.keys())
        # Missing keys
        for key in baseline_keys - current_keys:
            drift_path = f"{path}.{key}" if path else key
            results.append(DriftResult(
                DriftType.MISSING_KEY,
                drift_path,
                baseline[key],
                None,
                assign_severity(DriftType.MISSING_KEY, drift_path)
            ))
        # Extra keys
        for key in current_keys - baseline_keys:
            drift_path = f"{path}.{key}" if path else key
            results.append(DriftResult(
                DriftType.EXTRA_KEY,
                drift_path,
                None,
                current[key],
                assign_severity(DriftType.EXTRA_KEY, drift_path)
            ))
        # Compare common keys
        for key in baseline_keys & current_keys:
            compare_json(
                baseline[key],
                current[key],
                f"{path}.{key}" if path else key,
                results
            )
    # Compare lists
    elif isinstance(baseline, list) and isinstance(current, list):
        min_len = min(len(baseline), len(current))
        for i in range(min_len):
            compare_json(baseline[i], current[i], f"{path}[{i}]", results)
        # Extra items
        for i in range(min_len, len(baseline)):
            drift_path = f"{path}[{i}]"
            results.append(DriftResult(
                DriftType.MISSING_KEY,
                drift_path,
                baseline[i],
                None,
                assign_severity(DriftType.MISSING_KEY, drift_path)
            ))
        for i in range(min_len, len(current)):
            drift_path = f"{path}[{i}]"
            results.append(DriftResult(
                DriftType.EXTRA_KEY,
                drift_path,
                None,
                current[i],
                assign_severity(DriftType.EXTRA_KEY, drift_path)
            ))
    # Compare values
    elif baseline != current:
        results.append(DriftResult(
            DriftType.CHANGED_VALUE,
            path,
            baseline,
            current,
            assign_severity(DriftType.CHANGED_VALUE, path)
        ))
    return results

def generate_drift_report(drift_results: List[DriftResult]) -> str:
    if not drift_results:
        return "No drift detected. Baseline and current configurations match."
    lines = ["Configuration Drift Report:", "="*30]
    for drift in drift_results:
        lines.append(f"Severity: {drift.severity}")
        lines.append(f"Type: {drift.drift_type}")
        lines.append(f"Path: {drift.path}")
        lines.append(f"Expected: {drift.expected}")
        lines.append(f"Current: {drift.current}")
        lines.append("-"*30)
    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configuration Drift Checker")
    parser.add_argument("--baseline", required=True, help="Path to baseline JSON file")
    parser.add_argument("--current", required=True, help="Path to current JSON file")
    args = parser.parse_args()

    with open(args.baseline, "r", encoding="utf-8") as f:
        baseline = json.load(f)
    with open(args.current, "r", encoding="utf-8") as f:
        current = json.load(f)

    drift_results = compare_json(baseline, current)
    report = generate_drift_report(drift_results)
    print(report)
def generate_drift_report(drift_results: List[DriftResult]) -> str:
    if not drift_results:
        return "No drift detected. Baseline and current configurations match."
    lines = ["Configuration Drift Report:", "="*30]
    for drift in drift_results:
        lines.append(f"Severity: {drift.severity}")
        lines.append(f"Type: {drift.drift_type}")
        lines.append(f"Path: {drift.path}")
        lines.append(f"Expected: {drift.expected}")
        lines.append(f"Current: {drift.current}")
        lines.append("-"*30)
    return "\n".join(lines)
def assign_severity(drift_type, path):
    # Example logic: customize as needed for your environment
    path_lower = path.lower()
    if drift_type == DriftType.MISSING_KEY:
        if "admin" in path_lower or "root" in path_lower:
            return DriftSeverity.CRITICAL
        return DriftSeverity.HIGH
    elif drift_type == DriftType.EXTRA_KEY:
        if "debug" in path_lower or "test" in path_lower:
            return DriftSeverity.MEDIUM
        return DriftSeverity.LOW
    elif drift_type == DriftType.CHANGED_VALUE:
        if "password" in path_lower or "secret" in path_lower:
            return DriftSeverity.CRITICAL
        return DriftSeverity.HIGH
    return DriftSeverity.LOW
import json
import os

def compare_json(baseline, current, path="", results=None):
    if results is None:
        results = []
    # Compare dictionaries
    if isinstance(baseline, dict) and isinstance(current, dict):
        baseline_keys = set(baseline.keys())
        current_keys = set(current.keys())
        # Missing keys
        for key in baseline_keys - current_keys:
            drift_path = f"{path}.{key}" if path else key
            results.append(DriftResult(
                DriftType.MISSING_KEY,
                drift_path,
                baseline[key],
                None,
                assign_severity(DriftType.MISSING_KEY, drift_path)
            ))
        # Extra keys
        for key in current_keys - baseline_keys:
            drift_path = f"{path}.{key}" if path else key
            results.append(DriftResult(
                DriftType.EXTRA_KEY,
                drift_path,
                None,
                current[key],
                assign_severity(DriftType.EXTRA_KEY, drift_path)
            ))
        # Compare common keys
        for key in baseline_keys & current_keys:
            compare_json(
                baseline[key],
                current[key],
                f"{path}.{key}" if path else key,
                results
            )
    # Compare lists
    elif isinstance(baseline, list) and isinstance(current, list):
        min_len = min(len(baseline), len(current))
        for i in range(min_len):
            compare_json(baseline[i], current[i], f"{path}[{i}]", results)
        # Extra items
        for i in range(min_len, len(baseline)):
            drift_path = f"{path}[{i}]"
            results.append(DriftResult(
                DriftType.MISSING_KEY,
                drift_path,
                baseline[i],
                None,
                assign_severity(DriftType.MISSING_KEY, drift_path)
            ))
        for i in range(min_len, len(current)):
            drift_path = f"{path}[{i}]"
            results.append(DriftResult(
                DriftType.EXTRA_KEY,
                drift_path,
                None,
                current[i],
                assign_severity(DriftType.EXTRA_KEY, drift_path)
            ))
    # Compare values
    elif baseline != current:
        results.append(DriftResult(
            DriftType.CHANGED_VALUE,
            path,
            baseline,
            current,
            assign_severity(DriftType.CHANGED_VALUE, path)
        ))
    return results

import json
import os
import argparse
from typing import Any, List

class DriftSeverity:
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class DriftType:
    MISSING_KEY = "Missing Key"
    EXTRA_KEY = "Extra Key"
    CHANGED_VALUE = "Changed Value"

class DriftResult:
    def __init__(self, drift_type: str, path: str, expected: Any, current: Any, severity: str):
        self.drift_type = drift_type
        self.path = path
        self.expected = expected
        self.current = current
        self.severity = severity

    def __repr__(self):
        return (f"[{self.severity}] {self.drift_type} at '{self.path}': "
                f"expected={self.expected}, current={self.current}")

    def to_dict(self):
        return {
            "drift_type": self.drift_type,
            "path": self.path,
            "expected": self.expected,
            "current": self.current,
            "severity": self.severity
        }
