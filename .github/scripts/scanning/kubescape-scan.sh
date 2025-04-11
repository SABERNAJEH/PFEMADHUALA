#!/bin/bash
set -eo pipefail

REPORT_DIR="$GITHUB_WORKSPACE/.github/reports"
OUTPUT_FILE="$REPORT_DIR/kubescape-scan.json"

echo "🔍 Running Kubescape cluster scan..."
kubescape scan --submit --enable-host-scan \
  --format json \
  --output "$OUTPUT_FILE" \
  --exclude-namespaces kube-system,kube-public

echo "✅ Kubescape report saved to $OUTPUT_FILE"
