import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def load_report(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading report {file_path}: {str(e)}")
        return {"error": str(e)}

def generate_email_content(kubescape_data, trivy_data):
    # Kubescape summary
    kubescape_summary = kubescape_data.get("summary", {})
    ks_passed = kubescape_summary.get("passed", "N/A")
    ks_failed = kubescape_summary.get("failed", "N/A")
    
    # Trivy summary
    trivy_vulns = len(trivy_data.get("Results", []))
    
    return f"""
    <h1>Rapport de Sécurité Kubernetes</h1>
    
    <h2>Kubescape</h2>
    <ul>
      <li>Contrôles passés: {ks_passed}</li>
      <li>Contrôles échoués: {ks_failed}</li>
    </ul>
    
    <h2>Trivy</h2>
    <ul>
      <li>Vulnérabilités détectées: {trivy_vulns}</li>
    </ul>
    """

def send_email(content, attachments=[]):
    msg = MIMEMultipart()
    msg['From'] = os.getenv('GMAIL_USER')
    msg['To'] = os.getenv('REPORT_EMAIL')
    msg['Subject'] = "Rapport de Sécurité Kubernetes"
    
    msg.attach(MIMEText(content, 'html'))
    
    for attachment in attachments:
        if os.path.exists(attachment):
            with open(attachment, "rb") as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASSWORD'))
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Get report paths from environment
        report_dir = os.path.join(os.getenv('GITHUB_WORKSPACE'), '.github', 'reports')
        kubescape_report = os.path.join(report_dir, 'kubescape.json')
        trivy_report = os.path.join(report_dir, 'trivy.json')
        
        # Load reports
        kubescape_data = load_report(kubescape_report)
        trivy_data = load_report(trivy_report)
        
        # Generate and send email
        email_content = generate_email_content(kubescape_data, trivy_data)
        send_email(email_content, [kubescape_report, trivy_report])
        
    except Exception as e:
        print(f"Script failed: {str(e)}")
        exit(1)
