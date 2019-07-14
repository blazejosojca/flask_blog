from flask import render_template

from app import db
from app.errors import bp


@bp.app_errorhandler(403)
def no_permission_error(error):
    return render_template('errors/403.html', title='Forbidden'), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', title='Page Not Found'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html', title='Server Error'), 500
