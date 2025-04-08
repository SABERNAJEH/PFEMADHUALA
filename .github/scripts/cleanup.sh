
#!/bin/bash
set -e

case "$1" in
  cleanup-goat)
    echo "🧹 Cleaning up Kubernetes Goat..."
    if [ -d "/tmp/kubernetes-goat" ]; then
      cd /tmp/kubernetes-goat
      bash reset-kubernetes-goat.sh || true
    fi
    ;;
    
  cleanup-minikube)
    echo "🧹 Cleaning up Minikube cluster..."
    minikube delete --all --purge || true
    ;;
    
  *)
    echo "❌ Usage: $0 {cleanup-goat|cleanup-minikube}"
    exit 1
    ;;
esac
