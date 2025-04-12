import smtplib
from email.mime.text import MIMEText



import os

# Récupérer les informations sensibles depuis les variables d'environnement
email_address = os.getenv("OUTLOOK_EMAIL", "ktdtchofo@gmail.com")  # Remplacez par votre email Outlook
email_password = os.getenv("OUTLOOK_PASSWORD", "zqxp ovdk baaj ugvx")  # Remplacez par votre mot de passe

# Préparer le message
ms = "first_message"
msg = MIMEText(ms)
msg['Subject'] = "Alerte Baisse de Prix Adidas"
msg['From'] = email_address
msg['To'] = email_address

try:
    # Envoyer l'email via Outlook
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Activer le chiffrement TLS
        server.login(email_address, email_password)
        server.sendmail(email_address, email_address, msg.as_string())
    print("Email envoyé avec succès!")
except smtplib.SMTPAuthenticationError:
    print("Erreur d'authentification : Vérifiez votre email et mot de passe.")
except smtplib.SMTPException as e:
    print(f"Erreur SMTP : {e}")
except Exception as e:
    print(f"Une erreur inattendue s'est produite : {e}")