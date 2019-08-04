from flask import abort, render_template, session, redirect, url_for, request
from flask_login import current_user, login_required
from flask_admin import Admin, BaseView
from flask_admin.contrib.sqla import ModelView

from app.models import User, Post
from app import db, admin



class MyModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authrnticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect()

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))

