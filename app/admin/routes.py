from functools import wraps

from flask import abort, render_template
from flask_login import current_user, login_required

from app.admin import bp
from app.models import User


def check_admin(func):
    @wraps(func)
    def wrap():
        if not current_user.is_admin:
            abort(403)
    return wrap

@bp.route('/dashboard')
@check_admin
@login_required
def admin_dashboard():

    return render_template('admin/dashboard.html', title='Dashboard')



@bp.route('/users_list', methods=['GET', 'POST'])
@check_admin
@login_required
def list_users():
    users = User.query.all()
    user_status = str()
    for user in users:
        if user.is_admin:
            user_status = 'Admin'
        else:
            user_status = 'No admin'
    return render_template('admin/users_list.html', users=users, title = 'Users', status=user_status)
