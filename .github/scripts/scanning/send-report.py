jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup environment
        run: |
          sudo apt update && sudo apt install -y \
            pandoc \
            texlive-xetex \
            fonts-dejavu \
            fonts-liberation \
            python3-pip \
            jq
          pip install markdown2
          mkdir -p .github/reports
          echo "$HOME/.kubescape/bin" >> $GITHUB_PATH

      - name: Install Kubescape
        run: |
          curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh  | bash
          kubescape version
          echo "✅ Version installée: $(kubescape version)"

      - name: Find and verify Kubernetes manifests
        id: find-manifests
        run: |
          MANIFESTS=$(find . -name '*.yaml' -o -name '*.yml' | grep -v 'scan-results' | tr '\n' ' ')
          
          if [ -z "$MANIFESTS" ]; then
            echo "::error::❌ Aucun manifest Kubernetes trouvé!"
            exit 1
          fi
          
          echo "📄 Fichiers à analyser:"
          echo "$MANIFESTS" | tr ' ' '\n'
          echo "MANIFESTS=${MANIFESTS}" >> $GITHUB_OUTPUT
      - name: Install Pandoc and LaTeX dependencies
        run: |
          sudo apt update && sudo apt install -y \
            pandoc \
            texlive-xetex \
            fonts-dejavu \
            fonts-liberation
      - name: Run Kubescape scan with debug
        run: |
          echo "🚀 Exécution du scan sur: ${{ steps.find-manifests.outputs.MANIFESTS }}"
          
          kubescape scan ${{ steps.find-manifests.outputs.MANIFESTS }} \
            --format json \
            --output .github/reports/scan-results.json \
            2>&1 | tee scan-debug.log

          if [ ! -s ".github/reports/scan-results.json" ]; then
            echo "::error::❌ Le rapport est vide!"
            cat scan-debug.log
            exit 1
          fi

      - name: Generate human-readable summary table and recommendations
        run: |
          echo "📊 Génération du résumé et des recommandations..."
          .github/scripts/scanning/generate-table.sh > .github/reports/table-summary.md

      - name: Generate PDF Report
        run: |
          echo "🖨️ Génération du rapport PDF..."
          python .github/scripts/scanning/send-report.py
