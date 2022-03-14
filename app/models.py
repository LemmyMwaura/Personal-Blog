from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return f'User {self.name}'

class User(db.Model, UserMixin):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Blog', backref='user', lazy='dynamic', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', lazy='dynamic', passive_deletes=True)
    likes = db.relationship('Like', backref='user', lazy='dynamic', passive_deletes=True)

    def __init__(self, firstname, lastname, email, username, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'User {self.username}'

class Category(db.Model):
    __tablename__='categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    post_id = db.relationship('Blog', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name

class Blog(db.Model):
    __tablename__='blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'))
    comments = db.relationship('Comment', backref='blog', lazy='dynamic', passive_deletes=True)
    likes = db.relationship('Like', backref='blog', lazy='dynamic', passive_deletes=True)
    
    def __init__(self, title, content, category_id, poster_id):
        self.title = title
        self.content = content
        self.category_id = category_id
        self.poster_id = poster_id

class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('blogs.id', ondelete='CASCADE'))
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

class Like(db.Model):
    __tablename__='likes'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('blogs.id', ondelete='CASCADE'))
    author = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

class Quote():
    def __init__(self, author, quote):
        self.author = author
        self.quote = quote