from flask import render_template, url_for, flash, redirect
from flask_login import current_user, login_user, logout_user

from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User


posts = [
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


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"A new user: {form.username.data}added. Congratulations!", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('/home'))
    else:
        flash('Credentials are incorrect', 'danger')

    #TODO - verification of credentials
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/home'))
