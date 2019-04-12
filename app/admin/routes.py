from flask import abort, render_template
from flask_login import current_user, login_required

from app.admin import bp
from app.models import User


def check_admin():
    if not current_user.is_admin:
        abort(403)


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    check_admin()
    return render_template('admin/dashboard.html', title='Dashboard')


@bp.route('/users_list', methods=['GET', 'POST'])
@login_required
def list_users():
    check_admin()
    users = User.query.all()
    return render_template('admin/users_list.html', users=users, title='Users')
