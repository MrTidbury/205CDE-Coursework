from flask.ext.wtf import Form #importing all of the required packages that are needed for these forms
from wtforms import TextField, IntegerField, StringField, SelectField, DateField, TextAreaField, SubmitField, BooleanField, validators, ValidationError, PasswordField
from wtforms.validators import Required, DataRequired, ValidationError
from models import db, User #imort the DB models that are defined in models.py

class ContactForm(Form): #creating a class for contact form that inherits from flask WTF form
    name = TextField("Name", [validators.Required(" Please enter your name")]) #for each needed field, define the field and then set a custom validator text
    email = TextField("Email", [validators.Required(" Please enter your email address"), validators.Email("Invalid Email Address")]) #the email validator makes sure it is a valid email address
    subject = TextField("Subject", [validators.Required(" Please enter a subject")])
    message = TextAreaField("Message", [validators.Required(" What? No message?")])
    submit = SubmitField("Send", [validators.Required()]) #defining the submit button

class SignupForm(Form): #the same as the contact form but for the Signup form
    firstname = TextField("First name",  [validators.Required("Please provide your first name.")])
    lastname = TextField("Last name",  [validators.Required("Please provide your last name.")])
    email = TextField("Email",  [validators.Required("Please provide your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please provide a password.")]) #using password field to automatically censor password
    submit = SubmitField("Create account")
    
    def __init__(self,*args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        
    def validate(self): #setting up the validation function for main.py to call
        if not Form.validate(self):
            return False
            
        user = User.query.filter_by(email = self.email.data.lower()).first() #to check if email is already in the database
        if user:
            self.email.errors.append("That email address is already in use, please try to login") #if the email adress is already in the database then display error
            return False
        else:
            return True

class loginForm(Form): #same as above but different fields
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Log In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self): #same as above, making a validation function for later use
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first() #check if user is in the database
    if user and user.check_password(self.password.data): #if the user exists and the password is correct (this calls a function that is defined in models.py and uses the password given in the form as an argument)
      return True
    else:
      self.email.errors.append("Invalid Login details provided, please try again") #if it fails then display this error message
      return False