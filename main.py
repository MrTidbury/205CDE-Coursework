import os
from flask import Flask
from flask import *
from flask_bootstrap import Bootstrap
import flask_bootstrap
from flask_mail import Mail, Message
from forms import ContactForm, SignupForm, loginForm
from models import db, User
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:email001@localhost/main'
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='mail.tidbury.xyz',
	MAIL_PORT=26,
	MAIL_USE_SSL=False,
	MAIL_USERNAME = 'griffindesign@tidbury.xyz',
	MAIL_PASSWORD = 'email001',
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	)

mail=Mail(app)
db.init_app(app)
app.secret_key= '1234thisisasecurestringihope1234'

@app.route('/')
def index():
    if 'email' in session:
      user = (User.query.filter_by(email=session['email']).first()).firstname
      return render_template('homepage.html', user=user)
    else:
      return render_template('homepage.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form=ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are reqired')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='contactform@griffindesign.com', recipients=['jack@tidbury.xyz'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            msg = Message('Your recent Enquiry', sender='enquiries@griffindesign.com', recipients=[form.email.data])
            msg.body = "Hello, %s\nThank you for your interest in Griffin Design, we aim to contact you with regards you your request in approximatly 24 hours. Your enquiry was as follows; if that is not correct please contact us.\n\nYour Message: %s\n\nRegards,\nGriffin Design"% (form.name.data, form.message.data)
            mail.send(msg)
            return render_template('contact.html', success=True)
    elif request.method == 'GET':
        return render_template('contact.html',form=form,name='need to contact us?')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('basic.html',name="Oh,dear this page doesnt exist"), 404

@app.route('/signup', methods=['GET', 'POST'])
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

@app.route('/login', methods=['GET','POST'])
def login():
  form = loginForm()
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('login.html',form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
  elif request.method == 'GET':
    return render_template('login.html', form=form)
  
@app.route('/signout', methods=['GET','POST'])
def signout():
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route('/profile')
def profile():
  if 'email' not in session:
    return redirect(url_for('login'))
 
  user = User.query.filter_by(email = session['email']).first()
  firstname = user.firstname
  lastname = user.lastname
  if user is None:
    return redirect(url_for('signup'))
  else:
    return render_template('profile.html', firstname=firstname, lastname=lastname)
@app.route('/removeaccount')
def removeaccount():
    user = User.query.filter_by(email = session['email']).first()
    db.session.delete(user)
    session.pop('email', None)
    db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)