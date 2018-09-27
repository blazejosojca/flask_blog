from flask import Flask, render_template

app = Flask(__name__)


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
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
