# -*- coding: utf-8 -*-
from flask import Flask, g
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine


app = Flask(__name__)
app.config.from_object('config')

#Flask Debug-toolbar
toolbar = DebugToolbarExtension(app)

db = MongoEngine(app)

# attention: important de laisser a la fin :
from app import views, models
