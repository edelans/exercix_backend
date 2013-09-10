# -*- coding: utf-8 -*-
from flask.ext.wtf import Form, Field, TextInput, TextField, BooleanField, IntegerField, TextAreaField, SelectField, FieldList
from flask.ext.wtf import Required, Length, Email

#Definition d'un field perso pour pouvoir traiter les listes de tags et de filières
class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []



class ExoEditForm(Form):
    # id -> attribué par le serveur
    source = TextField(id='source', label='Source', validators = [Required()])
    author = TextField(id='author', label='Auteur', validators = [Email(), Required()])
    school = TextField(id='school', label='Concours', validators = [Required()])

    tracks = TagListField(id='tracks', label='Filière'.decode('utf8'), validators = [Required()])
    part = TextField(id='part', label='Catégorie'.decode('utf8'), validators = [Required()])
    chapter = TextField(id='chapter', label='Chapitre', validators = [Required()])
    # number -> attribué par le serveur
    difficulty = SelectField(id='difficulty', label='Difficulté'.decode('utf8'), choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')], coerce=int)
    tags = TagListField(id='tags', label='Tags', validators = [Required()])

    question = TextAreaField(id='question', label='Enoncé'.decode('utf8'), validators = [Length(min = 0, max = 2500)])
    hint = TextAreaField(id='hint', label='Indice', validators = [Length(min = 0, max = 500)])
    solution = TextAreaField(id='solution', label='Correction', validators = [Length(min = 0, max = 5000)])
