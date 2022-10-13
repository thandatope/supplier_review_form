import sys

from flask import Flask
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
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
        app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['SESSION_PROTECTION'] = 'strong'
        app.config['UPLOADS_DEFAULT_DEST'] = "/temp/"
        app.config['MAX_CONTENT_LENGTH'] = (32 * 1024 * 1024)

        app.debug = os.getenv('DEBUG')
        app.logger = os.getenv('LOGGING')
        app.env = os.getenv('ENV')

        from .review_form import review_form
        from .home import index
        from .datapack import datapack

        app.register_blueprint(review_form)
        app.register_blueprint(index)
        app.register_blueprint(datapack)

        from .ext import csrf, mail, datapack_set, form_set

        csrf.init_app(app)
        mail.init_app(app)

        # create required upload sets

        configure_uploads(app, datapack_set)
        configure_uploads(app, form_set)
        # 32 MB file size limit

        return app
