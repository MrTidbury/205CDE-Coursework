from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, StringField, SelectField, DateField, TextAreaField, SubmitField, BooleanField, validators, ValidationError, PasswordField
from wtforms.validators import Required, DataRequired, ValidationError
from models import db, User

class ContactForm(Form):
    name = TextField("Name", [validators.Required(" Please enter your name")])
    email = TextField("Email", [validators.Required(" Please enter your email address"), validators.Email("Invalid Email Address")])
    subject = TextField("Subject", [validators.Required(" Please enter a subject")])
    message = TextAreaField("Message", [validators.Required(" What? No message?")])
    submit = SubmitField("Send", [validators.Required()])

class SignupForm(Form):
    firstname = TextField("First name",  [validators.Required("Please provide your first name.")])
    lastname = TextField("Last name",  [validators.Required("Please provide your last name.")])
    email = TextField("Email",  [validators.Required("Please provide your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please provide a password.")])
    submit = SubmitField("Create account")
    
    def __init__(self,*args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        
    def validate(self):
        if not Form.validate(self):
            return False
            
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email address is already in use, please try to login")
            return False
        else:
            return True

class loginForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Log In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid Login details provided, please try again")
      return False