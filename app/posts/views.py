from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
from .functions import read_posts, write_posts, get_new_id
from .models import Post, Tag
from app.users.models import User
from app import db



@post_bp.route('/')
def get_posts():
    stmt= db.select(Post).order_by(Post.posted)
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    stmt = db.select(Post).where(Post.id == id)
    post = db.session.scalar(stmt)
    if post is None:
        abort(404)
    return render_template("detail_post.html", post=post)


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    form.author_id.choices = [(author.id, author.username) for author in User.query.all()]
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, 
                        content=form.content.data, 
                        category=form.category.data,
                        is_active = form.is_active.data,
                        author=User.query.get(form.author_id.data),
                        date = form.publish_date.data
                        )
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        new_post.tags.extend(selected_tags)
        db.session.add(new_post)
        db.session.commit()
        flash('Post {new_post.title} added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))

    return render_template('add_post.html', form=form)
@post_bp.route('/<int:id>/edit', methods=['GET','POST'])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    form.publish_date.data = post.posted
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        post.posted = form.publish_date.data
        db.session.commit()
        flash('Post updated succsessfully')
        return redirect(url_for(".get_posts"))
    return render_template("add_post.html", form=form, post=post)


