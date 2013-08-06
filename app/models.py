from flaskext.couchdb import Document, TextField, ListField, IntegerField, BooleanField

ROLE_USER=0
ROLE_ADMIN=1



class User(Document):
    doc_type = 'user'
    nickname    = TextField()
    email       = TextField()
    admin       = BooleanField(default=False)
    prepa       = TextField()


class Exo(Document):
    doc_type = 'exo'
# id
    source      = TextField()
    author      = TextField()
    school      = TextField()
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


"""
class Count(Document):
    doc_type = 'count'
    id_exo      =
    id_user     =
    timestamp   = DateTimeField(default=datetime.datetime.now)
    action_type = #view / request / flag 
"""