from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/signoff"

db = SQLAlchemy(app)

from form import routes

app.run()

