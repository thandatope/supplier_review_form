import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    SESSION_COOKIE_SECURE = True
    SESSION_PROTECTION = "strong"
    UPLOADS_DEFAULT_DEST = "/temp/"
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    UPLOADED_DATAPACKFILES_DEST = basedir + "/temp/datapack"
    UPLOADED_FORMFILES_DEST = basedir + "/temp/form"
    UPLOADED_ZIPFILES_DEST = basedir + "/temp/zip"
    TOASTR_TIMEOUT = 5000
    TOASTR_POSITION_CLASS = "toast-top-full-width"
    EXPLAIN_TEMPLATE_LOADING = False
    HOME_CARD_JSON = os.path.join(basedir, "home_cards.json")


class Production(Config):
    pass


class Development(Config):
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
