from flask_mailman import Mail
from flask_wtf import CSRFProtect
from flask_uploads import UploadSet, DEFAULTS
from flask_debugtoolbar import DebugToolbarExtension
import bleach


csrf = CSRFProtect()
mail = Mail()
debug_toolbar = DebugToolbarExtension()
datapackset = UploadSet(name="datapackfiles", extensions=DEFAULTS)
formset = UploadSet(name="formfiles", extensions=DEFAULTS)


def identity_mapper(identity):
    return bleach.clean(identity, strip=True)