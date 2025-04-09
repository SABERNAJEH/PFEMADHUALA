#!/bin/bash
set -eo pipefail  # Gestion améliorée des erreurs

# Configuration des chemins
REPORT_DIR="$GITHUB_WORKSPACE/.github/reports"
OUTPUT_FILE="$REPORT_DIR/scan-results.json"

echo "🔍 Initialisation du scan de sécurité Kubernetes..."

# Installation de Kubescape si absent
if ! command -v kubescape &>/dev/null; then
    echo "⬇️ Téléchargement de Kubescape..."
    curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | bash
    export PATH="$HOME/.kubescape:$PATH"
fi

# Création du répertoire de rapports
mkdir -p "$REPORT_DIR"

echo "⚙️ Paramètres:"
echo "• Répertoire: $GITHUB_WORKSPACE"
echo "• Cible: ./**/*.yaml"
echo "• Exclusions: kind:Secret"
echo "• Sortie: $OUTPUT_FILE"

# Exécution du scan avec gestion des erreurs
echo "🔄 Lancement de l'analyse..."
if kubescape scan "$GITHUB_WORKSPACE" \
    --format json \
    --output "$OUTPUT_FILE" \
    --exclude-nodes "kind:Secret" \
    --verbose; then
    
    echo "✅ Analyse terminée avec succès"
    echo "📊 Rapport disponible: $OUTPUT_FILE"
    exit 0
else
    echo "❌ Échec de l'analyse"
    echo "⚠️ Consultez les logs pour plus de détails"
    exit 1
fi
