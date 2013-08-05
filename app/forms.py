# -*- coding: utf-8 -*-
from flask.ext.wtf import Form, TextField, BooleanField, IntegerField, TextAreaField, SelectField
from flask.ext.wtf import Required, Length, Email

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class ExoEditForm(Form):
    # id -> attribué par le serveur
    source = TextField(id='source', label='Source', validators = [Required()])
    author = TextField(id='author', label='Auteur', validators = [Email(), Required()])
    school = TextField(id='school', label='Concours', validators = [Required()])


    track = TextField(id='track', label='Filière'.decode('utf8'), validators = [Required()])
    category = TextField(id='category', label='Catégorie'.decode('utf8'), validators = [Required()])
    chapter = TextField(id='chapter', label='Chapitre', validators = [Required()])
    # number -> attribué par le serveur
    difficulty = SelectField(id='difficulty', label='Difficulté'.decode('utf8'), choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')], coerce=int)
    taglist = TextField(id='taglist', label='Tags', validators = [Required()])


    question = TextAreaField(id='question', label='Enoncé'.decode('utf8'), validators = [Length(min = 0, max = 700)])
    hint = TextAreaField(id='hint', label='Indice', validators = [Length(min = 0, max = 280)])
    solution = TextAreaField(id='solution', label='Correction', validators = [Length(min = 0, max = 2800)])

class ExoEditQuestion(Form):
	question = TextAreaField(id='question', label='Enoncé'.decode('utf8'), default='', validators = [Length(min = 0, max = 700)])

class ExoEditHint(Form):
	hint = TextAreaField(id='hint', label='Indice', validators = [Length(min = 0, max = 280)])

class ExoEditSolution(Form):
	solution = TextAreaField(id='solution', label='Correction', validators = [Length(min = 0, max = 2800)])

class ExoEditTheme(Form):
    track = TextField(id='track', label='Filière'.decode('utf8'), validators = [Required()])
    category = TextField(id='category', label='Catégorie'.decode('utf8'), validators = [Required()])
    chapter = TextField(id='chapter', label='Chapitre', validators = [Required()])
    difficulty = SelectField(id='difficulty', label='Difficulté'.decode('utf8'), choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')], validators = [Required()])
    taglist = TextField(id='taglist', label='Tags', validators = [Required()])

    
class ExoEditId(Form):
    source = TextField(id='source', label='Source', validators = [Required()])
    author = TextField(id='author', label='Auteur', validators = [Email(), Required()])
    school = TextField(id='school', label='Concours', validators = [Required()])

   