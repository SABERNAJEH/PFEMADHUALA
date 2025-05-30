#!/usr/bin/env python3
import os
import smtplib
import json
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF
import tempfile

class SecurityPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Rapport de Sécurité Kubernetes', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f"Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(json_path):
    pdf = SecurityPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Style personnalisé
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    
    # Charger les données JSON
    with open(json_path) as f:
        data = json.load(f)
    
    # Section Résumé
    pdf.cell(0, 10, 'Résumé Global', 0, 1, 'L', 1)
    pdf.set_font('Arial', '', 10)
    
    summary = data.get('summary', {})
    pdf.multi_cell(0, 7, 
        f"Score de sécurité: {summary.get('score', 'N/A')}%\n"
        f"Risques critiques: {summary.get('criticalCount', 0)}\n"
        f"Risques élevés: {summary.get('highCount', 0)}\n"
        f"Ressources analysées: {summary.get('resourceCount', 0)}", 0, 1)
    
    # Détails des vulnérabilités
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Vulnérabilités Détectées', 0, 1, 'L', 1)
    pdf.set_font('Arial', '', 10)
    
    for control in data.get('results', [{}])[0].get('controls', []):
        if control.get('status') != 'passed':
            pdf.set_font('', 'B')
            pdf.cell(0, 7, f"[{control.get('status').upper()}] {control.get('name')}", 0, 1)
            pdf.set_font('', '')
            pdf.multi_cell(0, 6, f"Description: {control.get('description', 'N/A')}\n"
                                f"Remédiation: {control.get('remediation', 'N/A')}\n", 0, 1)
            pdf.ln(2)
    
    # Enregistrer le PDF
    output_path = os.path.join(tempfile.gettempdir(), 'k8s_security_report.pdf')
    pdf.output(output_path)
    return output_path

def send_email_with_reports(pdf_path, json_path):
    msg = MIMEMultipart()
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['REPORT_EMAIL']
    msg['Subject'] = f"Rapport de Sécurité Kubernetes - {datetime.now().strftime('%d/%m/%Y')}"
    
    # Corps du message
    body = f"""
    <h3>Rapport d'Analyse de Sécurité</h3>
    <p>Veuillez trouver ci-joint :</p>
    <ul>
        <li>Le <b>rapport détaillé (PDF)</b> avec synthèse visuelle</li>
        <li>Les <b>données brutes (JSON)</b> pour analyse approfondie</li>
    </ul>
    <p>Recommandations :</p>
    <ol>
        <li>Traiter d'abord les risques <span style='color:red;'>critiques</span></li>
        <li>Vérifier les configurations anormales</li>
        <li>Consulter les suggestions de remédiation</li>
    </ol>
    """
    msg.attach(MIMEText(body, 'html'))
    
    # Attachement PDF
    with open(pdf_path, 'rb') as f:
        pdf_part = MIMEApplication(f.read(), _subtype='pdf')
        pdf_part.add_header('Content-Disposition', 'attachment', filename='Rapport_Securite_Kubernetes.pdf')
        msg.attach(pdf_part)
    
    # Attachement JSON
    with open(json_path, 'rb') as f:
        json_part = MIMEApplication(f.read(), _subtype='json')
        json_part.add_header('Content-Disposition', 'attachment', filename='Donnees_Completes.json')
        msg.attach(json_part)
    
    # Envoi
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.environ['GMAIL_USER'], os.environ['GMAIL_PASSWORD'])
        server.send_message(msg)

if __name__ == "__main__":
    try:
        # Chemins des fichiers
        workspace = os.environ.get('GITHUB_WORKSPACE', '.')
        json_path = os.path.join(workspace, '.github', 'reports', 'scan-results.json')
        
        # Génération du PDF
        pdf_path = generate_pdf_report(json_path)
        
        # Envoi des rapports
        send_email_with_reports(pdf_path, json_path)
        print("✅ Rapport envoyé avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        exit(1)
