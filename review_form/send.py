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
from pretty_html_table import build_table

oauth2 = os.getenv('CREDENTIALS')

email_start = """<html>
                <body>
                <p align="center">Completed Supplier Review</p><br>
                <span style="height: 25px;">
                """

email_end = """</span>
            </body>
            </html>
            """


def send_report(report_email, dataframe):
    html_table = build_table(dataframe,
                             'grey_dark',
                             index=True,
                             font_size='12px',
                             width_dict=['50px', '250px'],
                             padding='5px'
                             )
    yag = yagmail.SMTP(os.getenv('MAIL_USERNAME'), oauth2_file="credentials.json")
    yag.send(to=report_email,
             subject="report",
             contents=email_start + html_table + email_end
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
