"""

Condense down json settings and fix paths for use on pythonanywhere
Use templates for reports once out of testing, generally make less ugly
Should probably make form responsive to reflect the differing question requirements
Implement actions to do on review, such as checking certificate attachments, reviewing company change etc.
    Maybe leave space for review notes which can then be saved + signed?
Switch to lists vs strings if poss in models, use funcs to convert to <br> strings
Add contextual/severity font colourings etc to template
Maybe add tick boxes for supplier to indicate what has been attached? Would make assessment easier

Mostly working for quality based suppliers at the moment as others are just going to be based on this with irrelevant info removed


"""

import pandas as pd
from flask import Flask, render_template_string, request, send_file

from forms import TestForm
from review_funcs import process_form

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
            if type(x.data) is str:
                d = x.data.replace("\r\n", "<br>")
            else:
                d = x.data
            response_data.append([name_str, x.label.text, d])

        df = pd.DataFrame(
            response_data,
            columns=["field", "question", "answer"],
        )
        df.set_index("field", drop=True, inplace=True, verify_integrity=True)
        out = process_form(df)
        return send_file(
            out, mimetype="html", as_attachment=True, download_name="report.html"
        )

    return render_template_string(
        """<html><body style="font-family:Calibri; background-color:FloralWhite; text-align:center; align-items:center;">
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
