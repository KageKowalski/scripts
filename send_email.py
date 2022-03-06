# Sends an email


# Imports
import env_var
from ssl import create_default_context
from smtplib import SMTP_SSL


# Sends an email to receiver (string)
# Message sent is made of subject (string) and body (string)
def send_email(receiver, subject, body):
    # Get sender username and password from credentials file
    sender_username = ''
    sender_password = ''
    with open(env_var.CRED_PATH + env_var.EMAIL_CRED_FILE, mode='r') as f:
        sender_username = f.readline().strip()
        sender_password = f.readline().strip()

    # Setup SMTP server
    port = 465
    smtp_server = "smtp.gmail.com"
    context = create_default_context()
    with SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_username, sender_password)
        server.sendmail(sender_username, receiver, "Subject: " + subject + "\n\n" + body)
