import os

import pandas as pd
from flask import flash, render_template, request, current_app, redirect, url_for

from . import new_supplier as bp
from . import forms, send
from ...funcs import check_email_confirmed

report_email = os.getenv("REPORT_EMAIL")
current_folder = os.path.dirname(os.path.abspath(__file__))


@bp.route("/new_supplier/form/", methods=["GET", "POST"])
@check_email_confirmed
def new_supplier_form():
    form = forms.NewSupplierQuestionnaire()
    if request.method == "POST":
        question_dict = request.form.to_dict()

        # start automatic processing based on service type
        response_data = []
        for x in iter(form):
            name_str = str(x.name)
            if type(x.data) is str:
                # d = x.data.replace("\r\n", '<br>')
                d = x.data
            else:
                d = x.data
            response_data.append([name_str, x.label.text, d])

        response_df = pd.DataFrame(
                response_data,
                columns=["field", "question", "answer"],
        )
        response_df.set_index("field", drop=True, inplace=True, verify_integrity=True)
        flash("Form Submitted!", "success")
        with current_app.app_context():
            send.send_report(report_email, question_dict, response_df)
        return redirect(url_for("home.supplier"))
    return render_template("new_supplier/form.html", form=form)
