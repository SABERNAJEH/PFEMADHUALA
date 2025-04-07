#!/bin/bash

minikube delete -p "$CLUSTER_NAME" || true
docker system prune -af
set -euo pipefail

CLUSTER_NAME=$1
echo "Initializing cluster: $CLUSTER_NAME"

# Télécharger la dernière version de Minikube
MINIKUBE_VERSION=$(curl -s https://api.github.com/repos/kubernetes/minikube/releases/latest | grep '"tag_name"' | cut -d '"' -f 4)
echo "Installing Minikube $MINIKUBE_VERSION"

curl -Lo minikube "https://github.com/kubernetes/minikube/releases/download/${MINIKUBE_VERSION}/minikube-linux-amd64"
chmod +x minikube
sudo mv minikube /usr/local/bin/

# Démarrer le cluster avec paramètres optimisés
minikube start -p "$CLUSTER_NAME" \
  --driver=docker \
  --memory=4096 \
  --cpus=2 \
  --disk-size=20g \
  --image-mirror-country=cn \  # Pour les problèmes de téléchargement
  --base-image="registry.cn-hangzhou.aliyuncs.com/google_containers/kicbase:v0.0.46" 

minikube status -p "$CLUSTER_NAME"
