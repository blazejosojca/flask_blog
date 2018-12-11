import os
import secrets
from hashlib import md5
from flask import (render_template,
                   url_for,
                   flash,
                   request,                   
                   redirect)

from werkzeug.urls import url_parse
from datetime import datetime
from flask_login import (current_user,
                         login_user,
                         logout_user,
                         login_required)

from app import app, db
from app.forms import (RegistrationForm,
                       LoginForm,
                       UpdateUserForm)
from app.models import User


POSTS = [
    {
        'author': 'Name Surname',
        'title': 'Post title',
        'content': 'Post 1 content',
        'date_posted': '01.01.2011',
    },
    {
        'author': 'Jan Kowalski',
        'title': 'Poemat',
        'content': 'Post 2 content',
        'date_posted': '02.02.2018',
    }
]


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='home', posts=POSTS)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(f"A new user added. Congratulations!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/user_update", methods=['GET', 'POST'])
@login_required
def user_update():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file = User.save_image_file(form.image_file.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes has been saved!")
        return redirect(url_for('user_update'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('user_update.html', title='User update', form=form)


# TODO - finish this part - add links and template
@app.route('/user/<username>', methods=['GET'])
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user_details.html', user=user, posts=posts, title='User details', image_file=image_file)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Credentials are incorrect!', 'warning')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('about'))


@app.route('/account/<username>', methods=['GET', 'POST'])
@login_required
def account(username):
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('account.html', user=user, image_file=image_file, title='Account')
