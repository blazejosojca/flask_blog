import os

from flask import url_for, render_template, flash, request, abort
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from app import db
from app.models import Post, User
from app.posts import bp
from app.posts.forms import UpdatePostForm, CreatePostForm


@bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post was created", 'success')
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
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated!', 'success')
        return redirect(url_for('posts.post_view', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('posts/create_post.html', title='Update Post', form=form, legend='Update Post')


@bp.route('/post/delete/<int:post_id>', methods=['POST', 'GET'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('main.home'))