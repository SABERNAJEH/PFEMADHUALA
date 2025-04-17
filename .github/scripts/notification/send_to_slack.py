import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_alert(issues):
    blocks = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*{len(issues)} security issues found*"
        }
    }]
    
    for issue in issues[:5]:  # Limite à 5 pour Slack
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{issue['severity']}*: {issue['name']}\n*Resource*: {issue['resource']}"
            }
        })
    
    requests.post(
        os.getenv("SLACK_WEBHOOK"),
        json={"blocks": blocks}
    )
