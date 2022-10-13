import os
import shutil
from flask import (flash, redirect, render_template,
                   request, url_for, current_app)
from werkzeug.utils import secure_filename
from . import datapack as bp
from . import forms, send
from ..funcs import check_email_confirmed, current_folder
import tempfile
from time import sleep
from ..ext import datapackset
from flask_uploads.exceptions import UploadNotAllowed
import shutil

report_email = os.getenv('REPORT_EMAIL')

@bp.route("/supplier/datapack", methods=['GET', 'POST'])
@check_email_confirmed
def datapack():
    form = forms.DataPackUpload()
    if request.method == 'POST' and 'datapack' in request.files:
        try:
            file_list = request.files.getlist('datapack')
            for f in file_list:
                datapackset.save(f, folder=request.form['company'])
            name = request.form['name']
            company = request.form['company']
            email = request.form['email']
            send.send_report(name, company, email)
            flash("Files uploaded!", "success")
            return redirect(url_for('home.supplier'))
        except UploadNotAllowed:
            flash("File types not allowed", "danger")
            return redirect(url_for('datapack.datapack', form=form))
    return render_template('datapack.html', form=form)
