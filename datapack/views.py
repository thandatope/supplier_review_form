import os
import shutil
from flask import (flash, redirect, render_template,
                   request, url_for, current_app)
from werkzeug.utils import secure_filename
from . import datapack as bp
from . import forms, send
from ..funcs import check_email_confirmed
import tempfile
from time import sleep
from ..ext import datapack_set

report_email = os.getenv('REPORT_EMAIL')
current_folder = os.path.dirname(os.path.abspath(__file__))


@bp.route("/supplier/datapack", methods=['GET', 'POST'])
@check_email_confirmed
def datapack():
    form = forms.DataPackUpload()
    if request.method == 'POST' and 'files' in request.files:
        filename = datapack_set.save(request.files, folder=request.form['company_name'])
        flash(filename, "success")
        return redirect(url_for('home.supplier'))

    return render_template('datapack.html', form=form)
