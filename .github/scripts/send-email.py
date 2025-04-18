import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import json
import os

# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Lecture du rapport JSON
with open("results.json", "r") as f:
    scan_results = json.load(f)

# Création de l'email
msg = MIMEMultipart()
msg["From"] = SMTP_USER
msg["To"] = RECIPIENT_EMAIL
msg["Subject"] = "🔍 Kubescape Scan Report - Minikube Cluster"

# Corps du message (HTML)
body = f"""
<h1>Kubescape Scan Report</h1>
<p><strong>Cluster:</strong> Minikube</p>
<p><strong>Total Failures:</strong> {scan_results.get("summary", {}).get("failed", 0)}</p>
<p><strong>Critical Issues:</strong> {scan_results.get("summary", {}).get("critical", 0)}</p>
<pre>{json.dumps(scan_results, indent=2)}</pre>
"""
msg.attach(MIMEText(body, "html"))

# Ajout du fichier JSON en pièce jointe
with open("results.json", "rb") as f:
    part = MIMEApplication(f.read(), Name="kubescape-report.json")
    part["Content-Disposition"] = 'attachment; filename="kubescape-report.json"'
    msg.attach(part)

# Envoi de l'email
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, RECIPIENT_EMAIL, msg.as_string())
    print("📧 Email envoyé avec succès !")
except Exception as e:
    print(f"❌ Erreur lors de l'envoi de l'email : {e}")
