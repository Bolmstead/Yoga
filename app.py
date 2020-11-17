import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort , url_for, jsonify 
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import *
import email_validator

CURR_USER_KEY = "curr_user"
CURR_INSTRUCTOR_KEY = "curr_instructor"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///yoga"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.drop_all()
db.create_all()

toolbar = DebugToolbarExtension(app)


##############################################################################
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    elif CURR_INSTRUCTOR_KEY in session:
        g.user = Instructor.query.get(session[CURR_INSTRUCTOR_KEY])

    else:
        g.user = None


def do_user_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_instructor_login(instructor):
    """Log in user."""

    session[CURR_INSTRUCTOR_KEY] = instructor.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    if CURR_INSTRUCTOR_KEY in session:
        del session[CURR_INSTRUCTOR_KEY]


@app.route('/', methods=["GET", "POST"])
def homepage():
    """Show homepage: """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        instructor = Instructor.authenticate(form.username.data, form.password.data)

        if user:
            do_user_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        if instructor:
            do_instructor_login(instructor)
            flash(f"Hello, {instructor.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('home.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    if CURR_INSTRUCTOR_KEY in session:
        del session[CURR_INSTRUCTOR_KEY]

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_user_login(user)

        return redirect("/")

    return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        instructor = Instructor.authenticate(form.username.data, form.password.data)

        if user:
            do_user_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        if instructor:
            do_instructor_login(instructor)
            flash(f"Hello, {instructor.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have logged out", 'success')
    return redirect("/")


@app.route('/users/detail', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user

    return render_template('users/detail.html', user=user)

############################ CLASSES #####################3

@app.route('/json')
def display_json():
    """view/signup for available yoga classes using API"""

    serialized_classes = [c.serialize() for c in Classes.query.all()]

    return jsonify(serialized_classes)

################################ INSTRUCTOR ACCESS ########################

@app.route('/instructor_access')
def view_classes():

    return render_template('instructor_access/index.html')

@app.route('/instructor_access/signup', methods=["GET", "POST"])
def instructor_signup():
    """view/signup for available yoga classes using API"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    if CURR_INSTRUCTOR_KEY in session:
        del session[CURR_INSTRUCTOR_KEY]

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            instructor = Instructor.instructor_signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                image_url=form.image_url.data or Instructor.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('instructor_access/index.html', form=form)

        do_instructor_login(instructor)

        return redirect("/instructor_access")


    return render_template('instructor_access/signup.html',form=form)

@app.route('/instructor_access/add_class', methods=["GET", "POST"])
def add_class():
    """view/signup for available yoga classes using API"""
    if (not g.user) or (CURR_INSTRUCTOR_KEY not in session) :
        flash("Access unauthorized.", "danger")
        return redirect("/instructor_access")

    form = ClassAddForm()

    if form.validate_on_submit():
        yoga_class = Classes(
            instructor=form.instructor.data,
            location=form.location.data,
            start_date_time=form.start_date_time.data,
            )

        db.session.add(yoga_class)
        db.session.commit()

        return redirect("/instructor_access")


    return render_template('instructor_access/add_class.html', form=form)

# @app.route('/users/delete', methods=["POST"])
# def delete_user():
#     """Delete user."""

#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")

#     do_logout()

#     db.session.delete(g.user)
#     db.session.commit()

#     return redirect("/signup")


# ##############################################################################
# # Homepage and error pages


# @app.errorhandler(404)
# def page_not_found(e):
#     """404 NOT FOUND page."""

#     return render_template('404.html'), 404


# ##############################################################################
# # Turn off all caching in Flask
# #   (useful for dev; in production, this kind of stuff is typically
# #   handled elsewhere)
# #
# # https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

# @app.after_request
# def add_header(req):
#     """Add non-caching headers on every request."""

#     req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     req.headers["Pragma"] = "no-cache"
#     req.headers["Expires"] = "0"
#     req.headers['Cache-Control'] = 'public, max-age=0'
#     return req
