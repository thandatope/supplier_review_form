"""

Use gmail for testing due to limits on free pythonanywhere

Upgrade to something else later

"""

from flask_mailman import EmailMessage
import logging
from flask import current_app
import yagmail
import os


logger = logging.getLogger()


def send_report(report_email, html_report):
    yag = yagmail.SMTP(os.getenv('MAIL_USERNAME'), oauth2_file="credentials.json")
    yag.send(to=report_email,
             subject="report",
             contents="helo is report",
             attachments=[html_report]
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
