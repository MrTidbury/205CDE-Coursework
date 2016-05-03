import os
from flask import Flask
from flask import *
from flask_bootstrap import Bootstrap
import flask_bootstrap
from flask_mail import Mail, Message
from forms import ContactForm, SignupForm, loginForm          #Importing the Forms that are defined in forms.py
from models import db, User                                   #Importing the DB settings and the User class from models.py 
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:email001@localhost/main' #configuring SQL alchemy with my settings
app.config.update(
	DEBUG=True,
	MAIL_SERVER='mail.tidbury.xyz',                             #The following lines are the server configutations for my Mail server to allow the site to send emails
	MAIL_PORT=26,
	MAIL_USE_SSL=False,
	MAIL_USERNAME = 'griffindesign@tidbury.xyz',
	MAIL_PASSWORD = 'email001',
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	)

mail=Mail(app)                                                #tells WTF mail to initialise for later use
db.init_app(app)                                              #tells SQLalchemy to initialise for later use
app.secret_key= '5yZ7dYU_9ne2Dv7ElrUO'                        #sets the encyription key for the session (cookies)     

@app.route('/')
def index():
    if 'email' in session:                                                      #checks to see if the user is signed in by looking for the email cookie created on sign in
      user = (User.query.filter_by(email=session['email']).first()).firstname   #queries the database to find the users first name
      return render_template('homepage.html', user=user)                        #First name is then passed to the template to display a custom message
    else: 
      return render_template('homepage.html')                                   #if the user is not logged in it returns a default template

@app.route('/about')                                          #this is a simple case of routing, no variables being passed
def about():
    return render_template('about.html')
    
@app.route('/contact', methods=['GET', 'POST'])               #By passing both GET and POST, these can be used later to get infomation from the form
def contact():
    form=ContactForm()                                        #Setting the Form as the class created called ContactForm in forms.py
    if request.method == 'POST':                              #If this page was requested with post, meaning that the form was submitted
        if form.validate() == False:                          #If the form fails the validation fucntion, re-render the template and error messages are shown
            flash('All fields are reqired')
            return render_template('contact.html', form=form)
        else:                                                #The following lines of code, send 2 different emails, one to me (as an admin) and the other to whatever email was passed in the form                                                         
            msg = Message(form.subject.data, sender='contactform@griffindesign.com', recipients=['jack@tidbury.xyz'])
            msg.body = """
            NEW MESSAGE : %s
            From: %s <%s>
            """ % (form.message.data, form.name.data, form.email.data ) #Sends the admin an email with the contents of the contact form
            mail.send(msg)
            msg = Message('Your recent Enquiry', sender='enquiries@griffindesign.com', recipients=[form.email.data])
            msg.body = "Hello, %s\nThank you for your interest in Griffin Design, we aim to contact you with regards you your request in approximatly 24 hours. Your enquiry was as follows; if that is not correct please contact us.\n\nYour Message: %s\n\nRegards,\nGriffin Design"% (form.name.data, form.message.data)
            mail.send(msg)                                    #Sends the customer an email thanking them for contacting the site
            return render_template('contact.html', success=True) #re-renders the page with the sucsessflag marked as true so the sucsess box can be displayed
    elif request.method == 'GET':                               #if the page was fethced via get it means that the form was not submitted, therefor it just displays the page normally
        return render_template('contact.html',form=form)
    
@app.errorhandler(404)    #Routing for the common 404 error displays a nice error page
def page_not_found(e):
    return render_template('error404.html'), 404

@app.route('/signup', methods=['GET', 'POST']) #Just like before as this page contains a form both GET and POST are needed
def signup():
  form = SignupForm()
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      session['email'] = newuser.email
      return redirect(url_for('profile'))
   
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET','POST']) #Just like before as this page contains a form both GET and POST are needed
def login():
  form = loginForm()                          #sets the form as the login form class as defined
  if request.method == 'POST':                #this is the same as the contact form, checking for POST and Validation
    if form.validate() == False:
      return render_template('login.html',form=form)
    else:
      session['email'] = form.email.data      #if all is passed, it logs the user in by creating a cookie of thier email address. this is done by using the session command in flask as thier data is then secure
      return redirect(url_for('index'))       #sends user to the home page after logging in    
  elif request.method == 'GET':
    return render_template('login.html', form=form)
  
@app.route('/signout')
def signout():
  session.pop('email', None)          #signs the user out by removing the cookie from the browser
  return redirect(url_for('index'))   #sends them back to the home page

@app.route('/profile')
def profile():
  if 'email' not in session:            #if the user is not loged in then return them to the login page
    return redirect(url_for('login'))
 
  user = User.query.filter_by(email = session['email']).first() #find the user by quiering the database with the cookie as the email
  firstname = user.firstname  #store the firstname of the user
  lastname = user.lastname    #store the lastname of the user 
  if user is None:    #if it cant find the user then redirect them to the signup page
    return redirect(url_for('signup'))
  else:
    return render_template('profile.html', firstname=firstname, lastname=lastname) #if the user is found then render the template with the infomation passed
    
@app.route('/removeaccount') #allowing the user to remove thier account from the database
def removeaccount():
    user = User.query.filter_by(email = session['email']).first() #find the user by the cookie stored in thier browser
    db.session.delete(user) #tell the db to remove the user
    session.pop('email', None) #remove the cookie from the browser, the same as logging out
    db.session.commit() #commit the changes to the database, IE remove the DB
    
    return redirect(url_for('index'))

if __name__ == '__main__': #if this app is run as the main app then do the following
    port = int(os.getenv('PORT', 8080)) #get default port (8080)
    host = os.getenv('IP', '0.0.0.0') #get the ip from the os
    app.run(port=port, host=host) #run the app with the above information