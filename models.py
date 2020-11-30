from datetime import datetime, date, time
import pytz
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete

# dt = datetime.datetime()

bcrypt = Bcrypt()
db = SQLAlchemy()


class Signups(db.Model):
    """Class to establish the many-to-many relationship between the 'users' and 
    'classes' tables. Shows which users have signed up for which classes"""

    __tablename__ = 'signups'

    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    class_id = db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,)
    is_instructor = db.Column(db.Boolean)
    password = db.Column(db.Text, nullable=False, unique=True,)
    email = db.Column(db.String(50), nullable=False, unique=True,)
    first_name = db.Column(db.String(50), nullable=False,)
    last_name = db.Column(db.String(50), nullable=False,)
    phone = db.Column(db.String(12), nullable=False,)

    classes_signed_up = db.relationship('YogaClass', secondary='signups', backref='users')
    classes_teaching = db.relationship('YogaClass', backref='instructor')

    @classmethod
    def signup(cls, is_instructor, first_name, last_name, email, password, phone):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            is_instructor=is_instructor,
            password=hashed_pwd,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `email` and `password` combination."""

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        #If can't find matching user (or if password is invalid), returns False.
        return False


class YogaClass(db.Model):
    """Yoga Class Model"""

    __tablename__ = 'classes'

    id = db.Column( db.Integer, primary_key=True,)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"),)
    location = db.Column(db.String,)
    start_date_time = db.Column(db.DateTime,)
    end_date_time = db.Column(db.DateTime,)

    def serialize(self):
        """Serialize classes SQLAlchemy obj to dictionary."""
        return {
            "id": self.id,
            "instructor": self.instructor.first_name,
            "location": self.location,
            "start_date_time": self.start_date_time,
            "end_date_time": self.end_date_time,
        }
    

def connect_db(app):
    """Connect this database to Yoga Website."""
    db.app = app
    db.init_app(app)
