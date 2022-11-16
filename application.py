from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from models import *
from flask_cdn import CDN 
import os
import pymysql

pymysql.install_as_MySQLdb()

UPLOAD_FOLDER = 'static/img/profilePictures/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

application = Flask(__name__)
application.secret_key = 'dev'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['CDN_DOMAIN'] = 'd2swf54x8mldch.cloudfront.net'
application.config['CDN_TIMESTAMP'] = False

# If application detects rds database, use cloud database, if not use localhost
if 'RDS_HOSTNAME' in os.environ:
    print('AWS ELB ENV DETECTED')
    CDN(application)
    RDS_Connection_String = 'mysql+pymysql://' + os.environ['RDS_USERNAME'] + ':' + os.environ['RDS_PASSWORD'] + '@' + os.environ['RDS_HOSTNAME'] + ':' + os.environ['RDS_PORT'] + '/' + os.environ['RDS_DB_NAME']
    application.config['SQLALCHEMY_DATABASE_URI'] = RDS_Connection_String
else:
    print('LOCAL ENV DETECTED')
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

def allowed_file(filename):     
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    msg = ''
    return render_template("index.html", cont=cont, contList=contList, msg=msg, name="Contact App", user=current_user)

@application.route("/test")
@login_required
def test():
    contList=Contacts.query.all()
    cont=Contacts.query.first()
    return render_template("test1.html", cont=cont, contList=contList, name="Contact App", user=current_user)


@application.route('/addContact', methods=['POST', 'GET'])
@login_required
def addContact():
    if request.method == 'POST':
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
        imageURLforDB='img/profilePictures/default.jpg'
        
        if 'profilePicture' not in request.files:
            print("No file part")
        file=request.files['profilePicture']
        if file.filename == '':
            print("No selected file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            imageURL = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            imageURLforDB = os.path.join('img/profilePictures/', filename)
            file.save(imageURL)
            
        
        # Pass on the local values to the corresponding model
        contact = Contacts( fName=fName,lName=lName,mName=mName,workCompany=workCompany,jobTitle=jobTitle,mobile=mobile,homePhone=homePhone,workPhone=workPhone,email=email,imageURL=imageURLforDB)
        db.session.add(contact)
        db.session.commit()
        
    contList=Contacts.query.all()
    return render_template("index.html", msg='', contList=contList, name="Contact App", user=current_user)

    
@application.route("/showContact/<conid>")
def showContact(conid):
    # select row from contacts table for contact ID passed from main page
    cont=Contacts.query.filter_by(contactID=conid).one()
    contList=Contacts.query.all()
    return render_template("showContact.html", cont=cont, contList=contList, name="Contact App", user=current_user)


@application.route("/deleteContact/<int:conid>")
def deleteContact(conid):
    # select row from contacts table for contact ID passed from main page
    cont = Contacts.query.filter_by(contactID=conid).one()
    db.session.delete(cont)
    db.session.commit()
    logThis("deleted", current_user.name, current_user.id, cont.fName, cont.contactID)
    return redirect(url_for('index'))

@application.route("/editContact/<conid>", methods=['POST', 'GET'])
def editContact(conid):
    if request.method == 'POST':
        # select row from contacts table for contact ID passed from main page
        cont = Contacts.query.filter_by(contactID=conid).one()
        fName=request.form.get("FirstName")
        lName=request.form.get("LastName")
        mName=request.form.get("MiddleName")
        workCompany=request.form.get("WorkCompany")
        jobTitle=request.form.get("JobTitle")
        mobile=request.form.get("Mobile")
        homePhone=request.form.get("HomePhone")
        workPhone=request.form.get("WorkPhone")
        email=request.form.get("email")

        if 'profilePicture' not in request.files:
            print("No file")
        file=request.files['profilePicture']
        if file.filename == '':
            print("No selected file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            imageURL = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            imageURLforDB = os.path.join('img/profilePictures/', filename)
            cont.imageURL = imageURLforDB
            file.save(imageURL)
        
        cont.fName = fName
        cont.lName = lName
        cont.mName = mName
        cont.workCompany = workCompany
        cont.jobTitle = jobTitle
        cont.mobile = mobile
        cont.homePhone = homePhone
        cont.workPhone = workPhone
        cont.email = email
        
        db.session.commit()
        logThis("edited", current_user.name, current_user.id, cont.fName, cont.contactID)
    return redirect(url_for('index'))

@application.route("/profile")
def profile():
    return render_template('profile.html')


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
    



  