import os
from typing import Dict
import smtplib
from email.message import EmailMessage
from agents import Agent, function_tool


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body"""
    mailtrap_username = os.getenv('MAILTRAP_USERNAME')
    mailtrap_password = os.getenv('MAILTRAP_PASSWORD')

    if not mailtrap_username or not mailtrap_password:
        return {"status": "error", "message": "Identifiants Mailtrap non configurés dans le .env"}

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "sales@complai.com"
    msg['To'] = "ceo@example.com"
    msg.set_content("Veuillez utiliser un client mail supportant le HTML pour lire ce message.")
    msg.add_alternative(html_body, subtype='html')

    try:
        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
            server.starttls()
            server.login(mailtrap_username, mailtrap_password)
            server.send_message(msg)
        return {"status": "success", "message": "Email envoyé vers Mailtrap avec succès"}
    except Exception as e:
        return {"status": "error", "message": f"Erreur lors de l'envoi : {str(e)}"}


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
