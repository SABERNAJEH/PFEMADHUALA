name: ✅ Validation et Déploiement

on:
  workflow_call:
    inputs:
      scan-results:
        required: true
        type: string

jobs:
  validate-and-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Kubernetes tools
        run: |
          curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
          chmod +x kubectl
          sudo mv kubectl /usr/local/bin/

      - name: Run dynamic scan
        run: .github/scripts/validation/deploy-scan.sh
