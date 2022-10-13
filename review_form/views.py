import os

from flask import flash, render_template, request, current_app
import pandas
from . import review_form as bp
from . import forms, send
from ..funcs import check_email_confirmed

report_email = os.getenv('REPORT_EMAIL')
current_folder = os.path.dirname(os.path.abspath(__file__))


@bp.route("/supplier/form/", methods=['GET', 'POST'])
@check_email_confirmed
def review_form():
    form = forms.SupplierReviewQuestionnaire()
    if request.method == 'POST':
        question_dict = request.form.to_dict()
        answer_df = pandas.DataFrame().from_dict(question_dict, orient='index', columns=['Answer'])
        answer_df.index
        flash('Form Submitted!', 'success')
        with current_app.app_context():
            send.send_report(report_email, answer_df)
        return render_template('form.html', form=form)
    return render_template('form.html', form=form)
