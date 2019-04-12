from app import db, create_app
from app.models import User, Post
from flask_script import Manager
import unittest


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

if __name__ == '__main__':
    app.run()
