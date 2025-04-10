#!/bin/bash
set -eo pipefail

echo "🔍 Validating Kubernetes manifests with kubeval..."

# Install kubeval if not present
if ! command -v kubeval &> /dev/null; then
  echo "⬇️ Installing kubeval..."
  wget https://github.com/instrumenta/kubeval/releases/latest/download/kubeval-linux-amd64.tar.gz
  tar xf kubeval-linux-amd64.tar.gz
  chmod +x kubeval
  sudo mv kubeval /usr/local/bin/
fi

# Validate all YAML files
ERRORS=0
for file in $(find . -name '*.yaml' -o -name '*.yml'); do
  echo "Validating $file..."
  if ! kubeval --strict "$file"; then
    ERRORS=$((ERRORS + 1))
  fi
done

if [ "$ERRORS" -gt 0 ]; then
  echo "❌ Validation failed with $ERRORS errors"
  exit 1
else
  echo "✅ All manifests are valid"
  exit 0
fi
