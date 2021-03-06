import services
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from forms import LoginForm, RegistrationForm, ExpenseForm, CategoryForm
from flask_oauthlib.client import OAuth, OAuthException

import services
import secret 

import os
import ptvsd
import socket

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# ptvsd.enable_attach(redirect_output=True)

app = Flask(__name__)
oauth = OAuth(app)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = secret.FLASK_SECRET

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=secret.FACEBOOK_APP_ID,
    consumer_secret=secret.FACEBOOK_SECRET,
    request_token_params={'scope': 'email'}
)

@app.teardown_request
def remove_session(ex=None):
	services.remove_session()

@login_manager.user_loader
def load_user(user_id):
    return services.get_user(user_id)

@app.route('/index')
def landing_page():
	return redirect(url_for('login'))

@app.route('/')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('user_expenses'))
	return redirect(url_for('landing_page'))


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


@app.route('/login-facebook')
def login_facebook():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	callback = url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
	return facebook.authorize(callback=callback)


@app.route('/login/authorized')
def facebook_authorized():
	resp = facebook.authorized_response()
	if resp is None:
		return 'Access denied: reason=%s error=%s' % (
			request.args['error_reason'],
			request.args['error_description']
		)
	if isinstance(resp, OAuthException):
		return 'Access denied: %s' % resp.message
	session['oauth_token'] = (resp['access_token'], '')
	me = facebook.get('/me')
	user = services.add_new_user_facebook(id=me.data['id'], name=me.data['name'])
	if user:
		login_user(user)
		return redirect(url_for('index'))
	
	return redirect(url_for('login'))


@facebook.tokengetter
def get_facebook_oauth_token():
	return session.get('oauth_token')


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


@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def user_expenses():
	form = ExpenseForm()
	category_query = services.get_categories_query(
		current_user.id)
	form.category.query = category_query

	if form.validate_on_submit():
		# TODO: Insert expense here
		services.add_expense(
			name=form.name.data,
			value=form.value.data,
			category=form.category.data,
			user=current_user
		)
		return redirect(url_for('register'))
		
	expenses = services.get_expenses_by_user(
		current_user.id)

	return render_template(
		'expenses.html', 
		expenses=expenses, form=form)


@app.route('/expenses/<int:id>', methods=['GET', 'POST'])
@login_required
def expense_detail(id):
	
	form = ExpenseForm()
	category_query = services.get_categories_query(
			current_user.id)
	form.category.query = category_query
	
	if request.method == 'GET':
		expense = services.get_expense_by_id(id)	
		form.name.data = expense.Expense.name
		form.value.data = expense.Expense.value
		form.category.data = expense.Category

	if form.validate_on_submit():
		services.update_expense(
			id=id,
			name=form.name.data,
			value=form.value.data,
			category=form.category.data
		)
		return redirect(url_for('user_expenses'))
		
	return render_template(
		'expenses_detail.html', form=form)


# @app.route('/profile')
# @login_required
# def profile():
# 	return 'User: Id {}'.format(current_user.username)


@app.route('/category', methods=['GET','POST'])
@login_required
def category():
	form = CategoryForm()
	
	if form.validate_on_submit():
		services.add_category(
			name = form.name.data,
			description = form.description.data,
			user = current_user
		)
		return  redirect(url_for('user_expenses'))

	return render_template('category.html', form=form)


if __name__ == '__main__':
	app.debug = True
	app.run(use_reloader=False, host='0.0.0.0', port=5000)
	#app.run()
