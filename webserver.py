import services
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from forms import LoginForm, RegistrationForm

import services
import secret 

import os
import ptvsd
import socket

ptvsd.enable_attach(redirect_output=True)

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = secret.FLASK_SECRET

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return services.get_user(user_id)

@app.route('/')
@app.route('/index')
def index():
	# This should redirect to the landing page
	if current_user.is_authenticated:
		return 'User is Authenticated'
	return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = LoginForm()
	if form.validate_on_submit():
		user = services.get_user_by_username(form.username.data)
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = RegistrationForm()
	if form.validate_on_submit():
		new_user = services.add_new_user(
			username=form.username.data,
			firstname=form.firstname.data,
			lastname=form.lastname.data,
			email=form.email.data,
			password=form.password.data)
		if new_user is None:
			flash('Error during registration, try again later!')
			return redirect(url_for('register'))
		return redirect(url_for('login'))
	return render_template('register.html', title='Registration', form=form)


if __name__ == '__main__':
	app.debug = True
	app.run(use_reloader=False, host='0.0.0.0', port=5000)
