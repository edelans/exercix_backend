# -*- coding: utf-8 -*-
from flask import g, render_template, url_for, flash, redirect, send_from_directory, jsonify, request, Response
from app import app, User, db, LoginForm, RegistrationForm, login_manager
from forms import *
from models import *
from utility import *
import json
import os
import datetime
from mongoengine.queryset import Q
import simplejson
from functools import wraps

from flask.ext import login



#############################################################
#
#       Basic authentication to protect backend
#
#############################################################

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

def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated



#############################################################
#
#       misc
#
#############################################################

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404



#############################################################
#
#       routing
#
#############################################################

@app.route('/')
@app.route('/index')
@admin_only
def index():
    stats = fetch_last_stats()
    rep_fil = stats["repartition_filiere"]
    rep_os = stats["platform"]
    nbFlagsToProcess = Improver.objects(processed=False).count()
    nbFlagsTotal     = Improver.objects().count()
    proportionFlagsToProcess = int(100*nbFlagsToProcess/nbFlagsTotal)
    activeUsersL7D = stats["activeUsersL7D"]


    list_fil         =[[str(x),rep_fil[x]] for x in rep_fil]
    list_platform    = [['Android',sum(rep_os['android'].values())], ['iOS',sum(rep_os['ios'].values())]]
    list_ver_android = [[str(x).replace('p','.'),rep_os['android'][x]] for x in rep_os['android']]
    list_ver_ios     = [[str(x).replace('p','.'),rep_os['ios'][x]] for x in rep_os['ios']]
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
        nbviewsL7D      = stats["nbviewsL7D"],
        rep_fil         = list_fil,
        prepas          = stats["prepas_users"],
        rep_platforms   = list_platform,
        rep_android     = list_ver_android,
        rep_ios         = list_ver_ios,
        nbFlagsToProcess= nbFlagsToProcess,
        nbFlagsTotal    = nbFlagsTotal,
        proportionFlagsToProcess= proportionFlagsToProcess,
        activeUsersL7D  = activeUsersL7D)



@app.route('/users_evolution')
@admin_only
def users_evolution():
    chartdata=[]
    stats = Stat.objects().order_by('-date')
    for stat in stats:
        chartdata.append([js_timestamp_from_datetime(stat["date"]), stat["nbusers"]])
    print chartdata
    return render_template("navigation/users_evolution.html",
        chartdata = chartdata)



@app.route('/viewsL7D_evolution')
@admin_only
def viewsL7D_evolution():
    chartdata=[]
    stats = Stat.objects().order_by('-date')
    for stat in stats:
        if "nbviewsL7D" in stat:
            chartdata.append([js_timestamp_from_datetime(stat["date"]), stat["nbviewsL7D"]])
    return render_template("navigation/viewsL7D_evolution.html",
        chartdata = chartdata)



@app.route('/activeUsersL7D')
@admin_only
def activeUsersL7D():
    chartdata=[]
    stats = Stat.objects().order_by('-date')
    for stat in stats:
        if "activeUsersL7D" in stat:
            chartdata.append([js_timestamp_from_datetime(stat["date"]), stat["activeUsersL7D"]])
    return render_template("navigation/activeUsersL7D.html",
        chartdata = chartdata)



@app.route('/flags_to_process')
@admin_only
def flags_to_process():
    improvements = Improver.objects(processed=False).order_by('-date')
    return render_template("navigation/flags_to_process.html",
        improvements= improvements)



@app.route('/process_improvement/<improvement>')
#@admin_only pas de flag admin_only car aussi utilisé par authors !
def process_improvement(improvement):
    document = Improver.objects(id=improvement).first()
    document['processed'] = True
    document.save()
    return flags_to_process()



@app.route('/prepa_users_evolution/<prep>')
@admin_only
def prepa_users_evolution(prep):
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




@app.route('/exercices')
@admin_only
def exercices_l0():
    return render_template("navigation/exercices_level0.html",
        title = 'Exercices',
        parts = give_list_of_parts()
        )


#function appelée par le bouton de génération du json
#attention, ne pas supprimer le decorateur pour que cela fonctionne
@app.route('/generatejson/', methods = ['GET'])
@admin_only
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



@app.route('/exercices/<part>')
@admin_only
def exercices_l1(part):
    return render_template("navigation/exercices_level1.html",
        title = 'Exercices',
        part = part,
        chapters = give_list_of_chapters(part)
        )


@app.route('/exercices/<part>/<chapter>')
@admin_only
def exercices_l2(part, chapter):
    return render_template("navigation/exercices_level2.html",
        title = 'Exercices',
        part = part,
        chapter = chapter,
        exos = exo_stats(part, chapter)
        )


@app.route('/exo_id/<exo_id>', methods = ['GET', 'POST'])
@admin_only
def exo_edit_content(exo_id):
    document = Exo.objects(id=exo_id).first() #returns None if no result

    stats = fetch_last_stats()
    chartdata=[]
    try:
        chartdata=hc_readify(stats["views"][exo_id],100)
    except:
        pass

    improvements = Improver.objects(Q(processed=False) & Q(exo=document)).order_by('-date')

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
            document['appli']         = form.appli.data
            document['package']       = form.package.data
            document['author']        = form.author.data
            document['school']        = form.school.data
            document['question']      = form.question.data
            document['question_html'] = latex_to_html(form.question.data)
            document['hint']          = form.hint.data
            document['solution']      = form.solution.data
            document['solution_html'] = latex_to_html(form.solution.data)
            document.save()
            flash('Succes! L\'exercice a été mis à jour'.decode('utf8'),'success')
            return redirect(url_for('exo_edit_content', exo_id=exo_id, chartdata = chartdata, improvements=improvements))
        else:
            flash('ATTENTION! La mise à jour ne peut être effectuée car des données fournies sont invalides'.decode('utf8'),'error')


    # try retrieving the exo in the couchdb
    if document is not None:
        return render_template("edition/exo_edit_content.html",
            title = 'Informations sur l\'exercice',
            exo_id = exo_id,
            exo_data = document,
            form =form,
            chartdata = chartdata,
            improvements=improvements
            )

    else: # en cas de presence vestiges de la phase d'initialisation de la bdd
        return render_template("errors/404.html")


@app.route('/new_exo', methods = ['GET', 'POST'])
@admin_only
def new_exo():
    form = ExoEditForm()
    if form.validate_on_submit():
        new_number = give_new_number(form.chapter.data)
        #build object with posted values
        exo = Exo(
            source = form.source.data,
            appli = form.appli.data,
            package = form.package.data,
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




#############################################################
#
#       Configuration de l'API
#
#############################################################

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


#############################################################
#
#       test
#
#############################################################

@app.route('/test')
def test():
    docs = fetch_last_stats()
    return json.dumps(docs["platform"])



###############################################################################
#
#       interface profs
#
###############################################################################


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


@app.before_request
def before_request():
    g.user = login.current_user


@app.route('/auteur')
def auteur():
    if not (g.user and g.user.is_authenticated()):
        return redirect(url_for('login_view'))
    nbexos=Exo.objects(author=g.user.email).count()

    nbFlagsToProcess=0
    nbFlagsTotal=0
    improvers = Improver.objects()
    if len(improvers)>0:
        for imp in improvers:
            if imp.exo.author==g.user.email:
                nbFlagsTotal+=1
                if imp.processed==False:
                    nbFlagsToProcess+=1

    if nbFlagsTotal != 0:
        proportionFlagsToProcess=int(100*nbFlagsToProcess/nbFlagsTotal)
    else:
        proportionFlagsToProcess=0

    return render_template('authors/index.html',
        user=login.current_user,
        nbexos=nbexos,
        nbFlagsToProcess=nbFlagsToProcess,
        nbFlagsTotal=nbFlagsTotal,
        proportionFlagsToProcess=proportionFlagsToProcess
        )


@app.route('/login/', methods=('GET', 'POST'))
def login_view():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.get_user()
        login.login_user(user)
        return redirect(url_for('auteur'))

    return render_template('authors/login_form.html', form=form)


@app.route('/register/', methods=('GET', 'POST'))
def register_view():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()

        form.populate_obj(user)
        user.save()

        login.login_user(user)
        return redirect(url_for('auteur'))

    return render_template('authors/register_form.html', form=form)



@app.route('/logout/')
def logout_view():
    login.logout_user()
    return redirect(url_for('auteur'))


@app.route('/authors/new_exo', methods = ['GET', 'POST'])
@login.login_required
def authors_new_exo():
    form = ExoEditForm()
    if form.validate_on_submit():
        new_number = give_new_number(form.chapter.data)
        #build object with posted values
        exo = Exo(
            source        = form.source.data,
            appli        = form.appli.data,
            package        = form.package.data,
            author        = g.user.email,
            school        = form.school.data,
            # theme
            chapter       = form.chapter.data.capitalize(),
            part          = form.part.data.capitalize(),
            number        = new_number,
            difficulty    = form.difficulty.data,
            tags          = form.tags.data,
            tracks        = form.tracks.data,
            # content
            question      = form.question.data,
            question_html = latex_to_html(form.question.data),
            hint          = form.hint.data,
            solution      = form.solution.data,
            solution_html = latex_to_html(form.solution.data))

        # Insert into database
        try:
            exo.save()
            flash('Succes ! Le nouvel exercice a été entré dans la base'.decode('utf8'),'success')
            try:
                return redirect(url_for('authors_exo_edit_content', exo_id=exo.id))
            except:
                flash("ATTENTION! Le nouvel exercice a bien été entré dans la base mais il n'a pas été possible d'y acceder".decode('utf8'),'error')
                return render_template('authors/exo_edit_new.html',
                    title = 'Nouvel exo',
                    form = form)
        except Exception as e:
            flash('ATTENTION! Le nouvel exercice n\'a PAS été entré dans la base'.decode('utf8'),'error')
    return render_template('authors/exo_edit_new.html',
        title = 'Nouvel exo',
        form = form)



@app.route('/authors/flags_to_process')
@login.login_required
def authors_flags_to_process():
    improvements= []

    imp        = Improver.objects(processed=False)
    for i in imp:
        if i.exo.author == g.user.email:
            improvements.append(i)

    return render_template("authors/flags_to_process.html",
        improvements= improvements)


@app.route('/authors/process_improvement/<improvement>')
@login.login_required
def authors_process_improvement(improvement):
    document = Improver.objects(id=improvement).first()
    document['processed'] = True
    document.save()
    return authors_flags_to_process()


@app.route('/authors/exercices')
@login.login_required
def authors_exercices_l0():
    return render_template("authors/exercices_level0.html",
        title = 'Exercices',
        parts = authors_give_list_of_parts(g.user.email)
        )


@app.route('/authors/exercices/<part>')
@login.login_required
def authors_exercices_l1(part):
    return render_template("authors/exercices_level1.html",
        title = 'Exercices',
        part = part,
        chapters = authors_give_list_of_chapters(g.user.email, part)
        )


@app.route('/authors/exercices/<part>/<chapter>')
@login.login_required
def authors_exercices_l2(part, chapter):
    return render_template("authors/exercices_level2.html",
        title = 'Exercices',
        part = part,
        chapter = chapter,
        exos = authors_exo_stats(g.user.email, part, chapter)
        )


@app.route('/authors/exo_id/<exo_id>', methods = ['GET', 'POST'])
@login.login_required
def authors_exo_edit_content(exo_id):
    document = Exo.objects(id=exo_id).first() #returns None if no result

    stats = fetch_last_stats()
    chartdata=[]
    try:
        chartdata=hc_readify(stats["views"][exo_id],100)
    except:
        pass

    improvements = Improver.objects(Q(processed=False) & Q(exo=document)).order_by('-date')
    print 'improvements:'
    print str(improvements)
    print 'document: '
    print str(document)
    print '-'*80
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
            document['appli']        = form.appli.data
            document['package']        = form.package.data
            document['author']        = g.user.email
            document['school']        = form.school.data
            document['question']      = form.question.data
            document['question_html'] = latex_to_html(form.question.data)
            document['hint']          = form.hint.data
            document['solution']      = form.solution.data
            document['solution_html'] = latex_to_html(form.solution.data)
            document.save()
            flash('Succes! L\'exercice a été mis à jour'.decode('utf8'),'success')
            return redirect(url_for('authors_exo_edit_content', exo_id=exo_id, chartdata = chartdata, improvements=improvements))
        else:
            flash('ATTENTION! La mise à jour ne peut être effectuée car des données fournies sont invalides'.decode('utf8'),'error')


    # try retrieving the exo in the couchdb
    if document is not None:
        return render_template("authors/exo_edit_content.html",
            title = 'Informations sur l\'exercice',
            exo_id = exo_id,
            exo_data = document,
            form =form,
            chartdata = chartdata,
            improvements=improvements
            )

    else: # en cas de presence vestiges de la phase d'initialisation de la bdd
        return render_template("errors/404.html")
