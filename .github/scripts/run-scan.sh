#!/bin/bash
set -e

case "$1" in
  install-kubescape)
    echo "🔍 Installing Kubescape..."
    curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash
    echo "$HOME/.kubescape/bin" >> $GITHUB_PATH
    $HOME/.kubescape/bin/kubescape version
    ;;
    
  execute-scan)
    echo "🛡️ Running security scan..."
    $HOME/.kubescape/bin/kubescape scan \
      --enable-host-scan \
      --format json \
      --verbose \
      --output $CLUSTER_SCAN_OUTPUT \
      || echo "Scan completed with exit code $?"
    
    [ -f "$CLUSTER_SCAN_OUTPUT" ] && \
      jq '.' "$CLUSTER_SCAN_OUTPUT" > temp.json && \
      mv temp.json "$CLUSTER_SCAN_OUTPUT"
    ;;
    
  *)
    echo "❌ Usage: $0 {install-kubescape|execute-scan}"
    exit 1
    ;;
esac