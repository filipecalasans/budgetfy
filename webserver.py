import services
from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, login_user, LoginManager, login_required
from forms import LoginForm

import services

import os
import ptvsd
import socket

ptvsd.enable_attach(redirect_output=True)

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'asdhkhjakj1912&@#{?8912qonvxm,cvcn!&@!@#%@#!'

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return services.get_user(user_id)

@app.route('/')
@app.route('/index')
@login_required
def index():
	return "Home page budget control"

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = LoginForm()
	if form.validate_on_submit():
		user = services.get_user_by_name(form.username.data)
		if user is None or not user.check_password(form.password.data):
			# flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.debug = True
	app.run(use_reloader=False, host='0.0.0.0', port=5000)
