# -*- coding: utf-8 -*-
from flask import Flask, g
import flaskext.couchdb



app = Flask(__name__)
app.config.from_object('config')


"""
CouchDB permanent view

docs_by_author = ViewDefinition('docs', 'byauthor',
                                'function(doc) { emit(doc.author, doc); }')
"""

#flask-couchdb :
manager = flaskext.couchdb.CouchDBManager()
manager.setup(app)
#manager.add_viewdef(docs_by_author)  # Install the view
manager.sync(app)


# attention: important de laisser a la fin :
from app import views, models

