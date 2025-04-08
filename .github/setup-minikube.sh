#!/bin/bash
set -e

case "$1" in
  configure-system)
    echo "⚙️ Configuring system..."
    sudo apt-get update -qq
    sudo apt-get install -qq -y --no-install-recommends \
      conntrack socat curl jq git
    sudo swapoff -a 2>/dev/null || true
    ;;
    
  install-components)
    echo "📦 Installing Minikube and dependencies..."
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/$MINIKUBE_VERSION/minikube-linux-amd64
    chmod +x minikube
    sudo install minikube /usr/local/bin/minikube
    minikube version
    
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install kubectl /usr/local/bin/kubectl
    ;;
    
  start-cluster)
    echo "🚀 Starting Minikube cluster..."
    minikube start \
      --driver=docker \
      --container-runtime=containerd \
      --kubernetes-version=stable \
      --wait=all \
      --wait-timeout=$MINIKUBE_WAIT_TIMEOUT \
      --memory=6144 \
      --cpus=4 \
      --disk-size=20g \
      --addons=metrics-server \
      --delete-on-failure
    ;;
    
  *)
    echo "❌ Usage: $0 {configure-system|install-components|start-cluster}"
    exit 1
    ;;
esac