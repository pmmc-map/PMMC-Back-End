import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
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

        # # Test file, will be list of files
        # f = open("Text.txt", "w+")
        # f.write("TEST!!")
        # f.close()

        # Open file as binary and read
        with open(files[0][1] + ".csv", "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment; filename=Test.txt",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()
        server.send_message(message)
        server.quit()

    except Exception as e:
        print(str(e))
        raise Exception(str(e))

if __name__ == "__main__":
    send_email("billycastelli@gmail.com", "Test subject", "Test body")