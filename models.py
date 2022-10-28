from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Create db Module
db = SQLAlchemy()

# Users Table Model
class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    passcode = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    is_Admin = db.Column(db.Boolean, nullable=False, default=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        template = '{0.id} {0.name} {0.is_Admin} {0.date_created}'
        return template.format(self)

# Contacts Table Model
class Contacts(db.Model):
    __tablename__="Contacts"
    contactID = db.Column(db.Integer, primary_key=True)
    fName =db.Column(db.String(50), nullable=False)
    lName =db.Column(db.String(50), nullable=True)
    mName =db.Column(db.String(50), nullable=True)
    workCompany = db.Column(db.String(50), nullable=True)
    mobile =db.Column(db.String(20), nullable=True)
    homePhone =db.Column(db.String(20), nullable=True)
    workPhone =db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    jobTitle = db.Column(db.String(50), nullable=True)
    imageURL = db.Column(db.String(200), nullable=True)
    createdBy = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        template = '{0.contactID} {0.fName} {0.mobile}'
        return template.format(self)
