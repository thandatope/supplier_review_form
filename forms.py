import flask_wtf
import wtforms
from wtforms import Form, StringField, validators, SelectField, SubmitField, MultipleFileField, DateField, \
    TextAreaField, SelectMultipleField
from flask_wtf import FlaskForm


class FrontForm(FlaskForm):
    email = StringField(u'Email Address', validators=[validators.input_required(), validators.email()])


class CodeForm(FlaskForm):
    code = StringField(u'Code', validators=[validators.input_required()])


class ReviewType(FlaskForm):
    review_type = SelectField(u'Type of Review', validators=[validators.input_required()],
                              choices=[('datapack', 'Provide Supplier Data Pack'),
                                       ('form', 'Complete Supplier Review Form')])


class SupplierReviewQuestionnaire(FlaskForm):
    q1 = StringField('Completed By Name')
    q2 = DateField("Completed On Date")
    q3 = StringField('Completed By Email')
    q4 = TextAreaField('Address')

    company_types = [('vendor', 'Sale of Equipment and/or Reagents'),
                     ('servicing', 'Equipment Maintenance (excluding calibration)'),
                     ('media', 'Microbiological Media'),
                     ('prof', 'Proficiency Testing Materials'),
                     ('calibration', 'Calibration of equipment'),
                     ('subcon', 'Testing subcontractor'),
                     ('test_kits', 'Supplier of test kits'),
                     ('archiving', 'Document archiving and/or secure disposal'),
                     ('confidential', 'Confidential, hazardous or commercially sensitive waste disposal'),
                     ('facilities', "Operational support (Facilities, IT)"),
                     ('other', 'Other')]

    accreditation = [('9001', 'ISO 9001'),
                     ('17025', 'ISO 17025'),
                     ('17034', 'ISO 17034'),
                     ('17043', 'ISO 17043'),
                     ('regulatory', 'Inspected by a regulatory body (MHRA, FDA)')]

    q5 = SelectField('What best describes the services your company provides?', choices=company_types)
    q6 = SelectMultipleField('Are you accredited to any of the below? Select all that apply.', choices=accreditation)
    q7 = StringField('Address Line 4')
    q8 = StringField('Address Line 5')
    q9 = StringField('Address Line 6')
    submit = SubmitField(label='Submit')


class DataPackUpload(FlaskForm):
    name = StringField('Submitted By')
    company = StringField('Company')
    email = StringField('Contact Email')
    files = MultipleFileField(label='')
