
from wtforms import StringField, SelectField, SubmitField, DateField, TextAreaField, SelectMultipleField, IntegerField, BooleanField, MultipleFileField, EmailField, TelField, URLField
from flask_wtf import FlaskForm


class SupplierReviewQuestionnaire(FlaskForm):
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

    accreditation = [('ISO 9001', 'ISO 9001'),
                     ('ISO 17025', 'ISO 17025'),
                     ('ISO 17034', 'ISO 17034'),
                     ('ISO 7043', 'ISO 17043'),
                     ('Regulatory', 'Inspected by a regulatory body (MHRA, FDA)')]

    # person
    completed_name = StringField('Completed By Name')
    date = DateField("Completed On Date")
    email = EmailField('Completed By Email')
    phone = TelField('Phone Number')
    # company
    company = StringField('Company Name')
    address = TextAreaField('Address')
    website = URLField('Company Website')
    company_registration_number = IntegerField('Company Registration Number')
    vat_number = IntegerField('Company VAT Number')
    service_provided = SelectField('What best describes the services your company provides?', choices=company_types)
    accredit = SelectMultipleField('Are you accredited to any of the below? Select all that apply.', choices=accreditation)
    core_activity = TextAreaField('Please describe your core service and/or products.')
    other_activities = TextAreaField('Do you provide any other services that may be of interest to RSSL?')
    company_change = BooleanField('Has there been any significant changes to company structure within the last 30 months?')

    # quality
    accreditation_change = BooleanField('Have there been any changes in your accreditation status in the last 30 months?')
    certifications = MultipleFileField('Please attach current accreditation schedules or similar')
    # other
    comments = TextAreaField('Any comments or further information?')