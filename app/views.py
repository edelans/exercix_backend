# -*- coding: utf-8 -*-
from flask import render_template, url_for, flash, redirect, send_from_directory
from app import app, db
from forms import *
from models import *
from utility import *
import json
import os


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', 
        title = 'Sign In',
        form = form)


#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'edelans' } # placeholder fake user
    
    stat_exo_viewcount=[ #placeholder top 5 vues des exos
    {
    'exo_id': 4654,
    'viewcount': 45
    },
    {
    'exo_id': 78942,
    'viewcount': 32
    },
    {
    'exo_id': 721,
    'viewcount': 21
    }
    ]

    stat_exo_flagcount= [ #placeholder top 5 flag des exos
    {
    'exo_id': 1111,
    'flagcount': 45
    },
    {
    'exo_id': 22,
    'flagcount': 32
    },
    {
    'exo_id': 333333,
    'flagcount': 21
    }
    ]

    sales_data = { #placeholder for sales figures
    'sales':5000,
    'subscription_count':1000
    }

    operations_data ={ #placeholder for sales figures
    'viewcount_peruser_perweek':5
    }

    return render_template("index.html",
        title = 'Dashboard',
        user = user,
        stat_exo_viewcount= stat_exo_viewcount,
        stat_exo_flagcount = stat_exo_flagcount,
        sales_data= sales_data,
        operations_data=operations_data)



@app.route('/exercices')
def exercices_l0():
    return render_template("exercices_level0.html",
        title = 'Exercices',
        structure = structure
        )

@app.route('/exercices/<part>')
def exercices_l1(part):
    return render_template("exercices_level1.html",
        title = 'Exercices',
        structure = structure,
        part = part 
        )

@app.route('/exercices/<part>/<chapter>')
def exercices_l2(part, chapter):
    return render_template("exercices_level2.html",
        title = 'Exercices',
        structure = structure,
        part = part,  
        chapter = chapter
        )



@app.route('/exercices/<int:exo_id>')
def exo_edit_content(exo_id):
    formId = ExoEditId()
    formTheme = ExoEditTheme()
    formQuestion = ExoEditQuestion()
    formHint = ExoEditHint()
    formSolution = ExoEditSolution()
    if formQuestion.validate_on_submit() or formHint.validate_on_submit() or formSolution.validate_on_submit() or formId.validate_on_submit() or formTheme.validate_on_submit():
        flash('L\'exercice a été mis à jour'.decode('utf8'))
        return redirect(url_for('exo_edit_content', exo_id=exo_id))
    return render_template("exo_edit_content.html",
        title = 'Informations sur l\'exercice',
        exo_id = exo_id,
        exo_data = exo_data, #placeholder
        chart_data = chart_data, #placeholder
        formQuestion =formQuestion,
        formHint = formHint,
        formSolution = formSolution,
        formId = formId,
        formTheme = formTheme
        )


@app.route('/new_exo', methods = ['GET', 'POST'])
def new_exo():
    form = ExoEditForm()
    new_id= 56 #placeholder
    if form.validate_on_submit():
        new_number = 10 #placeholder: new_number a calculer en fonction du number du dernier exo du chapitre !
        exo = Exo(source = form.source.data, 
            author = form.author.data,
            number = new_number,
            difficulty = form.difficulty.data,
            question_html= latex_to_html(form.question.data),
            hint= form.hint.data,
            solution_html= latex_to_html(form.question.data) )
        db.session.add(exo)
        db.session.commit()
        flash('Le nouvel exercice a été entré dans la base'.decode('utf8'))
        return redirect(url_for('exo_edit_content', exo_id=new_id))
    return render_template('exo_edit_new.html', 
        title = 'Nouvel exo',
        form = form,
        new_id= new_id)




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
    
    "track":["PC","MP","PSI"],
    "category": "Algebre",
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

chart_data = { #placeholder
    "viewcount": hc_readify(exo_data["viewcount"],15),
    "flagcount": hc_readify(exo_data["flagcount"],15),
    "requestcount": hc_readify(exo_data["requestcount"],15)
}