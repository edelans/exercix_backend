from app import db 
import datetime


class User(db.Document):
    doc_type    = 'user'
    nickname    = db.StringField()
    email       = db.StringField(primary_key=True)
    prepa       = db.StringField()
    signin_at   = db.DateTimeField(default=datetime.datetime.now)


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
    question        = db.StringField()
    question_html   = db.StringField()
    hint            = db.StringField()
    solution        = db.StringField()
    solution_html   = db.StringField()

class Flag(db.Document):
    doc_type    = 'flag'
    exo_id      = db.StringField()
    user_id     = db.StringField()
    timestamp   = db.DateTimeField(default=datetime.datetime.now)

class Request(db.Document):
    doc_type    = 'request'
    exo_id      = db.StringField()
    user_id     = db.StringField()
    timestamp   = db.DateTimeField(default=datetime.datetime.now)


class View(db.Document):
    doc_type    = 'view'
    exo_id      = db.StringField()
    user_id     = db.StringField()
    timestamp   = db.DateTimeField(default=datetime.datetime.now)


class Stat(db.Document):
    doc_type                = 'stat'
    timestamp               = db.DateTimeField(default=datetime.datetime.now)
    exos                    = db.IntField()
    users                   = db.IntField()
    active_users_L7D        = db.IntField()
    views_per_user_per_week = db.IntField()
    view_L7D                = db.IntField()
