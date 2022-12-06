from form import db #set env variable
from sqlalchemy.orm import backref
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = db
db_session = scoped_session(sessionmaker(autocommit=False,
autoflush=False,
bind=engine))

Base = declarative_base()
Base.query = db_session.query_property



class SignOffForms(db.Model):
    __tablename__ = "SignOffForms"

    id = db.Column(db.Integer, primary_key=True)
    prov_form_id = db.Column(db.Integer)
    provisioningForm = db.relationship('Provisioning',backref='SignOffForms',cascade="all, delete", lazy=True)
    

    desktop_form_id = db.Column(db.Integer)
    desktopForm = db.relationship('Desktop',backref='SignOffForms' ,cascade="all, delete" , lazy=True)
    

    user_form_id = db.Column(db.Integer)
    userForm = db.relationship('User',backref='SignOffForms' ,cascade="all, delete", lazy=True )
    closed = db.Column(db.Boolean)
    
    
   

class Provisioning(db.Model):
    __tablename__ = "Provisioning"
    id = db.Column(db.Integer, primary_key=True)
    deviceModel = db.Column(db.String)
    serviceTag = db.Column(db.String)
    assetTag = db.Column(db.String)
    windowsUpdates = db.Column(db.Boolean)
    bitlocker = db.Column(db.Boolean)
    userSoftware = db.Column(db.Boolean)
    ADgroups = db.Column(db.Boolean)
    desktopIcons = db.Column(db.Boolean)
    vpnInstalled = db.Column(db.Boolean)
    hardwareChecked = db.Column(db.Boolean)
    staffMember = db.Column(db.String)
    date = db.Column(db.Date)
    form_id = db.Column(db.Integer, db.ForeignKey("SignOffForms.id"))
    closed = db.Column(db.Boolean)
    

  


class Desktop(db.Model):
    __tablename__ = "Desktop"
    id = db.Column(db.Integer, primary_key=True)
    contactedUser = db.Column(db.Boolean)
    collectOldDevice = db.Column(db.Boolean)
    Onedrive = db.Column(db.Boolean)
    bitlockerPin = db.Column(db.Boolean)
    IPreservation = db.Column(db.Boolean)
    StaffMember = db.Column(db.String)
    date = db.Column(db.Date)
    form_id = db.Column(db.Integer, db.ForeignKey("SignOffForms.id",ondelete="CASCADE"))
    closed = db.Column(db.Boolean)
    

    
class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    staffMember = db.Column(db.String)
    date = db.Column(db.Date)
    form_id = db.Column(db.Integer, db.ForeignKey("SignOffForms.id",ondelete="CASCADE"))
    closed = db.Column(db.Boolean)
    

