from flask import (url_for, render_template,
                   flash, request, abort, g)
from flask_login import current_user, login_required
from flask_babel import _
from werkzeug.utils import redirect

from app import db
from app.models import Post, User
from app.posts import bp
from app.posts.forms import PostForm, SearchForm
from app.main.routes import before_request

from app import Config
from flask_whooshalchemy import search_index

@bp.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.search_form = SearchForm()


@bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    status=form.status.data)
        db.session.add(post)
        db.session.commit()
        flash(_("Post was created"), 'success')
        return redirect(url_for('main.home'))
    return render_template('posts/create_post.html', title='New Post', form=form, legend='New Post')


@bp.route('/post/<int:post_id>')
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post_details.html', title=post.title, post=post)


@bp.route('/post/update/<int:post_id>', methods=['POST', 'GET'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.status = form.status.data
        db.session.add(post)
        db.session.commit()
        flash(_('Post has been updated!'), 'success')
        return redirect(url_for('posts.post_view', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.status.data = post.status
    return render_template('posts/create_post.html', title='Update Post', form=form, legend='Update Post')


@bp.route('/post/delete/<int:post_id>', methods=['POST', 'GET'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    post.status = Post.DELETED_STATUS
    db.session.add(post)
    db.session.commit()
    flash(_('Post has been deleted'))
    return redirect(url_for('main.home'))


@bp.route('/post/<username>', methods=['GET'])
def list_posts_per_user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # order_by(Post.date_posted.desc())
    posts = Post.query.filter_by(user_id=user.id)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('auth/user_details.html',
                           user=user, posts=posts,
                           title='User details',
                           image_file=image_file)
