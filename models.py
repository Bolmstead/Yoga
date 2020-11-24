from datetime import datetime, date, time
import pytz
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
# import pytz

# dt = datetime.datetime()

bcrypt = Bcrypt()
db = SQLAlchemy()


class Signups(db.Model):
    """Class to establish the many-to-many relationship between the tables 'users' and 'classes'
    for when a user signs up for a class"""

    __tablename__ = 'signups'

    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    class_id = db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,)
    is_instructor = db.Column(db.Boolean)
    password = db.Column(db.Text, nullable=False, unique=True,)
    email = db.Column(db.String(30), nullable=False, unique=True,)
    first_name = db.Column(db.String(30), nullable=False,)
    last_name = db.Column(db.String(30), nullable=False,)
    image_url = db.Column(db.Text, default="/static/images/profile_pic.png",)

    classes_signed_up = db.relationship('YogaClass', secondary='signups', backref='users')
    classes_teaching = db.relationship('YogaClass', backref='instructor')

    @classmethod
    def signup(cls, is_instructor, first_name, last_name, email, password, image_url):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            is_instructor=is_instructor,
            password=hashed_pwd,
            email=email,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `email` and `password` combination.
        If can't find matching user (or if password is invalid), returns False."""

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

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
    """Connect this database to provided Yoga Website."""
    db.app = app
    db.init_app(app)
