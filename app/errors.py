from flask import render_template
from flask_login import current_user

def not_found(e):
    return render_template('404.html', user=current_user.id), 404