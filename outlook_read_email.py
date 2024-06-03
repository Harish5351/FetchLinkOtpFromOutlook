import imaplib
import email
import re
import logging
import time


class EmailReader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read_email(self, email_address, password):
        try:
            mail = imaplib.IMAP4_SSL('outlook.office365.com')
            mail.login(email_address, password)
            time.sleep(5)
            mailbox = 'INBOX'
            mail.select(mailbox)
            result, data = mail.search(None, 'UNSEEN')
            for num in data[0].split():
                result, email_data = mail.fetch(num, '(RFC822)')
                raw_email = email_data[0][1]
                msg = email.message_from_bytes(raw_email)
                subject = msg.get('Subject')
                print(subject)
                sender = msg.get('From')
                print(sender)
                if subject and sender:
                    # subject = subject.lower()
                    # sender = sender.lower()
                    if subject == 'AutomationTest: Please Reset Your Password' and sender == 'sender@email.com':
                        body = self.extract_email_body(msg)
                        if body:
                            otp = self.extract_otp(body)
                            if otp:
                                self.logger.info("OTP extracted successfully: {}".format(otp))
                                return otp
            # except Exception as e:
            #     self.logger.error("Error occurred while reading email: {}".format(str(e)))
            # finally:
            #     if mail:
            mail.close()
            mail.logout()

        except imaplib.IMAP4.error as e:
            print("IMAP login failed:", e)
        # return None

    def extract_email_body(self, msg):
        body = None
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                try:
                    body = part.get_payload(decode=True).decode('utf-8')
                except Exception as e:
                    self.logger.error("Error decoding email body: {}".format(str(e)))
                break
        return body

    # def extract_otp(self, body):
    #     result = re.sub(r'<.*?>', '', body)  # Remove HTML tags
    #     print("body" ,result)
    #     result = re.sub(r'.*?}', '', result)  # Remove special characters
    #     pattern = re.compile(r'\b\d{6}\b')  # Match 6-digit OTP
    #     matcher = pattern.search(result)
    #     if matcher:
    #         return matcher.group(0)
    #     return None

    def extract_otp(self, body):
        # Define a regular expression pattern to match the OTP format
        pattern = re.compile(r'Your activation code is (\d{6})')

        # Search for the OTP pattern in the email body
        matcher = pattern.search(body)
        if matcher:
            # If a match is found, return the OTP
            return matcher.group(1)
        return None


# if __name__ == '__main__':
#     email_reader = read_email(self, "user@email.com", "password")
# Example usage:
# email_reader = EmailReader()
# otp = email_reader.read_email("email@outlook.com", "password")
# if otp:
#     print("OTP:", otp)
# else:
#     print("No OTP found in emails.")
