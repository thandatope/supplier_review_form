from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    DateField,
    TextAreaField,
    SelectMultipleField,
    IntegerField,
    BooleanField,
    MultipleFileField, EmailField, URLField, TelField)


class NewSupplierQuestionnaire(FlaskForm):
    company_types = [
            ("vendor", "Sale of Equipment and/or Reagents"),
            ("servicing", "Equipment Maintenance (excluding calibration)"),
            ("media", "Microbiological Media"),
            ("prof", "Proficiency Testing Materials"),
            ("calibration", "Calibration of equipment"),
            ("subcon", "Testing subcontractor"),
            ("test_kits", "Supplier of test kits"),
            ("archiving", "Document archiving and/or secure disposal"),
            (
                    "confidential",
                    "Confidential, hazardous or commercially sensitive waste disposal",
            ),
            ("facilities", "Operational support (Facilities, IT)"),
            ("other", "Other"),
    ]

    standards = [
            ("ISO 9001", "ISO 9001"),
            ("ISO 17025", "ISO 17025"),
            ("ISO 17034", "ISO 17034"),
            ("ISO 7043", "ISO 17043"),
            ("Regulatory", "Inspected by a regulatory body (MHRA, FDA)"),
    ]

    # person
    completed_name = StringField("Completed By Name")
    date = DateField("Completed On Date")
    email = EmailField("Completed By Email")
    phone = TelField("Phone Number")

    # company
    company = StringField("Company Name")
    address = TextAreaField("Address")
    website = URLField("Company Website")
    company_registration_number = IntegerField("Company Registration Number")
    vat_number = IntegerField("Company VAT Number")
    sales_email = StringField("Please provide the contact email address for sales enquiries")
    quality_email = StringField("Please provide the contact email address for quality enquiries")
    finance_email = StringField("Please provide the contact email address for finance enquiries")
    service_provided = SelectField(
            "What best describes the services your company provides?", choices=company_types
    )
    accreditation = SelectMultipleField(
            "Are you accredited to any of the below? Select all that apply.",
            choices=standards,
    )
    core_activity = TextAreaField("Please describe your core service and/or products.")
    other_activities = TextAreaField(
            "Do you provide any other services that may be of interest to RSSL?"
    )
    certifications = MultipleFileField(
            "Please attach current accreditation schedules or similar"
    )
    comments = TextAreaField("Any comments or further information?")
