from flask_wtf import FlaskForm
from wtforms import StringField, validators


class FrontForm(FlaskForm):
    email = StringField(
            "Email Address", validators=[validators.input_required(), validators.email()]
    )


class CodeForm(FlaskForm):
    code = StringField("Code", validators=[validators.input_required()])
