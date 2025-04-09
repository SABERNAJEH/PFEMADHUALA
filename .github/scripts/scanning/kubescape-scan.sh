#!/bin/bash

echo "🔍 Démarrage du scan Kubescape..."
kubescape scan . --format json --output scan-results.json --exclude-nodes "kind:Secret"

if [ $? -ne 0 ]; then
    echo "❌ Échec du scan Kubescape"
    exit 1
fi

echo "✅ Scan Kubescape terminé avec succès"
