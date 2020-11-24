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












### NOTES ###

# Twilio Phone Number is +16814343687

# https://pypi.org/project/pytz/   website to figure out timezones