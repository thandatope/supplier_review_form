from flask import Blueprint

datapack = Blueprint('datapack',
                     __name__,
                     template_folder='templates',
                     static_folder='static'
                     )

from . import views
