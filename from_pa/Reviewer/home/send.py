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
import random
import math

oauth2 = os.getenv('CREDENTIALS')

email_start = """<html>
                <body>
                <p style="font-size: 16px;">RSSL Supplier Portal<br>
                Your email verification code is:</p>
                <p style=font-size: 16px;>
                """

email_end = """</p>
            </body>
            </html>
            """


def gen_otp():
    items = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    otp = ""
    length = len(items)
    for i in range(20):
        otp += items[math.floor(random.random() * length)]
    print(f"otp: {otp}")
    return otp


def send_otp(user_email):
    otp = gen_otp()
    yag = yagmail.SMTP(os.getenv('MAIL_USERNAME'), oauth2_file="oauth2.json")
    yag.send(to=user_email,
             subject="Your RSSL Confirmation Code",
             contents=email_start + otp + email_end
             )
    return otp
