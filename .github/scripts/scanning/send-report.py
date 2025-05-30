#!/usr/bin/env python3
import os
import smtplib
import json
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_pdf_report(json_path, pdf_path):
    """Génère un PDF professionnel à partir des résultats JSON"""
    
    # Supprimer l'ancien PDF s'il existe
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    
    # Charger les données JSON
    with open(json_path) as f:
        scan_data = json.load(f)
    
    # Création du PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Titre et métadonnées
    story.append(Paragraph("Rapport de Sécurité Kubernetes", styles['Title']))
    story.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 24))
    
    # Résumé global
    summary = scan_data.get('summary', {})
    story.append(Paragraph("Résumé Global", styles['Heading2']))
    
    summary_data = [
        ["Score de sécurité", f"{summary.get('score', 'N/A')}%"],
        ["Risques critiques", summary.get('criticalCount', 0)],
        ["Risques élevés", summary.get('highCount', 0)],
        ["Ressources analysées", summary.get('resourceCount', 0)]
    ]
    
    summary_table = Table(summary_data, colWidths=[200, 100])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 24))
    
    # Détails des vulnérabilités
    story.append(Paragraph("Vulnérabilités Détectées", styles['Heading2']))
    
    for control in scan_data.get('results', [{}])[0].get('controls', []):
        if control.get('status') != 'passed':
            status_color = colors.red if control['status'] == 'failed' else colors.orange
            story.append(Paragraph(
                f"<font color='{status_color}'><b>{control['status'].upper()}</b></font> - {control['name']}",
                styles['Heading3']))
            
            story.append(Paragraph(f"<b>Description:</b> {control.get('description', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"<b>Remédiation:</b> {control.get('remediation', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 12))
    
    # Génération finale
    doc.build(story)
    return pdf_path

def send_reports(json_path, pdf_path):
    """Envoie les rapports par email"""
    
    msg = MIMEMultipart()
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['REPORT_TO']
    msg['Subject'] = f"Rapport de Sécurité Kubernetes - {datetime.now().strftime('%d/%m/%Y')}"
    
    # Corps du message
    body = f"""
    <html>
      <body>
        <h2>Analyse de Sécurité Kubernetes</h2>
        <p>Veuillez trouver ci-joint :</p>
        <ul>
          <li><b>Rapport PDF</b> - Synthèse des vulnérabilités</li>
          <li><b>Données complètes (JSON)</b> - Pour analyse technique</li>
        </ul>
        <p><i>Ce rapport a été généré automatiquement par Kubescape.</i></p>
      </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))
    
    # Ajout des pièces jointes
    for file_path, display_name in [
        (pdf_path, "Rapport_Securite_Kubernetes.pdf"),
        (json_path, "Resultats_Kubescape.json")
    ]:
        with open(file_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=display_name)
            part['Content-Disposition'] = f'attachment; filename="{display_name}"'
            msg.attach(part)
    
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
        pdf_path = os.path.join(workspace, '.github', 'reports', 'security-report.pdf')
        
        # Génération du nouveau PDF
        generate_pdf_report(json_path, pdf_path)
        
        # Envoi des rapports
        send_reports(json_path, pdf_path)
        print("✅ Rapports générés et envoyés avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        exit(1)
