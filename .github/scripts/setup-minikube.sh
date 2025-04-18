#!/bin/bash
# Script pour installer et démarrer Minikube

echo "🔄 Installation de Minikube..."
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

echo "🚀 Démarrage du cluster Minikube..."
minikube start --driver=docker

echo "✅ Minikube est opérationnel !"
