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
import shutil

oauth2 = os.getenv('CREDENTIALS')


def generate_email_attachment(company):
    basedir = os.path.abspath(os.path.dirname(__file__))
    root_path = basedir + "/temp/datapack"
    folder_zip = root_path + f"/{company}/"
    shutil.make_archive(base_name=company, format="zip", root_dir=root_path, base_dir=folder_zip)


    def send_report(report_email, datapack, customer, customer_email, company):
        yag = yagmail.SMTP(os.getenv('MAIL_USERNAME'), oauth2_file="oauth2")
    yag.send(to=report_email,
             subject="report",
             contents="helo is datapack",
             attachments=[datapack]
             )


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
