
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_EMAIL = "bindu@gmail.com"
SENDER_PASSWORD = ""  # Replace with your actual email password

def send_mail(to, subject, message_body):
    server = None
    try:
        # Create message
        msg = MIMEMultipart()
        msg["To"] = to
        msg["From"] = SENDER_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(message_body, "html"))

        # Connect to SMTP server
        server = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)

        # Login to the email account
        server.login(user=SENDER_EMAIL, password=SENDER_PASSWORD)

        # Send the email
        server.send_message(msg)
        print("Email sent successfully.")

    except ConnectionRefusedError as e:
        print(f"Error: Connection to SMTP server refused. {e}")
    except smtplib.SMTPException as e:
        print(f"Error: SMTP Exception. {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred. {e}")
    finally:
        # Close the connection
        if server:
            server.quit()

