import os
import shutil
from flask import flash, redirect, render_template, request, url_for, current_app
from werkzeug.utils import secure_filename
from . import datapack as bp
from . import forms, send
from ..funcs import check_email_confirmed
import tempfile
from time import sleep
from flask_uploads import UploadSet

report_email = os.getenv("REPORT_EMAIL")
current_folder = os.path.dirname(os.path.abspath(__file__))
datapack_files = UploadSet()


@bp.route("/supplier/datapack", methods=["GET", "POST"])
@check_email_confirmed
def datapack():
    form = forms.DataPackUpload()
    if request.method == "POST":
        if request.files is None:
            flash("No file attached.", category="danger")
        else:
            for x in request.files:
                file = request.files[x]
                name = request.form.get("company")
                sec_filename = secure_filename(file.filename)
                save_path = os.path.join(current_folder, "tmp", name)
                file_to_save = os.path.join(save_path, sec_filename)
                if os.path.exists(save_path) is not True:
                    os.mkdir(save_path)
                if os.path.exists(file_to_save):
                    flash("Not saved - File exists", "danger")
                else:
                    file.save(file_to_save)
            name = request.form.get("company")
            path = os.path.join("review_uploads", name)
            z_name = f"{name}.zip"
            shutil.make_archive(name, "zip", path)
            send.send_report(report_email, z_name)
            os.remove(z_name)
            flash("Datapack submitted.", "success")
            return redirect(url_for("home.supplier"))

    return render_template("datapack.html", form=form)
