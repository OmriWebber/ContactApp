from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_login import LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *
import os

application = Flask(__name__)

application.secret_key = 'dev'

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if 'RDS_DB_NAME' in os.environ:
    application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:password@contact-app-database.ch0or1bnad8y.ap-southeast-2.rds.amazonaws.com:3306/contact_app_db'
else:
    # application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:password@contact-app-database.ch0or1bnad8y.ap-southeast-2.rds.amazonaws.com:3306/contact_app_db'
    application.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/contactapp"
    
db.init_app(application)
migrate = Migrate(application, db)

# Init Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# blueprint for auth routes in our application
from auth import auth as auth_blueprint
application.register_blueprint(auth_blueprint)

def logThis(function, user, userID, contact, contactID):
    date = datetime.now()
    dateString = str(date)
    tuple = ('[',dateString,'] ',user,':',userID,' ',function,' ',contact,':',contactID)
    log = "".join(map(str, tuple))
    with open("log.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        file_object.write(log)


@application.route("/")
@login_required
def index():
    contList=Contacts.query.all()
    cont=Contacts.query.first()
    return render_template("index.html", cont=cont, contList=contList, name="Contact App", user=current_user)

@application.route("/test")
@login_required
def test():
    contList=Contacts.query.all()
    cont=Contacts.query.first()
    return render_template("test1.html", cont=cont, contList=contList, name="Contact App", user=current_user)


@application.route("/addContact", methods=["POST"])
@login_required
def addContact():
    #store values recieved from HTML form in local variables
    fName=request.form.get("FirstName")
    lName=request.form.get("LastName")
    mName=request.form.get("MiddleName")
    workCompany=request.form.get("WorkCompany")
    jobTitle=request.form.get("WorkJobTitle")
    mobile=request.form.get("Mobile")
    homePhone=request.form.get("HomePhone")
    workPhone=request.form.get("WorkPhone")
    email=request.form.get("email")
    
    # Pass on the local values to the corresponding model
    contact = Contacts( fName=fName,lName=lName,mName=mName,workCompany=workCompany,jobTitle=jobTitle,mobile=mobile,homePhone=homePhone,workPhone=workPhone,email=email)
    db.session.add(contact)
    db.session.commit()
    cont=Contacts.query.filter_by(contactID=contact.contactID).first()
    contList=Contacts.query.all()
    return render_template("showContact.html", cont=cont, msg='', contList=contList, name="Contact App", user=current_user)

    
@application.route("/showContact/<conid>")
def showContact(conid):
    # select row from contacts table for contact ID passed from main page
    cont=Contacts.query.filter_by(contactID=conid).one()
    contList=Contacts.query.all()
    print(cont)
    return render_template("showContact.html", cont=cont, contList=contList, name="Contact App", user=current_user)


@application.route("/deleteContact/<int:conid>")
def deleteContact(conid):
    # select row from contacts table for contact ID passed from main page
    cont = Contacts.query.filter_by(contactID=conid).one()
    db.session.delete(cont)
    db.session.commit()
    logThis("deleted", current_user.name, current_user.id, cont.fName, cont.contactID)
    return redirect(url_for('index'))

@application.route("/profile")
def profile():
    return render_template('profile.html')


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
    



  