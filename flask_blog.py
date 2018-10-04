from flask import Flask, render_template, url_for
from config_dir.config import keys
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = keys['secret_key']

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

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True)
