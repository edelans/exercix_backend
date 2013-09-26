from app import db
import datetime



class Exo(db.Document):
    doc_type = 'exo'
# id
    source      = db.StringField()
    author      = db.StringField()
    school      = db.StringField()
    created_at  = db.DateTimeField(default=datetime.datetime.now)
#theme
    chapter     = db.StringField()
    part        = db.StringField()
    number      = db.IntField()
    difficulty  = db.IntField()
    tags        = db.ListField(db.StringField(max_length=50))
    tracks      = db.ListField(db.StringField(max_length=50))
# content
    question        = db.StringField(max_length=2500)
    question_html   = db.StringField(max_length=2500)
    hint            = db.StringField(max_length=500)
    solution        = db.StringField(max_length=5000)
    solution_html   = db.StringField(max_length=5000)


class Exercix(db.DynamicDocument):
    doc_type   = 'exercix'
    mail       = db.StringField()
    nomprepa   = db.StringField()
    zipcode    = db.StringField()
    filiere    = db.StringField()
    data       = db.DictField()
    OS         = db.StringField()
    lastupdate = db.IntField()
    appversion = db.StringField()
    meta = {
        'collection': 'exercix'
    }

class Stat(db.Document):
    date                = db.DateTimeField()
    nbusers             = db.IntField()
    repartition_filiere = db.DictField()
    prepas_users        = db.DictField()
    platform            = db.DictField()
    views               = db.DictField()
    nbviewsL7D          = db.IntField()
    activeUsersL7D      = db.IntField()
    meta = {
        'collection': 'stats'
    }

class Improver(db.Document):
    date                = db.IntField()
    msg                 = db.StringField(max_length=2500)
    exoid               = db.StringField()
    processed           = db.BooleanField()
    meta = {
        'collection': 'improver'
    }