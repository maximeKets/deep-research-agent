import os
import smtplib
from email.message import EmailMessage
from typing import Dict
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


INSTRUCTIONS = """Vous êtes capable d'envoyer un e-mail au format HTML joliment présenté à partir d'un rapport détaillé.
Un rapport détaillé vous sera fourni. Vous devez utiliser votre outil pour envoyer un e-mail unique, en y intégrant 
le rapport converti en un code HTML propre et bien présenté, avec un objet approprié.
Après l'envoi de l'e-mail, vous DEVEZ retourner le contenu intégral du rapport original comme résultat final (au format Markdown).
Ne le résumez pas et ne le tronquez pas."""


email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
    handoff_description="Convertir un rapport en HTML et l'envoyer par e-mail, puis retourner le rapport complet.",
)
