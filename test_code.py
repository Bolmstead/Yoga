# THIS DOCUMENT IS A PLACEHOLDER FOR POSSIBLE CODE TO PLACE IN PROJECT

######################################################################
############################# APP.PY #################################
######################################################################


############## API TO SEND SMS message ###############################

# message = client.messages.create(from_="+16814343687", body=f"Thank you for signing 
# up for {yoga_class.instructor}'s yoga class at {yoga_class.location}! The class starts
#  at {yoga_class.start_date_time}.", to=user.phone) 


############ POSSIBLE DELETE SIGNUP ROUTE ############################

# @app.route('/classes/cancel_signup/<int:class_id>', methods=["DELETE"])
# def delete_user(class_id):
#     """Delete user."""

#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")

#     signup = Signups.query.get_or_404(primary_key)

#     db.session.delete(signup)
#     db.session.commit()

#     return redirect("/signup")



############# Code to pull up instructors names as select field

# function to get instructor's first name for the ClassAddForm
# def choice_query():
#     return User.query

# class ClassAddForm(FlaskForm):
#     """Form for adding or editing classes."""
#     instructor = QuerySelectField(query_factory=choice_query, allow_blank=True, get_label='first_name', blank_text='(Instructor)')
   




######################################################################
############################# MODELS.PY ##############################
######################################################################

### POSSIBLE CODES TO LIST NAME OF INSTRUCTOR OR PROPER DATE DISPLAY###

    # def __repr__(self):
    #     return f"<User #{self.id}: {self.email}>"

    # def __repr__(self):
    # return '<Instructor {}>'.format(self.first_name)

    # def readable_dates(self):
    #     """Change Classes dates object to something readable"""
    #     return {
    #         date: self.start_date_time(strftime, '%b %d, %Y')
    #         # time: self.start_date_time + "-" + 
    #     }





use this code
    # user = g.user

    # if user.is_instructor:
    #     Signups.query.filter_by(user_id=user.id, class_id=class_id).delete
    #     db.session.commit()

    #     flash("Class had been deleted", "success")
    #     return redirect("/")

    # else:
    #     flash("Access unauthorized.", "danger")
    #     return redirect("/")










### NOTES ###

# Twilio Phone Number is +16814343687

# https://pypi.org/project/pytz/   website to figure out timezones



<div id="background-image">
  <div class="card text-center col-md-5 mx-auto my-auto card-position" >
    <div class="col-md-12 p-lg-5 mx-auto my-1">
      <h1 class="display-4 font-weight-normal">Lunchtime Yoga for Professionals</h1>
      <p class="lead font-weight-normal">This is the homepage for the yoga website.</p>

      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          {% for category,msg in messages %}
          <div class="alert alert-{{ category }}" role="alert">
            {{msg}}
          </div>
          {% endfor %}
        {% endif %}
      {% endwith %}

      {% if g.user %}
      <br><div class="col-md-8 order-md-1 mx-auto">
        <img src="{{ g.user.image_url }}" alt="Profile Image" id="profile-image" class="shadow">
      </div>
      <p class="lead font-weight-normal">Hi, {{ g.user.first_name }}</p>

      {% else %}
      <div class="row justify-content-sm-center">
        <div class="col-md-7 col-lg-7">
          <form method="POST" id="user_form">
            {{ form.hidden_tag() }}
      
            {% for field in form if field.widget.input_type != 'hidden' %}
              {% for error in field.errors %}
                <span class="text-danger">{{ error }}</span>
              {% endfor %}
              {{ field(placeholder=field.label.text, class="form-control shadow") }}
            {% endfor %}
      
            <button class="btn btn-primary btn-lg btn-block shadow">Log in</button>
            <p class="lead font-weight-normal">or</p>
            <a href="/signup" class="btn btn-success btn-lg btn-block shadow">Sign up</a>
          </form>
        </div>
      </div>

      {% endif %}
    </div>
  </div>
</div>







<div id="background-image">
    <div class="card shadow" id="login-card">
        <div class="row no-gutters">
            <div class="col-sm-6 text-center">
              <br><br><br><br>
              <h1 class="">Lunchtime Yoga for Professionals</h1><br>
              <span>Ready for a break from the chaos? </span><br><span>Ground yourself with local yoga classes.</span>
              <br><span>Virtual classes available.</span>
            </div>
            <div class="vl"></div>

            <div class="col-sm-6">
                <div class="card-body">
                  {% with messages = get_flashed_messages(with_categories=true) %}
                  {% if messages %}
                    {% for category,msg in messages %}
                    <div class="alert alert-{{ category }}" role="alert">
                      {{msg}}
                    </div>
                    {% endfor %}
                  {% endif %}
                {% endwith %}
                  <article class="card-body">
                    <a href="/users/signup" class="float-right btn btn-outline-primary">Sign up</a>
                    <h4 class="card-title mb-4 mt-1">Sign in</h4>
                  
                    <form method="POST" id="user_form">
                      
                      {% for field in form if field.widget.input_type != 'hidden' %}
                      {% for error in field.errors %}
                        <span class="text-danger">{{ error }}</span>
                      {% endfor %}
                      <div class="form-group">
                      <label>{{field.label.text}}</label>
                      {{ field(class="form-control shadow-sm") }}</div> 
                    {% endfor %}
                    
                        <div class="form-group">
                            <br><button type="submit" class="btn btn-primary btn-block"> Login  </button>
                        </div> <!-- form-group// -->                                                           
                    </form>
                    </article>
                </div>
            </div>
        </div>
    </div>
</div>