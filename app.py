import logging
import os

from flask import (flash, redirect, render_template,
                   request, url_for, session)
from flask.logging import default_handler
from werkzeug.utils import secure_filename
from . import create_app, forms, models
from .send import send_report
import pandas
from .ext import login

log_format = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename='logfile.log', filemode='w', format=log_format, level=logging.DEBUG)
logger = logging.getLogger()
logger.addHandler(default_handler)

basedir = os.path.abspath(os.path.dirname(__file__))
report_email = os.getenv('REPORT_EMAIL')

app = create_app()
app.debug = True


@login.user_loader
def load_user(user_id):
    return models.User.Objects(id=user_id).first()


@app.route("/", methods=['GET', 'POST'])
def index():
    form = forms.FrontForm()
    if form.validate_on_submit():
        session['email'] = request.form['email']
        flash("A confirmation code has been sent to the email address entered.\n\n Please enter the code received "
              "below.", category="success")
        return redirect(url_for("passcode"))
    return render_template("index.html", form=form)


@app.route("/login")
def login():
    # temporary until admin login sorted
    return redirect(url_for("admin.index"))


@app.route("/auth", methods=['GET', 'POST'])
def passcode():
    # get OTP
    form = forms.CodeForm()
    if form.validate_on_submit():
        return redirect(url_for("supplier"))
    # here put in OTP logic or something similar to avoid needing account
    return render_template("index.html", form=form)


@app.route("/supplier", methods=['GET', 'POST'])
def supplier():
    form = forms.ReviewType()
    if request.method == 'POST':
        if request.form['review_type'] == 'datapack':
            return redirect(url_for('datapack'))
        elif request.form['review_type'] == 'form':
            return redirect(url_for('review_form'))
    else:
        return render_template("review_type.html", form=form)
    render_template("review_type.html", form=form)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/supplier/datapack", methods=['GET', 'POST'])
def datapack():
    form = forms.DataPackUpload()
    uploaded_files = []
    if request.method == 'POST':
        logger.info('=== request info datapack submit ===')
        logger.info(request.values)
        logger.info(request.files)
        logger.info(request.files.values())
        if request.files is None:
            logger.info('no file')
        else:
            for x in request.files:
                logger.info(request.files[x])
                file = request.files[x]
                name = request.form.get('company')
                sec_filename = secure_filename(file.filename)
                save_path = os.path.join(basedir, 'review_uploads', name)
                file_to_save = os.path.join(save_path, sec_filename)
                if os.path.exists(save_path) is not True:
                    os.mkdir(save_path)
                    uploaded_files = os.listdir(save_path)

                else:
                    uploaded_files = os.listdir(save_path)

                if os.path.exists(file_to_save):
                    logger.info('FILE EXISTS - NOT SAVED')
                    flash('Not saved - File exists', 'danger')
                else:
                    file.save(os.path.join(file_to_save))
                    logger.info('file saved: ' + sec_filename)

                    flash(sec_filename + ' saved!', 'success')
            return redirect(url_for('datapack', form=form, uploaded_files=uploaded_files))
    return render_template('datapack.html', form=form, uploaded_files=uploaded_files)


@app.route("/supplier/form/", methods=['GET', 'POST'])
def review_form():
    form = forms.SupplierReviewQuestionnaire()
    if request.method == 'POST':
        logger.info('=== request info form submit ===')
        logger.info(request.values)
        logger.info(request.form.to_dict)
        question_dict = request.form.to_dict()
        logger.info(question_dict)
        answer_df = pandas.DataFrame().from_dict(question_dict, orient='index', columns=['Answer'])
        print(f"Answer DF: \n\n\n{answer_df.to_string()}\n\n\n")
        # USE A PANDAS DATAFRAME TO STORE QUESTIONS, ANSWERS AND SCORES FOR REPLIES ETC
        # ALSO FIX AND USE CLASS FOR RESULTS
        # generate_report(answer_df)
        flash('Form Submitted!', 'success')
        env = app.jinja_env
        temp = env.get_template(name='report/report_pd.html')

        with open('reports/html/report_pd.html', "w") as f:
            f.write(temp.render(dataframe=answer_df))
        with app.app_context():
            send_report(report_email, "reports/html/report_pd.html")
        return render_template('form.html', form=form)

    return render_template('form.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
