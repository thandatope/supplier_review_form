import datetime
from io import BytesIO

from flask import current_app, render_template

from .config import conf
from .score_models import QualityReviewScore, BusinessReviewScore, OtherReviewScore


def get_response(results_dataframe, question):
    col = results_dataframe.answer
    change = col.loc[question]
    return change


def render_report_template(review_object):
    review_dict = review_object.generate_assessment_document_html()
    with current_app.app_context():
        env = current_app.jinja_env
        t = env.get_template()
        today = datetime.date.today()
        html = render_template("review.html", review_dict=review_dict)
        return html


def get_relevant_accreditations(supplier_type):
    # condense jsons down once decided on what to use and where
    a = conf["supplier_accreditations"][supplier_type]
    return a


def quality_supplier_review(results_dataframe, supplier_type):
    weightings = conf["review_weightings"]

    to_check = conf["score_fields"]["quality"]
    score = QualityReviewScore()
    score.company_name = get_response(results_dataframe, "company")
    score.company_type = supplier_type
    score.company_accreditations = get_response(results_dataframe, "accreditation")
    score.expected_accreditations = get_relevant_accreditations(score.company_type)
    score.company_change_details = get_response(
        results_dataframe, "company_change_details"
    )
    score.accreditation_change_details = get_response(
        results_dataframe, "accreditation_change_details"
    )
    score.supplier_comments = get_response(results_dataframe, "comments")
    for x in to_check:
        r = get_response(results_dataframe, x)
        if x == "company_change":
            if r is True:
                score.company_change = weightings["QUALITY"]["company_change"]
                score.company_change_comment = weightings["QUALITY"][
                    "company_change_comment"
                ]
                score.actions.append(weightings["QUALITY"]["company_change_action"])
            elif r is False:
                score.company_change = weightings["QUALITY"]["no_company_change"]
                score.company_change_comment = weightings["QUALITY"][
                    "no_company_change_comment"
                ]
        elif x == "accreditation_change":
            if r is True:
                score.accreditation_change = weightings["QUALITY"][
                    "accreditation_change"
                ]
                score.accreditation_change_comment = weightings["QUALITY"][
                    "accreditation_change_comment"
                ]
                score.actions.append(
                    weightings["QUALITY"]["accreditation_change_action"]
                )
            elif r is False:
                score.accreditation_change = weightings["QUALITY"][
                    "no_accreditation_change"
                ]
                score.accreditation_change_comment = weightings["QUALITY"][
                    "no_accreditation_change_comment"
                ]
        elif x == "certifications":
            for item in r:
                if item == "":
                    score.attachments = weightings["QUALITY"]["no_attachments"]
                    score.attachments_comment = weightings["QUALITY"][
                        "no_attachments_comment"
                    ]
                    score.actions.append(weightings["QUALITY"]["no_attachments_action"])
                else:
                    score.attachments = weightings["QUALITY"]["has_attachments"]
                    score.attachments_names.append(str(item))
                    score.attachments_comment = weightings["QUALITY"][
                        "has_attachments_comment"
                    ]

    html = render_report_template(score)
    return html


def business_supplier_review(results_dataframe, supplier_type):
    # fix path when on pythonanywhere
    weightings = conf["review_weightings"]

    to_check = conf["score_fields"]["business"]
    score = BusinessReviewScore()
    score.company_name = get_response(results_dataframe, "company")
    score.company_type = supplier_type
    score.company_accreditations = get_response(results_dataframe, "accreditation")
    score.expected_accreditations = get_relevant_accreditations(score.company_type)
    score.company_change_details = get_response(
        results_dataframe, "company_change_details"
    )
    score.accreditation_change_details = get_response(
        results_dataframe, "accreditation_change_details"
    )
    score.supplier_comments = get_response(results_dataframe, "comments")
    for x in to_check:
        r = get_response(results_dataframe, x)
        if x == "company_change":
            if r is True:
                score.company_change = weightings["QUALITY"]["company_change"]
                score.company_change_comment = weightings["QUALITY"][
                    "company_change_comment"
                ]
            elif r is False:
                score.company_change = weightings["QUALITY"]["no_company_change"]
                score.company_change_comment = weightings["QUALITY"][
                    "no_company_change_comment"
                ]
        elif x == "certifications":
            for item in r:
                if item == "":
                    score.attachments = weightings["QUALITY"]["no_attachments"]
                    score.attachments_comment = weightings["QUALITY"][
                        "no_attachments_comment"
                    ]
                else:
                    score.attachments = weightings["QUALITY"]["has_attachments"]
                    score.attachments_names += f"\n{str(item)}"
                    score.attachments_comment = weightings["QUALITY"][
                        "has_attachments_comment"
                    ]

    c = score.generate_assessment_document_html()
    out = BytesIO()
    out.write(c)
    out.seek(0)
    return out


def other_supplier_review(results_dataframe, supplier_type):
    # fix path when on pythonanywhere
    weightings = conf["review_weightings"]

    to_check = conf["score_fields"]["other"]
    score = OtherReviewScore()
    score.company_name = get_response(results_dataframe, "company")
    score.company_type = supplier_type
    score.company_accreditations = get_response(results_dataframe, "accreditation")
    score.company_change_details = get_response(
        results_dataframe, "company_change_details"
    )
    score.supplier_comments = get_response(results_dataframe, "comments")
    for x in to_check:
        r = get_response(results_dataframe, x)
        if x == "company_change":
            if r is True:
                score.company_change = weightings["OTHER"]["company_change"]
                score.company_change_comment = weightings["OTHER"][
                    "company_change_comment"
                ]
            elif r is False:
                score.company_change = weightings["OTHER"]["no_company_change"]
                score.company_change_comment = weightings["OTHER"][
                    "no_company_change_comment"
                ]
        elif x == "certifications":
            for item in r:
                if item == "":
                    score.attachments = weightings["QUALITY"]["no_attachments"]
                    score.attachments_comment = weightings["QUALITY"][
                        "no_attachments_comment"
                    ]
                else:
                    score.attachments = weightings["QUALITY"]["has_attachments"]
                    score.attachments_names += f"\n{str(item)}"
                    score.attachments_comment = weightings["QUALITY"][
                        "has_attachments_comment"
                    ]

    c = score.generate_assessment_document_html()
    out = BytesIO()
    out.write(c)
    out.seek(0)
    return out


def process_form(results_dataframe):
    # fix path when on pythonanywhere
    supplier_types = conf["supplier_types"]

    service_type = get_response(results_dataframe, "service_provided")
    if service_type in supplier_types["quality_list"]:
        out = quality_supplier_review(results_dataframe, supplier_type=service_type)
        return out
    elif service_type in supplier_types["business_list"]:
        out = business_supplier_review(results_dataframe, supplier_type=service_type)
        return out
    elif service_type in supplier_types["other_list"]:
        out = other_supplier_review(results_dataframe, supplier_type=service_type)
        return out
