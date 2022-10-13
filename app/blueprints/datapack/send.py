"""

Use gmail for testing due to limits on free pythonanywhere

Upgrade to something else later

"""

from flask_mailman import EmailMessage
import logging
from flask import current_app, flash, send_from_directory
import yagmail
import os
import pathlib
from .funcs import generate_datapack_attachment

oauth2 = os.getenv("CREDENTIALS")
report_email = os.getenv("REPORT_EMAIL")


def build_body(name, company, email):
    body = f"""
    Datapack recieved from:<br>
    {name}<br>{email}<br>From {company}<br><br>
    See attached."""
    return body


def send_report(name, company, email):
    zip_file = generate_datapack_attachment(company)
    contents = build_body(name, company, email)
    if os.getenv('ENABLE_SEND') is True:
        yag = yagmail.SMTP(os.getenv("MAIL_USERNAME"), oauth2_file="creds.json")
        yag.send(
            to=report_email,
            subject="Datapack Submitted.",
            contents=contents,
            attachments=[zip_file],
        )
        os.remove(zip_file)
    else:
        flash("No email sent - testing", category="warning")
