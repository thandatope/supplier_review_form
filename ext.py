from flask_admin import Admin
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
import bleach


db = SQLAlchemy()
login = LoginManager()
csrf = CSRFProtect()
admin = Admin()
toolbar = DebugToolbarExtension()
migrate = Migrate()
sec = Security()
mail = Mail()


def identity_mapper(identity):
    return bleach.clean(identity, strip=True)