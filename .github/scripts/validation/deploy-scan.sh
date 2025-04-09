#!/bin/bash

echo "🚀 Déploiement de test..."

# Simulation de déploiement (à adapter selon votre environnement)
echo "🛠 Configuration du contexte Kubernetes..."
kubectl config set-cluster test-cluster --server=https://kubernetes.default.svc
kubectl config set-context test-context --cluster=test-cluster

echo "🔍 Scan des ressources déployées..."
kubescape scan --enable-host-scan --format json --output live-scan-results.json

if [ $? -ne 0 ]; then
    echo "❌ Échec du scan des ressources déployées"
    exit 1
fi

echo "✅ Scan post-déploiement terminé avec succès"
