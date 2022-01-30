from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user, logout_user, login_required

auth=Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')

@auth.route('/register/', methods=['GET', 'POST'])
@auth.route('/register', methods=['GET', 'POST'])
def register():
	return render_template('register.html')

@auth.route('/logout/', methods=['GET', 'POST'])
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('views.home'))
