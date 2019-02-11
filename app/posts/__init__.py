from flask import Blueprint

bp = Blueprint('posts', __name__)

from app.posts import forms, routes
