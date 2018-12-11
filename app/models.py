import os
import secrets
from PIL import Image
from app import app, db, login
from datetime import datetime
from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from flask_login import UserMixin


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

    def __repr__(self):
        return f'<User - {self.username}, {self.email}, {self.image_file} >'

    def set_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)

    @staticmethod
    def save_image_file(image_file):
        random_hex = secrets.token_hex(8)
        image_name, image_ext = os.path.split(image_file.filename)
        image_filename = random_hex + image_ext
        image_path = os.path.join(app.root_path, 'static/profile_pics', image_filename)
        image_file.save(image_path)
        return image_filename


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post - {self.title}, {self.date_posted}>'
