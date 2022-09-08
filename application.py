from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from flask_migrate import Migrate
from models import *
import os

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if 'RDS_DB_NAME' in os.environ:
    application.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://postgres:postgres@database-contact-app.ch0or1bnad8y.ap-southeast-2.rds.amazonaws.com/database-contact-app"
else:
    application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    
db.init_app(application)
migrate = Migrate(application, db)

@application.route("/")
def index():
    contList=Contacts.query.all()
    cont=Contacts.query.first()
    return render_template("index.html", cont=cont, contList=contList)
    
@application.route("/addcontact", methods=["POST"])
def addcontact():
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
    #Pass on the local values to the corresponfding model
    contact = Contacts( fName=fName,lName=lName,mName=mName,workCompany=workCompany,jobTitle=jobTitle,mobile=mobile,homePhone=homePhone,workPhone=workPhone,email=email)
    db.session.add(contact)
    db.session.commit()
    cont=Contacts.query.filter_by(contactID=contact.contactID).first()
    contList=Contacts.query.all()
    return render_template("index.html",cont=cont, contList=contList) 
    
@application.route("/showContact/<int:conid>")
def showContact(conid):
    # select row from contacts table for contact ID passed from main page
    cont=Contacts.query.filter_by(contactID=conid).first()
    contList=Contacts.query.all()
    return render_template("index.html",cont=cont, contList=contList)  

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
    



  