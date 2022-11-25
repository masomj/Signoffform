from flask import Flask
from form import app, db

from flask import Flask, render_template, request, redirect, url_for
from .forms import Provisioning, DesktopSupport, User
from form import app, db
from .models import Provisioning, User, Desktop, SignOffForms

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def index():
    
  return render_template('base.html')



@app.route('/desktop')
def desktop():
  form = DesktopSupport()
  if form.validate_on_submit():
    return redirect(url_for("success"))

  return render_template("desktop.html", form=form)

@app.route('/provisioning')
def provisiong():

  return render_template("provisioning.html")

@app.route('/user')
def user():

  return render_template("user.html")