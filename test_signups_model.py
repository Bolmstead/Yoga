import os
from unittest import TestCase
from sqlalchemy import exc
from models import *

os.environ['DATABASE_URL'] = "postgresql:///yoga-test"

from app import app, CURR_USER_KEY

db.create_all()


app.config['WTF_CSRF_ENABLED'] = False

class SignupsModelTestCase(TestCase):
    """Test Signups Model"""
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

        self.start_dt_obj = datetime.strptime('2020-12-12 22:00:00-07:00', '%Y-%m-%d %H:%M:%S%z')
        self.end_dt_obj = datetime.strptime('2020-12-12 23:00:00-07:00', '%Y-%m-%d %H:%M:%S%z')

        # Create instance of yoga class
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

        # Create instance of a user1 signup for yoga_class1
        signup1 = Signups(
            user_id=1111,
            class_id=3333,
        )

        db.session.add(signup1)
        db.session.commit()

        self.user1 = User.query.get(user1_id)
        self.instructor1 = User.query.get(instructor1_id)
        self.yoga_class1 = YogaClass.query.get(yoga_class1_id)

        signup1_list = Signups.query.filter(Signups.user_id == 1111, Signups.class_id == 3333).all()
        self.signup1 = signup1_list[0]

        self.user1_id = user1_id
        self.instructor1_id = instructor1_id
        self.yoga_class1_id = yoga_class1_id

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_signups_model(self):
        """Does basic model work?"""       
        self.assertEqual(self.signup1.user_id, 1111)
        self.assertEqual(self.signup1.class_id, 3333)

    def test_user_class_signup(self):
        """Can a user signup for a class"""
        self.assertEqual(len(self.user1.classes_signed_up), 1)
        self.assertEqual(self.user1.classes_signed_up[0].id, 3333)

    def test_user_invalid_class_signup(self):
        """Does an error raise when an invalid signup occurs"""
        invalid = Signups(
            user_id=None,
            class_id=4444,
        )
        db.session.add(invalid)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()