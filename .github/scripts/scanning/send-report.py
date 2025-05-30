#!/usr/bin/env python3
import os
import smtplib
import json
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_security_reports():
    # Chemins des fichiers (doivent correspondre à ceux du workflow)
    workspace = os.environ.get('GITHUB_WORKSPACE', '.')
    json_report = os.path.join(workspace, '.github', 'reports', 'scan-results.json')
    pdf_report = os.path.join(workspace, '.github', 'reports', 'security-report.pdf')
    
    # Vérification des fichiers
    if not os.path.exists(json_report):
        raise FileNotFoundError(f"Fichier JSON manquant: {json_report}")
    if not os.path.exists(pdf_report):
        raise FileNotFoundError(f"Fichier PDF manquant: {pdf_report}")

    # Configuration de l'email
    msg = MIMEMultipart()
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['REPORT_EMAIL']
    msg['Subject'] = f"Rapport de Sécurité Kubernetes - {datetime.now().strftime('%d/%m/%Y')}"

    # Corps du message (HTML + texte simple)
    email_body = f"""
    <html>
      <body>
        <h2>Rapport d'Analyse Kubescape</h2>
        <p>Bonjour,</p>
        <p>Veuillez trouver ci-joint les résultats du scan de sécurité :</p>
        <ul>
          <li><a href="#pdf">Rapport PDF</a> - Synthèse visuelle</li>
          <li><a href="#json">Données complètes (JSON)</a> - Pour analyse technique</li>
        </ul>
        <p>Recommandations :</p>
        <ol>
          <li>Prioriser les risques <span style='color:red;font-weight:bold;'>critiques</span></li>
          <li>Vérifier les configurations anormales</li>
          <li>Consulter les suggestions de remédiation</li>
        </ol>
        <p>Cordialement,<br/>Équipe DevOps</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(email_body, 'html'))
    msg.attach(MIMEText("Rapports de sécurité en pièces jointes.", 'plain'))  # Version texte

    # Ajout des pièces jointes
    for filepath, filename in [
        (pdf_report, "Rapport_Securite.pdf"),
        (json_report, "Resultats_Complets.json")
    ]:
        with open(filepath, "rb") as attachment:
            part = MIMEApplication(
                attachment.read(),
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
        send_security_reports()
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {str(e)}")
        exit(1)
