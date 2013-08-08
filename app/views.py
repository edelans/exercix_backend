# -*- coding: utf-8 -*-
from flask import g, render_template, url_for, flash, redirect, send_from_directory
from app import app, number_by_chapter, list_of_parts, list_of_chapters, list_of_exos, list_of_viewcounts, list_of_flagcounts, list_of_requestcounts, view_hist
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

#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404


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



@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'edelans' } # placeholder fake user
    stat_exo_viewcount=view_stats(5)
    stat_exo_flagcount=flag_stats(5)

    sales_data = { #placeholder for sales figures
    'sales':5000,
    'subscription_count':1000
    }

    operations_data ={ #placeholder for operations figures
    'viewcount_peruser_perweek':5
    }

    return render_template("index.html",
        title = 'Dashboard',
        user = user,
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


def fetch_view_timestamps(exo_id, for_n_days=7, until_timestamp=datetime.datetime.now()):
    data=[] #recoit la liste des timestamps (str) des visites de exo_id sur les for_n_days derniers jours
    from_timestamp = str((datetime.datetime.now() - datetime.timedelta(days=for_n_days)))
    until_timestamp = str(until_timestamp + datetime.timedelta(days=1))
    for row in view_hist(g.couch)[[exo_id, from_timestamp]:[exo_id, until_timestamp[:10]]]:
        data.append(row.key[1])
    return data

def chart_view(exo_id, for_n_days=7, until_timestamp=datetime.datetime.now()):        
    data = [] #recoit la liste des timestamps tronqués (des str du type "2013-08-07") des visites de exo_id sur les for_n_days derniers jours
    data_input = fetch_view_timestamps(exo_id, for_n_days, until_timestamp)
    for elem in data_input:
        data.append(elem[:10])
    return [[1000.0*int(parser.parse(c).strftime('%s')),len(list(cs))] for c,cs in groupby(data)]

@app.route('/test')
def test():
    docs = chart_view("0933cf617dca479b816dc2ce906a8577")
    return json.dumps(docs)
    

@app.route('/exo_id/<exo_id>', methods = ['GET', 'POST'])
def exo_edit_content(exo_id):
    #log stats:
    view(exo_id, user_id)
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
        return render_template("exo_edit_content.html",
            title = 'Informations sur l\'exercice',
            exo_id = exo_id,
            exo_data = document,
            chart_data = chart_data(exo_id), #placeholder
            form =form
            )

    else: # on renvoit tous les placeholder 
        return render_template("exo_edit_content.html",
            title = 'Informations sur l\'exercice',
            exo_id = exo_id,
            exo_data = exo_data, #placeholder
            chart_data = chart_data(exo_id), #placeholder
            form =form
            )


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
        #placeholder: new_number a calculer en fonction du number du dernier exo du chapitre !
        
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




structure = {  #placeholder
    "parts":[
        {
            "part": "Algèbre",
            "chapters": 
            [
                {
                    "chapter":"Polynomes",
                    "exos":[
                        {
                            "exo_id":54,
                            "exo_nb": 74,
                            "viewcount":52,
                            "flagcount":63,
                            "requestcount":25
                        },
                        {
                            "exo_id":55,
                            "exo_nb": 1,
                            "viewcount":54,
                            "flagcount":2,
                            "requestcount":10
                        },
                        {
                            "exo_id":56,
                            "exo_nb": 25,
                            "viewcount":57,
                            "flagcount":47,
                            "requestcount":69
                        },
                        {
                            "exo_id":58,
                            "exo_nb": 12,
                            "viewcount":23,
                            "flagcount":45,
                            "requestcount":78
                        }
                    ]
                },
                {
                    "chapter":"Réduction",
                    "exos":[
                        {
                            "exo_id":54,
                            "exo_nb": 74,
                            "viewcount":52,
                            "flagcount":63,
                            "requestcount":25
                        },
                        {
                            "exo_id":55,
                            "exo_nb": 1,
                            "viewcount":54,
                            "flagcount":2,
                            "requestcount":10
                        },
                        {
                            "exo_id":56,
                            "exo_nb": 25,
                            "viewcount":57,
                            "flagcount":47,
                            "requestcount":69
                        },
                        {
                            "exo_id":58,
                            "exo_nb": 12,
                            "viewcount":23,
                            "flagcount":45,
                            "requestcount":78
                        }
                    ]
                }
            ]
        },
        {
            "part": "Analyse",
            "chapters": 
            [
                {
                    "chapter":"Topologie",
                    "exos":[
                        {
                            "exo_id":54,
                            "exo_nb": 74,
                            "viewcount":52,
                            "flagcount":63,
                            "requestcount":25
                        },
                        {
                            "exo_id":55,
                            "exo_nb": 1,
                            "viewcount":54,
                            "flagcount":2,
                            "requestcount":10
                        },
                        {
                            "exo_id":56,
                            "exo_nb": 25,
                            "viewcount":57,
                            "flagcount":47,
                            "requestcount":69
                        },
                        {
                            "exo_id":58,
                            "exo_nb": 12,
                            "viewcount":23,
                            "flagcount":45,
                            "requestcount":78
                        }
                    ]
                },
                {
                    "chapter":"Séries numériques",
                    "exos":[
                        {
                            "exo_id":54,
                            "exo_nb": 74,
                            "viewcount":52,
                            "flagcount":63,
                            "requestcount":25
                        },
                        {
                            "exo_id":55,
                            "exo_nb": 1,
                            "viewcount":54,
                            "flagcount":2,
                            "requestcount":10
                        },
                        {
                            "exo_id":56,
                            "exo_nb": 25,
                            "viewcount":57,
                            "flagcount":47,
                            "requestcount":69
                        },
                        {
                            "exo_id":58,
                            "exo_nb": 12,
                            "viewcount":23,
                            "flagcount":45,
                            "requestcount":78
                        }
                    ]
                }
            ]
        },
        {
            "part": "Géométrie",
            "chapters": 
            [
                {
                    "chapter":"Géométrie affine et métrique",
                    "exos":[
                        {
                            "exo_id":54,
                            "exo_nb": 74,
                            "viewcount":52,
                            "flagcount":63,
                            "requestcount":25
                        },
                        {
                            "exo_id":55,
                            "exo_nb": 1,
                            "viewcount":54,
                            "flagcount":2,
                            "requestcount":10
                        },
                        {
                            "exo_id":56,
                            "exo_nb": 25,
                            "viewcount":57,
                            "flagcount":47,
                            "requestcount":69
                        },
                        {
                            "exo_id":58,
                            "exo_nb": 12,
                            "viewcount":23,
                            "flagcount":45,
                            "requestcount":78
                        }
                    ]
                },
                {
                    "chapter":"Courbes paramétrées et coniques",
                    "exos":[
                        {
                            "exo_id":54,
                            "exo_nb": 74,
                            "viewcount":52,
                            "flagcount":63,
                            "requestcount":25
                        },
                        {
                            "exo_id":55,
                            "exo_nb": 1,
                            "viewcount":54,
                            "flagcount":2,
                            "requestcount":10
                        },
                        {
                            "exo_id":56,
                            "exo_nb": 25,
                            "viewcount":57,
                            "flagcount":47,
                            "requestcount":69
                        },
                        {
                            "exo_id":58,
                            "exo_nb": 12,
                            "viewcount":23,
                            "flagcount":45,
                            "requestcount":78
                        }
                    ]
                }
            ]
        }
    ]
}

question = """
    Soit $P \\in \\mathbb{R}[X]$ scindé sur $\\mathbb{R}$.
    \\begin{enumerate} 
    \\item Montrer que les racines multiples de $P'$ sont aussi racines de $P$. 
    \\item Montrer que $P'$ est aussi scindé sur $\\mathbb{R}$. 
    \\item Ce resultat reste-t-il valable dans $\\mathbb{C}[X]$ ? 
    \\end{enumerate}
    """
solution = """ 
    \\paragraph{1}
    $P \\in \\mathbb{R}[X]$ scindé sur $\\mathbb{R}$ $\\Rightarrow$ $\\exists \\gamma \\in \\mathbb{R}, q \\in \\mathbb{N}^{*}, \\alpha_{i \\in [1..q]} \\in (\\mathbb{N}^{*})^{q}$ \\ : \\\\ 
    \\[ P= \\gamma \\prod_{i=1}^{q} (X - X_{i})^{\\alpha_{i}}\\]
    avec $deg(P) = n \\ge 1$ et $deg(P') = n-1$.

    $X_{i}$ est racine de $P'$ d'ordre $(\\alpha_{i} - 1)$ (cours). Donc les racines multiples de $P'$ sont aussi racines de $P$. 

    \\paragraph{2}
    On procède en deux étapes:
    \\begin{itemize}
    \\item  Les $X_{i}$ sont racines de $P'$ avec une somme des ordres égale à : $\\sum_{i=1}^{q}(\\alpha_{i} - 1)=n-q$

    \\item On applique le théorème de Rolle à $P$ sur chaque $]X_{i},X_{i}+1[$ pour obtenir $q-1$ racines supplémentaires de $P'$.
    \\end{itemize}
    On a donc trouvé au total : $(n-q) + (q-1) = n-1 $ racines réelles de $P'$. Or $P'$ est de degré $n-1$. Donc $P'$ est scindé.\\\\

    \\paragraph{3}
    Si $P \\in \\mathbb{C}[X]$:
    Ce résultat n'est plus valable. Voici un contre exemple:
    $P(X) = (X-1)^{3} + 1$ est scindé dans $\\mathbb{C}$ mais n'admet pas comme racine $1$ qui est pourtant racine multiple de $P'=3(X-1)^{2}$.
    """


exo_data ={ #placeholder
    "id":465467,
    "source": "2006p3n7",
    "author": "edelans@gmail.com",
    "school": "Centrale",
    
    "tracks":["PC","MP","PSI"],
    "part": "Algebre",
    "chapter": "Polynômes",
    "number": 2,
    "difficulty": 1,
    "taglist": ["polynomes", "Théorême de Rolle", "Scindé à racines simples"],
    
    
    "viewcount": [1372250977555,1372269755320,1372269820641,1372695296476,1372695511747,1372790237555,1372837810944,1372841896217,1372841917849,1372842034236,1372842108128,1373437770238,1373445259453,1373445489926,1373445994814,1373445998759,1373450076093],
    "flagcount": [1372250977555, 1372250977555, 1372837810944,13728378109445,1373450076093,1373450076093],
    "paycount": "",
    "requestcount": [1372250977555, 1372250977555,1373450076093],
    
    
    "question": question,
    "hint": "Utiliser le théorème de Rolle",
    "solution": solution,

    "question_html": latex_to_html(question),
    "solution_html": latex_to_html(solution)
}




def chart_data(exo_id):
    data = { #placeholder
        "viewcount": chart_view(exo_id),
        "flagcount": hc_readify(exo_data["flagcount"],15),
        "requestcount": hc_readify(exo_data["requestcount"],15)
    }
    return data