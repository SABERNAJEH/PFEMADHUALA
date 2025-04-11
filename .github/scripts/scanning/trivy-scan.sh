#!/bin/bash
set -eo pipefail

REPORT_DIR="$GITHUB_WORKSPACE/.github/reports"
OUTPUT_FILE="$REPORT_DIR/trivy-scan.json"

echo "🔍 Running Trivy Kubernetes scan..."
trivy k8s --all-namespaces \
  --format json \
  --output "$OUTPUT_FILE" \
  --timeout 10m

echo "✅ Trivy report saved to $OUTPUT_FILE"
