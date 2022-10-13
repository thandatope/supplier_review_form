
from wtforms import StringField, validators, SelectField
from flask_wtf import FlaskForm


class FrontForm(FlaskForm):
    email = StringField(u'Email Address', validators=[validators.input_required(), validators.email()])


class CodeForm(FlaskForm):
    code = StringField(u'Code', validators=[validators.input_required()])


class ReviewType(FlaskForm):
    review_type = SelectField(u'Type of Review', validators=[validators.input_required()],
                              choices=[('datapack', 'Provide Supplier Data Pack'),
                                       ('form', 'Complete Supplier Review Form')])