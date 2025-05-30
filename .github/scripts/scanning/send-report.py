#!/usr/bin/env python3
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate

def send_reports():
    # Chemins des fichiers
    workspace = os.environ.get('GITHUB_WORKSPACE', '.')
    json_path = os.path.join(workspace, '.github', 'reports', 'scan-results.json')
    pdf_path = os.path.join(workspace, '.github', 'reports', 'security-report.pdf')
    
    # Vérification que les fichiers existent
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Fichier JSON introuvable : {json_path}")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Fichier PDF introuvable : {pdf_path}")

    # Configuration du message
    msg = MIMEMultipart()
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['REPORT_EMAIL']
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = '🔒 Rapport de Sécurité Kubernetes - Kubescape'
    
    # Corps du message (version HTML + texte)
    html_body = f"""
    <html>
      <body>
        <h2>Rapport d'Analyse de Sécurité Kubernetes</h2>
        <p>Bonjour,</p>
        <p>Veuillez trouver ci-joint les résultats du scan Kubescape :</p>
        <ul>
          <li><strong>Rapport détaillé (JSON)</strong> : Pour analyse automatisée</li>
          <li><strong>Synthèse PDF</strong> : Version imprimable avec priorités</li>
        </ul>
        <p>Bonne journée,<br/>L'équipe DevOps</p>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(html_body, 'html'))
    msg.attach(MIMEText("Rapports Kubescape en pièces jointes.", 'plain'))  # Fallback texte

    # Attachement des fichiers
    for filepath, filename in [
        (json_path, 'kubescape-results.json'),
        (pdf_path, 'security-report.pdf')
    ]:
        with open(filepath, 'rb') as f:
            part = MIMEApplication(
                f.read(),
                Name=filename
            )
            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            msg.attach(part)

    # Envoi via SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.environ['GMAIL_USER'], os.environ['GMAIL_PASSWORD'])
        server.send_message(msg)
        print("✅ Rapports envoyés avec succès !")

if __name__ == "__main__":
    try:
        send_reports()
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {str(e)}")
        exit(1)
