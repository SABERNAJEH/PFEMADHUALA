import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

def send_report():
    sender_email = os.getenv('GMAIL_USER')
    sender_password = os.getenv('GMAIL_PASSWORD')
    recipient = os.getenv('REPORT_EMAIL')
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = '📊 Rapport de Scan - PFEMADHUALA'
    
    body = """
    Bonjour,
    
    Veuillez trouver ci-joint le rapport de sécurité généré par Kubescape.
    
    Cordialement,
    Votre Pipeline CI/CD
    """
    msg.attach(MIMEText(body, 'plain'))
    
    with open('scan-results.json', 'rb') as f:
        attach = MIMEApplication(f.read(), _subtype='json')
        attach.add_header('Content-Disposition', 'attachment', filename='scan-results.json')
        msg.attach(attach)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        print("📤 Rapport envoyé avec succès!")
    except Exception as e:
        print(f"❌ Échec d'envoi du rapport: {e}")
        exit(1)

if __name__ == "__main__":
    send_report()
