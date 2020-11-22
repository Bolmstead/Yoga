from datetime import datetime, date, time

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()



class Signups(db.Model):
    """Table created to produce the many-to-many relationship between the tables 'users' and 'classes'"""

    __tablename__ = 'signups'

    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    class_id = db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,)
    password = db.Column(db.Text, nullable=False, unique=True,)
    email = db.Column(db.String(30), nullable=False, unique=True,)
    first_name = db.Column(db.String(30), nullable=False,)
    last_name = db.Column(db.String(30), nullable=False,)
    image_url = db.Column(db.Text, default="/static/images/profile_pic.png",)

    classes = db.relationship('Classes', secondary='signups', backref='users')

    @classmethod
    def signup(cls, first_name, last_name, email, password, image_url):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            password=hashed_pwd,
            email=email,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    # def __repr__(self):
    #     return f"<User #{self.id}: {self.email}>"

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `email` and `password`.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Instructor(db.Model):
    """An individual message ("warble")."""
    
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True,)
    password = db.Column(db.Text, nullable=False,)
    email = db.Column(db.String(30), nullable=False, unique=True,)
    first_name = db.Column(db.String(30), nullable=False,)
    last_name = db.Column(db.String(30), nullable=False,)
    image_url = db.Column(db.Text, default="/static/images/profile_pic.png",)

    classes = db.relationship('Classes', backref='instructor')

    def __repr__(self):
        return '<Instructor {}>'.format(self.first_name)

    @classmethod
    def instructor_signup(cls, first_name, last_name, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        instructor = Instructor(
            password=hashed_pwd,
            email=email,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
        )

        db.session.add(instructor)
        return instructor

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `email` and `password`.
        If can't find matching user (or if password is wrong), returns False.
        """

        instructor = cls.query.filter_by(email=email).first()

        if instructor:
            is_auth = bcrypt.check_password_hash(instructor.password, password)
            if is_auth:
                return instructor

        return False

class Classes(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'classes'

    id = db.Column( db.Integer, primary_key=True,)
    class_instructor = db.Column(db.Integer, db.ForeignKey('instructors.id', ondelete="cascade"),)
    location = db.Column(db.String,)
    start_date_time = db.Column(db.DateTime,)
    end_date_time = db.Column(db.DateTime,)
    class_users = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"),)

    def serialize(self):
        """Serialize classes SQLAlchemy obj to dictionary."""
        return {
            "id": self.id,
            "class_instructor": self.instructor.first_name,
            "location": self.location,
            "start_date_time": self.start_date_time,
            "end_date_time": self.end_date_time,
        }

    def readable_dates(self):
        """Change Classes dates object to something readable"""
        return {
            date: self.start_date_time(strftime, '%b %d, %Y')
            # time: self.start_date_time + "-" + 
        }



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
