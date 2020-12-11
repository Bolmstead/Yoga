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


class YogaClassModelTestCase(TestCase):
    """Test YogaClass Model"""
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

        self.start_dt_obj = datetime.strptime('2020-12-12 22:00:00-07:00', '%Y-%m-%d %H:%M:%S%z')
        self.end_dt_obj = datetime.strptime('2020-12-12 23:00:00-07:00', '%Y-%m-%d %H:%M:%S%z')


        yoga_class1 = YogaClass(
            instructor_id=2222,
            location="Paris",
            start_date_time= self.start_dt_obj,
            end_date_time= self.end_dt_obj,
            class_date = "December 12, 2020",
            start_time = "10:00 PM",
            end_time = "11:00 PM",
        )

        yoga_class1_id = 3333
        yoga_class1.id = yoga_class1_id

        db.session.add(yoga_class1)
        db.session.commit()

        self.user1 = User.query.get(user1_id)
        self.instructor1 = User.query.get(instructor1_id)
        self.yoga_class1 = YogaClass.query.get(yoga_class1_id)

        self.user1_id = user1_id
        self.instructor1_id = instructor1_id
        self.yoga_class1_id = yoga_class1_id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_YogaClass_model(self):
        """Does basic model work?"""

        # yoga_class should have 0 users signed up and "Verna" as the instructor
        self.assertEqual(len(self.yoga_class1.users), 0)
        self.assertEqual(self.yoga_class1.instructor.first_name, "Verna")

    # ###
    
    # Yoga Class Creation Tests
    
    # ###
    def test_valid_class(self):

        self.assertIsNotNone(self.yoga_class1)
        self.assertEqual(self.yoga_class1.instructor_id, 2222)
        self.assertEqual(self.yoga_class1.location, "Paris")
        self.assertIsNotNone(self.yoga_class1.start_date_time)
        self.assertIsNotNone(self.yoga_class1.end_date_time)
        self.assertEqual(self.yoga_class1.class_date, "December 12, 2020")
        self.assertEqual(self.yoga_class1.start_time, "10:00 PM")
        self.assertEqual(self.yoga_class1.end_time, "11:00 PM")


    def test_invalid_class_instructor_id(self):
        invalid = YogaClass(
            instructor_id=None,
            location="Paris",
            start_date_time= self.start_dt_obj,
            end_date_time= self.end_dt_obj,
            class_date = "December 12, 2020",
            start_time = "10:00 PM",
            end_time = "11:00 PM",
        )
        
        uid = 123789
        invalid.id = uid
        db.session.add(invalid)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_class_location(self):
        invalid = YogaClass(
            instructor_id=2222,
            location=None,
            start_date_time= self.start_dt_obj,
            end_date_time= self.end_dt_obj,
            class_date = "December 12, 2020",
            start_time = "10:00 PM",
            end_time = "11:00 PM",
        )
        
        uid = 123789
        invalid.id = uid
        db.session.add(invalid)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_class_start_dt(self):
        invalid = YogaClass(
            instructor_id=2222,
            location="Paris",
            start_date_time= None,
            end_date_time= self.end_dt_obj,
            class_date = "December 12, 2020",
            start_time = "10:00 PM",
            end_time = "11:00 PM",
        )
        
        uid = 123789
        invalid.id = uid
        db.session.add(invalid)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
        

    def test_invalid_class_end_dt(self):
        invalid = YogaClass(
            instructor_id=2222,
            location="Paris",
            start_date_time= self.start_dt_obj,
            end_date_time= None,
            class_date = "December 12, 2020",
            start_time = "10:00 PM",
            end_time = "11:00 PM",
        )
        
        uid = 123789
        invalid.id = uid
        db.session.add(invalid)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
