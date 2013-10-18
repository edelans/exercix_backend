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

parts=["Algèbre", "Analyse", "Géométrie"]
chapters=["Structure, arithmétique, complexes","Polynômes","Espaces vectoriels, matrices, déterminants","Réduction","Espace préhilbertiens, espaces euclidiens""Espaces normés et Topologie","Fonctions d'une variable réelle","Suites réelles ou complexes","Intégration sur un intervalle quelconque","Intégrales à paramètre","Séries numériques","Séries defonctions","Séries entières","Séries de Fourier","Equations différentielles","Fonctions de plusieurs variables réelles","Géométrie du plan et de l'espace","Courbes et surfaces"]


class ExoEditForm(Form):
    # id -> attribué par le serveur
    appli      = SelectField(id='appli', label='Appli', choices=[('prepasc1', 'Sup'), ('prepasc2', 'Spé'.decode('utf8')), ('prepacom1', 'Prepa Eco 1ere année'.decode('utf8')), ('prepacom2', 'Prepa Eco 2ème année'.decode('utf8'))])
    source     = TextField(id='source', label='Source', validators = [Required()])
    author     = TextField(id='author', label='Auteur') # validators = [Email(), Required()] enlevé car pour les profs il est assigné automatiquement dans views -> on ne le demande ps dans le form.
    school     = TextField(id='school', label='Concours', validators = [Required()])
    package    = SelectField(id='package', label='Package', choices=[('lite', 'lite'), ('full', 'full'), ('bonus', 'bonus')])

    tracks     = TagListField(id='tracks', label='Filière'.decode('utf8'), validators = [Required()])
    part       = SelectField(id='part', label='Catégorie'.decode('utf8'), validators = [Required()], choices=[(x.decode('utf8'),x.decode('utf8')) for x in parts])
    chapter    = SelectField(id='chapter', label='Chapitre', validators = [Required()], choices=[(x.decode('utf8'),x.decode('utf8')) for x in chapters])
    # number -> attribué par le serveur
    difficulty = SelectField(id='difficulty', label='Difficulté'.decode('utf8'), choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')], coerce=int)
    tags       = TagListField(id='tags', label='Tags', validators = [Required()])

    question   = TextAreaField(id='question', label='Enoncé'.decode('utf8'), validators = [Length(min = 0, max = 2500)])
    hint       = TextAreaField(id='hint', label='Indice', validators = [Length(min = 0, max = 500)])
    solution   = TextAreaField(id='solution', label='Correction', validators = [Length(min = 0, max = 5000)])
