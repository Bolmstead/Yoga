import os
from flask import Flask, render_template, request, flash, redirect, session, g, abort , url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

# Import API libraries
from twilio.rest import Client 
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#Import forms.py and email validator
from forms import *
import email_validator


CURR_USER_KEY = "curr_user"
SENDGRID_API_KEY = "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"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///yoga"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "warrior3ishard"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# Heroku
app.config['SQLALCHEMY_DATABSE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///yoga')

connect_db(app)
db.drop_all()
db.create_all()

toolbar = DebugToolbarExtension(app)

## Email API initialization
account_sid = 'AC61fba0a85692bf29f107b606ce31b6cc' 
auth_token = '[AuthToken]' 
client = Client(account_sid, auth_token) 

message = sendgrid.Mail()

##############################################################################
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/', methods=["GET", "POST"])
def homepage():
    """Show homepage: """
    form = LoginForm()

    # If post method and validated, save user to variable
    # using the each class's authenticate method. Then login user
    if form.validate_on_submit():
        user = User.authenticate(form.email.data,
                                 form.password.data)
       
        if user:
            do_login(user)
            flash(f"You have logged in!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    # If GET method and user not logged in, show homepage.
    if not g.user:
        return render_template('home.html', form=form)

    # If GET method and user logged in, save global user to variable andshow homepage.
    else:
        user = g.user
        return render_template('home.html', form=form, user=user)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """User and Instructor create account route"""
    do_logout()

    form = UserAddForm()

    # If post method and validated, save user instance to database
    if form.validate_on_submit():
        try:
            user = User.signup(
                is_instructor=form.is_instructor.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        # If email has already been taken, show error alert
        except IntegrityError as e:
            flash("Email already taken", 'danger')
            return render_template('users/signup.html', form=form)

        # Send email to user to confirm account creation
        message = Mail(
            from_email='olms2074@gmail.com',
            to_emails= form.email.data,
            subject='Lunchtime Yoga Account Created',
            html_content=f"Thank you, {form.first_name.data} {form.last_name.data} for creating an account with Lunchtime Yoga for Professionals! To view open yoga classes please go to http://localhost:5000/#calendar_classes")

        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)

        except Exception as e:
            print(e.message)

        # Login the newly registered user
        do_login(user)

        return redirect("/")
    # If get method, render the page
    return render_template('users/signup.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user/instructor."""

    do_logout()
    flash("You have logged out", 'success')

    return redirect("/")


@app.route('/users/detail', methods=["GET", "POST"])
def edit_profile():
    """Show information of the logged in user"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user

    if g.user.is_instructor:
        return render_template('instructor_access/detail.html', user=user)

    return render_template('users/detail.html', user=user)

############################ CLASSES #####################3

@app.route('/json')
def display_json():
    """Show JSON of all created classes"""

    serialized_classes = [c.serialize() for c in YogaClass.query.all()]
    return jsonify(serialized_classes)

@app.route('/classes/signup/<int:class_id>', methods=["POST"])
def class_signup(class_id):
    """User signs up for a yoga class"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    # Grab yoga class from database and save logged in user to variable
    yoga_class = YogaClass.query.get_or_404(class_id)
    user = g.user

    try: 
        signup = Signups(
        user_id=user.id,
        class_id=yoga_class.id,)

    except IntegrityError as e:
        flash("You have already registered for this class", 'danger')
        return redirect("/")

    db.session.add(signup)
    db.session.commit()

    # Send email to user confirming their class signup
    message = Mail(
        from_email='olms2074@gmail.com',
        to_emails= user.email,
        subject='Yoga Class Signup Confirmation',
        html_content=f"You have signed up for {yoga_class.instructor.first_name}'s yoga class on {yoga_class.start_date_time} at {yoga_class.location}! To view other open yoga classes please go to http://localhost:5000/#calendar_classes")

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e.message)
    
    flash(f"You have signed up for {yoga_class.instructor.first_name}'s yoga class on {yoga_class.start_date_time}", "success")
    return redirect("/")

################################ INSTRUCTOR ACCESS ########################
@app.route('/instructor_access/detail', methods=["GET", "POST"])
def view_instructor():
    """Update profile for current user."""

    if not g.user.is_instructor:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user

    return render_template('instructor_access/detail.html', user=user)


@app.route('/instructor_access/add_class', methods=["GET", "POST"])
def add_class():
    """view/signup for available yoga classes using API"""
    if not g.user.is_instructor:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = ClassAddForm()
    user = g.user

    # If POST method create Classes instance and add to database
    if form.validate_on_submit():
    
        yoga_class = YogaClass(
            instructor_id=user.id,
            location=form.location.data,
            start_date_time=form.start_date_time.data,
            end_date_time=form.end_date_time.data,
            )

        db.session.add(yoga_class)
        db.session.commit()

        flash("Class created", "success")
        return redirect("/instructor_access/detail")


    return render_template('instructor_access/add_class.html', form=form)

@app.route('/classes/delete/<int:class_id>', methods=["POST"])
def delete_class(class_id):
    """Allow logged in instructor to delete class."""

    user = g.user

    if user.is_instructor:
        Signups.query.filter_by(user_id=user.id, class_id=class_id).delete
        db.session.commit()

        flash("Class had been deleted", "success")
        return redirect("/")

    else:
        flash("Access unauthorized.", "danger")
        return redirect("/")


##################Homepage and error pages#####################################

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404

