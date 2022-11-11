import pandas as pd
from flask import Flask, render_template_string, request
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField,
    DateField,
    TextAreaField,
    SelectMultipleField,
    BooleanField,
    MultipleFileField,
    IntegerField, EmailField, TelField, URLField)


class TestForm(FlaskForm):
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
    company_change = BooleanField(
            "Has there been any significant changes to company structure within the last 30 months?"
    )
    company_change_details = TextAreaField("If Yes, please give further detail.")
    # quality
    accreditation_change = BooleanField(
            "Have there been any changes in your accreditation status in the last 30 months?"
    )
    accreditation_change_details = TextAreaField("If Yes, please give further details")
    certifications = MultipleFileField(
            "Please attach current accreditation schedules or similar"
    )
    # other
    comments = TextAreaField("Any comments or further information?")
    bool = BooleanField("this is boolean")
    submit = SubmitField(label="Submit")


def get_relevant_accreditations(supplier_type):
    accreditation_dict = {
            "media":        ["ISO9001", "ISO17025"],
            "prof":         ["ISO9001", "ISO17034"],
            "calibration":  ["ISO9001", "ISO17025"],
            "subcon":       ["ISO9001", "ISO17025"],
            "test_kits":    ["ISO9001"],
            "archiving":    ["ISO9001"],
            "confidential": ["ISO9001"],
    }
    return accreditation_dict[supplier_type]


def clean_accreditations(accreditation_reply):
    split = accreditation_reply.split(",")
    review_accreditations = []
    for x in split:
        x = x.replace("'", "")
        x = x.replace("[", "")
        x = x.replace("]", "")
        x = x.strip()
        review_accreditations.append(x)
    return review_accreditations


def accreditation_status_score(results_dataframe, supplier_type):
    # get accreditations that apply
    selected_accreditations = check_response(results_dataframe, "accreditation")
    cleaned_accreditations = clean_accreditations(selected_accreditations)
    relevant_accreditations = get_relevant_accreditations(supplier_type)
    if len(relevant_accreditations) >= len(cleaned_accreditations):
        num = 0
        for a in relevant_accreditations:
            if a in cleaned_accreditations:
                num = num + 5

    elif len(relevant_accreditations) < len(cleaned_accreditations):
        num = 0
        for a in cleaned_accreditations:
            if a in relevant_accreditations:
                num = num + 5

    return num


def quality_supplier_review(results_dataframe, supplier_type):
    review_weighting = {
            "company_no_change":         2,
            "company_change":            -2,
            "accreditation_not_changed": 5,
            "accreditation_changed":     -10,
            "attachments_found":         3,
            "attachments_not_found":     -5,
    }
    review_comments = {
            "company_no_change":         "No significant company changes indicated.",
            "company_change":            "Significant company changes indicated",
            "accreditation_not_changed": "No changes in company accreditation.",
            "accreditation_changed":     "Accreditation changes present",
            "attachments_found":         "Documents Attached",
            "attachments_not_found":     "No documentation attached",
    }
    # get dat scoring
    total_score = pd.DataFrame(columns=["points", "comment"])
    results_s = pd.Series(index=["points", "comments"])
    results_d = {}
    scores = accreditation_status_score(results_dataframe, supplier_type)
    to_check = ["company_change", "accreditation_change", "certifications"]
    for x in to_check:
        resp = check_response(results_dataframe, x)
        if x == "company_change":
            if resp is True:
                total_score.company_change = review_weighting["company_change"]
                total_score.company_change_comments = review_comments["company_change"]
            else:
                total_score.company_change = review_weighting["company_no_change"]
                total_score.company_change_comments = review_comments[
                    "company_no_change"
                ]
        elif x == "accreditation_change":
            if resp is True:
                total_score.accreditation_change = review_weighting[
                    "accreditation_changed"
                ]
                total_score.accreditation_change_comments = review_comments[
                    "accreditation_changed"
                ]
            else:
                total_score.accreditation_change = review_weighting[
                    "accreditation_not_changed"
                ]
                total_score.accreditation_change_comments = review_comments[
                    "accreditation_not_changed"
                ]
        elif x == "certifications":
            if resp is not None:
                total_score.certifications = review_weighting["attachments_found"]
                total_score.certifications_comments = review_comments[
                    "attachments_found"
                ]
            else:
                total_score.certifications = review_weighting["attachments_not_found"]
                total_score.certifications_comments = review_comments[
                    "attachments_not_found"
                ]


def business_supplier_review(results_dataframe, supplier_type):
    pass


def other_supplier_review(results_dataframe, supplier_type):
    pass


def check_response(results_dataframe, question):
    col = results_dataframe.answer
    change = col.loc[question]
    return change


def process_form(results_dataframe):
    quality_list = [
            "media",
            "prof",
            "calibration",
            "subcon",
            "test_kits",
            "archiving",
            "confidential",
    ]
    business_list = ["vendor", "servicing", "facilities"]
    other_list = ["other"]

    service_type = check_response(results_dataframe, "service_provided")
    # could maybe change this to index lookup for the question row
    if service_type in quality_list:
        quality_supplier_review(results_dataframe, supplier_type=service_type)
    elif service_type in business_list:
        business_supplier_review(results_dataframe, supplier_type=service_type)
    elif service_type in other_list:
        other_supplier_review(results_dataframe, supplier_type=service_type)


app = Flask(__name__)
app.config["SECRET_KEY"] = "helo"


@app.route("/", methods=["GET", "POST"])
def form_test():
    form = TestForm()
    if request.method == "POST":
        # start automatic processing based on service type
        response_data = []
        for x in iter(form):
            name_str = str(x.name)
            response_data.append([name_str, x.label.text, x.data])
        df = pd.DataFrame(
                response_data,
                columns=["field", "question", "answer"],
                dtype=pd.StringDtype(),
        )
        df.set_index("field", drop=True, inplace=True, verify_integrity=True)
        # could do with making 1st column the index
        process_form(df)

    return render_template_string(
            """<html><body>
                        <form method="POST">
                        {{ form.hidden_tag() }}
                        {% for field in form if field.widget.input_type != 'hidden' %}
                        <div class="field">
                        <span> {{ field.label }}</span>
                        <div class="control is-large">
                        <span> {{ field }} </span>
                        
                        </div>
                        </div>
                        {% endfor %}
                        </form>
                        </body>
                        </html>
                        """,
            form=form,
    )


if __name__ == "__main__":
    # pandasgui.show()
    app.run(debug=True)
