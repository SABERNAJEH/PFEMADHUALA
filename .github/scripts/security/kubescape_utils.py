"""Helper functions for Kubescape processing"""
from typing import Dict, List

SEVERITY_LEVELS = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}

def load_report(path: str) -> Dict:
    """Load and basic validation"""
    with open(path) as f:
        data = json.load(f)
    assert "results" in data, "Invalid Kubescape report format"
    return data

def extract_findings(data: Dict) -> List[Dict]:
    """Extract vulnerabilities with enhanced data"""
    findings = []
    for result in data["results"]:
        for control in result["controls"]:
            for rule in control["rules"]:
                for alert in rule["alerts"]:
                    findings.append({
                        **alert,
                        "control_id": control["id"],
                        "framework": result["framework"]
                    })
    return sorted(findings, key=lambda x: -SEVERITY_LEVELS[x["severity"]])

def group_by_namespace(findings: List[Dict]) -> Dict[str, List]:
    """Group vulnerabilities by namespace"""
    groups = {}
    for f in findings:
        ns = f.get("namespace", "cluster-wide")
        groups.setdefault(ns, []).append(f)
    return groups
