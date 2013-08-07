# -*- coding: utf-8 -*-
from flask import Flask, g
from couchdb.design import ViewDefinition
import flaskext.couchdb


app = Flask(__name__)
app.config.from_object('config')


"""
CouchDB permanent view
"""
number_by_chapter = ViewDefinition('test', 'number_by_chapter', '''\
    function (doc) {
        if(doc.doc_type == 'exo') {
            emit( doc.chapter, doc.number);
        }
    }''')

#returns a list of parts (key) with the number of chapters they contains (value)
list_of_parts = ViewDefinition('test', 'list_of_parts', '''\
	function(doc) {
	  if(doc.doc_type == 'exo') {
	    emit(doc.chapter, 1);
	  }
	}''', '''\
	function(keys, values) {
	   return sum(values);
	}
	''', group=True)


#flask-couchdb :
manager = flaskext.couchdb.CouchDBManager() #ajouter l'option auto_sync=False ?
manager.add_viewdef(number_by_chapter, list_of_parts)  # Install the views
manager.setup(app)
manager.sync(app)

# attention: important de laisser a la fin :
from app import views, models
