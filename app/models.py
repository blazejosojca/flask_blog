import jwt
from app import db, login
from time import time
from flask_login import UserMixin
from flask import current_app
from datetime import datetime
from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from whoosh.analysis import StemmingAnalyzer


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    image_file = db.Column(db.String(48), nullable=False,
                           default='default.jpg')
    password_hashed = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    about_me = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    is_admin = db.Column(db.Boolean, default=False)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def set_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)

    def __repr__(self):
        return '<User - {0}, {1},{2} >'.format(self.username, self.email, self.image_file)


def verify_reset_password_token(token):
    try:
        user_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                             algorithms=['HS256'])['reset_password']
    except:
        return None
    return User.query.get(user_id)


class Post(db.Model):

    __searchable__ = ['title', 'content']
    __analyzer__ = StemmingAnalyzer()

    PUBLIC_STATUS = 0
    DRAFT_STATUS = 1
    DELETED_STATUS = 2

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.SmallInteger)

    def display_post_status(self):
        if self.status == self.PUBLIC_STATUS:
            return 'Public'
        elif self.status == self.DRAFT_STATUS:
            return 'Draft'
        elif self.status == self.DELETED_STATUS:
            return'Deleted'

    def __repr__(self):
        return '<Post - {0}, {1}, status {2}>'.format(self.title, self.date_posted, self.status)
