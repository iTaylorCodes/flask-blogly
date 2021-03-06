"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS GO BELOW!

class User(db.Model):
    """Table of users"""

    __tablename__ = 'users'

    def __repr__(self):
        usr = self
        return f"<User id={usr.id} first_name={usr.first_name} last_name={usr.last_name} image_url={usr.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.Text, nullable=False)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    """Table of posts from users"""

    __tablename__ = 'posts'

    def __repr__(self):
        post = self
        return f"<Post id={post.id} title={post.title} content={post.content} created_at={post.created_at} user_id={post.user_id}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(50), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Returns a nicely formatted date."""

        return self.created_at.strftime('%a %b %-d  %Y, %-I:%M %p')

class PostTag(db.Model):
    """Join table of posts and their tags/tags and their posts"""

    __tablename__ = 'posts_tags'

    def __repr__(self):
        post_tag = self
        return f"<PostTag post_id={post_tag.post_id} tag_id={post_tag.tag_id}>"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    """Table of tags added to posts"""

    __tablename__ = 'tags'

    def __repr__(self):
        tag = self
        return f"<Tag id={tag.id} name={tag.name}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(25), nullable=False, unique=True)

    posts = db.relationship('Post', secondary = 'posts_tags', backref='tags',)

