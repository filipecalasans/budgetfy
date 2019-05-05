from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.validators import NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField

import services

class LoginForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    
    def validate_username(self, username):
        user = services.get_user_by_username(username.data)
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = services.get_user_by_email(email.data)
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ExpenseForm(FlaskForm):

    name = StringField('Expense', validators=[DataRequired()])
    value = FloatField('Amount $:', validators=[
        DataRequired(), NumberRange(min=0)])
    category = QuerySelectField(
        'Category',
        allow_blank=False,
        get_label='name',
        get_pk=lambda x: x.id
    )

class CategoryForm(FlaskForm):

    name = StringField('Category', validators=[DataRequired()])
    description = StringField('Description')
