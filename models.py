from flask_sqlalchemy import SQLAlchemy #import SQLAlchemy to manage the SQL database
from werkzeug import *
db = SQLAlchemy()

class User(db.Model): #creating a class for the user 
    __tablename__ = 'users' #tell SQLAlchemy to put this class in the users table
    uid = db.Column(db.Integer, primary_key = True) #tell SQLAlchemy the layout of the SQL table
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    email = db.Column(db.String(120), unique= True)
    pwdhash = db.Column(db.String(54))
    
    def __init__(self, firstname, lastname, email, password): #when the class is initialised set the folowing variables that can be called from outside the class
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower() #the email is always lowercase to avoid duplication or confusion
        self.set_password(password) #call the function below
        
    def set_password(self, password): #to set password use this function
        self.pwdhash = generate_password_hash(password) #uses werkzeug built in pswdhash function to avoid storing the password in plain text
        
    def check_password(self, password): #to check passwork use this function
        return check_password_hash(self.pwdhash, password) #call werkzeug check password that comapares the hash of the given password to that of the one in the database