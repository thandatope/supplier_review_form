"""
Maybe convert to using reportlab/rml templates in future
"""

import datetime

import pdfkit
import preppy


def render_template(template):
    module = preppy.getModule(template)
    supplier = "test supplier"
    email = "test@supplier.com"
    date = "01/69/0420"
    answer_dict = {
        "question 1": "answer 1",
        "question 2": "answer 2",
        "question 3": "answer 3",
        "question 4": "answer 4",
    }
    review_dict = {
        "company_name": "company_name",
        "company_type": "company_type",
        "company_change_comment": "company_change_comment",
        "company_change_details": "company_change_details",
        "accreditation_change_comment": "accreditation_change_comment",
        "accreditation_change_details": "accreditation_change_details",
        "attachments_comment": "attachments_comment",
        "supplier_comments": "supplier_comments",
        "missing": "missing",
        "score": "score",
        "rating": "rating",
        "comments": "comments",
        "held_accreditations": "held_accreditations",
        "expected_accreditations": "expected_accreditations",
        "attachments": ["attachment a", "attachment b", "attachment c"],
        "to_action": ["action 1", "action 2", "action 3"],
    }

    actions = review_dict["to_action"]
    today = datetime.date.today()
    data = module.get(supplier, email, date, answer_dict, review_dict, actions, today)
    return data


def gen_test_pdf():
    template = "responses.prep"
    data = render_template(template)
    pdfkit.from_string(data, "out.pdf")


def gen_test_html():
    template = "full.prep"
    data = render_template(template)
    with open("test.html", "w") as f:
        f.write(data)


if __name__ == "__main__":
    gen_test_pdf()
    gen_test_html()
