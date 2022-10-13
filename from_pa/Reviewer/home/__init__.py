from flask import Blueprint

index = Blueprint('home',
                  __name__,
                  template_folder='templates',
                  static_folder='static'
                  )

from . import views


