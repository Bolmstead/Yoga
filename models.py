from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )

    last_name = db.Column(
        db.String(30),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/profile_pic.png",
    )

    classes = db.relationship('Classes', backref='user')

    @classmethod
    def signup(cls, username, first_name, last_name, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    # def __repr__(self):
    #     return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Instructors(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'instructors'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )

    last_name = db.Column(
        db.String(30),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/profile_pic.png",
    )

    classes = db.relationship('Classes', backref='instructor')

    def __repr__(self):
        return '<Instructor {}>'.format(self.first_name)

    @classmethod
    def instructor_signup(cls, username, first_name, last_name, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        instructor = Instructors(
            username=username,
            password=hashed_pwd,
            email=email,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
        )

        db.session.add(instructor)
        return instructor

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        If can't find matching user (or if password is wrong), returns False.
        """

        instructor = cls.query.filter_by(username=username).first()

        if instructor:
            is_auth = bcrypt.check_password_hash(instructor.password, password)
            if is_auth:
                return instructor

        return False

class Classes(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'classes'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    start_time = db.Column(
        db.DateTime,
    )

    end_time = db.Column(
        db.DateTime,
    )

    class_instructor = db.Column(
        db.Integer,
        db.ForeignKey('instructors.id', ondelete="cascade"),
    )

    class_users = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
    )

    @classmethod
    def create_class(cls, instructor):

            yoga_class = Classes(
                instructor=instructor,
            )

            db.session.add(yoga_class)
            return yoga_class


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
