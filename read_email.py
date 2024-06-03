from dotenv import load_dotenv
from imap_tools import MailBox, AND
import os

# Load .env file
load_dotenv()

# read variables
email_user = os.getenv('EMAIL_USER')
email_pass = os.getenv('EMAIL_PASS')


def check_latest_email():
    # connect to Gmail's IMAP server
    with MailBox('imap.gmail.com').login(email_user, email_pass, 'INBOX') as mailbox:
        # Fetch the latest unread email
        emails = list(mailbox.fetch(AND(seen=False), limit=1, reverse=True))

        if len(emails) == 0:
            return None, None, None  # No Emails Found
        return emails[0]

if __name__ == "__main__":
    email = check_latest_email()
    print("email subject: ",email.subject)
    print(email.text)
    print(email.from_)
