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