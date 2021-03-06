import os
from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import *
import email_validator
from flask_cors import CORS, cross_origin
import pdb

# Import API libraries
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

CURR_USER_KEY = "curr_user"
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

app = Flask(__name__)

# to fix CORS error
cors = CORS(app)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',"postgres:///yoga")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "thisisayogawebsiteformymom")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

# connect to database. drop all tables (if any) then create all tables
connect_db(app)
# if using local server and want to drop/add tables, use code below:
# db.drop_all()
# db.create_all()


# toolbar = DebugToolbarExtension(app)

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
@cross_origin()
def homepage():
    """Show homepage: """
    form = LoginForm()

    # If post method and validated, login user
    if form.validate_on_submit():
        user = User.authenticate(form.email.data, form.password.data)
       
        if user:
            do_login(user)
            flash(f"You have logged in!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    # If GET method and user not logged in, show homepage 
    # passing form variable
    if not g.user:
        return render_template('home.html', form=form)

    # If GET method and user logged in, show homepage 
    # passing user and form variables.
    else:
        user = g.user
        return render_template('home.html', form=form, user=user)


######################## SIGNUP / LOGIN ################################

@app.route('/users/signup', methods=["GET", "POST"])
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
                phone=form.phone.data,
            )
            db.session.commit()

        # If email has already been taken, show error alert
        except IntegrityError as e:
            flash("Email already taken", 'danger')
            return render_template('users/signup.html', form=form)
        
        # Send email to user to confirm account creation
        message = Mail(
            from_email='olmssweeps@gmail.com',
            to_emails= user.email,
            subject='Lunchtime Yoga Account Created',
            html_content=f"Thank you, {form.first_name.data} {form.last_name.data} for creating an account with Lunchtime Yoga for Professionals! To view open yoga classes please go to https://yoga-website.herokuapp.com/#calendar_classes")

        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)

        except Exception as e:
            print(e)

        # Login the newly registered user
        do_login(user)
        flash(f"You have created an account!", "success")
        return redirect("/")
    # If get method, render the page
    else:
        return render_template('users/signup.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user/instructor."""

    do_logout()
    flash("You have logged out", 'success')

    return redirect("/")


###################### USER ACCESS ########################

@app.route('/users/detail')
def user_detail():
    """Show information of the logged in user"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    all_users = User.query.all()

    return render_template('users/detail.html', user=user, all_users=all_users)


@app.route('/users/edit', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    # If post method and validated, authenticate user and commit
    if form.validate_on_submit():
        if User.authenticate(user.email, form.password.data):
            user.email = form.email.data
            user.phone = form.phone.data

            db.session.commit()
            flash("Your account changes have been made!", "success")
            return redirect(f"/users/detail")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit.html', form=form)


####################### YOGA CLASSES SIGNUP ##########################3

@app.route('/classes/signup/<int:class_id>', methods=["POST"])
def class_signup(class_id):
    """User signs up for a yoga class"""

    if not g.user:
        flash("You must sign in to enroll in a class", "danger")
        return redirect("/")

    # Grab yoga class from database and save logged in user to variable
    yoga_class = YogaClass.query.get_or_404(class_id)
    user = g.user

    # if instructor tries to sign up for own class, redirect and flash error
    if user.id == yoga_class.instructor_id:
        flash("Signup not complete. You are unable to signup for your own class.",'danger')
        return redirect("/")

    if len(yoga_class.users) >= 6:
        flash("There are no more spots in this class. Please see calendar for more classes.",'danger')
        return redirect("/")

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
        from_email='olmssweeps@gmail.com',
        to_emails= user.email,
        subject='Yoga Class Signup Confirmation',
        html_content=f"You have signed up for {yoga_class.instructor.first_name}'s yoga class on {yoga_class.class_date} starting at {yoga_class.start_time} at {yoga_class.location}! To view other open yoga classes please go to https://yoga-website.herokuapp.com/#calendar_classes")

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e)
    
    flash(f"You have signed up for {yoga_class.instructor.first_name}'s yoga class on {yoga_class.class_date} starting at {yoga_class.start_time} at {yoga_class.location}", "success")
    return redirect("/")


@app.route('/classes/cancel_signup/<int:class_id>', methods=["POST"])
def cancel_signup(class_id):
    """Allows logged in user or instructor to cancel their class signup."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")


    user = g.user
    yoga_class = YogaClass.query.get_or_404(class_id)
    Signups.query.filter_by(user_id=user.id, class_id=class_id).delete()
        
    db.session.commit()

    message = Mail(
        from_email='olmssweeps@gmail.com',
        to_emails= user.email,
        subject='Yoga Class Signup Cancellation',
        html_content=f"You have been removed from {yoga_class.instructor.first_name}'s yoga class on {yoga_class.class_date}. To reschedule this yoga classes please go to https://yoga-website.herokuapp.com/#calendar_classes")

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e)

    flash(f"You have been removed from the {yoga_class.class_date} class.", "success")
    return redirect("/users/detail")


######################### INSTRUCTOR ACCESS ##############################

@app.route('/users/add_class', methods=["GET", "POST"])
def add_class():
    """ Allows instructor to add a class"""

    #if user is not an instructor, redirect to homepage with flash error
    if not g.user:
        flash("Access unauthorized. You must log in.", "danger")
        return redirect("/")

    if not g.user.is_instructor:
        flash("Access unauthorized. Must be an instructor to access content.", "danger")
        return redirect("/")

    form = ClassAddForm()
    user = g.user

    # If POST method create Classes instance and add to database
    if form.validate_on_submit():

        # If end datetime has passed, redirect and flash error
        if datetime.now() > form.end_date_time.data:
            flash("Classes cannot be scheduled in the past", "danger")
            return redirect("/users/add_class")

        # If the start time input is after the end time input, redirect and flash error.
        if form.start_date_time.data > form.end_date_time.data:
            flash("Class cannot end before its start time", "danger")
            return redirect("/users/add_class")

        # If yoga class is over 3.5 hours, redirect and flash error
        time_diff = form.end_date_time.data - form.start_date_time.data
        if (time_diff > timedelta(hours=3, minutes=30)):
            flash("Class is too long", "danger")
            return redirect("/users/add_class")

        # Grab start and end datetime objects
        start_dt = (form.start_date_time.data)
        end_dt = (form.end_date_time.data)

        # Localize the dt objects to MST timezone
        western_tz = timezone('US/Mountain')
        start_dt_tz = western_tz.localize(start_dt)
        end_dt_tz = western_tz.localize(end_dt)

        # Create readable dates and times that allow access to on HTML through Jinja
        class_date = start_dt_tz.strftime("%B %d, %Y")
        start_time = start_dt_tz.strftime("%I:%M %p")
        end_time = end_dt_tz.strftime("%I:%M %p")

        # #print all variables
        print("start_date_time", dir(start_dt_tz,))
        print("end_date_time", end_dt_tz,)
        print("class_date", class_date,)
        print("start_time", start_time,)
        print("end_time", end_time,)

        yoga_class = YogaClass(
            instructor_id=user.id,
            location=form.location.data,
            start_date_time=start_dt_tz,
            end_date_time=end_dt_tz,
            class_date = class_date,
            start_time = start_time,
            end_time = end_time,
        )

        db.session.add(yoga_class)
        db.session.commit()

        flash("Class created", "success")
        return redirect("/users/detail")


    return render_template('users/add_class.html', form=form)

@app.route('/classes/delete/<int:class_id>', methods=["POST"])
def delete_class(class_id):
    """Allows instructor to delete a class."""

    #if user is not an instructor, redirect to homepage with flash error
    if not g.user.is_instructor:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user

    #if user is an instructor, delete class
    if user.is_instructor:
        yoga_class = YogaClass.query.get_or_404(class_id)
        
        db.session.delete(yoga_class)
        db.session.commit()

        flash("Class had been deleted", "success")
        return redirect("/users/detail")

    else:
        flash("Access unauthorized.", "danger")
        return redirect("/")

@app.route('/users/view_users')
def view_users():
    """Show information of the logged in user"""

    if not g.user.is_instructor:
        flash("Access unauthorized. Must be an instructor to access content.", "danger")
        return redirect("/")

    users = User.query.filter_by(is_instructor=False)
    instructors = User.query.filter_by(is_instructor=True)


    return render_template('users/view_users.html', users=users, instructors=instructors)

################## JSON ENDPOINT  #####################################

@app.route('/json')
def display_json():
    """Show JSON of all created classes. Allows Javascript 
    to grab class information to populate calendar"""

    serialized_classes = [c.serialize() for c in YogaClass.query.all()]
    return jsonify(serialized_classes)


################## HOMEPAGE AND ERRORS #####################################

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404