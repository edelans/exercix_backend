import os
basedir = os.path.abspath(os.path.dirname(__file__))

#CSRF
#The CSRF_ENABLED setting activates the cross-site request forgery* prevention.
#In most cases you want to have this option enabled
#as it makes your app more secure.
CSRF_ENABLED = True
SECRET_KEY = 'N0m0reb00ks'

DEBUG = True
COUCHDB_SERVER = 'http://127.0.0.1:5984/'
COUCHDB_DATABASE = 'test'