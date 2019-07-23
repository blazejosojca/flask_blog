from datetime import datetime

from flask import request, render_template, g, url_for
from flask_login import current_user, login_required
from flask_babel import get_locale
from werkzeug.utils import redirect

from app import db, Config
from app.main import bp
from app.models import Post

from app.posts.forms import SearchForm


@bp.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route("/", methods=['GET', 'POST'])
@bp.route("/home", methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    query = Post.query.filter(Post.status == Post.PUBLIC_STATUS).order_by(Post.date_posted.desc())
    posts = query.paginate(page=page, per_page=5)
    return render_template('main/home.html', title='Home', posts=posts)


@bp.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('main.home'))
    return redirect(url_for('main.search_results',
                            query=g.search_form.search.data))


@bp.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.search(query, Config.MAX_SEARCH_RESULTS).all()
    return render_template('posts/search_results.html',
                           query=query,
                           results=results)


@bp.route("/about")
def about():
    return render_template('main/about.html', title='About')
