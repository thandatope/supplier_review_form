from wtforms import StringField, MultipleFileField
from flask_wtf import FlaskForm


class DataPackUpload(FlaskForm):
    name = StringField('Submitted By')
    company = StringField('Company')
    email = StringField('Contact Email')
    files = MultipleFileField(label='')


