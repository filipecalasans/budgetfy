from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalogdb import Base, User, Category, Expense, Location

import sys

import catalogdb

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

users=[
    {
        'username': 'mike',
        'firstname': 'Michael',
        'lastname': 'Jackson',
        'email': 'jackson@thriller.com',
        'id': 1,
        'password': '12345678',
    },
    {
        'username': 'clark',
        'firstname': 'Clark',
        'lastname': 'Kent',
        'email': 'clark@superman.com',
        'id': 2,
        'password': '12345678',
    },
    {
        'username': 'xavier',
        'firstname': 'Charles',
        'lastname': 'Xavier',
        'email': 'xavier@xmen.com',
        'id': 3,
        'password': '12345678',
    },
]

categories=[
    {   
        'id': 1,
        'name': 'groceries',
        'description': 'Groceries, Supermarket, Department Store',
        'user_id': None,
    },
    {   
        'id': 2,
        'name': 'car',
        'description': 'Repair, Gas, Tires, Oil, Car wash',
        'user_id': None,
    },
    {   
        'id': 3,
        'name': 'Entertainment',
        'description': 'Movies, Concerts, Sports',
        'user_id': None,
    },
    {   
        'id': 4,
        'name': 'Restaurants',
        'description': 'Restaurants, Fast food, Dinning, Bar',
        'user_id': None,
    },
    {   
        'id': 5,
        'name': 'Vacation',
        'description': 'Restaurants, Fast food, Dinning, Bar',
        'user_id': 1,
    },
    {   
        'id': 6,
        'name': 'Subscriptions',
        'description': 'Online subscriptions',
        'user_id': 1,
    },
    {   
        'id': 7,
        'name': 'Savings',
        'description': 'Savings to buy a car',
        'user_id': 2,
    }
]

locations=[
    {
        'id': 1,
        'name': "publix",
    },
    {
        'id': 2,
        'name': "amazon",
    },
    {
        'id': 3,
        'name': "exxon",
    },
    {
        'id': 4,
        'name': "Apple Itunes",
    },
    {
        'id': 5,
        'name': "petsmart"
    },
    {
        'id': 6,
        'name': "Cinema4d"
    },
]

expenses=[
    {   
        'name': 'Amazon Prime',
        'value': 14.99,
        'category_id': 6,
        'location_id': 3,
        'user_id': 1
    },
    {   
        'name': 'Publix Aventura',
        'value': 67.54,
        'category_id': 1,
        'location_id': 1,
        'user_id': 1
    },
    {   
        'name': 'Publix Aventura',
        'value': 78.54,
        'category_id': 1,
        'location_id': 1,
        'user_id': 2
    },
    {   
        'name': 'Cinema4d',
        'value': 45.00,
        'category_id': 3,
        'location_id': 1,
        'user_id': 1
    },
    {   
        'name': 'exxon mobile',
        'value': 35.00,
        'category_id': 2,
        'location_id':3,
        'user_id': 1
    },
]

def insert_users():
    """
    'username': 'mike',
    'firstname': 'Michael',
    'lastname': 'Jackson',
    'email': 'jackson@thriller.com',
    'id': 1,
    'password': '12345678',
    """
    try:
        for user in users:
            # print('user: {}'.format(user))
            u = User(username=user['username'],
                firstname=user['firstname'],
                lastname=user['lastname'],
                email=user['email'],
                id=user['id'])
            u.set_password(user['password'])
            session.add(u)        
            session.commit()
    except:
        sys.exit('Error inserting users')


def insert_categories():
    """
    'id': 1,
    'name': 'groceries',
    'description': 'Groceries, Supermarket, Department Store',
    'user_id': None,
    """
    try:
        for cat in categories:
            c = Category(id=cat['id'],
                name=cat['name'],
                description=cat['description'],
                user_id=cat['user_id'])
            session.add(c)
            session.commit()
    except:
        sys.exit('Error Inserting Categories:')


def insert_locations():
    """
    'id': 1,
    'name': "publix",
    """
    try:
        for loc in locations:
            l = Location(id=loc['id'],
                name=loc['name'])
            session.add(l)
            session.commit()
    except:
        sys.exit('Error Inserting Locations')    


def insert_expenses():
    """
    'name': 'Amazon Prime',
    'value': 14.99,
    'category_id': 6,
    'location': 3,
    'user_id': 1
    """
    try:
        for exp in expenses:
            e = Expense(
                name=exp['name'],
                value=exp['value'],
                category_id=exp['category_id'],
                # location_id=exp['location_id'],
                user_id=exp['user_id'])
            session.add(e)
            session.commit()
    except Exception as e:
        sys.exit('Error Inserting Expenses: {}'.format(e))

if __name__ == "__main__":
    insert_users()
    insert_categories()
    insert_locations()
    insert_expenses()
