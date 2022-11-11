from wtforms import StringField, EmailField
from flask_wtf import FlaskForm


class DataPackUpload(FlaskForm):
    name = StringField("Submitted By")
    company = StringField("Company")
    email = EmailField("Contact Email")
