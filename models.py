from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Create db Module
db = SQLAlchemy()

# Users Table Model
class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    passcode = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    is_Admin = db.Column(db.Boolean, nullable=False, default=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        template = '{0.id} {0.name} {0.is_Admin} {0.date_created}'
        return template.format(self)

# Contacts Table Model
class Contacts(db.Model):
    __tablename__="Contacts"
    contactID = db.Column(db.Integer, primary_key=True)
    fName =db.Column(db.String, nullable=False)
    lName =db.Column(db.String, nullable=False)
    mName =db.Column(db.String, nullable=False)
    workCompany = db.Column(db.String, nullable=True)
    mobile =db.Column(db.String, nullable=False)
    homePhone =db.Column(db.String, nullable=True)
    workPhone =db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    jobTitle = db.Column(db.String, nullable=True) 
    
    def __repr__(self):
        template = '{0.id} {0.fName} {0.mobile} {0.createdBy}'
        return template.format(self)
