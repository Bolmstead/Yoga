from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import *
from wtforms.fields.html5 import DateTimeLocalField


def choice_query():
    return Instructor.query

class ClassAddForm(FlaskForm):
    """Form for adding/editing messages."""

    instructor = QuerySelectField(query_factory=choice_query, allow_blank=True, get_label='first_name', blank_text='(Instructor)')
    location = StringField('Location', validators=[DataRequired()])
    start_date_time = DateTimeLocalField('Class Start', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_date_time = DateTimeLocalField('Class End', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=7)])
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')

class InstructorAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=7)])
    image_url = StringField('(Optional) Image URL')


class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=7), DataRequired()])


################### QUESTIONS ######################################
# Create instructor add form? How to know 