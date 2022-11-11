"""

Use gmail for testing due to limits on free pythonanywhere

Upgrade to something else later

Run yagmail steps in python console on pythonanywhere to get oauth2 token
https://console.cloud.google.com/ - for keys

"""

import os

import yagmail
from flask import current_app
from flask_mailman import EmailMessage

from .report_generator import generate_report_documents

oauth2 = os.getenv("CREDENTIALS")

body_content = """
    <body>
    <h1 style="font-size: 24px;">Supplier Questionnaire From SUPPLIER</h1>
                <h2 style="font-size: 16px;">Completed by: EMAIL</h2>
                <h2 style="font-size: 12px;">Completed on: DATE</h2>
                </body>
"""


def send_report(report_email, response_dict, review_df):
    files = generate_report_documents(response_dict, review_df)

    yag = yagmail.SMTP(os.getenv("MAIL_USERNAME"), oauth2_file="creds.json")
    yag.send(
        to=report_email,
        subject="Supplier Questionnaire",
        contents="helo",
        attachments=files,
    )


def built_in_flask_email(report_email, html_report):
    email1 = EmailMessage(
        subject="Report",
        body="this has a report attached",
        from_email=("Test Flask Notification <jmflasktest@gmail.com>"),
        to=[report_email],
    )
    email1.attach_file(html_report)
    with current_app.app_context():
        email1.send()
