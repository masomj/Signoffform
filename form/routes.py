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
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

date=datetime.now()

engine = db
db_session = scoped_session(sessionmaker(autocommit=False,
autoflush=False,
bind=engine))

Base = declarative_base()
Base.query = db_session.query_property


from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError
# ldap server hostname and port
ldsp_server = f""
# ldap server hostname and port
ldsp_server = f"ldap://localhost:389"


















def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import form.models
    Base.metadata.create_all(bind=engine)

with app.app_context():
    db.create_all()
    db.session.commit()

#pagination
def get_open_forms(offset=0, per_page=20):
  signoffs = list(SignOffForms.query.order_by(SignOffForms.id).all())
  forms=[]
  for record in  signoffs:
        if (record.closed == None):
          forms.append(record)
  return forms[offset: offset+per_page]

def get_closed_forms(offset=0, per_page=20):
  signoffs = list(SignOffForms.query.order_by(SignOffForms.id).all())
  forms=[]
  for record in  signoffs:
        if (record.closed == True):
          forms.append(record)
  return forms[offset: offset+per_page]


@app.route('/')
def index():
  page, per_page,offset = get_page_args(page_parameter="page",per_page_parameter="per_page")
  forms = list(SignOffForms.query.filter_by(closed=None).all())
  total = len(forms)
  pagination_forms= get_open_forms(offset=offset,per_page=per_page)
  pagination = Pagination(page=page, per_page=per_page,total=total,css_framework='bootstrap5')
  provForms = list(Provisioning.query.order_by(Provisioning.id).all())
  userForms = list(User.query.order_by(User.id).all())
  desktopForms = list(Desktop.query.order_by(Desktop.id).all())
  return render_template('allform.html', provForms=provForms,userForms=userForms,desktopForms=desktopForms, forms = pagination_forms,page=page, per_page = per_page, pagination = pagination)

@app.route('/closed')
def closed():
  page, per_page,offset = get_page_args(page_parameter="page",per_page_parameter="per_page")
  forms = list(SignOffForms.query.filter_by(closed=True).all())
  total = len(forms)
  pagination_forms= get_closed_forms(offset=offset,per_page=per_page)
  pagination = Pagination(page=page, per_page=per_page,total=total,css_framework='bootstrap5')
  provForms = list(Provisioning.query.order_by(Provisioning.id).all())
  userForms = list(User.query.order_by(User.id).all())
  desktopForms = list(Desktop.query.order_by(Desktop.id).all())
    
  return render_template('closed.html', provForms=provForms,userForms=userForms,desktopForms=desktopForms, forms = pagination_forms,page=page, per_page = per_page, pagination = pagination)

@app.route('/search', methods=['GET','POST'])
def search():
  if request.method == 'POST':
    id = request.form.get('search')
    form = SignOffForms.query.get_or_404(id)
    print(form.id)
    render_template('results.html', form=form) 
  return render_template('results.html', form=form)

@app.route('/close/<int:form_id>')
def close(form_id):
  form = SignOffForms.query.get_or_404(form_id)
  form.closed = True
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/closeProv/<int:form_id>')
def closeProv(form_id):
  form = Provisioning.query.get_or_404(form_id)
  form.closed = True
  print(form_id)
  db.session.commit()
  print(Provisioning.query.get_or_404(form_id).closed)

  return redirect(url_for('index'))


@app.route('/closeDesk/<int:form_id>')
def closeDesk(form_id):
  print(form_id)
  form = Desktop.query.get_or_404(form_id)
  print(form.closed)
  form.closed = True
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/closeUser/<int:form_id>')
def closeUser(form_id):
  form = User.query.get_or_404(form_id)
  form.closed = True
  db.session.commit()
  return redirect(url_for('index'))


@app.route('/create_form', methods=['GET','POST'])
def create_form():
  new_form = SignOffForms()
  db.session.add(new_form)

  db.session.commit()
  id = int(new_form.id)
  new_prov = Provisioning(
    deviceModel="",
    serviceTag="",
    assetTag="",
    windowsUpdates=False,
    bitlocker=False,
    userSoftware=False,
    ADgroups=False,
    desktopIcons=False,
    vpnInstalled=False,
    hardwareChecked=False,
    staffMember="",
    form_id = id,
    date=date
  )
  form = SignOffForms.query.get_or_404(id)
  new_desk = Desktop(
      contactedUser = False,
      collectOldDevice = False,
      Onedrive = False,
      bitlockerPin = False,
      IPreservation = False,
      StaffMember="",
      date=date,
      form_id=id,
  )
  new_user = User(
      date=date,
      staffMember="",
      form_id=id
  )
  
  db.session.add(new_form)
  db.session.commit()
  db.session.add(new_prov)
  db.session.commit()
  db.session.add(new_desk)
  db.session.commit()
  db.session.add(new_user)
  

  form.prov_form_id = new_prov.id
  form.desktop_form_id = new_desk.id
  form.user_form_id = new_user.id
  db.session.commit()
  return redirect(url_for('index'))


@app.route("/editdesktop/<int:form_id>/<int:desktop_form_id>" ,methods=["GET","POST"])
def editdesktop(form_id, desktop_form_id):
  form = SignOffForms.query.get_or_404(form_id)
  desktop_form_data = Desktop.query.get_or_404(desktop_form_id)
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

    desktop_form_data.contactedUser = contuser
    desktop_form_data.collectOldDevice = collect
    desktop_form_data.Onedrive = onedrive
    desktop_form_data.bitlockerPin = bitlocker
    desktop_form_data.IPreservation = IPcheck
    desktop_form_data.StaffMember=request.form.get("desktopUser")

    db.session.commit()
    return redirect(url_for('index'))
  return render_template("editdesktop.html",form=form, desktop_form_data=desktop_form_data)


@app.route("/Editprovisioning/<int:form_id>/<int:prov_form_id>" ,methods=["GET","POST"])
def editprovisioning(form_id, prov_form_id):
  form = SignOffForms.query.get_or_404(form_id)
  provisioning_form = Provisioning.query.get_or_404(prov_form_id)
  winup = False
  bitlock = False
  soft = False
  ADgroups = False
  desktopIcons = False
  vpnInstalled = False
  hardwareChecked = False
  
  if request.method =="POST":
    if request.form.get("windowsUpdates") == "True":
        winup = True
    if request.form.get("bitlocker") == "True":
       bitlock = True
    if request.form.get("userSoftware") == "True":
      soft = True
    if request.form.get("ADgroups") == "True":
      ADgroups = True
    if request.form.get("desktopIcons") == "True":
      desktopIcons = True
    if request.form.get("vpnInstalled") == "True":
      vpnInstalled = True
    if request.form.get("hardwareCheck") == "True":
      hardwareChecked = True

   
    provisioning_form.deviceModel=request.form.get("deviceModel")
    provisioning_form.assetTag=request.form.get("assetTag")
    provisioning_form.serviceTag=request.form.get("serviceTag")
    provisioning_form.windowsUpdates=winup
    provisioning_form.bitlocker=bitlock
    provisioning_form.userSoftware = soft
    provisioning_form.ADgroups=ADgroups
    provisioning_form.desktopIcons=desktopIcons
    provisioning_form.vpnInstalled=vpnInstalled
    provisioning_form.hardwareChecked=hardwareChecked
    provisioning_form.staffMember=request.form.get("provisioningUser")
    provisioning_form.date=date
    db.session.commit()
    return redirect(url_for('index'))
  return render_template("editprovisioning.html",form=form, prov_form=provisioning_form)


@app.route('/edituser/<int:form_id>/<int:user_form_id>' ,methods=["GET","POST"])
def edituser(form_id, user_form_id):
  form = SignOffForms.query.get_or_404(form_id)
  user_form_data = User.query.get_or_404(user_form_id)
  if request.method == "POST":
    
    user_form_data.staffMember = request.form.get("username")
    db.session.commit()

    return redirect(url_for('index'))

  return render_template("EditUser.html",form=form, user_form_data=user_form_data)




  