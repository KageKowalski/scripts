# Utility functions for interacting with the OS


# Imports
import os
from smtplib import SMTP_SSL
from ssl import create_default_context
from time import time


# Deletes all files contained in directory (String)
# If days (Integer) is passed a value, only files that were last modified days (Integer) days ago or more are deleted
# Only deletes directories in addition to files if ignore_directories (Boolean) is set to False
def clean_dir(directory, days=0, ignore_directories=True):
    now = time()
    for item in os.scandir(directory):
        if os.stat(item).st_mtime <= now - days * 86400:
            if ignore_directories and item.is_file():
                os.remove(item.path)
            elif not ignore_directories and (item.is_file() or item.is_dir()):
                os.remove(item.path)


# Touches all files that begin with prefix (String) and are located at directory (String)
# Assumes that all touched files' names contain a number between their prefixes and their file extensions
# Increments the number contained by each filename by increment_value (Integer)
def increment_filename_numbers(directory, prefix, increment_value=1):
    for item in os.scandir(directory):
        if item.is_file() and item.name.startswith(prefix):
            os.rename(item.path,
                      directory +
                      item.name[:len(prefix)] +
                      str((int(item.name[len(prefix):item.name.find('.')]) + increment_value)) +
                      item.name[item.name.find('.'):])


# Sends an email to receiver (String)
# Message sent is made of subject (String) and body (String)
# sender_username (String) and sender_password (String) are the credentials for the sender's email account
def send_email(receiver, subject, body, sender_username, sender_password):
    port = 465
    smtp_server = "smtp.gmail.com"
    context = create_default_context()
    with SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_username, sender_password)
        server.sendmail(sender_username, receiver, "Subject: " + subject + "\n\n" + body)
