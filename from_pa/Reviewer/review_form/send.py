"""

Use gmail for testing due to limits on free pythonanywhere

Upgrade to something else later

Run yagmail steps in python console on pythonanywhere to get oauth2 token
https://console.cloud.google.com/ - for keys

"""

from flask_mailman import EmailMessage
from flask import current_app
import yagmail
import os
import dataframe_image as dfi
from .pdf_report import form_to_pdf

oauth2 = os.getenv('CREDENTIALS')

body_content = """
    <body>
    <h1 style="font-size: 24px;">Supplier Questionnaire From SUPPLIER</h1>
                <h2 style="font-size: 16px;">Completed by: EMAIL</h2>
                <h2 style="font-size: 12px;">Completed on: DATE</h2>
                </body>
"""

def send_report(report_email, result_dict):
    pdf_buffer = form_to_pdf(result_dict)
    pdf_buffer.seek(0)
    pdf_buffer.name = "report.pdf"

    yag = yagmail.SMTP(os.getenv('MAIL_USERNAME'), oauth2_file="oauth2.json")
    yag.send(to=report_email,
             subject="Supplier Questionnaire",
             contents="helo",
             attachments=[pdf_buffer]
             )


def built_in_flask_email(report_email, html_report):
    email1 = EmailMessage(
        subject='Report',
        body='this has a report attached',
        from_email=("Test Flask Notification <jmflasktest@gmail.com>"),
        to=[report_email]
    )
    email1.attach_file(html_report)
    with current_app.app_context():
        email1.send()
