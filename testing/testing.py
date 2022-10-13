import datetime
import wtforms
from flask import Flask, render_template_string, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import StringField, SelectField, SubmitField, DateField, TextAreaField, SelectMultipleField, BooleanField, \
    MultipleFileField
from flask_wtf import FlaskForm
from spacy.lang.en import English
import pandas as pd
import pandasgui
import threading


class TestForm(FlaskForm):
    name = StringField('Completed By Name')
    date = DateField("Completed On Date")
    email = StringField('Completed By Email')
    address = TextAreaField('Address')

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

    accreditation = [('9001', 'ISO 9001'),
                     ('17025', 'ISO 17025'),
                     ('17034', 'ISO 17034'),
                     ('17043', 'ISO 17043'),
                     ('regulatory', 'Inspected by a regulatory body (MHRA, FDA)')]

    service_type = SelectField('What best describes the services your company provides?', choices=company_types)
    accreditation = SelectMultipleField('Are you accredited to any of the below? Select all that apply.',
                                        choices=accreditation)
    free_text = StringField('Free text enter here')
    bool = BooleanField('this is boolean')
    file = MultipleFileField('oh dear files')
    submit = SubmitField(label='Submit')

def quality_supplier_review(results_dataframe):
    pass

def business_supplier_review(results_dataframe):
    pass

def other_supplier_review(results_dataframe):
    pass

def process_form(results_dataframe):
    quality_list = ['media', 'prof', 'calibration', 'subcon', 'test_kits', 'archiving', 'confidential']
    business_list = ['vendor', 'servicing', 'facilities']
    other_list = ['other']
    is_in = results_dataframe.isin(quality_list)
    for x in quality_list:
        resp = results_dataframe.answer.str.contains(x)
        if resp.any():
            print("there is a tru")
            print(f"The type of supplier is: {x}")
            print("confirmed qualiy supplier -> go to further review")
            break


app = Flask(__name__)
app.config['SECRET_KEY'] = "helo"


@app.route("/", methods=['GET', 'POST'])
def form_test():
    form = TestForm()
    if request.method == 'POST':
        # start automatic processing based on service type
        response_data = []
        for x in iter(form):
            name_str = str(x.name)
            response_data.append([name_str, x.label.text, x.data])
        print(response_data)
        df = pd.DataFrame(response_data, columns=['field', 'question', 'answer'], dtype=pd.StringDtype())
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
        """, form=form
    )


if __name__ == "__main__":
    # pandasgui.show()
    app.run(debug=True)
