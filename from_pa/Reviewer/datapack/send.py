"""

Use gmail for testing due to limits on free pythonanywhere

Upgrade to something else later

"""

from flask_mailman import EmailMessage
import logging
from flask import current_app
import yagmail
import os
import pathlib
from .funcs import generate_datapack_attachment

oauth2 = os.getenv('CREDENTIALS')
report_email = os.getenv('REPORT_EMAIL')

def build_body(name, company, email):
    body = f"""
    Datapack recieved from:<br>
    {name}<br>{email}<br>From {company}<br><br>
    See attached."""

def send_report(name, company, email):
    zip_file = generate_datapack_attachment(company)
    contents = build_body(name, company, email)
    yag = yagmail.SMTP(os.getenv('MAIL_USERNAME'), oauth2_file="oauth2.json")
    yag.send(to=report_email,
             subject="Datapack Submitted.",
             contents=contents,
             attachments=[zip_file]
             )
    os.remove(zip_file)

def old_mail():
    logger.info("Sending report")
    email1 = EmailMessage(
        subject='Report',
        body='this has a report attached',
        from_email=("Test Flask Notification <jmflasktest@gmail.com>"),
        to=[email_address]
    )
    email1.attach_file(report_path)
    with current_app.app_context():
        email1.send()
        logger.info("End Send")
