#!/usr/bin/env python3
import os
import smtplib
import json
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import subprocess

def generate_pdf_report(json_path, pdf_path):
    """Génère un PDF via Pandoc à partir des données JSON"""
    
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier JSON: {e}")
        exit(1)

    summary = data.get("summary", {})
    controls = data.get("results", [{}])[0].get("controls", [])

    md_content = f"""# Rapport de Sécurité Kubernetes
**Date** : {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Résumé Global
- **Score de sécurité** : {summary.get('score', 'N/A')}%
- **Risques critiques** : {summary.get('criticalCount', 0)}
- **Risques élevés** : {summary.get('highCount', 0)}
- **Risques moyens** : {summary.get('mediumCount', 0)}
- **Risques faibles** : {summary.get('lowCount', 0)}

## Vulnérabilités Détectées
"""

    for control in controls:
        status = str(control.get("status", "unknown"))  # Convertir en string
        name = str(control.get("name", "Inconnue"))
        description = str(control.get("description", "Aucune description fournie."))
        remediation = str(control.get("remediation", "Aucune remédiation fournie."))

        md_content += f"""
### ❌ {name} ({status.upper()})
**Description** : {description}
**Remédiation** : {remediation}
"""

    md_path = os.path.join(os.path.dirname(pdf_path), 'temp_report.md')
    try:
        with open(md_path, 'w') as f:
            f.write(md_content)
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture du fichier Markdown : {e}")
        exit(1)

    try:
        subprocess.run([
            'pandoc', md_path,
            '-o', pdf_path,
            '--template=eisvogel',
            '--pdf-engine=xelatex',
            '-V', 'mainfont=DejaVu Sans',
            '-V', 'geometry:margin=2cm'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la génération du PDF : {e}")
        exit(1)

    os.remove(md_path)

def send_reports(json_path, pdf_path):
    msg = MIMEMultipart()
    msg['From'] = os.environ.get('GMAIL_USER')
    msg['To'] = os.environ.get('REPORT_TO')
    msg['Subject'] = f"Rapport de Sécurité Kubernetes - {datetime.now().strftime('%d/%m/%Y')}"

    body = f"""
    <html>
      <body>
        <h2>Analyse de Sécurité Kubernetes</h2>
        <p>Veuillez trouver ci-joint :</p>
        <ul>
          <li><b>Rapport PDF</b> - Synthèse des vulnérabilités</li>
          <li><b>Données complètes (JSON)</b> - Pour analyse technique</li>
        </ul>
        <p><i>Ce rapport a été généré automatiquement par Kubescape.</i></p>
      </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    for file_path, display_name in [
        (pdf_path, "Rapport_Securite_Kubernetes.pdf"),
        (json_path, "Resultats_Kubescape.json")
    ]:
        if not os.path.exists(file_path):
            print(f"⚠️ Fichier manquant : {file_path}")
            continue

        with open(file_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=display_name)
            part['Content-Disposition'] = f'attachment; filename="{display_name}"'
            msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(msg['From'], os.environ.get('GMAIL_PASSWORD'))
            server.send_message(msg)
        print("✅ Rapports générés et envoyés avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {e}")
        exit(1)

if __name__ == "__main__":
    workspace = os.environ.get('GITHUB_WORKSPACE', '.')
    json_path = os.path.join(workspace, '.github', 'reports', 'scan-results.json')
    pdf_path = os.path.join(workspace, '.github', 'reports', 'security-report.pdf')

    try:
        generate_pdf_report(json_path, pdf_path)
        send_reports(json_path, pdf_path)
    except Exception as e:
        print(f"❌ Erreur générale : {e}")
        exit(1)
