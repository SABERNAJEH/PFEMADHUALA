import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys

def send_email(to_emails, subject="🔄 Modification du Repository PFEMADHUALA", body="Une modification a été détectée dans le repository."):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv('GMAIL_USERNAME')
    sender_password = os.getenv('GMAIL_PASSWORD')
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_emails
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_emails.split(','), msg.as_string())
        server.quit()
        print("Email envoyé avec succès!")
    except Exception as e:
        print(f"Échec d'envoi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    recipients = sys.argv[1]
    repo_name = os.getenv('GITHUB_REPOSITORY', 'PFEMADHUALA')
    commit_sha = os.getenv('GITHUB_SHA', 'latest commit')
    repo_url = f"https://github.com/{repo_name}"
    commit_url = f"{repo_url}/commit/{commit_sha}"
    
    email_body = f"""
    🚨 Alerte de Modification - PFEMADHUALA
    
    Une nouvelle modification a été détectée dans le repository:
    
    Repository: {repo_name}
    Commit SHA: {commit_sha}
    Lien du commit: {commit_url}
    Lien du repository: {repo_url}
    
    Les scans de sécurité Kubescape et Trivy vont maintenant s'exécuter sur le code modifié.
    """
    
    send_email(recipients, body=email_body)
