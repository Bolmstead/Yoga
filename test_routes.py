"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import *
from app import app, CURR_USER_KEY
from flask import session

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///yoga-test"
app.config['WTF_CSRF_ENABLED'] = False


# Now we can import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

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

##############################  HOME PAGE #################################

    def test_homepage_not_logged_in(self):
        """Make sure homepage HTML is displayed"""

        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIsNone(session.get('CURR_USER_KEY'))
            self.assertIn('<span>Ready for a break from the chaos?', html)
            self.assertIn('id="home-h4">Sign in</h4>', html)

    def test_homepage_logged_in_user(self):
        """Make sure homepage HTML is displayed for logged in user (not instructor)"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<span>Ready for a break from the chaos?', html)
            self.assertIn('id="home-greeting">Hi,', html)
            self.assertIn('btn-block btn-lg">View your enrolled classes', html)

    def test_homepage_logged_in_instructor(self):
        """Make sure homepage HTML is displayed for logged in user (not instructor)"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.instructor1.id

            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<span>Ready for a break from the chaos?', html)
            self.assertIn('id="instructor-greeting">Hi,', html)
            self.assertIn('btn-lg">Instructor Access</button></a>', html)

    # def test_homepage_login_function(self):
    #     """Make sure a user's is logged in on the Homepage"""

    #     with app.test_client() as client:

    #         resp = client.post('/users/signup', data={"text": "Hello"})
    #         html = resp.get_data(as_text=True)

##############################  SIGNUP PAGE #################################

    def test_signup_page_not_logged_in(self):
        """Make sure signup page HTML is displayed for user (not logged in)"""

        with app.test_client() as client:
            resp = client.get('/users/signup')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIsNone(session.get('CURR_USER_KEY'))
            self.assertIn('id="create-account-title">Create Account</h1>', html)

    def test_signup_page_logged_in(self):
        """Make sure signup page HTML is displayed for user (logged in).
            Make sure route logs the signed in user out"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.instructor1.id

            resp = client.get('/users/signup')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIsNone(session.get('CURR_USER_KEY'))
            self.assertIn('id="create-account-title">Create Account</h1>', html)

    # def test_signup_function(self):
    #     """Make sure a user's account is created and they are logged in after account registration"""

    #     with app.test_client() as client:

    #         resp = client.post('/users/signup', data={"text": "Hello"})
    #         html = resp.get_data(as_text=True)


    # def test_cancel_signup_function(self):
    #     """Make sure a user can cancel their signup"""

##############################  DETAIL PAGE #################################

    def test_detail_page_not_logged_in(self):
        """Make sure user is rerouted when not logged in."""

        with app.test_client() as client:
            resp = client.get('/users/detail')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_detail_page_logged_in_user(self):
        """Make sure detail page HTML is displayed for user (logged in)."""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.get('/users/detail')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('btn-md">Edit Account Information</a>', html)
            self.assertNotIn('btn-md">Create Class</a></div>', html)

    def test_detail_page_logged_in_instructor(self):
        """Make sure detail page HTML is displayed for user (logged in)."""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.instructor1.id

            resp = client.get('/users/detail')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('btn-md">Edit Account Information</a>', html)
            self.assertIn('btn-md">Create Class</a></div>', html)

##############################  EDIT PAGE #################################

    def test_edit_page_not_logged_in(self):
        """Make sure user is rerouted when not logged in."""

        with app.test_client() as client:
            resp = client.get('/users/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_edit_page_logged_in_user(self):
        """Make sure detail page HTML is displayed for user when logged in."""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.get('/users/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('placeholder="Enter your password to confirm', html)
        
    # def test_edit_user_function(self):
    #     """Make sure a user is successfully edited."""

##############################  ADD CLASS PAGE #################################

    def test_add_class_page_not_logged_in(self):
        """Make sure user is rerouted when not logged in."""

        with app.test_client() as client:
            resp = client.get('/users/add_class')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_add_class_page_not_instructor(self):
        """Make sure user is rerouted when logged in (not as an instructor)."""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.get('/users/add_class')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_add_class_page_instructor(self):
        """Make sure HTML shows on the add class page"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.instructor1.id

            resp = client.get('/users/add_class')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('btn-block">Create Class</button>', html)

    # def test_add_class(self):
    #     """Can instructor add a class?"""

    #     with self.client as client:
    #         with client.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.instructor1.id

    #         resp = client.post("/users/add_class", data={"text": "Hello"})

    #         self.assertEqual(resp.status_code, 302)

    # def test_delete_class(self):
    #     """Can instructor delete a class?"""

    #     with self.client as client:
    #         with client.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.instructor1.id

    #         resp = client.post("/classes/delete/{self.yoga_class1_id}")

    #         self.assertEqual(resp.status_code, 302)

########################### LOGOUT ROUTE ################################

    # def test_logout(self):
    #     """Can a user logout?"""

######################### DELETE CLASS ROUTE ############################

    def test_add_class(self):
        """Can instructor delete a class?"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.instructor1.id

            resp = client.post(f"/classes/delete/{self.yoga_class1_id}", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIsNone(YogaClass.query.get(self.yoga_class1_id))

######################### CLASS SIGNUP ROUTE ############################

    def test_class_signup(self):
        """Can user signup for a class?"""

        yoga_class2_start = datetime.strptime('2020-12-13 01:00:00-07:00', '%Y-%m-%d %H:%M:%S%z')
        yoga_class2_end = datetime.strptime('2020-12-13 02:00:00-07:00', '%Y-%m-%d %H:%M:%S%z')


        yoga_class2 = YogaClass(
            instructor_id=2222,
            location="Paris",
            start_date_time= yoga_class2_start,
            end_date_time= yoga_class2_end,
            class_date = "December 13, 2020",
            start_time = "01:00 AM",
            end_time = "02:00 AM",
        )

        yoga_class2_id = 3313
        yoga_class2.id = yoga_class2_id

        db.session.add(yoga_class2)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.post(f"/classes/signup/{yoga_class2_id}")

            signups_all = Signups.query.filter(Signups.user_id == 1111, Signups.class_id == 3313).all()
            signup2 = signups_all[0]

            self.assertEqual(resp.status_code, 302)
            self.assertIsNotNone(signup2)
            self.assertEqual(signup2.user_id, 1111)
            self.assertEqual(signup2.class_id, 3313)

    def test_class_signup(self):
        """Can user delete their class signup?"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.post(f"/classes/cancel_signup/{self.yoga_class1_id}")

            signups_all = Signups.query.filter(Signups.user_id == 1111, Signups.class_id == 3313).all()

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(signups_all, [])

######################### JSON ENDPOINT ROUTE ############################
