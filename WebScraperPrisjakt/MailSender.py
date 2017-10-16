import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


class Mailer(object):
    def __init__(self, attach_name):
        self.attach_name = attach_name
        self.main(attach_name)

    def main(self, attach_name):
        gmail_user = 'XXXXXXXXXXXX.crawler@gmail.com'
        gmail_password = 'XXXXXXXXXXXXXXXXXXX'
        body = 'Hello,\nSee the attached file'
        to = ['o.heurlin@gmail.com']

        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = ", ".join(to)
        msg['Subject'] = 'Such a cheap computer screen!'
        body = 'Hello,\nSee the attached file'

        msg.attach(MIMEText(body, 'plain'))
        attach = open(attach_name, "r")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attach.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename = attach_name)
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, to, text)
        server.quit()
