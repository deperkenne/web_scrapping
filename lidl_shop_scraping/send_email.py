import os
from email.message import EmailMessage

from dotenv import load_dotenv
import smtplib
from email.utils import formataddr
from pathlib import Path

PORT = 587
EMAIL_SERVER = "smtp.gmail.com"

#Load the environment
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env.txt"
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")
print(sender_email)
print(password_email)

def send_email(subject,receiver_email,name,due_date,invoice_no):
    # Create the base text message
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Coding Is Fun Corp.", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        Hi {name},
        I hope you enjoy you days 
        I just want to take some time with you cann you 
        have a nice day 
        """
    )
    msg.add_alternative(
       f"""\
    <html>
      <body>
        <p>Hi <strong>Rodrigue</strong> </p>
        <p>cann you read my email please. </p>
      </body>
    </html>
    """,
        subtype="html"
    )
    try:
        with smtplib.SMTP(EMAIL_SERVER,PORT) as server:
            server.starttls()
            server.login(sender_email,password_email)
            server.sendmail(sender_email,receiver_email,msg.as_string())
    except smtplib.SMTPAuthenticationError:
        print("Erreur d'authentification : Vérifiez votre email et mot de passe.")
    except smtplib.SMTPException as e:
        print(f"Erreur SMTP : {e}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")



if __name__ == "__main__":
    send_email(
        subject="Alert to answer",
        receiver_email="tchofodep@gmail.com",
        name="deper",
        due_date="11, Aug 2022",
        invoice_no="INV-21-12-009"
    )