# -*- coding: utf-8 -*-
from flask import g, render_template, url_for, flash, redirect, send_from_directory
from app import app, number_by_chapter, list_of_parts, list_of_chapters, list_of_exos, list_of_viewcounts, list_of_flagcounts, list_of_requestcounts, view_hist, flag_hist, request_hist, list_of_viewcounts_per_user, list_of_users
from forms import *
from models import *
from utility import *
import json
import os
from uuid import uuid4
import datetime
from itertools import groupby
from dateutil import parser
from time import mktime

user_id = 'edelans'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data),'info')
        return redirect('/index')
    return render_template('login.html', 
        title = 'Sign In',
        form = form)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def view_stats(n):
    stats=[]
    for row in list_of_viewcounts(g.couch).rows:
        stats.append({'exo_id':row.key, 'viewcount':row.value})
    return sorted(stats, key= lambda stat: stat['viewcount'], reverse=True)[0:n]

def flag_stats(n):
    stats=[]
    for row in list_of_flagcounts(g.couch).rows:
        stats.append({'exo_id':row.key, 'flagcount':row.value})
    return sorted(stats, key= lambda stat: stat['flagcount'], reverse=True)[0:n]

def request_stats(n):
    stats=[]
    for row in list_of_requestcounts(g.couch).rows:
        stats.append({'exo_id':row.key, 'requestcount':row.value})
    return sorted(stats, key= lambda stat: stat['requestcount'], reverse=True)[0:n]

def how_many_exos():
    return len(list_of_exos(g.couch))


def how_many_views(for_n_days=7, until_timestamp=datetime.datetime.now()):
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    return len(view_hist(g.couch)[[" ", from_timestamp[:10]]:["ZZZZZZZZ", until_timestamp[:10]]])

def how_many_viewing_users(for_n_days=7, until_timestamp=datetime.datetime.now()):
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    return len(list_of_viewcounts_per_user(g.couch)[[" ", from_timestamp[:10]]:["ZZZZZZZZ", until_timestamp[:10]]])


def how_many_views_per_user(for_n_days=7, until_timestamp=datetime.datetime.now()):
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    output=0
    nb_users= len(list_of_viewcounts_per_user(g.couch)[[" ", from_timestamp[:10]]:["ZZZZZZZZ", until_timestamp[:10]]])
    if nb_users==0:
        return output
    else: 
        for row in list_of_viewcounts_per_user(g.couch)[[" ", from_timestamp[:10]]:["ZZZZZZZZ", until_timestamp[:10]]]:
            output+= row.value
        return output/nb_users


def how_many_new_users(for_n_days=7, until_timestamp=datetime.datetime.now()):
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    return len(list_of_users(g.couch)[from_timestamp[:10]:until_timestamp[:10]])

def how_many_users():
    return len(list_of_users(g.couch))



@app.route('/test')
def test():
    docs = how_many_users()
    return json.dumps(docs)


@app.route('/')
@app.route('/index')
def index():
    stat_exo_viewcount=view_stats(5)
    stat_exo_flagcount=flag_stats(5)

    sales_data = { #placeholder for sales figures
    'sales':5000,
    'subscription_count':1000
    }
                                                   
    operations_data =[{
            "content":"Nombre total d'exercices dans la base".decode('utf8'),
            "number": how_many_exos()
        },{
            "content":"Nombre d'utilisateurs enregistrés cette année".decode('utf8'),
            "number": how_many_users()
        },{
            "content":"Nombre d'utilisateurs actifs sur les 7 derniers jours".decode('utf8'),
            "number": how_many_viewing_users()
        },{ 
            "content":"Nombre d'exercices vus / utilisateur / semaine".decode('utf8'),   
            "number": how_many_views_per_user()
        },{
            "content":"Nombre de nouveaux utilisateurs sur la dernière semaine".decode('utf8'),
            "number": how_many_new_users()
        },{
            "content":"Nombre de vues sur la dernière semaine".decode('utf8'),
            "number": how_many_views()
        }]

    return render_template("index.html",
        title = 'Dashboard',
        stat_exo_viewcount= stat_exo_viewcount,
        stat_exo_flagcount = stat_exo_flagcount,
        sales_data= sales_data,
        operations_data=operations_data)

def view_count(exo_id):
    views=0
    for row in list_of_viewcounts(g.couch)[exo_id]:
        views = row.value
    return views

def flag_count(exo_id):
    flags=0
    for row in list_of_flagcounts(g.couch)[exo_id]:
        flags = row.value
    return flags

def request_count(exo_id):
    requests=0
    for row in list_of_requestcounts(g.couch)[exo_id]:
        requests = row.value
    return requests


def give_list_of_parts():
    parts = []
    for row in list_of_parts(g.couch)['a':'z']:
        parts.append((row.key, row.value))
    return parts

def give_list_of_chapters(part):
    chapters = []
    for row in list_of_chapters(g.couch):
        if row.key[0]==part:
            chapters.append(row.key)
    return chapters

def give_list_of_exos(part, chapter):
    exos = []
    for row in list_of_exos(g.couch):
        if row.key[0]==part and row.key[1]==chapter:
            exos.append(row.key)
    return exos # de la forme [[pars, chapter, exo_id, exo_nb],...]



def exo_stats(part, chapter):
    res = []
    exos = give_list_of_exos(part, chapter)
    for exo in exos:
        dic={
            "exo_id":exo[2],
            "exo_nb": exo[3],
            "viewcount":view_count(exo[2]),
            "flagcount":flag_count(exo[2]),
            "requestcount":request_count(exo[2])
        }
        res.append(dic)
    return res







@app.route('/exercices')
def exercices_l0():
    return render_template("exercices_level0.html",
        title = 'Exercices',
        parts = give_list_of_parts()
        )

@app.route('/exercices/<part>')
def exercices_l1(part):
    return render_template("exercices_level1.html",
        title = 'Exercices',
        part = part,
        chapters = give_list_of_chapters(part),
        )

@app.route('/exercices/<part>/<chapter>')
def exercices_l2(part, chapter):
    return render_template("exercices_level2.html",
        title = 'Exercices',
        part = part,  
        chapter = chapter,
        exos = exo_stats(part, chapter)
        )


def fetch_view_timestamps(exo_id, for_n_days=15, until_timestamp=datetime.datetime.now()):
    data=[] 
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    for row in view_hist(g.couch)[[exo_id, from_timestamp[:10]]:[exo_id, until_timestamp[:10]]]:
        data.append(row.key[1])
    return data  #liste des timestamps (str) des visites de exo_id sur les for_n_days derniers jours

def fetch_flag_timestamps(exo_id, for_n_days=15, until_timestamp=datetime.datetime.now()):
    data=[] #recoit la liste des timestamps (str) des visites de exo_id sur les for_n_days derniers jours
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    for row in flag_hist(g.couch)[[exo_id, from_timestamp[:10]]:[exo_id, until_timestamp[:10]]]:
        data.append(row.key[1])
    return data

def fetch_request_timestamps(exo_id, for_n_days=15, until_timestamp=datetime.datetime.now()):
    data=[] #recoit la liste des timestamps (str) des visites de exo_id sur les for_n_days derniers jours
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    for row in request_hist(g.couch)[[exo_id, from_timestamp[:10]]:[exo_id, until_timestamp[:10]]]:
        data.append(row.key[1])
    return data

def chart_view(exo_id, for_n_days=15, until_timestamp=datetime.datetime.now()):        
    #recoit la liste des timestamps tronqués (des str du type "2013-08-07") des visites de exo_id sur les for_n_days derniers jours
    datadic = {}
    data_input = fetch_view_timestamps(exo_id, for_n_days, until_timestamp)

    # on construit un dictionnaire du type {"2013-08-07":compteur} avec tous les timestamps de la periode qu'on va tracer sur le graph, compteurs initialisés à 0
    for k in range(for_n_days):
        timestamp = str(until_timestamp-datetime.timedelta(days=k))[:10]
        datadic[timestamp]=0

    # on parcourt tous les timestamps sortis de la view et on incrémente les compteurs
    for elem in data_input:
        if elem[:10] in datadic:
            datadic[elem[:10]]+=1

    # on transforme le dico en liste, et on transforme les timestamps "2013-08-07" en millisec pour le javascript de highcharts
    output = [[1000.0*int(parser.parse(key).strftime('%s')) ,value] for key, value in datadic.iteritems()]

    # on trie par timestamp car le dico n'est pas ordonné 
    return sorted(output, key=lambda couple: couple[0])


def chart_data(fetch_timestamps_func, exo_id, for_n_days=15, until_timestamp=datetime.datetime.now()):        
    #recoit la liste des timestamps tronqués (des str du type "2013-08-07") des visites de exo_id sur les for_n_days derniers jours
    datadic = {}
    data_input = fetch_timestamps_func(exo_id, for_n_days, until_timestamp)

    # on construit un dictionnaire du type {"2013-08-07":compteur} avec tous les timestamps de la periode qu'on va tracer sur le graph, compteurs initialisés à 0
    for k in range(for_n_days):
        timestamp = str(until_timestamp-datetime.timedelta(days=k))[:10]
        datadic[timestamp]=0

    # on parcourt tous les timestamps sortis de la view et on incrémente les compteurs
    for elem in data_input:
        if elem[:10] in datadic:
            datadic[elem[:10]]+=1

    # on transforme le dico en liste, et on transforme les timestamps "2013-08-07" en millisec pour le javascript de highcharts
    output = [[1000.0*int(parser.parse(key).strftime('%s')) ,value] for key, value in datadic.iteritems()]

    # on trie par timestamp car le dico n'est pas ordonné 
    return sorted(output, key=lambda couple: couple[0])



    

@app.route('/exo_id/<exo_id>', methods = ['GET', 'POST'])
def exo_edit_content(exo_id):

    #try to log the document:
    document = g.couch.get(exo_id) # returns None if it doesn't exist

    # en cas de mise a jour de l'exo:
    form = ExoEditForm()
    if form.is_submitted():
        if form.validate():
            document['tracks']        = form.tracks.data
            document['part']          = form.part.data.capitalize()
            document['chapter']       = form.chapter.data.capitalize()
            document['difficulty']    = form.difficulty.data
            document['tags']          = form.tags.data
            document['source']        = form.source.data
            document['author']        = form.author.data
            document['school']        = form.school.data
            document['question']      = form.question.data
            document['question_html'] = latex_to_html(form.question.data)
            document['hint']          = form.hint.data
            document['solution']      = form.solution.data
            document['solution_html'] = latex_to_html(form.solution.data)
            g.couch.save(document)
            flash('Succes! L\'exercice a été mis à jour'.decode('utf8'),'success')
            return redirect(url_for('exo_edit_content', exo_id=exo_id))
        else:
            flash('ATTENTION! La mise à jour ne peut être effectuée car des données fournies sont invalides'.decode('utf8'),'error')


    # try retrieving the exo in the couchdb
    if document:
        #log stats:
        view(exo_id, user_id) # must be done after checking that doc exists, if not it will pollute the timestamps tables with exo_id that leads to nothing !
        return render_template("exo_edit_content.html",
            title = 'Informations sur l\'exercice',
            exo_id = exo_id,
            exo_data = document,
            chart_data = chart(exo_id),
            form =form
            )

    else: # en cas de presence vestiges de la phase d'initialisation de la bdd 
        redirect(url_for('page_not_found', e="cet exercice n'existe plus"))


def give_new_number(chapter):
    """
    todo:   - rendre plus robuste aux typos de chapitres
            - rendre plus robuste aux "trous" dans les noms: ici on ne fait qu'incrémenter
                la valeur la plus elevée, mais on ne remplira pas les trous !
    """
    numbers = [0]
    for row in number_by_chapter(g.couch)[chapter]:
        numbers.append(row.value)
    return sorted(numbers)[-1]+1


@app.route('/new_exo', methods = ['GET', 'POST'])
def new_exo():
    form = ExoEditForm()
    if form.validate_on_submit():
        new_number = give_new_number(form.chapter.data)
         
        #build object with posted values
        exo = Exo(source = form.source.data, 
            author = form.author.data,
            school = form.school.data,
            # theme
            chapter= form.chapter.data.capitalize(),
            part= form.part.data.capitalize(),
            number = new_number,
            difficulty = form.difficulty.data,
            tags = form.tags.data,
            tracks = form.tracks.data,
            # content
            question = form.question.data,
            question_html= latex_to_html(form.question.data),
            hint= form.hint.data,
            solution= form.solution.data,
            solution_html= latex_to_html(form.solution.data) )
        new_id = uuid4().hex
        exo.id = new_id
        
        # Insert into database
        try:
            exo.store()
            flash('Succes ! Le nouvel exercice a été entré dans la base'.decode('utf8'),'success')
            return redirect(url_for('exo_edit_content', exo_id=new_id))
        except Exception as e:
            flash('ATTENTION! Le nouvel exercice n\'a PAS été entré dans la base'.decode('utf8'),'error')
    return render_template('exo_edit_new.html', 
        title = 'Nouvel exo',
        form = form)



def chart(exo_id):
    data = {
        "viewcount": chart_data(fetch_view_timestamps, exo_id),
        "flagcount": chart_data(fetch_flag_timestamps, exo_id),
        "requestcount": chart_data(fetch_request_timestamps, exo_id)
    }
    return data