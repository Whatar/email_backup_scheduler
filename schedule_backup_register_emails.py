import imaplib
import email
from email.message import EmailMessage
import os
import schedule
import time
from datetime import datetime
from email.header import decode_header

"""
env example:
[DEFAULT]
EMAIL_USER=user
EMAIL_PASSWORD=password
"""

# Configuration of environment variables
from configparser import ConfigParser
env = ConfigParser()
env.read(".env")

# Email configuration and credentials
IMAP_SERVER = "imap.register.it"
IMAP_PORT = 993
EMAIL_USER = env["DEFAULT"]["EMAIL_USER"]
EMAIL_PASSWORD = env["DEFAULT"]["EMAIL_PASSWORD"]
BACKUP_FILE = "out/emails_backup.mbox"
LOG_FILE = "out/backup.log"


def fetch_and_backup_emails():
    print("Starting email backup...")

    # Connection to the IMAP server
    imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    try:
        # Login
        imap.login(EMAIL_USER, EMAIL_PASSWORD)
        print("Successfully logged into the IMAP server.")

        # Select the mailbox
        imap.select("INBOX")

        # Check the last saved ID
        last_saved_id = 0
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as log:
                lines = log.readlines()
                last_line = lines[-1]
                last_saved_id = last_line.split(";")[-1].split(":")[1]

        print(f"Last saved ID: {last_saved_id}")

        # Search for all emails with ID greater than the last saved
        status, messages = imap.search(None, f"UID {last_saved_id + 1}:*")
        if status != "OK":
            print("Error during email search.")
            return

        mail_ids = messages[0].split()
        print(f"New emails found: {len(mail_ids)}")

        # Add the new emails to the backup file
        with open(BACKUP_FILE, "a") as backup:
            for mail_id in mail_ids:
                status, msg_data = imap.fetch(mail_id, "(RFC822)")
                last_saved_id = mail_id
                if status == "OK":
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            # Decode the message
                            msg = email.message_from_bytes(response_part[1])
                            body = msg.get_payload(decode=True)
                            if body is None:
                                body = "Missing data".encode()
                            # Decode the email subject
                            subject, encoding = decode_header(
                                msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding or "utf-8")

                            separator = f"From {msg.get('From')} {
                                msg.get('Date')}"
                            from_ = f"From: {msg.get('From')}\n"
                            to = f"To: {msg.get('To')}\n"
                            date = f"Date: {msg.get('Date')}\n"

                            formatted_email = f"{separator}\n{
                                from_}{to}{date}\n{body.decode()}"

                            backup.write(formatted_email)
                            backup.write("\n\n")

            # Update the last saved ID
            with open(LOG_FILE, "a") as log:
                log.write(f"last_run:{datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S')};new_emails:{len(mail_ids)};last_id:{last_saved_id}\n")

        print("Backup completed successfully.")
    finally:
        # Disconnect from the IMAP server
        imap.logout()


# Schedule the script to run every Sunday at 01:00
# schedule.every().sunday.at("01:00").do(fetch_and_backup_emails)
fetch_and_backup_emails()

print("Scheduler active. Waiting...")
while True:
    schedule.run_pending()
    time.sleep(1)
