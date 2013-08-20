# -*- coding: utf-8 -*-
from flask import Flask, g
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required
import datetime
from flask_security.forms import *
from flask.ext.wtf import TextField, IntegerField, SelectField
from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore

app = Flask(__name__)
app.config.from_object('config')

#Flask Debug-toolbar
toolbar = DebugToolbarExtension(app)

db = MongoEngine(app)

class Role(db.Document, RoleMixin):
    name        = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
	doc_type         = 'user'
	first_name       = db.StringField()
	last_name        = db.StringField()
	prepa_name       = db.StringField()
	prepa_postalcode = db.IntField()
	prepa_track		 = db.StringField()
	signin_at        = db.DateTimeField(default=datetime.datetime.now)
#flask-security:
	email            = db.EmailField(max_length=255)
	password         = db.StringField(max_length=255)
	active           = db.BooleanField(default=True)
	roles            = db.ListField(db.ReferenceField(Role), default=[])
#flask-security options
	confirmed_at      = db.DateTimeField()
	last_login_at     = db.DateTimeField()
	current_login_at  = db.DateTimeField()
	last_login_ip     = db.StringField()
	current_login_ip  = db.StringField()
	login_count       = db.IntField()


class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
	first_name       = TextField('First Name', validators =[Required()])
	last_name        = TextField('Last Name', validators =[Required()])
	prepa_name       = TextField(id='prepa_name', validators =[Required()])
	prepa_postalcode = IntegerField(id='prepa_name', validators =[Required()])
	prepa_track      = SelectField(id='prepa_track', validators =[Required()], choices=[('MP', 'MP'), ('PC', 'PC'), ('PSI', 'PSI'), ('BCPST', 'BCPST'), ('TSI', 'TSI'), ('autre', 'autre')])



# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore, confirm_register_form=ExtendedConfirmRegisterForm)

"""
# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(email='edelans@gmail.com', password='password')
"""

# setup mail
mail = Mail(app)


# attention: important de laisser a la fin :
from app import views, models

