import os
basedir = os.path.abspath(os.path.dirname(__file__))

#CSRF
#The CSRF_ENABLED setting activates the cross-site request forgery* prevention.
#In most cases you want to have this option enabled
#as it makes your app more secure.
CSRF_ENABLED = True
SECRET_KEY = 'N0m0reb00ks'


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
