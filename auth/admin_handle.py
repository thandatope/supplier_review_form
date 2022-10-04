from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from . import models
from flask import g, current_app
import os.path as op
from flask_admin import Admin


class AdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/admin-index.html')


def create_admin_views(admin):
    admin = Admin(template_mode='bootstrap3')
    admin.add_view(ModelView(models.User, db.session))
    admin.add_view(ModelView(models.SupplierUser, db.session))
    admin.add_view(ModelView(models.Supplier, db.session))
    admin.add_view(ModelView(models.Capa, db.session))
    admin.add_view(ModelView(models.ReviewStatus, db.session))
    admin.add_view(ModelView(models.FormResponse, db.session))
    path = op.join(op.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

    return admin
