#!/bin/bash
set -e

case "$1" in
  deploy)
    echo "🐐 Deploying Kubernetes Goat..."
    git clone --depth 1 --branch $KUBERNETES_GOAT_VERSION \
      https://github.com/SABERNAJEH/PFEMADHUALA.git /tmp/kubernetes-goat
    
    cd /tmp/kubernetes-goat
    bash setup-kubernetes-goat.sh -y
    ;;
    
  *)
    echo "❌ Usage: $0 deploy"
    exit 1
    ;;
esac