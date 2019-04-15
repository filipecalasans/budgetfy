from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalogdb import Base, Category, Expense, User, Category

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
	return True

def get_expanses():
	pass


def get_categories(user_id):
	pass


