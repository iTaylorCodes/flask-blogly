"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def to_users():
    """Shows a list of all users in db"""
    return redirect('/users')

# Users Routes

@app.route('/users')
def list_users():
    """Shows a list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def show_new_user_form():
    """Shows a form to add a new user"""
    return render_template('user_form.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """Adds a new user to db"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Shows a form to edit a user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Processes the user edits and updates db"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deletes a user"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# Posts routes

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """Displays a form to add a new post"""
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_add_post_form(user_id):
    """Handler for adding a new post"""
    user = User.query.get_or_404(user_id)

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """Displays detail page for a post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """Shows a form to edit a post, or to cancel and go back to user page"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit_form.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_post_edit_form(post_id):
    """Handler for editing of a post."""
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def handle_post_delete(post_id):
    """Handler for deleting of a post."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')