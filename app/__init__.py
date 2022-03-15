from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from app.errors import not_found
import os

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

DB_USER='postgres'
DB_PASS='adminlemmy'
ENV='Prod'

def create_app():
    app = Flask(__name__)

    from .views import view, cat, blog
    from .auth import auth

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(blog, url_prefix='/blogs')
    app.register_blueprint(cat, url_prefix='/blogs/category')
    app.register_error_handler(404, not_found)

    if ENV =='dev':
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost/blogapp'
    else:
        URI = os.environ.get('DATABASE_URL')
        if URI.startswith('postgres://'):
            URI= URI.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = URI

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('SEND_MAIL')
    app.config['MAIL_PASSWORD'] = os.environ.get('SEND_MAIL_PASS')

    db.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)

    if ENV == 'dev': create_database(app)
    
    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

from app import views
