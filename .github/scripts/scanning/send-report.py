#!/usr/bin/env python3
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_report():
    report_path = os.path.join(os.environ['GITHUB_WORKSPACE'], '.github', 'reports', 'scan-results.json')
    
    msg = MIMEMultipart()
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['REPORT_EMAIL']
    msg['Subject'] = 'Kubescape Scan Report'
    
    body = "Veuillez trouver ci-joint le rapport de scan Kubescape."
    msg.attach(MIMEText(body, 'plain'))
    
    with open(report_path, 'rb') as f:
        part = MIMEApplication(f.read(), Name='scan-results.json')
        part['Content-Disposition'] = f'attachment; filename="scan-results.json"'
        msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.environ['GMAIL_USER'], os.environ['GMAIL_PASSWORD'])
        server.sendmail(os.environ['GMAIL_USER'], os.environ['REPORT_EMAIL'], msg.as_string())

if __name__ == "__main__":
    send_report()
