#!/bin/bash

echo "🔎 Validation des manifests Kubernetes..."

# Installation de kubeval si nécessaire
if ! command -v kubeval &> /dev/null
then
    echo "🛠 Installation de kubeval..."
    wget https://github.com/instrumenta/kubeval/releases/latest/download/kubeval-linux-amd64.tar.gz
    tar xf kubeval-linux-amd64.tar.gz
    sudo mv kubeval /usr/local/bin
fi

# Validation des fichiers YAML
for file in $(find . -name "*.yaml" -o -name "*.yml"); do
    echo "🔍 Validation de $file"
    kubeval --strict $file
    if [ $? -ne 0 ]; then
        echo "❌ Échec de validation pour $file"
        exit 1
    fi
done

echo "✅ Tous les manifests sont valides"
