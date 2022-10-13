from flask import Blueprint

new_supplier = Blueprint(
        "new_supplier", __name__, template_folder="templates", static_folder="static"
)

from . import views
