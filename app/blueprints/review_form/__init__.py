from flask import Blueprint

review_form = Blueprint(
        "review_form", __name__, template_folder="templates", static_folder="static"
)

from . import views
