#!/bin/bash
set -eo pipefail  # Gestion des erreurs

# Définir les chemins
REPORT_DIR="${GITHUB_WORKSPACE}/.github/reports"
OUTPUT_FILE="${REPORT_DIR}/scan-results.json"
TEMP_FILE="${REPORT_DIR}/temp-scan.json"

# Créer le dossier de rapports
mkdir -p "$REPORT_DIR"

# Lancer le scan avec Kubescape et formater le JSON
kubescape scan "$GITHUB_WORKSPACE" \
  --format json \
  --output "$TEMP_FILE" \
  --exclude-namespaces kube-system,kube-public \
  --verbose

# Structurer le JSON avec jq (indentation + tri)
jq '.' "$TEMP_FILE" > "$OUTPUT_FILE" && rm "$TEMP_FILE"

# Vérifier la sortie
echo "✅ Rapport généré : $OUTPUT_FILE"
jq -r '.summary | "Résumé : \(.passed) contrôles passés, \(.failed) échoués"' "$OUTPUT_FILE"
