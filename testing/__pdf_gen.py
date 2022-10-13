import jinja2.utils
import pandas as pd
import string
import random
from io import BytesIO
from flask import render_template, current_app, url_for
import datetime


def apply_template(answer_dict, supplier, date, email):
    with current_app.app_context():
        env = current_app.jinja_env
        t = env.get_template()
        today = datetime.date.today()
        html = render_template('report.html', answer_dict=answer_dict, supplier=supplier, date=date, email=email,
                               today=today)
        return html


def a_t(answer_dict, supplier, date, email):
    from jinja2 import Environment, FileSystemLoader
    today = datetime.date.today()
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader, autoescape=True)
    t = env.get_template('report_test.html')
    out = t.render(answer_dict=answer_dict, supplier=supplier, date=date, email=email, today=today)
    return out


def form_to_pdf(answer_dict):
    # actually need to get email/date/company at some point - from session?
    # email = session['email']
    email = "hello@hello.com"
    supplier = "Bobs Lab Supplies"
    date = "69/420/69420"
    pdf_buffer = BytesIO()
    report = a_t(answer_dict, supplier, date, email)
    print(report)
    # add "attachment=x" to write_pdf to attach form files etc to pdf
    HTML(string=report).write_pdf("test.pdf")
    CSS()
    print("dun")


if __name__ == "__main__":
    from weasyprint import HTML, CSS
    HTML().write_pdf(stylesheets=[CSS(url_for('static/css/report.css'))])
    CSS()
    print("generating df")
    num_strings = 10
    q = []
    a = []
    letters = string.ascii_letters
    d = {}
    for x in range(5):
        s = jinja2.utils.generate_lorem_ipsum()
        d[x] = s
    url_for()
    form_to_pdf(d)
