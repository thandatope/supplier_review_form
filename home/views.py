import logging
import os

from flask import (flash, redirect, render_template,
                   request, url_for, session)
from . import index as bp
from . import forms
from . import send
from ..funcs import check_email_confirmed
from datetime import timedelta


@bp.before_request
def before_request():
    session.permanent = True
    bp.permanent_session_lifetime = timedelta(minutes=30)
    session.modified = True


@bp.route("/", methods=['GET', 'POST'])
def index():
    form = forms.FrontForm()
    session['email_confirmed'] = False
    if request.method == 'POST':
        user_email = request.form['email']
        session['email'] = request.form['email']
        session['otp'] = send.send_otp(user_email)
        flash("A confirmation code has been sent to the email address entered.\n\n Please enter the code received "
              "below.", category="success")
        return redirect(url_for("home.passcode"))
    return render_template("index.html", form=form)


@bp.route("/auth", methods=['GET', 'POST'])
def passcode():
    form = forms.CodeForm()
    if request.method == 'POST':
        if not session['email']:
            return redirect(url_for('home.index'))
        else:
            if request.form['code'] == session['otp']:
                session['email_confirmed'] = True
                return redirect(url_for("home.supplier"))
            else:
                flash("Incorrect Code!", "danger")
                redirect(url_for('home.passcode'))
    return render_template("index.html", form=form)


@bp.route("/supplier", methods=['GET', 'POST'])
@check_email_confirmed
def supplier():
    form = forms.ReviewType()
    if request.method == 'POST':
        if request.form['review_type'] == 'datapack':
            return redirect(url_for('datapack.datapack'))
        elif request.form['review_type'] == 'form':
            return redirect(url_for('review_form.review_form'))
    else:
        return render_template("review_type.html", form=form)
    render_template("review_type.html", form=form)


@bp.route("/contact")
def contact():
    return render_template("contact.html")
