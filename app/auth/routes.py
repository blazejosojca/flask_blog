from datetime import datetime

from flask import url_for, render_template, flash, request, g
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import lazy_gettext as _l, get_locale
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import db
from app.models import User

from app.auth import bp
from app.auth.email import send_password_reset_email
from app.auth.utils import save_image_file
from app.auth.forms import (RegistrationForm,
                            LoginForm,
                            UpdateUserForm,
                            RequestResetForm,
                            ResetPasswordForm,
                            DeleteUserForm,
                            )
from app.posts.forms import SearchForm


@bp.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(_l("A new user added. Congratulations!"), 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(_l('You were logged in!'), 'info')

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.home')
            return redirect(next_page)
        else:
            flash(_l('Credentials are incorrect!'), 'warning')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.about'))


@bp.route('/account/<username>', methods=['GET', 'POST'])
@login_required
def account(username):
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('auth/account.html', user=user, image_file=image_file, title='Account')


@bp.route("/user_update", methods=['GET', 'POST'])
@login_required
def user_update():
    form = UpdateUserForm(current_user.username, current_user.email)
    if form.validate_on_submit() is True:
        if form.image_file.data:
            image_file = save_image_file(form.image_file.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash(_l("Your change has been saved!"), 'info')
        return redirect(url_for('auth.user_update'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('auth/user_update.html', title='User update', form=form)


@bp.route('/user/delete', methods=['GET', 'POST'])
@login_required
def user_delete():
    form = DeleteUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if current_user == user or current_user.is_admin:
            db.session.delete(user)
            db.session.commit()
            flash(_l("User was deleted"))
            if current_user.is_admin:
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('main.home'))
        else:
            return redirect('errors/403.html')
    return render_template('auth/user_delete.html', title='User delete', form=form)


# @bp.route('/user/<username>', methods=['GET'])
# #TODO -> add variables 'public, drafts, deleted' for feature which allow to sees posts by categories
#
# def user_posts(username, category):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     # order_by(Post.date_posted.desc())
#     posts = Post.query.filter_by(user_id=user.id)\
#         .filter_by(statusposts=category)\
#         .order_by(Post.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#     return render_template('auth/posts_user_details.html',
#                            user=user, posts=posts,
#                            title='User details',
#                            image_file=image_file)


@bp.route("/reset_password", methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_l('The email has been sent to reset your password!'), 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_l('Your password has been reset!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password',
                           title='Reset Password',
                           form=form)
