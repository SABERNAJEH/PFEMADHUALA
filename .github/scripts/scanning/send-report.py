import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_report():
    try:
        # Chemin absolu vers le fichier de rapport
        report_path = os.path.join(os.getcwd(), '.github', 'reports', 'scan-results.json')
        
        # Vérification que le fichier existe
        if not os.path.exists(report_path):
            raise FileNotFoundError(f"Le fichier de rapport {report_path} n'existe pas")

        # Configuration email
        sender = os.getenv('GMAIL_USER')
        password = os.getenv('GMAIL_PASSWORD')
        recipient = os.getenv('REPORT_EMAIL')

        if not all([sender, password, recipient]):
            raise ValueError("Variables d'environnement manquantes")

        # Construction du message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = '📊 Rapport de Scan - PFEMADHUALA'
        
        msg.attach(MIMEText("Veuillez trouver ci-joint le rapport de scan.", 'plain'))

        # Ajout de la pièce jointe
        with open(report_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name='scan-results.json')
            part['Content-Disposition'] = f'attachment; filename="scan-results.json"'
            msg.attach(part)

        # Envoi
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        
        print("✅ Rapport envoyé avec succès")

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    send_report()
