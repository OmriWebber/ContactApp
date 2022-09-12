from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_login import LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from flask_migrate import Migrate
from models import *
import os

application = Flask(__name__)

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if 'RDS_DB_NAME' in os.environ:
    application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:contactapp@sql-database-contact-app.ch0or1bnad8y.ap-southeast-2.rds.amazonaws.com/sql-database-contact-app?charset=utf8mb4"
else:
    # application.config['SQLALCHEMY_DATABASE_URI'] = "mysql://admin:contactapp@sql-database-contact-app.ch0or1bnad8y.ap-southeast-2.rds.amazonaws.com/sql-database-contact-app?charset=utf8mb4"
    application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    
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

@application.route("/")
def index():
    contList=Contacts.query.all()
    cont=Contacts.query.first()
    return render_template("index.html", cont=cont, contList=contList, name="Contact App")
    
@application.route("/addContact", methods=["POST"])
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
    return render_template("index.html",cont=cont, contList=contList, name="Contact App", msg="Contact Added!") 
    
@application.route("/showContact/<conid>")
def showContact(conid):
    # select row from contacts table for contact ID passed from main page
    cont=Contacts.query.filter_by(contactID=conid).one()
    contList=Contacts.query.all()
    return render_template("index.html",cont=cont, contList=contList, name="Contact App")

@application.route("/deleteContact/<int:conid>")
def deleteContact(conid):
    # select row from contacts table for contact ID passed from main page
    cont = Contacts.query.filter_by(contactID=conid).one()
    db.session.delete(cont)
    db.session.commit()
    contList=Contacts.query.all()
    return redirect(url_for('index'))  

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
    



  