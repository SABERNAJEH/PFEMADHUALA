import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

def load_report(file_path):
    with open(file_path) as f:
        return json.load(f)

def generate_summary(kubescape_data, trivy_data):
    summary = {
        "kubescape": {
            "passed": kubescape_data.get("summary", {}).get("passed", 0),
            "failed": kubescape_data.get("summary", {}).get("failed", 0)
        },
        "trivy": {
            "vulnerabilities": len(trivy_data.get("Results", []))
        }
    }
    return summary

def send_email(summary, attachments):
    msg = MIMEMultipart()
    msg['From'] = os.getenv('GMAIL_USER')
    msg['To'] = os.getenv('REPORT_EMAIL')
    msg['Subject'] = "Rapport de Sécurité Kubernetes"

    body = f"""
    Résumé des Scans:
    - Kubescape: {summary['kubescape']['passed']} contrôles passés, {summary['kubescape']['failed']} échoués.
    - Trivy: {summary['trivy']['vulnerabilities']} vulnérabilités détectées.
    """
    msg.attach(MIMEText(body, 'plain'))

    for file in attachments:
        with open(file, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(file))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file)}"'
            msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASSWORD'))
        server.sendmail(os.getenv('GMAIL_USER'), os.getenv('REPORT_EMAIL'), msg.as_string())

if __name__ == "__main__":
    kubescape_report = os.path.join(os.getenv('GITHUB_WORKSPACE'), '.github', 'reports', 'kubescape-scan.json')
    trivy_report = os.path.join(os.getenv('GITHUB_WORKSPACE'), '.github', 'reports', 'trivy-scan.json')
    
    kubescape_data = load_report(kubescape_report)
    trivy_data = load_report(trivy_report)
    
    summary = generate_summary(kubescape_data, trivy_data)
    send_email(summary, [kubescape_report, trivy_report])
