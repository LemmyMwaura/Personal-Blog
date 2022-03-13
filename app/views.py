from app import db
from app.models import Category, Blog, Comment, Like
from flask import redirect, render_template, Blueprint, flash, request, url_for, jsonify
from flask_login import current_user,login_required

view = Blueprint('view',__name__)
cat = Blueprint('cat',__name__)
blog = Blueprint('blog',__name__)

@view.route('/')
@view.route('/home')
def home():
    categories = ['Buiness/Ecommerce','Tech','Games','Fashion','Science','Crypto/Web3']
    for category in categories:
        if not (_ := Category.query.filter_by(name=category).first()):
            new_category = Category(category)
            db.session.add(new_category)
            db.session.commit()

    all_categories = Category.query.order_by(Category.id)
    return render_template('index.html', user=current_user, categories=all_categories)

@blog.route('/')
def posts():
    title='All Blogs'
    all_posts = Blog.query.order_by(Blog.date_posted)
    return render_template('posts.html', user=current_user, posts=all_posts, title=title)

@blog.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post_to_delete = Blog.query.get_or_404(post_id)
    try:
        if current_user.id != post_to_delete.poster.id:
            flash('You do not have permission to delete this post.(Not the author)', category='danger')
        else:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Blog post was deleted", category='success')
    except:
        flash('Woops there was a problem deleting post. Try again', category='danger')

    title='All Blog Posts'
    all_posts = Blog.query.order_by(Blog.date_posted)
    return render_template('posts.html', user=current_user, posts=all_posts, title=title)

@blog.route('/create-comment/<post_id>', methods=['GET', 'POST'])
@login_required
def create_comment(post_id):
    if text := request.form.get('text'):
        if _ := Blog.query.filter_by(id=post_id):
            comment = Comment(text=text, post_id=post_id, poster_id=current_user.id)
            print(comment.text)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist', category='error')
    else:
        flash('Comment cannot be empty.', category='error')  

    return redirect(url_for('blog.posts'))

@blog.route('/delete_comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist', category='error')
    elif current_user.id != comment.poster_id and current_user.id != comment.post.poster_id:
        flash('You do not have permission to delete this comment', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('blog.posts'))

@blog.route('/like-post/<post_id>', methods=['GET','POST'])
@login_required
def like(post_id):
    post = Blog.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({'likes':len(post.likes.all()), 'liked':current_user.id in map(lambda x:x.author, post.likes)})

@cat.route('/Business')
def bsns():
    title='Business'
    bsns_posts = Blog.query.filter_by(category_id=1)
    return render_template('posts.html', user=current_user, posts=bsns_posts, title=title)

@cat.route('/Technology')
def tech():
    title='Technology'
    tech_posts = Blog.query.filter_by(category_id=2)
    return render_template('posts.html', user=current_user, posts=tech_posts, title=title)

@cat.route('/Gaming')
def games():
    title='Gaming'
    games_posts = Blog.query.filter_by(category_id=3)
    return render_template('posts.html', user=current_user, posts=games_posts, title=title)

@cat.route('/Fashion')
def fashion():
    title='Fashion'
    fashion_posts = Blog.query.filter_by(category_id=4)
    return render_template('posts.html', user=current_user, posts=fashion_posts, title=title)

@cat.route('/Science')
def science():
    title='Science'
    science_posts = Blog.query.filter_by(category_id=5)
    return render_template('posts.html', user=current_user, posts=science_posts, title=title)

@cat.route('/Crypto-web3')
def crypto():
    title='Crypto/Web-3'
    web3_posts = Blog.query.filter_by(category_id=6)
    return render_template('posts.html', user=current_user, posts=web3_posts, title=title)

