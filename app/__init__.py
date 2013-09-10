# -*- coding: utf-8 -*-
from flask import Flask, g
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine
import datetime
from flask.ext.wtf import TextField, IntegerField, SelectField



app = Flask(__name__)
app.config.from_object('config')

#Flask Debug-toolbar
toolbar = DebugToolbarExtension(app)

db = MongoEngine(app)


class User(db.Document):
	doc_type         = 'user'
	first_name       = db.StringField()
	last_name        = db.StringField()
	prepa_name       = db.StringField()
	prepa_postalcode = db.IntField()
	prepa_track		 = db.StringField()
	signin_at        = db.DateTimeField(default=datetime.datetime.now)


# setup mail
mail = Mail(app)


# attention: important de laisser a la fin :
from app import views, models

