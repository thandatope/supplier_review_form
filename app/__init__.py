import os
import sys

from flask import Flask
from flask_uploads import configure_uploads

from .config import Config, Development, Production

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(Development)
        """        
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
        app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
        app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
        app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL")
        app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config["SESSION_PROTECTION"] = "strong"
        app.config["UPLOADS_DEFAULT_DEST"] = "/temp/"
        app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024
        app.config["UPLOADED_DATAPACKFILES_DEST"] = basedir + "/temp/datapack"
        app.config["UPLOADED_FORMFILES_DEST"] = basedir + "/temp/form"
        app.config["UPLOADED_ZIPFILES_DEST"] = basedir + "/temp/zip"
        app.config['DEBUG_TB_ENABLED'] = True
        app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
        app.config["DEBUG_TB_TEMPLATE_EDITOR_ENABLED"] = True
        app.config["TOASTR_TIMEOUT"] = 5000
        app.config["TOASTR_POSITION_CLASS"] = "toast-top-full-width"
        """

        app.debug = os.getenv("DEBUG")
        app.logger = os.getenv("LOGGING")
        app.env = os.getenv("ENV")

        from .blueprints.review_form import review_form
        from .blueprints.home import index
        from .blueprints.datapack import datapack
        from .blueprints.new_supplier import new_supplier

        app.register_blueprint(review_form)
        app.register_blueprint(index)
        app.register_blueprint(datapack)
        app.register_blueprint(new_supplier)

        from .ext import csrf, mail, datapackset, formset, toolbar, toast

        csrf.init_app(app)
        # mail.init_app(app)
        toolbar.init_app(app)
        configure_uploads(app, datapackset)
        configure_uploads(app, formset)
        toast.init_app(app)

        return app
