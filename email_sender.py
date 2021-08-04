import os
import smtplib
from email import encoders, message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


emails = [
    p.stem for p in Path("./Certs").glob("*.png")
]  # Get filename from Certs folder


mail_content = "Hello, This is a test email."

sender_address = os.environ.get("EMAIL_ADDRESS")  # Get Email Address from .env
sender_pass = os.environ.get("EMAIL_PASSWORD")  # Get Password from .env
receiver_address = "reciever email here"  # Reciever Email here


message = MIMEMultipart()
message["From"] = sender_address
message["To"] = receiver_address
message["Subject"] = "Mail Subject here."
message.attach(MIMEText(mail_content, "plain"))
attach_file_name = f"./Certs/Example.png"
attach_file = open(attach_file_name, "rb")
payload = MIMEBase("application", "octate-stream")
payload.set_payload((attach_file).read())
encoders.encode_base64(payload)
payload.add_header(
    "Content-Decompostion", "attachment", filename=f"{attach_file_name}.png"
)  # Attaching a .png file with the E-mail
message.attach(payload)
session = smtplib.SMTP("smtp.gmail.com", 587)
session.starttls()
session.login(sender_address, sender_pass)
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
