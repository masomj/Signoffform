from flask import Flask
from form import app, db
from flask import Flask, render_template, request, redirect, url_for
from .forms import Provisioning, DesktopSupport, User
from form import app, db
from .models import Provisioning, User, Desktop, SignOffForms
from flask_paginate import Pagination, get_page_args
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField,SubmitField
from wtforms.validators import InputRequired, Length
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

date=datetime.now()

engine = db
db_session = scoped_session(sessionmaker(autocommit=False,
autoflush=False,
bind=engine))

Base = declarative_base()
Base.query = db_session.query_property

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import form.models
    Base.metadata.create_all(bind=engine)


#pagination
def get_forms(offset=0, per_page=10):
  forms = list(SignOffForms.query.order_by(SignOffForms.id).all())
  return forms[offset: offset+per_page]


@app.route('/')
def index():
  editableForms =[] 
  page, per_page,offset = get_page_args(page_parameter="page",per_page_parameter="per_page")
  forms = list(SignOffForms.query.order_by(SignOffForms.id).all())
  total = len(forms)
  pagination_forms= get_forms(offset=offset,per_page=per_page)
  pagination = Pagination(page=page, per_page=per_page,total=total,css_framework='bootstrap5')
  provForms = list(Provisioning.query.order_by(Provisioning.id).all())
  userForms = list(User.query.order_by(User.id).all())
  desktopForms = list(Desktop.query.order_by(Desktop.id).all())

  return render_template('allform.html', editableForms=editableForms, provForms=provForms,userForms=userForms,desktopForms=desktopForms, forms = pagination_forms,page=page, per_page = per_page, pagination = pagination)


@app.route('/create_form', methods=['GET','POST'])
def create_form():
  new_form = SignOffForms()
  db.session.add(new_form)
  db.session.commit()

  return redirect(url_for('index'))

#new desktop form submit
@app.route('/desktop/<int:form_id>',methods=["GET","POST"])
def desktop(form_id):
  form = SignOffForms.query.get_or_404(form_id)
  
  if request.method=="POST":
    contuser = False
    collect = False
    onedrive = False
    bitlocker = False
    IPcheck = False
    if request.form.get("contactedUser") == "True":
        contuser = True
    if request.form.get("collectOldDevice") == "True":
        collect = True
    if request.form.get("Onedrive") == "True":
        onedrive = True
    if request.form.get("changeBitlocker") == "True":
        bitlocker = True
    if request.form.get("checkIP") == "True":
        IPcheck = True

    desk_form = Desktop(
      contactedUser = contuser,
      collectOldDevice = collect,
      Onedrive = onedrive,
      bitlockerPin = bitlocker,
      IPreservation = IPcheck,
      StaffMember=request.form.get("desktopUser"),
      date=date,
      form_id=form_id,
    )
    db.session.add(desk_form)
    db.session.commit()
    return redirect(url_for('index'))

  return render_template("desktop.html", form=form)

@app.route("/Editprovisioning/<int:form_id>/<prov_form>")
def editprovisioning(form_id, prov_form):
  form = SignOffForms.query.get_or_404(form_id)
  split = prov_form.split(" ")
  no = split[1].replace(">]","")
  newNo = int(no)
  print(newNo)
  print(type(newNo))

  provisioning_form = Provisioning.query.get_or_404(newNo)

  print(provisioning_form.deviceModel)
  
  return render_template("editprovisioning.html",form=form,prov_form=provisioning_form)


#new provisioning form submit
@app.route('/provisioning/<int:form_id>', methods=["GET","POST"])
def provisioning(form_id):
  form = SignOffForms.query.get_or_404(form_id)
  if request.method =="POST":
    winup = False
    bitlock = False
    soft = False
    ADgroups = False
    desktopIcons = False
    vpnInstalled = False
    hardwareChecked = False
    if request.form.get("windowsUpdates") == "True":
        winup = True
    if request.form.get("Bitlocker") == "True":
       bitlock = True
    if request.form.get("userSoftware") == "True":
      soft = True
    if request.form.get("ADgroups") == "True":
      ADgroups = True
    if request.form.get("desktopIcons") == "True":
      desktopIcons = True
    if request.form.get("vpnInstalled") == "True":
      vpnInstalled = True
    if request.form.get("hardwareChecked") == "True":
      hardwareChecked = True

    prov_form = Provisioning(
      deviceModel=request.form.get("deviceModel"),
      serviceTag=request.form.get("serviceTag"),
      assetTag=request.form.get("assetTag"),
      windowsUpdates=winup,
      bitlocker=bitlock,
      userSoftware = soft,
      ADgroups=ADgroups,
      desktopIcons=desktopIcons,
      vpnInstalled=vpnInstalled,
      hardwareChecked=hardwareChecked,
      staffMember=request.form.get("provisioningUser"),
      form_id = form_id,
      date=date,)
    
    print(prov_form)
    db.session.add(prov_form)
    db.session.commit()

    return redirect(url_for('index'))
  return render_template("provisioning.html",form=form)


@app.route('/user/<int:form_id>' , methods=["GET","POST"])
def user(form_id):
  form = SignOffForms.query.get_or_404(form_id)
  if request.method=="POST":
    user_form=User(
      date=date,
      staffMember = request.form.get("username"),
      form_id=form_id
      )
    db.session.add(user_form)
    db.session.commit
    return redirect(url_for('index'))
      

  return render_template("user.html",form=form)