# Kubescape Remediation Playbook

## Critical Vulnerabilities
1. **Privilege Escalation**
   - Action: Set `allowPrivilegeEscalation: false` in pod specs
   - Verification:
     ```sh
     kubectl get pods -o json | jq '.items[].spec.containers[].securityContext'
     ```

2. **Host PID Sharing**
   - Action: Set `hostPID: false`
   - Reference: [CIS Benchmark 5.2.2]

## High Severity
1. **Read-only Root Filesystem**
   ```yaml
   securityContext:
     readOnlyRootFilesystem: true
