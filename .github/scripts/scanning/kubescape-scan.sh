#!/bin/bash

echo "🔍 Démarrage du scan Kubescape..."
OUTPUT_FILE="$(pwd)/.github/reports/scan-results.json"
mkdir -p $(dirname "$OUTPUT_FILE")
kubescape scan . --format json --output "$OUTPUT_FILE" --exclude-nodes "kind:Secret"

if [ $? -ne 0 ]; then
    echo "❌ Échec du scan Kubescape"
    exit 1
fi

echo "✅ Scan Kubescape terminé avec succès - Rapport sauvegardé à $OUTPUT_FILE"
