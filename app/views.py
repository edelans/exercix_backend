# -*- coding: utf-8 -*-
from flask import g, render_template, url_for, flash, redirect, send_from_directory, jsonify, request, Response
from app import app, User, db
from forms import *
from models import *
from utility import *
import json
import os
import datetime
from dateutil import parser
from operator import itemgetter
from mongoengine.queryset import Q
import simplejson
from functools import wraps

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'adminbook'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


def fetch_last_stats():
    stat = Stat.objects().order_by('-date').first()  #(to indicate a descending sort, i.e. highest first).
    return stat

@app.route('/test')
def test():
    docs = fetch_last_stats()
    rep_fil = docs["repartition_filiere"]
    l=[[str(x),rep_fil[x]] for x in rep_fil]
    return json.dumps(l) #

@app.route('/')
@app.route('/index')
@requires_auth
def index():
    stats = fetch_last_stats()
    rep_fil = stats["repartition_filiere"]
    l=[[str(x),rep_fil[x]] for x in rep_fil]
    # querying an empty database triggers a bug, so before doing it, we check:
    if len(Exo.objects)>0:
        operations_data =[{
            "content":"Statistiques du",
            "number":stats["date"].strftime('%d/%m/%Y')
        },
        {
            "content":"Nombre d'utilisateurs (adresses mail uniques)",
            "number":stats["nbusers"]
        }]
    else:
        operations_data = []

    return render_template("index.html",
        title           = 'Dashboard',
        date            = stats["date"].strftime('%d/%m/%Y'),
        nbusers         = stats["nbusers"],
        rep_fil         = l,
        prepas          = stats["prepas_users"])




@app.route('/users_evolution')
@requires_auth
def users_evolution():
    chartdata=[]
    stats = Stat.objects().order_by('-date')
    for stat in stats:
        chartdata.append([js_timestamp_from_datetime(stat["date"]), stat["nbusers"]])
    print chartdata
    return render_template("navigation/users_evolution.html",
        chartdata = chartdata)


@app.route('/prepa_users_evolution/<prep>')
def prepa_users_evolution(prep):
    print 'affichage de prep:'
    print prep
    chartdata=[]
    stats = Stat.objects().order_by('-date')
    for stat in stats:
        try:
            chartdata.append([js_timestamp_from_datetime(stat["date"]), stat["prepas_users"][prep]])
        except:
            pass
    return render_template("navigation/prepa_users_evolution.html",
        chartdata = chartdata,
        prepa=prep)



def give_list_of_parts():
    res=[]
    if len(Exo.objects)>0:
        partdic = Exo.objects.only('part').item_frequencies('part')
        res = partdic.items()
    return res


def give_list_of_chapters(part):
    res=[]
    if len(Exo.objects)>0:
        chapdic = Exo.objects(part=part).only('chapter').item_frequencies('chapter')
        res = chapdic.items()
    return res


def exo_stats(part, chapter):
    res = []
    exos = Exo.objects(Q(part=part) & Q(chapter=chapter)).only('id', 'part', 'chapter', 'number')
    for exo in exos:
        print exo.id
        exo_id=str(exo.id)
        dic={
            "exo_id":exo_id,
            "exo_nb": exo.number,
        }
        res.append(dic)
    return res


@app.route('/exercices')
@requires_auth
def exercices_l0():
    return render_template("navigation/exercices_level0.html",
        title = 'Exercices',
        parts = give_list_of_parts()
        )

@app.route('/exercices/<part>')
@requires_auth
def exercices_l1(part):
    return render_template("navigation/exercices_level1.html",
        title = 'Exercices',
        part = part,
        chapters = give_list_of_chapters(part)
        )

@app.route('/exercices/<part>/<chapter>')
@requires_auth
def exercices_l2(part, chapter):
    return render_template("navigation/exercices_level2.html",
        title = 'Exercices',
        part = part,
        chapter = chapter,
        exos = exo_stats(part, chapter)
        )




@app.route('/exo_id/<exo_id>', methods = ['GET', 'POST'])
@requires_auth
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
        return render_template("edition/exo_edit_content.html",
            title = 'Informations sur l\'exercice',
            exo_id = exo_id,
            exo_data = document,
            form =form
            )

    else: # en cas de presence vestiges de la phase d'initialisation de la bdd
        return render_template("errors/404.html")


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
@requires_auth
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



@app.route('/api/v1.0/request/<exo_id>', methods = ['GET'])
def API_request_exo(exo_id):
    document = Exo.objects(id=exo_id).first()# returns None if it doesn't exist
    output = {'error':'Not found'}
    if document is not None:
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

#function appelée par le bouton de génération du json
#attention, ne pas supprimer le decorateur pour que cela fonctionne
@app.route('/generatejson/', methods = ['GET'])
def generate_json():
    output = []
    exos = Exo.objects()
    for exo in exos:
        output.append({
            "_id":str(exo.id),
            "chapter":exo.chapter,
            "category":exo.part,
            "difficulty":exo.difficulty,
            "number":exo.number,
            "difficulty":exo.difficulty,
            "author":exo.author,
            "question":exo.question_html,
            "hint":exo.hint,
            "solution":exo.solution_html,
            "school":exo.school})

    #create a new file and write the list in it
    timestamp = datetime.datetime.now().strftime('%Y%m%d:%H%M%S')
    filename = 'data-' + str(timestamp) + '.json'
    #with open('tmp/'+ filename, 'w') as outfile:
    outfile=open('tmp/'+ filename, 'w')
    simplejson.dump(output, outfile)
    outfile.close()
    #return jsonify({"res":output})
    import os.path
    return send_from_directory(os.path.dirname(__file__) + '/../tmp/', filename, as_attachment=True)