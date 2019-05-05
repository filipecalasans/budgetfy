from sqlalchemy import create_engine, desc, or_
from sqlalchemy.orm import sessionmaker
from catalogdb import Base, Category, Expense, User, Category, Location

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

def get_user(id):
	session = DBSession()
	return session.query(User).filter_by(id=int(id)).first()


def get_user_by_username(username):
	session = DBSession()
	return session.query(User).filter_by(
		username=username).first()


def get_user_by_email(email):
	session = DBSession()
	return session.query(User).filter_by(
		email=email).first()

def add_new_user(**kwargs):
	'''
		kwargs must match the User Schema.
	'''
	session = DBSession()
	new_user = User(
		username=kwargs['username'], 
		firstname=kwargs['firstname'],
		lastname=kwargs['lastname'], 
		email=kwargs['email'])

	new_user.set_password(kwargs['password'])
	session.add(new_user)
	try:
		session.commit()
	except Exception as e:
		# Log Exception here
		return None
	return new_user

def get_expenses_by_user(user_id):
	'''
		Return user's expenses sorted by date
	'''
	session= DBSession()
	expenses = session.query(Expense, Category, Location).\
		join(Category).\
		join(Location).\
		filter(Expense.user_id==user_id).\
		order_by(desc(Expense.created_time)).all()
	return expenses


def get_expense_by_id(id):
	'''
		Return user's expense sorted by date
	'''
	session= DBSession()
	expense = session.query(Expense, Category, Location).\
		join(Category).\
		join(Location).\
		filter(Expense.id==id).first()
	return expense


def get_categories_query(user_id):
	'''
		Return the category query applicable to
		a given user.
	'''
	session=DBSession()
	return session.query(Category).filter(
		or_(Category.user_id==user_id,
		Category.user_id==None)
	).order_by(Category.name)


def add_expense(**kwargs):
	category = Category(kwargs['category'])
	user = User(kwargs['user'])
	expense = Expense(
		name=kwargs['name'],
		value=kwargs['value'],
		category=category,
		user=user)
	
	



