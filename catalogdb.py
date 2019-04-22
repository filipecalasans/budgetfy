import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import Float, Text 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Base = declarative_base()

class User(UserMixin, Base):
	
	__tablename__ = 'user'
	
	username = Column(String(80), nullable=False)
	firstname = Column(String(80), nullable = False)
	lastname = Column(String(80), nullable = False)
	email = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	password_hash = Column(String, nullable = False)
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Category(Base):
	
	__tablename__	= 'category'
	
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	description = Column(Text, nullable = True)
	user_id = Column(Integer, ForeignKey('user.id'), nullable = True)


class Location(Base):

	__tablename__ = 'location'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)	


class Expense(Base):
	
	__tablename__ = 'expense'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	value = Column(Float(precision=2), nullable = False)
	created_time = Column(DateTime, default=datetime.datetime.utcnow)
	category_id = Column(Integer, ForeignKey('category.id'))
	location_id = Column(Integer, ForeignKey('location.id'))
	user_id = Column(Integer, ForeignKey('user.id'))

	user = relationship(User,
		backref=backref('expenses',
		uselist=True))

	location = relationship(Location,
		backref=backref('expenses',
		uselist=True))

	category = relationship(Category,
		backref=backref('expenses',
		uselist=True))


engine = create_engine(
	'sqlite:///catalog.db')

Base.metadata.create_all(engine)
