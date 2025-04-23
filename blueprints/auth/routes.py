from flask import Blueprint, render_template, redirect, url_for, request, session
from config import PASSWORD, USERNAME
auth = Blueprint('auth',__name__, template_folder="templates")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['user_id'] = username
            return redirect(url_for('home.index'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login_page.html', error=error)
    return render_template('login_page.html', error=None)

@auth.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))