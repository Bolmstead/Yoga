import os
from unittest import TestCase
from sqlalchemy import exc
from models import *
from flask import session

os.environ['DATABASE_URL'] = "postgresql:///yoga-test"

from app import app, CURR_USER_KEY

app.config['WTF_CSRF_ENABLED'] = False

db.create_all()


class FlaskTests(TestCase):

    def setUp(self):
        """Setup for tests by creating user, instructor, and yoga class.
        Also, sign the user up for the yoga class"""

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
        """Make sure homepage HTML is displayed for user not logged in.
        Make sure user is not logged in the session."""

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

            # The following HTML only shows for this instructor when logged in
            self.assertIn('id="home-greeting">Hi, Bob', html)

            # The following HTML only shows for a logged in user (not instructor)
            self.assertIn('btn-block btn-lg">View your enrolled classes', html)


    def test_homepage_logged_in_instructor(self):
        """Make sure homepage HTML is displayed for a logged in instructor"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.instructor1.id

            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<span>Ready for a break from the chaos?', html)

            # The following HTML only shows for this instructor when logged in
            self.assertIn('id="instructor-greeting">Hi, Verna', html)

            # The following HTML only shows for a logged in instructor
            self.assertIn('btn-lg">Instructor Access</button></a>', html)


    def test_homepage_login_function(self):
        """Make sure the login post route for the homepage is functioning"""

        with app.test_client() as client:
            user1_login= {
                'password': 'password',
                'email': 'user1email@email.com',
            }

            resp = client.post('/', data=user1_login, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You have logged in!', html)
            self.assertIn('id="home-greeting">Hi, Bob', html)


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
        """Make sure signup page HTML is displayed for logged in user.
        Make sure route logs out the signed in user"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.instructor1.id

            resp = client.get('/users/signup')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIsNone(session.get('CURR_USER_KEY'))
            self.assertIn('id="create-account-title">Create Account</h1>', html)


    def test_successful_signup(self):
        """Make sure signup post route functions properly"""

        with app.test_client() as client:

            user_jim = {
                'id': '1212',
                'is_instructor': 'y',
                'password': 'password',
                'email': 'email@email.com',
                'first_name': 'Jim',
                'last_name': 'Halpert',
                'phone': '8888888888',
                }

            resp = client.post('/users/signup', data=user_jim, follow_redirects=True)
            html = resp.get_data(as_text=True)
            user_jimm = User.query.get(1212)


            self.assertEqual(resp.status_code, 200)
            self.assertIn('You have created an account!', html)
            self.assertIn('Jim', html)


##############################  DETAIL PAGE #################################

    def test_detail_page_not_logged_in(self):
        """Make sure user (not logged in) is rerouted when trying to access detail page."""

        with app.test_client() as client:
            resp = client.get('/users/detail')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)


    def test_detail_page_logged_in_user(self):
        """Make sure detail page HTML is displayed for logged in user."""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.get('/users/detail')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('btn-md">Edit Account Information</a>', html)
            self.assertNotIn('btn-md">Create Class</a></div>', html)


    def test_detail_page_logged_in_instructor(self):
        """Make sure detail page HTML is displayed for logged in instructor."""

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
        """Make sure user (not logged in) is rerouted when trying to access the edit page."""

        with app.test_client() as client:
            resp = client.get('/users/edit')
            html = resp.get_data(as_text=True)

            self.assertIsNone(session.get('CURR_USER_KEY'))
            self.assertEqual(resp.status_code, 302)


    def test_edit_page_logged_in_user(self):
        """Make sure edit page HTML is displayed for user when logged in."""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.get('/users/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('placeholder="Enter your password to confirm', html)
        

    def test_edit_user_function(self):
        """Make sure edit user post route is functioning properly"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            user_edit = {
                'id': '1212',
                'password': 'password',
                'email': 'email@email.com',
                'phone': '8888888888',
                }

            resp = client.post('/users/edit', data=user_edit, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Your account changes have been made!', html)


##############################  ADD CLASS PAGE #################################

    def test_add_class_page_not_logged_in(self):
        """Make sure user is rerouted when not logged in."""

        with app.test_client() as client:
            resp = client.get('/users/add_class', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIsNone(session.get('CURR_USER_KEY'))
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized. You must log in.', html)


    def test_add_class_page_not_instructor(self):
        """Make sure user is rerouted when logged in but is not instructor."""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.get('/users/add_class', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Must be an instructor to access content', html)


    def test_add_class_page_instructor(self):
        """Make sure HTML shows on the add class page for logged in instructor"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.instructor1.id

            resp = client.get('/users/add_class')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('btn-block">Create Class</button>', html)


    def test_add_class(self):
        """Make sure post route for adding a class functions properly"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.instructor1.id

            add_class_test = {
                'id': '1212',
                'instructor_id': '2222',
                "location": "Moscow",
                "start_date_time": "2020-12-11T15:21",
                "end_date_time": "2020-12-11T16:20",
                }

            resp = client.post('/users/add_class', data=add_class_test, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Class created', html)
            self.assertIn('<h5 class="card-title">December 12, 2020</h5>', html)
            self.assertIn('<p class="card-text">Moscow</p>', html)


########################### LOGOUT ROUTE ################################

    def test_logout(self):
        """Make sure get route for logging a user out functions properly"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.get('/logout', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You have logged out', html)
            self.assertIsNone(session.get('CURR_USER_KEY'))


######################### DELETE CLASS ROUTE ############################

    def test_delete_class(self):
        """Make sure post route for deleting a class functions properly"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.instructor1.id

            resp = client.post('/classes/delete/3333', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Class had been deleted', html)
            self.assertIsNone(YogaClass.query.get(self.yoga_class1_id))


######################### CLASS SIGNUP ROUTE ############################

    def test_class_signup(self):
        """Make sure user can successfully sign up for a yoga class"""

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

            resp = client.post(f"/classes/signup/{yoga_class2_id}", follow_redirects=True)
            html = resp.get_data(as_text=True)

            signups_all = Signups.query.filter(Signups.user_id == 1111, Signups.class_id == 3313).all()
            signup2 = signups_all[0]

            self.assertEqual(resp.status_code, 200)

            # Make sure signup is saved to database
            self.assertIsNotNone(signup2)
            self.assertEqual(signup2.user_id, 1111)
            self.assertEqual(signup2.class_id, 3313)

            # Make sure HTML shows up on webpage
            self.assertIn(f"You have signed up for", html)


    def test_cancel_signup(self):
        """Make sure a user can cancel their signup successfully"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.post('/classes/cancel_signup/3333', follow_redirects=True)
            html = resp.get_data(as_text=True)
            signups_all = Signups.query.filter(Signups.user_id == 1111, Signups.class_id == 3313).all()
            
            self.assertEqual(resp.status_code, 200)

            # Make sure the only signup has been deleted from database
            self.assertEqual(signups_all, [])

            # Make sure proper HTML shows up on webpage
            self.assertIn('You have been removed from the December 12, 2020 class.', html)

