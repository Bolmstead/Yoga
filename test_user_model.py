"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import *

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///yoga-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test Users Model"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        user1 = User.signup(
            is_instructor=False,
            password="password",
            email="user1email@email.com",
            first_name="Bob",
            last_name="Bobby",
            phone="5555555555",
        )

        user1_id = 1111
        user1.id = user1_id

        instructor1 = User.signup(
            is_instructor=True,
            password="password",
            email="instructor1email@email.com",
            first_name="Verna",
            last_name="Verny",
            phone="5555555555",
        )

        instructor1_id = 2222
        instructor1.id = instructor1_id

        db.session.commit()

        user1 = User.query.get(user1_id)
        instructor1 = User.query.get(instructor1_id)

        self.user1 = user1
        self.user1_id = user1_id

        self.instructor1 = instructor1
        self.instructor1_id = instructor1_id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Does basic model work?"""

        u = User.signup(
            is_instructor=True,
            password="password",
            email="email@email.com",
            first_name="Ted",
            last_name="User",
            phone="5555555555",
        )

        db.session.add(u)
        db.session.commit()

        # User should have no classes_signed_up & no classes_teaching
        self.assertEqual(len(u.classes_signed_up), 0)
        self.assertEqual(len(u.classes_teaching), 0)

    ####
    #
    # Signup Tests
    #
    ####

    # test the validity of the user1 signup
    def test_valid_signup(self):

        user1 = User.query.get(1111)
        self.assertIsNotNone(user1)
        self.assertNotEqual(user1.password, "password")
        self.assertEqual(user1.email, "user1email@email.com")
        self.assertEqual(user1.first_name, "Bob")
        self.assertEqual(user1.last_name, "Bobby")
        self.assertEqual(user1.phone, "5555555555")
        # Bcrypt strings should start with $2b$
        self.assertTrue(user1.password.startswith("$2b$"))


    def test_invalid_email_signup(self):
        invalid = User.signup(
            is_instructor=True,
            password="password",
            email=None,
            first_name="Ted",
            last_name="User",
            phone="5555555555",
        )
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup(
                is_instructor=False,
                password=None,
                email="email@email.com",
                first_name="Donald",
                last_name="Trump",
                phone="5555555555",
            )
        
        with self.assertRaises(ValueError) as context:
            User.signup(
                is_instructor=True,
                password="",
                email="email@email.com",
                first_name="Donald",
                last_name="Trump",
                phone="5555555555",
            )

    def test_invalid_first_name_signup(self):
        invalid = User.signup(
            is_instructor=True,
            password="password",
            email="email@email.com",
            first_name=None,
            last_name="User",
            phone="5555555555",
        )
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_last_name_signup(self):
        invalid = User.signup(
            is_instructor=True,
            password="password",
            email="email@email.com",
            first_name="Ted",
            last_name=None,
            phone="5555555555",
        )
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_phone_signup(self):
        invalid = User.signup(
            is_instructor=True,
            password="password",
            email="email@email.com",
            first_name="Ted",
            last_name="User",
            phone=None,
        )
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    ####
    #
    # Authentication Tests
    #
    ####
    def test_valid_authentication(self):
        u = User.authenticate(self.user1.email, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.user1_id)
    
    def test_invalid_email(self):
        self.assertFalse(User.authenticate("bademail@bademail.com", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.user1.email, "badpassword"))