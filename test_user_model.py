import os
from unittest import TestCase
from sqlalchemy import exc
from models import *

os.environ['DATABASE_URL'] = "postgresql:///yoga-test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test Users Model"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        # Create instance of user
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

        # Create instance of instructor
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
        """Does Integrity Error raise when create user with invalid email?"""
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
        """Does Integrity Error raise when create user with invalid password?"""

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
        """Does Integrity Error raise when create user with invalid first_name?"""

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
        """Does Integrity Error raise when create user with invalid last_name?"""

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
        """Does Integrity Error raise when create user with invalid phone number?"""

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