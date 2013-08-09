from flaskext.couchdb import Document, DateTimeField, TextField, ListField, IntegerField, BooleanField
import datetime

ROLE_USER=0
ROLE_ADMIN=1



class User(Document):
    doc_type = 'user'
    nickname    = TextField()
    email       = TextField()
    admin       = BooleanField(default=False)
    prepa       = TextField()
    signin_at   = DateTimeField(default=datetime.datetime.now)


class Exo(Document):
    doc_type = 'exo'
# id
    source      = TextField()
    author      = TextField()
    school      = TextField()
    created_at  = DateTimeField(default=datetime.datetime.now)
#theme
    chapter     = TextField()
    part        = TextField()
    number      = IntegerField()
    difficulty  = IntegerField()
    tags        = ListField(TextField())
    tracks      = ListField(TextField())
# content    
    question        = TextField()
    question_html   = TextField()
    hint            = TextField()
    solution        = TextField()
    solution_html   = TextField()

class Flag(Document):
    doc_type    = 'flag'
    exo_id      = TextField()
    user_id     = TextField()
    timestamp   = DateTimeField(default=datetime.datetime.now)

class Request(Document):
    doc_type    = 'request'
    exo_id      = TextField()
    user_id     = TextField()
    timestamp   = DateTimeField(default=datetime.datetime.now)


class View(Document):
    doc_type    = 'view'
    exo_id      = TextField()
    user_id     = TextField()
    timestamp   = DateTimeField(default=datetime.datetime.now)
