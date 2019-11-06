import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO: Add as environment variables
# GMAIL_USER = os.environ(name)...
GMAIL_USER = "MapAnalyticsPMMC@gmail.com"
GMAIL_PASS = "pmmc-map"

def send_email(to_email, subject, body, files=[]):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)

        message = MIMEMultipart()
        message['From'] = GMAIL_USER
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        server.send_message(message)
        print("Sent")
        server.quit()
    except Exception as e:
        print(str(e))
        raise Exception(str(e))

if __name__ == "__main__":
    send_email("billycastelli@gmail.com", "Test subject", "Test body")