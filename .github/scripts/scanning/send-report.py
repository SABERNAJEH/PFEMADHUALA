import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

def ensure_report_exists(file_path):
    """Crée un rapport vide si le fichier n'existe pas"""
    if not os.path.exists(file_path):
        print(f"Creating empty report at {file_path}")
        with open(file_path, 'w') as f:
            json.dump({"status": "error", "message": "Report file was not generated"}, f)

def load_report(file_path):
    """Charge un rapport JSON avec gestion des erreurs"""
    try:
        ensure_report_exists(file_path)
        with open(file_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading report {file_path}: {str(e)}")
        return {"error": str(e)}

def generate_email_content():
    """Génère le contenu HTML de l'email"""
    return """
    <h1>Rapport de Sécurité Kubernetes</h1>
    <p>Veuillez trouver ci-joint les rapports de scan de sécurité.</p>
    <ul>
      <li>Kubescape: Analyse des configurations Kubernetes</li>
      <li>Trivy: Analyse des vulnérabilités et secrets</li>
    </ul>
    """

def send_email_with_attachments():
    """Envoie l'email avec les pièces jointes"""
    # Configuration de l'email
    msg = MIMEMultipart()
    msg['From'] = os.getenv('GMAIL_USER')
    msg['To'] = os.getenv('REPORT_EMAIL')
    msg['Subject'] = "Rapport de Sécurité Kubernetes - " + os.getenv('GITHUB_RUN_ID', '')
    
    # Corps du message
    msg.attach(MIMEText(generate_email_content(), 'html'))
    
    # Pièces jointes
    attachments = [
        os.getenv('KUBESCAPE_REPORT_PATH'),
        os.getenv('TRIVY_REPORT_PATH')
    ]
    
    for attachment in attachments:
        if attachment and os.path.exists(attachment):
            with open(attachment, "rb") as f:
                part = MIMEApplication(
                    f.read(),
                    Name=Path(attachment).name
                )
                part['Content-Disposition'] = f'attachment; filename="{Path(attachment).name}"'
                msg.attach(part)
        else:
            print(f"Fichier non trouvé: {attachment}")

    # Envoi de l'email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASSWORD'))
            server.send_message(msg)
        print("Email envoyé avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Vérification des variables d'environnement
        required_vars = ['GMAIL_USER', 'GMAIL_PASSWORD', 'REPORT_EMAIL']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Variables manquantes: {', '.join(missing_vars)}")
        
        send_email_with_attachments()
    except Exception as e:
        print(f"ERREUR: {str(e)}")
        exit(1)
