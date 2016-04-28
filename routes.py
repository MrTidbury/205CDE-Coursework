import os
from flask import Flask
from flask import *
from flask_bootstrap import Bootstrap
import flask_bootstrap
from flask_mail import Mail, Message
from forms import ContactForm
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='mail.tidbury.xyz',
	MAIL_PORT=26,
	MAIL_USE_SSL=False,
	MAIL_USERNAME = 'griffindesign@tidbury.xyz',
	MAIL_PASSWORD = 'email001'
	)
mail=Mail(app)
app.secret_key= '1234thisisasecurestringihope1234'

@app.route('/')
def index():
    return render_template('homepage.html', name="Welcome to Griffin Design")

@app.route('/about')
def about():
    return render_template('basic.html', name="ABOUT")

@app.route('/projects')
def projects():
    return render_template('basic.html', name="PROJECTS")
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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)