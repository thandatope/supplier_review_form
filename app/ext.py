import bleach
import flask_toastr
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import (
    UploadSet,
    DEFAULTS,
)
from flask_wtf import CSRFProtect
from flask_redmail import RedMail

csrf = CSRFProtect()
toolbar = DebugToolbarExtension()
mail = RedMail()
toast = flask_toastr.Toastr()
datapackset = UploadSet(name="datapackfiles", extensions=DEFAULTS)
formset = UploadSet(name="formfiles", extensions=DEFAULTS)


def identity_mapper(identity):
    return bleach.clean(identity, strip=True)
