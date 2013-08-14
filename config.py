import os
basedir = os.path.abspath(os.path.dirname(__file__))

#CSRF
#The CSRF_ENABLED setting activates the cross-site request forgery* prevention.
#In most cases you want to have this option enabled
#as it makes your app more secure.
CSRF_ENABLED = True
SECRET_KEY = 'N0m0reb00ks'

DEBUG = True

#flask debug toolbar:
DEBUG_TB_PANELS = [
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        # Add the MongoDB panel
        'flask.ext.mongoengine.panels.MongoDebugPanel']
DEBUG_TB_PROFILER_ENABLED = True

MONGODB_SETTINGS = {
        "db":"exercix",
        "host":"localhost",
        "port":27017
        }

"""
,
	"username":"backend",		# if auth needed by db
	"password":"N0m0reb00ks",	# if auth needed by db

"""


# flask-mail settings
MAIL_SERVER     = 'smtp.exercix.net'
MAIL_PORT       = 587
MAIL_USE_SSL    = True
MAIL_USERNAME   = 'postmaster@exercix.net'
MAIL_PASSWORD   = 'N0morebooks'


###############################################################################
#
# flask-security settings 
#
# see http://pythonhosted.org/Flask-Security/configuration.html
#
###############################################################################

# Core
#SECURITY_PASSWORD_HASH = sha512_crypt # a activer une fois que la page de login sera ok
#SECURITY_PASSWORD_SALT = ???? needed with SECURITY_PASSWORD_HASH other than plaintext
SECURITY_EMAIL_SENDER = postmaster@exercix.net

#Feature Flags
SECURITY_CONFIRMABLE  = True 
SECURITY_REGISTERABLE = True 
SECURITY_RECOVERABLE  = True 
SECURITY_TRACKABLE    = True
SECURITY_CHANGEABLE   = True 

# Email 
SECURITY_EMAIL_SUBJECT_REGISTER               = 'Bienvenue sur ExerciX !'
SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE        = 'Votre mot de passe a été modifié'
SECURITY_EMAIL_SUBJECT_PASSWORD_RESET         = 'Demande de changement de mot de passe'
SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = 'Votre mot de passe a été modifié'
SECURITY_EMAIL_SUBJECT_CONFIRM                = 'Merci de confirmer votre adresse mail'
