#!/usr/bin/env python3
import os
import smtplib
import json
import subprocess
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def generate_pdf_report(json_path, pdf_path):
    """Génère un PDF via Pandoc à partir des données JSON"""
    
    # Supprimer l'ancien PDF s'il existe
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    
    # Convertir JSON en Markdown temporaire
    with open(json_path) as f:
        data = json.load(f)
    
    md_content = f"""
# Rapport de Sécurité Kubernetes
**Date** : {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Résumé Global
- **Score de sécurité** : {data.get('summary', {}).get('score', 'N/A')}%
- **Risques critiques** : {data.get('summary', {}).get('criticalCount', 0)}
- **Risques élevés** : {data.get('summary', {}).get('highCount', 0)}

## Vulnérabilités Détectées
"""
    
    for control in data.get('results', [{}])[0].get('controls', []):
        if control.get('status') != 'passed':
            status_emoji = "❌" if control['status'] == 'failed' else "⚠️"
            md_content += f"""
### {status_emoji} {control['name']} ({control['status'].upper()})
**Description** : {control.get('description', 'N/A')}  
**Remédiation** : {control.get('remediation', 'N/A')}  
"""
    
    # Écrire le contenu Markdown temporaire
    md_path = os.path.join(os.path.dirname(pdf_path), 'temp_report.md')
    with open(md_path, 'w') as f:
        f.write(md_content)
    
    # Convertir en PDF avec Pandoc
    subprocess.run([
        'pandoc', md_path,
        '-o', pdf_path,
        '--template=eisvogel',
        '--pdf-engine=xelatex',
        '-V', 'mainfont=DejaVu Sans',
        '-V', 'geometry:margin=2cm'
    ], check=True)
    
    # Nettoyer le fichier temporaire
    os.remove(md_path)

def send_reports(json_path, pdf_path):
    """Envoie les rapports par email"""
    
    msg = MIMEMultipart()
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['REPORT_TO']
    msg['Subject'] = f"Rapport de Sécurité Kubernetes - {datetime.now().strftime('%d/%m/%Y')}"
    
    # Corps du message
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
    
    # Ajout des pièces jointes
    for file_path, display_name in [
        (pdf_path, "Rapport_Securite_Kubernetes.pdf"),
        (json_path, "Resultats_Kubescape.json")
    ]:
        with open(file_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=display_name)
            part['Content-Disposition'] = f'attachment; filename="{display_name}"'
            msg.attach(part)
    
    # Envoi
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.environ['GMAIL_USER'], os.environ['GMAIL_PASSWORD'])
        server.send_message(msg)

if __name__ == "__main__":
    try:
        # Chemins des fichiers
        workspace = os.environ.get('GITHUB_WORKSPACE', '.')
        json_path = os.path.join(workspace, '.github', 'reports', 'scan-results.json')
        pdf_path = os.path.join(workspace, '.github', 'reports', 'security-report.pdf')
        
        # Génération du nouveau PDF
        generate_pdf_report(json_path, pdf_path)
        
        # Envoi des rapports
        send_reports(json_path, pdf_path)
        print("✅ Rapports générés et envoyés avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        exit(1)
