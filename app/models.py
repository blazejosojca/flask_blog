import jwt
from app import db, login
from time import time
from flask_login import UserMixin
from flask import current_app
from datetime import datetime
from werkzeug.security import (generate_password_hash,
                               check_password_hash)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


post_tags = db.Table(
    'post_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

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
    __searchable__ = ['body']
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1
    STATUS_DELETED = 2
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status =  db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    tags = db.relationship('Tag', secondary=post_tags,
                           backref=db.backref('posts', lazy='dynamic'))


    def __repr__(self):
        return '<Post - {0}, {1}>'.format(self.title, self.date_posted)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return '<Tag {}>'.format(self.name) 
