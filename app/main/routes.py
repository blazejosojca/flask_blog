from datetime import datetime

from flask import Blueprint, request, render_template
from flask_login import current_user

from app import db
from app.main import bp
from app.models import Post

from app import main


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route("/")
@bp.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    query = Post.query.order_by(Post.date_posted.desc())
    posts = query.paginate(page=page, per_page=5)
    return render_template('main/home.html', title='Home', posts=posts)


@bp.route("/about")
def about():
    return render_template('main/about.html', title='About')



