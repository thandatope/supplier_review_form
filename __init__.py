import os.path as op
import sys

from flask import Flask
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
import os

from .sqlite import db_session, init_db

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


def create_app():
    app = Flask(__name__)
    app.template_folder = "templates"
    app.static_folder = "static"

    init_db()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    app.debug = os.getenv('DEBUG')
    app.logger = os.getenv('LOGGING')
    app.env = os.getenv('ENV')

    from . import models
    from .ext import db, csrf, admin, migrate, login, mail

    db.init_app(app)
    csrf.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    admin.add_view(ModelView(models.User, db.session))
    path = op.join(op.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

    return app
