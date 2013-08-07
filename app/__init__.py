# -*- coding: utf-8 -*-
from flask import Flask, g
from couchdb.design import ViewDefinition
import flaskext.couchdb


app = Flask(__name__)
app.config.from_object('config')


"""
CouchDB permanent view
"""
# used to compute the 'new_number' when creating a new exercise
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
	    emit(doc.part, 1);
	  }
	}''', '''\
	function(keys, values) {
	   return sum(values);
	}
	''', group=True)

#returns a list of chapters (key) 
list_of_chapters = ViewDefinition('test', 'list_of_chapters', '''\
	function(doc) {
	  if(doc.doc_type == 'exo') {
	    emit([doc.part, doc.chapter], 1);
	  }
	}''', '''\
	function(keys, values) {
	   return null;
	}
	''', group=True)

#returns a list of exos (key)
list_of_exos = ViewDefinition('test', 'list_of_exos', '''\
	function(doc) {
	  if(doc.doc_type == 'exo') {
	    emit([doc.part, doc.chapter, doc._id, doc.number], 1);
	  }
	}''', '''\
	function(keys, values) {
	   return null;
	}
	''', group=True)


list_of_viewcounts = ViewDefinition('test', 'list_of_viewcounts', '''\
	function(doc) {
	  if(doc.doc_type == 'view') {
	    emit(doc.exo_id, 1);
	  }
	}''', '''\
	function(keys, values) {
	   return sum(values);
	}
	''', group=True)

view_hist = ViewDefinition('test', 'list_of_viewcounts', '''\
	function(doc) {
	  if(doc.doc_type == 'view') {
	    emit([doc.timestamp, doc.exo_id], 1);
	  }
	}''')

list_of_flagcounts = ViewDefinition('test', 'list_of_flagcounts', '''\
	function(doc) {
	  if(doc.doc_type == 'flag') {
	    emit(doc.exo_id, 1);
	  }
	}''', '''\
	function(keys, values) {
	   return sum(values);
	}
	''', group=True)

list_of_requestcounts = ViewDefinition('test', 'list_of_requestcounts', '''\
	function(doc) {
	  if(doc.doc_type == 'request') {
	    emit(doc.exo_id, 1);
	  }
	}''', '''\
	function(keys, values) {
	   return sum(values);
	}
	''', group=True)

#flask-couchdb :
manager = flaskext.couchdb.CouchDBManager() #ajouter l'option auto_sync=False ?
manager.add_viewdef((number_by_chapter, list_of_parts, list_of_chapters, list_of_exos, list_of_viewcounts, list_of_flagcounts, list_of_requestcounts, view_hist))  # Install the views
manager.setup(app)
manager.sync(app)

# attention: important de laisser a la fin :
from app import views, models
