from form import db #set env variable
from sqlalchemy.orm import backref
from sqlalchemy import Column, Integer, String, Boolean, Date

class SignOffForms(db.Model):
    __tablename__ = "SignOffForms"
    id = db.Column(db.Integer, primary_key=True)
    provisioningForm = db.relationship('Provisioning',backref='SignOffForms',cascade="all, delete", lazy=True)
    desktopForm = db.relationship('Desktop',backref='signoff' ,cascade="all, delete", lazy=True)
    userForm = db.relationship('User',backref='signoff' ,cascade="all, delete", lazy=True)
   

class Provisioning(db.Model):
    __tablename__ = "Provisioning"
    id = db.Column(db.Integer, primary_key=True)
    deviceModel = db.Column(db.String, nullable=False)
    serviceTag = db.Column(db.String, nullable=False)
    assetTag = db.Column(db.String, nullable=False)
    windowsUpdates = db.Column(db.Boolean, nullable=False)
    bitlocker = db.Column(db.Boolean, nullable=False)
    userSoftware = db.Column(db.Boolean, nullable=False)
    ADgroups = db.Column(db.Boolean, nullable=True)
    desktopIcons = db.Column(db.Boolean, nullable=False)
    vpnInstalled = db.Column(db.Boolean, nullable=False)
    hardwareChecked = db.Column(db.Boolean, nullable=False)
    staffMember = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    form_id = db.Column(db.Integer, db.ForeignKey("SignOffForms.id"), nullable=False)

class Desktop(db.Model):
    __tablename__ = "Desktop"
    id = db.Column(db.Integer, primary_key=True)
    contactedUser = db.Column(db.Boolean, nullable=False)
    collectOldDevice = db.Column(db.Boolean)
    Onedrive = db.Column(db.Boolean, nullable=False)
    bitlockerPin = db.Column(db.Boolean, nullable=False)
    IPreservation = db.Column(db.Boolean)
    StaffMember = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    form_id = db.Column(db.Integer, db.ForeignKey("SignOffForms.id",ondelete="CASCADE"), nullable=False)

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    staffMember = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    form_id = db.Column(db.Integer, db.ForeignKey("SignOffForms.id",ondelete="CASCADE"), nullable=False)

