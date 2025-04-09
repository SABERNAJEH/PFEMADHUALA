#!/usr/bin/env python3
import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_emails):
    # Vérification des variables d'environnement
    sender_email = os.getenv('GMAIL_USER')
    sender_password = os.getenv('GMAIL_PASSWORD')
    
    if not sender_email or not sender_password:
        print("❌ Erreur: GMAIL_USER ou GMAIL_PASSWORD non défini")
        sys.exit(1)

    # Configuration du message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_emails
    msg['Subject'] = "Notification GitHub Actions"
    
    body = f"""
    Nouvelle modification détectée dans le repository.
    Repository: {os.getenv('GITHUB_REPOSITORY', 'inconnu')}
    Commit: {os.getenv('GITHUB_SHA', 'inconnu')}
    """
    msg.attach(MIMEText(body, 'plain'))

    # Envoi de l'email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_emails.split(','), msg.as_string())
        print("✅ Email envoyé avec succès")
    except Exception as e:
        print(f"❌ Échec d'envoi: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send-alert.py recipient1@example.com,recipient2@example.com")
        sys.exit(1)
    
    send_email(sys.argv[1])
