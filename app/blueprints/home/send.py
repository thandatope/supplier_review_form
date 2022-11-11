"""

Use gmail for testing due to limits on free pythonanywhere

Upgrade to something else later

Run yagmail steps in python console on pythonanywhere to get oauth2 token
https://console.cloud.google.com/ - for keys

"""

import math
import os
import random

import yagmail
from ...ext import mail

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
    for i in range(15):
        otp += items[math.floor(random.random() * length)]
    return otp


def send_otp(user_email):
    otp = gen_otp()
    if os.getenv('ENABLE_SEND') is True:
        yag = yagmail.SMTP(os.getenv("MAIL_USERNAME"), oauth2_file="creds.json")
        yag.send(
                to=user_email,
                subject="Your RSSL Confirmation Code",
                contents=email_start + otp + email_end,
        )
        return otp
    else:
        return otp


def flask_send_otp(user_email):
    otp = gen_otp()
    mail.send(subject="Your RSSL OTP",
              receivers=[user_email],
              contents="helo"
              )