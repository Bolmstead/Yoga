from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import *
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField


# function to get instructor's first name for the ClassAddForm
# def choice_query():
#     return User.query

class ClassAddForm(FlaskForm):
    """Form for adding or editing classes."""
    # instructor = QuerySelectField(query_factory=choice_query, allow_blank=True, get_label='first_name', blank_text='(Instructor)')
    location = StringField('Location', validators=[DataRequired()])
    start_date_time = DateTimeLocalField('Class Start', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_date_time = DateTimeLocalField('Class End', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])

class UserAddForm(FlaskForm):
    """Form for adding users."""
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=7)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    is_instructor = BooleanField('Are you an instructor?', false_values=None)

class UserEditForm(FlaskForm):
    """Form for editing users."""
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=7)])
    phone = StringField('Phone', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Form to login user or instructor."""
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=7), DataRequired()])