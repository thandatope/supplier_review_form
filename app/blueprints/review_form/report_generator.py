import datetime
from io import BytesIO

import pdfkit
import preppy

from .review_funcs import process_review


def render_report_template(template, answer_dict, review_dict):
    module = preppy.getModule(template)
    supplier = answer_dict["company"]
    email = answer_dict["email"]
    date = answer_dict["date"]
    actions = review_dict["to_action"]
    today = datetime.date.today()
    html = module.get(supplier, email, date, answer_dict, review_dict, actions, today)
    return html


def generate_report_documents(answer_dict, review_df):
    generated_files = []
    review_dict = get_review_dict(review_df)
    response_template = "responses.prep"
    review_template = "review.prep"
    response_report = render_report_template(
        response_template, answer_dict, review_dict
    )
    review_report = render_report_template(review_template, answer_dict, review_dict)
    response_buffer = BytesIO()
    review_buffer = BytesIO()
    # add "attachment=x" to write_pdf to attach form files etc to pdf
    # HTML(string=report).write_pdf("test-pdf.pdf")
    response_buffer.write(pdfkit.from_string(response_report))
    response_buffer.seek(0)
    response_buffer.name = "Responses.pdf"
    review_buffer.write(review_report)
    review_buffer.seek(0)
    review_buffer.name = "Review.html"
    generated_files.append(response_buffer)
    generated_files.append(review_buffer)
    return generated_files


def get_review_dict(review_df):
    review_dict = process_review(review_df)
    return review_dict


if __name__ == "__main__":
    a_d = {
        "question 1": "answer 1",
        "question 2": "answer 2",
        "question 3": "answer 3",
        "question 4": "answer 4",
    }
    r_d = {
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
    docs = generate_report_documents(a_d, r_d)
    print(docs)
