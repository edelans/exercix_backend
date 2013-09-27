from app import db
import datetime
from mongoengine import CASCADE


class Exo(db.Document):
    doc_type = 'exo'
# id
    appli       = db.StringField() #prepasc1, prepasc2, prepacom1, prepacom2
    source      = db.StringField()
    author      = db.StringField()
    school      = db.StringField()
    created_at  = db.DateTimeField(default=datetime.datetime.now)
    package     = db.StringField() #lite, full or bonus
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
    exo                 = db.ReferenceField(Exo, dbref=True) #, reverse_delete_rule=CASCADE
    processed           = db.BooleanField()
    meta = {
        'collection': 'improver'
    }