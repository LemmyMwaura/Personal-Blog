from flask import render_template,redirect,url_for,request,flash
from sqlalchemy import desc
from app.auth import auth
from app import db
from app import mail
from app.mailapp import mail_message
from app.models import Blog, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if user:= User.query.filter_by(email=email).first():
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('view.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('login.html', text='Testing', user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form.get('fname')
        lastname = request.form.get('lname')
        email = request.form.get('email')
        username = request.form.get('uname')
        password = request.form.get('pass')
        confirm_password = request.form.get('cpass')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use', category='error')
        elif username_exists:
            flash('Username is alredy in use', category='error')
        elif password != confirm_password:
            flash('Passwords don\'t match', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif len(password) < 8:
            flash('Password is too short', category='error')
        elif len(email) < 4:
            flash('Email is invalid', category='error')
        else:
            new_user= User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                username=username,
                password=generate_password_hash(password, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            # mail_message('Welcome to Blogs App',
            #                     'email/welcome',
            #                     new_user.email, 
            #                     user=new_user
            # )
            
            flash(f'Hi {username}, Your Account was created', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('view.home'))

    return render_template('sign_up.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('view.home'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_picked = request.form.get('category')
        poster_id = current_user.id

        if category_picked == 'Buiness/Ecommerce':
            category_id = 1
        elif category_picked == 'Tech':
            category_id = 2
        elif category_picked == 'Games':
            category_id = 3
        elif category_picked == 'Fashion':
            category_id = 4
        elif category_picked == 'Science':
            category_id = 5
        elif category_picked == 'Crypto/Web3':
            category_id = 6

        new_post = Blog(title, content, category_id, poster_id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created')
    user_posts = Blog.query.filter_by(poster_id=current_user.id)
    user_posts = user_posts.order_by(desc(Blog.date_posted))
    return render_template('profile.html', user=current_user, posts=user_posts)
