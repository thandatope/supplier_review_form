from flask_admin import Admin
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_uploads import UploadConfiguration, EXECUTABLES, SCRIPTS, AllExcept, UploadSet, DEFAULTS
import bleach

db = SQLAlchemy()
login = LoginManager()
csrf = CSRFProtect()
admin = Admin()
toolbar = DebugToolbarExtension()
migrate = Migrate()
sec = Security()
mail = Mail()
datapack_set = UploadSet(name="datapack_files", extensions=DEFAULTS)
form_set = UploadSet(name="form_files", extensions=DEFAULTS)


def identity_mapper(identity):
    return bleach.clean(identity, strip=True)
