from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalogdb import Base, Category, Expense, User, Category

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def get_user(id):
	return session.query(User).filter_by(id=int(id)).first()


def get_user_by_name(username):
	return sessin.query(User).filter_by(
		username=name).first()


def get_expanses():
	pass


def get_categories(user_id):
	pass


