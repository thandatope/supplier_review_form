import jinja2
from io import BytesIO
from flask import render_template, current_app, Flask, url_for
import datetime
from weasyprint import HTML, CSS
import os
import datetime

def apply_template(answer_dict, supplier, date, email):
    # app = Flask(__name__)
    with current_app.app_context():
        today = datetime.date.today()
        html = render_template('report.html', answer_dict=answer_dict, supplier=supplier, date=date, email=email,
                               today=today)
        # with open("testhtml.html", "w") as f:
        #     f.write(html)
        return html


def form_to_pdf(answer_dict):
    # actually need to get email/date/company at some point - from session?
    # email = session['email']
    email = answer_dict['email']
    supplier = answer_dict['company']
    date = answer_dict['date']
    pdf_buffer = BytesIO()
    report = apply_template(answer_dict, supplier, date, email)
    # add "attachment=x" to write_pdf to attach form files etc to pdf
    # HTML(string=report).write_pdf("test-pdf.pdf")
    pdf_buffer.write(HTML(string=report).write_pdf())
    return pdf_buffer

if __name__ == "__main__":
    print("generating dict")
    d = {}
    for x in range(5):
        s = jinja2.utils.generate_lorem_ipsum()
        d[x] = s
    print(f"dict generated:\n{d}")
    pdf_buffer = form_to_pdf(d)

