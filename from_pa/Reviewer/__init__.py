import sys

from flask import Flask, Blueprint
import os
from flask_uploads import configure_uploads

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
basedir = os.path.abspath(os.path.dirname(__file__))
report_email = os.getenv('REPORT_EMAIL')


def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
        app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
        app.config['MAIL_USE_SSL'] = True
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['SESSION_PROTECTION'] = 'strong'
        app.config['MAX_CONTENT_LENGTH'] = (32 * 1024 * 1024)
        app.config["UPLOADED_DATAPACKFILES_DEST"] = basedir + "/temp/datapack"
        app.config["UPLOADED_FORMFILES_DEST"] = basedir + "/temp/form"
        app.config["UPLOADED_ZIPFILES_DEST"] = basedir + "/temp/zip"
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = False


        app.debug = os.getenv('DEBUG')
        app.logger = os.getenv('LOGGING')
        app.env = os.getenv('ENV')

        from .review_form import review_form
        from .home import index
        from .datapack import datapack

        app.register_blueprint(review_form)
        app.register_blueprint(index)
        app.register_blueprint(datapack)

        from .ext import csrf, mail, datapackset, formset, debug_toolbar

        csrf.init_app(app)
        mail.init_app(app)
        # debug_toolbar.init_app(app)
        configure_uploads(app, datapackset)
        configure_uploads(app, formset)

        return app
