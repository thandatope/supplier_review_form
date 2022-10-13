from functools import wraps
from flask import session, flash, redirect, url_for


def check_email_confirmed(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            session.get('email_confirmed')
            if session['email_confirmed'] is False:
                flash("Email not confirmed", "danger")
                return redirect(url_for('home.index'))
            elif session['email_confirmed'] is True:
                return f(*args, **kwargs)
        except:
            flash("No session!", "danger")
            return redirect(url_for('home.index'))

    return wrap


def get_test_flask():
    from . import create_app
    app = create_app()
    return app
