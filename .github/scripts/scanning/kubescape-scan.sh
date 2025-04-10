#!/bin/bash
set -eo pipefail

REPORT_DIR="$GITHUB_WORKSPACE/.github/reports"
OUTPUT_FILE="$REPORT_DIR/scan-results.json"

echo "🔍 Running Kubescape scan on: $GITHUB_WORKSPACE"
mkdir -p "$REPORT_DIR"

# Commande Kubescape mise à jour
kubescape scan "$GITHUB_WORKSPACE" \
  --format json \
  --output "$OUTPUT_FILE" \
  --exclude-namespaces kube-system,kube-public \
  --verbose

echo "✅ Scan completed. Report saved to $OUTPUT_FILE"
