from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, StringField, SelectField, DateField, TextAreaField, SubmitField, BooleanField, validators
from wtforms.validators import Required, DataRequired, ValidationError

class ContactForm(Form):
    name = TextField("Name", [validators.Required(" Please enter your name")])
    email = TextField("Email", [validators.Required(" Please enter your email address"), validators.Email("Invalid Email Address")])
    subject = TextField("Subject", [validators.Required(" Please enter a subject")])
    message = TextAreaField("Message", [validators.Required(" What? No message?")])
    submit = SubmitField("Send", [validators.Required()])