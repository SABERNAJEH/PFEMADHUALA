#!/usr/bin/env python3
"""
Process Kubescape JSON report and generate:
- GitHub issues
- Developer recommendations
- Slack/Teams alerts
"""
import json
from typing import List, Dict
from kubescape_utils import (  # Fichier séparé pour les helpers
    load_report,
    validate_report,
    group_by_namespace
)

CONFIG = {
    "MIN_SEVERITY": "Medium",  # Ignore les vulnérabilités en dessous
    "AUTO_ASSIGN": True,       # Assignation automatique aux devs
    "REPO_OWNER": "my-org",
    "REPO_NAME": "my-repo"
}

def generate_issues(findings: List[Dict]) -> List[Dict]:
    """Format findings for GitHub API"""
    return [{
        "title": f"[Security] {f['severity']}: {f['name']}",
        "body": f"""
**Description**\n{f['description']}\n
**Resource**\n```yaml\n{f['resource']}\n```\n
**Namespace**: `{f['namespace']}`\n
**Recommended Fix**\n{f['remediation']}\n
**Control**: {f['control_name']}\n
**Full Path**: {f.get('resource_path', 'N/A')}
        """,
        "labels": ["security", f"severity:{f['severity'].lower()}"],
        "assignees": ["dev-team"] if CONFIG["AUTO_ASSIGN"] else []
    } for f in findings if f['severity'] >= CONFIG["MIN_SEVERITY"]]

def main():
    # 1. Load and validate report
    report = load_report("results.json")
    validate_report(report)
    
    # 2. Process findings
    findings = extract_findings(report)
    grouped_findings = group_by_namespace(findings)
    
    # 3. Generate outputs
    issues = generate_issues(findings)
    with open("security_issues.json", "w") as f:
        json.dump(issues, f, indent=2)
    
    # 4. Create summary report
    create_summary(grouped_findings)

if __name__ == "__main__":
    main()
