from flask import render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from app import app


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
        'content': 'Post 2 contetnt',
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


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login and password are correct. Welcome user! ", "success")

        return redirect(url_for('home'))
    else:
        flash('Credentials are incorect', 'danger')

    #TODO - verification of credentials
    return render_template('login.html', title='Login', form=form)



