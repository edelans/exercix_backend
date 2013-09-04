#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
DEBUG_TB_INTERCEPT_REDIRECTS = False

MONGODB_SETTINGS = {
        "db":"exercix",
        "host":"paulo.mongohq.com",
        "port":10068,
        "username":"edelans",       # if auth needed by db
        "password":"nobooks",   # if auth needed by db
        }

"""
,
	"username":"backend",		# if auth needed by db
	"password":"N0m0reb00ks",	# if auth needed by db

"""


# flask-mail settings
MAIL_SERVER     = 'smtp.exercix.net'
MAIL_PORT       = 587
MAIL_USE_SSL    = False
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
SECURITY_EMAIL_SENDER = 'postmaster@exercix.net'
SECURITY_FLASH_MESSAGES = False

#URL and Views
SECURITY_POST_LOGIN_VIEW    ='/'
SECURITY_POST_REGISTER_VIEW ='/post_register'
SECURITY_POST_CONFIRM_VIEW  ='/profile_confirmed'

#Feature Flags
SECURITY_CONFIRMABLE  = True 
SECURITY_REGISTERABLE = True 
SECURITY_RECOVERABLE  = True 
SECURITY_TRACKABLE    = False
SECURITY_CHANGEABLE   = True 

# Email 
SECURITY_EMAIL_SUBJECT_REGISTER               = 'Bienvenue sur ExerciX !'
SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE        = 'Votre mot de passe a été modifié'
SECURITY_EMAIL_SUBJECT_PASSWORD_RESET         = 'Demande de changement de mot de passe'
SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = 'Votre mot de passe a été modifié'
SECURITY_EMAIL_SUBJECT_CONFIRM                = 'Merci de confirmer votre adresse mail'

###############################################################################
#
# flask-social settings 
#
###############################################################################


SOCIAL_FACEBOOK = {
    'consumer_key': '508113522605459',
    'consumer_secret': 'a10f2475a7cd11626f9dacc797b899ec'
}