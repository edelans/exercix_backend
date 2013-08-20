# -*- coding: utf-8 -*-
from flask import g, render_template, url_for, flash, redirect, send_from_directory, jsonify
from app import app, User, Role, social
from forms import *
from models import *
from utility import *
import json
import os
from uuid import uuid4
import datetime
from dateutil import parser
from operator import itemgetter
from mongoengine.queryset import Q
from flask.ext.security import Security, login_required


user_id = 'edelansgmail.com' #attention, present ds multiples endroits du fichier, placeholder à traiter... g.user ?




@app.route('/profile')
@login_required
def profile():
    return render_template(
        'social/profile.html',
        content='Profile Page',
        facebook_conn=social.facebook.get_connection())


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


def view_stats(n):
    # get a dictionary of the frequencies of items {"exo_id":frequence}
    stats = []
    if len(View.objects)>0:
        view_freqs = View.objects.item_frequencies('exo_id') 
        top_viewed = sorted(view_freqs.items(), key=itemgetter(1), reverse=True)[:n]
        for pair in top_viewed:
            stats.append({'exo_id':pair[0], 'viewcount':pair[1]})
    return stats


def flag_stats(n):
    stats = []
    if len(Flag.objects)>0:
        # get a dictionary of the frequencies of items {"exo_id":frequence}
        flag_freqs = Flag.objects.item_frequencies('exo_id') 
        top_viewed = sorted(flag_freqs.items(), key=itemgetter(1), reverse=True)[:n]
        for pair in top_viewed:
            stats.append({'exo_id':pair[0], 'flagcount':pair[1]})
    return stats


def request_stats(n):
    stats = []
    if len(Request.objects)>0:
        # get a dictionary of the frequencies of items {"exo_id":frequence}
        request_freqs = Request.objects.item_frequencies('exo_id') 
        top_viewed = sorted(request_freqs.items(), key=itemgetter(1), reverse=True)[:n]
        for pair in top_viewed:
            stats.append({'exo_id':pair[0], 'requestcount':pair[1]})
    return stats


def how_many_exos():
    return len(Exo.objects)


def how_many_views(for_n_days=7, until_timestamp=datetime.datetime.now()):
    from_timestamp = str(datetime.datetime.now() - datetime.timedelta(days=for_n_days))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    return len(View.objects(Q(timestamp__gte=from_timestamp) & Q(timestamp__lte=until_timestamp)))


def how_many_viewing_users(for_n_days=7, until_timestamp=datetime.datetime.now()):
    #define timeframe
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    # filter View to fit timeframe, and then build a dictionary of the frequencies of items {"user_id":frequence}
    if len(View.objects)>0:
        view_freqs = View.objects(Q(timestamp__gte=from_timestamp ) & Q(timestamp__lte=until_timestamp)).item_frequencies('user_id')
    # return length of the dico
    return len(view_freqs)


def how_many_views_per_user(for_n_days=7, until_timestamp=datetime.datetime.now()):
    #define timeframe
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    # filter View to fit timeframe, and then build a dictionary of the frequencies of items {"user_id":frequence}
    view_freqs = View.objects(Q(timestamp__gte=from_timestamp ) & Q(timestamp__lte=until_timestamp)).item_frequencies('user_id')
    
    # compute average of frequencies
    output=0
    if len(view_freqs)>0:
        output = float(sum(view_freqs.values()))/len(view_freqs)

    return output


def how_many_new_users(for_n_days=7, until_timestamp=datetime.datetime.now()):
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    if len(User.objects)>0:
        return len(User.objects(Q(signin_at__gte=from_timestamp ) & Q(signin_at__lte=until_timestamp)))
    else:
        return 0

def how_many_users():
    if len(User.objects)>0:
        return len(User.objects)
    else:
        return 0


@app.route('/post_register')
def post_register():
    return render_template('security/post_register.html')

@app.route('/profile_confirmed')
def profile_confirmed():
    return render_template('security/profile_confirmed.html')

@app.route('/CGU')
def CGU():
    return render_template('legal/CGU.html')

@app.route('/')
@app.route('/index')
@login_required
def index():
    stat_exo_viewcount=view_stats(10)
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
    return len(View.objects(exo_id=str(exo_id)))

@app.route('/test')
def test():
    docs = exo_stats("Algebre", "Polynomes")
    return json.dumps(docs)


def flag_count(exo_id):
    return len(Flag.objects(exo_id=str(exo_id)))

def request_count(exo_id):
    return len(Request.objects(exo_id=str(exo_id)))


def give_list_of_parts():
    partdic = Exo.objects.only('part').item_frequencies('part')
    return partdic.items()

def give_list_of_chapters(part):
    chapdic = Exo.objects(part=part).only('chapter').item_frequencies('chapter')
    return chapdic.items()




def exo_stats(part, chapter):
    res = []
    exos = Exo.objects(Q(part=part) & Q(chapter=chapter)).only('id', 'part', 'chapter', 'number')
    for exo in exos:
        print exo.id
        exo_id=str(exo.id)
        dic={
            "exo_id":exo_id,
            "exo_nb": exo.number,
            "viewcount":view_count(exo_id),
            "flagcount":flag_count(exo_id),
            "requestcount":request_count(exo_id)
        }
        res.append(dic)
    return res







@app.route('/exercices')
def exercices_l0():
    return render_template("navigation/exercices_level0.html",
        title = 'Exercices',
        parts = give_list_of_parts()
        )

@app.route('/exercices/<part>')
def exercices_l1(part):
    return render_template("navigation/exercices_level1.html",
        title = 'Exercices',
        part = part,
        chapters = give_list_of_chapters(part),
        )

@app.route('/exercices/<part>/<chapter>')
def exercices_l2(part, chapter):
    return render_template("navigation/exercices_level2.html",
        title = 'Exercices',
        part = part,  
        chapter = chapter,
        exos = exo_stats(part, chapter)
        )



def fetch_view_timestamps(exo_id, for_n_days=15, until_timestamp=datetime.datetime.now()):
    data=[] 
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    views = View.objects(Q(exo_id = exo_id) & Q(timestamp__gte=from_timestamp ) & Q(timestamp__lte=until_timestamp))
    for view in views:
        data.append(view.timestamp)
    return data  #liste des timestamps (str) des visites de exo_id sur les for_n_days derniers jours

def fetch_flag_timestamps(exo_id, for_n_days=15, until_timestamp=datetime.datetime.now()):
    data=[] #recoit la liste des timestamps (str) des visites de exo_id sur les for_n_days derniers jours
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    flags = Flag.objects(Q(exo_id = exo_id) & Q(timestamp__gte=from_timestamp ) & Q(timestamp__lte=until_timestamp))
    for flag in flags:
        data.append(flag.timestamp)
    return data

def fetch_request_timestamps(exo_id, for_n_days=15, until_timestamp=datetime.datetime.now()):
    data=[] #recoit la liste des timestamps (str) des visites de exo_id sur les for_n_days derniers jours
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    requests = Request.objects(Q(exo_id = exo_id) & Q(timestamp__gte=from_timestamp ) & Q(timestamp__lte=until_timestamp))
    for request in requests:
        data.append(request.timestamp)
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
        elem = str(elem)
        if elem[:10] in datadic:
            datadic[elem[:10]]+=1

    # on transforme le dico en liste, et on transforme les timestamps "2013-08-07" en millisec pour le javascript de highcharts
    output = [[1000.0*int(parser.parse(key).strftime('%s')) ,value] for key, value in datadic.iteritems()]

    # on trie par timestamp car le dico n'est pas ordonné 
    return sorted(output, key=lambda couple: couple[0])



    

@app.route('/exo_id/<exo_id>', methods = ['GET', 'POST'])
def exo_edit_content(exo_id):
    document = Exo.objects(id=exo_id).first() #returns None if no result  

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
            document.save()
            flash('Succes! L\'exercice a été mis à jour'.decode('utf8'),'success')
            return redirect(url_for('exo_edit_content', exo_id=exo_id))
        else:
            flash('ATTENTION! La mise à jour ne peut être effectuée car des données fournies sont invalides'.decode('utf8'),'error')


    # try retrieving the exo in the couchdb
    if document is not None:
        #log stats:
        view(exo_id, user_id) # must be done after checking that doc exists, if not it will pollute the timestamps tables with exo_id that leads to nothing !
        return render_template("edition/exo_edit_content.html",
            title = 'Informations sur l\'exercice',
            exo_id = exo_id,
            exo_data = document,
            chart_data = chart(exo_id),
            form =form
            )

    else: # en cas de presence vestiges de la phase d'initialisation de la bdd 
        abort(404)


def give_new_number(chapter):
    """
    todo:   - rendre plus robuste aux typos de chapitres -> doit etre fait en amont (le form ne doit accepter que les "bons" chapters)
            - rendre plus robuste aux "trous" dans les noms: ici on ne fait qu'incrémenter
                la valeur la plus elevée, mais on ne remplira pas les trous !
    """
    numbers = [0]
    exos = Exo.objects(chapter=chapter).only('number')
    for exo in exos:
        numbers.append(exo.number)
    return sorted(numbers)[-1]+1


@app.route('/new_exo', methods = ['GET', 'POST'])
def new_exo():
    form = ExoEditForm()
    if form.validate_on_submit():
        new_number = give_new_number(form.chapter.data)
        #build object with posted values
        exo = Exo(
            source = form.source.data, 
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
            solution_html= latex_to_html(form.solution.data))
        
        # Insert into database
        try:
            exo.save()
            flash('Succes ! Le nouvel exercice a été entré dans la base'.decode('utf8'),'success')
            try:
                return redirect(url_for('exo_edit_content', exo_id=exo.id))
            except:
                flash("ATTENTION! Le nouvel exercice a bien été entré dans la base mais il n'a pas été possible d'y acceder".decode('utf8'),'error')
                return render_template('edition/exo_edit_new.html', 
                    title = 'Nouvel exo',
                    form = form)
        except Exception as e:
            flash('ATTENTION! Le nouvel exercice n\'a PAS été entré dans la base'.decode('utf8'),'error')
    return render_template('edition/exo_edit_new.html', 
        title = 'Nouvel exo',
        form = form)



def chart(exo_id):
    data = {
        "viewcount": chart_data(fetch_view_timestamps, exo_id),
        "flagcount": chart_data(fetch_flag_timestamps, exo_id),
        "requestcount": chart_data(fetch_request_timestamps, exo_id)
    }
    return data


@app.route('/logstats')
def logstats():
    stats = Stat(exos               = how_many_exos(), 
            users                   = how_many_users(),
            active_users_L7D        = how_many_viewing_users(),
            views_per_user_per_week = how_many_views_per_user(),
            view_L7D                = how_many_views())

    # Insert into database
    try:
        stats.save()
        state = True
    except Exception, e:
        state = False
    
    return json.dumps({'ok': state})

"""
----------------------------------------------------------
Configuration de l'API
----------------------------------------------------------
"""

@app.route('/api/v1.0/view/<exo_id>', methods = ['GET'])
def API_get_exo(exo_id):
    document = Exo.objects(id=exo_id).first() # returns None if it doesn't exist
    output = {'error':'Not found'}
    if document is not None:          
        #log stats:
        view(exo_id, user_id) # must be done after checking that doc exists, if not it will pollute the timestamps tables with exo_id that leads to nothing !
        output = {"tracks"  : document.tracks,
            "part"          : document.part,
            "chapter"       : document.chapter,
            "number"        : document.number,
            "difficulty"    : document.difficulty,
            "tags"          : document.tags,
            "school"        : document.school, 
            "question_html" : document.question_html,
            "hint"          : document.hint,
            "solution_html" : document.solution_html}
    return jsonify(output)


@app.route('/api/v1.0/flag/<exo_id>', methods = ['GET'])
def API_flag_exo(exo_id):
    document = Exo.objects(id=exo_id).first()# returns None if it doesn't exist
    output = {'error':'Not found'}
    if document is not None:          
        #log stats:
        flag(exo_id, user_id) # must be done after checking that doc exists, if not it will pollute the timestamps tables with exo_id that leads to nothing !
        output = {"state"  : "flaged"}
    return jsonify(output)

@app.route('/api/v1.0/request/<exo_id>', methods = ['GET'])
def API_request_exo(exo_id):
    document = Exo.objects(id=exo_id).first()# returns None if it doesn't exist
    output = {'error':'Not found'}
    if document is not None:          
        #log stats:
        request(exo_id, user_id) # must be done after checking that doc exists, if not it will pollute the timestamps tables with exo_id that leads to nothing !
        output = {"state"  : "requested"}
    return jsonify(output)


@app.route('/api/v1.0/partslist', methods = ['GET'])
def API_list_of_parts():
    parts = give_list_of_parts() #list
    return jsonify({"parts":parts})


@app.route('/api/v1.0/chapterslist/<part>', methods = ['GET'])
def API_list_of_chapters(part):
    chapters = give_list_of_chapters(part) #list
    return jsonify({"chapters":chapters})


@app.route('/api/v1.0/exoslist/<part>/<chapter>/', methods = ['GET'])
@login_required
def API_list_of_exos(part,chapter):
    output = []
    exos = Exo.objects(Q(part=part) & Q(chapter=chapter)).only('id', 'part', 'chapter', 'number', 'difficulty', 'tags', 'tracks', 'school', 'question_html', 'hint', 'solution_html')
    for exo in exos:
        output.append({
            "part":exo.part,
            "chapter":exo.chapter,
            "number":exo.number,
            "difficulty":exo.difficulty,
            "tags":exo.tags,
            "tracks":exo.tracks,
            "school":exo.school,
            "question_html":exo.question_html,
            "hint":exo.hint,
            "solution_html":exo.solution_html
            })
    return jsonify({"exos":output})

