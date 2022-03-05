# Sends an email


# Imports
from ssl import create_default_context
from smtplib import SMTP_SSL


# Constants
CREDENTIALS_PATH = "../.cred/"
CREDENTIALS_FILE = "email_credentials.txt"


# Sends an email to receiver (string)
# Message sent is made of subject (string) and body (string)
def send_email(receiver, subject, body):
    # Get sender username and password from credentials file
    sender_username = ''
    sender_password = ''
    with open(CREDENTIALS_PATH + CREDENTIALS_FILE, mode='r') as f:
        sender_username = f.readline().strip()
        sender_password = f.readline().strip()

    # Setup SMTP server
    port = 465
    smtp_server = "smtp.gmail.com"
    context = create_default_context()
    with SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_username, sender_password)
        server.sendmail(sender_username, receiver, "Subject: " + subject + "\n\n" + body)
