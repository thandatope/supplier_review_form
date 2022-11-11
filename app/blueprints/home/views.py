import json
import os
from datetime import timedelta

from flask import flash, redirect, render_template, request, url_for, session, current_app

from . import index as bp
from . import forms, send
from ...funcs import check_email_confirmed


@bp.before_app_first_request
def before_request():
    session.permanent = True
    bp.permanent_session_lifetime = timedelta(minutes=30)
    session.modified = True


@bp.route("/", methods=["GET", "POST"])
def index():
    form = forms.FrontForm()
    if request.method == "POST":
        user_email = request.form["email"]
        session["email"] = request.form["email"]
        session["otp"] = send.send_otp(user_email)
        flash(
                "A confirmation code has been sent to the email address entered.",
                category="success"
        )
        return redirect(url_for("home.passcode"))
    return render_template("home/index.html", form=form)


@bp.route("/auth", methods=["GET", "POST"])
def passcode():
    form = forms.CodeForm()
    if request.method == "POST":
        if not session["email"]:
            return redirect(url_for("home.index"))
        else:
            if request.form["code"] == session["otp"]:
                session["email_confirmed"] = True
                return redirect(url_for("home.supplier"))
            else:
                flash("Incorrect Code!", "danger")
                redirect(url_for("home.passcode"))
    return render_template("home/index.html", form=form)


@bp.route("/supplier", methods=["GET", "POST"])
@check_email_confirmed
def supplier():
    with open(current_app.config['HOME_CARD_JSON'], "r") as json_file:
        card_data = json.load(json_file)
    if request.method == "POST":
        if request.form["review_type"] == "datapack":
            return redirect(url_for("datapack.datapack"))
        elif request.form["review_type"] == "form":
            return redirect(url_for("review_form.review_form"))
    else:
        return render_template("home/review_type.html", card_data=card_data)
    render_template("home/review_type.html", card_data=card_data)


@bp.route("/contact")
def contact():
    return render_template("home/contact.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out", category="success")
    return redirect(url_for('home.index'))


@bp.route("/login")
def login():
    return redirect(url_for('home.index'))
