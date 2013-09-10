#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from time import mktime
from models import *
import re
from dateutil import parser


###############################################################################
#
# chart data formatting js
#
###############################################################################


def aggregate_by_date(list_of_timestamps):
    ################################################################
    # takes a list_of_timestamps of timestamps
    # returns a dic {'day':'number of timestamps inside that day'}
    ################################################################
    output = {}
    for timestamp in list_of_timestamps:
        date = datetime.datetime.fromtimestamp(int(timestamp/1000)).\
            strftime('%d/%m/%Y')
        if date in output:
            output[date] += 1
        else:
            output[date] = 1
    return output


def count_views_LnD(list_of_timestamps, n):
    ################################################################
    # takes a list of timestamps and a number of days (n)
    # returns a list of number of occurences over the last n days
    # [occurences today, occurences yesterday, ...]
    ################################################################
    output = [0]*n
    for timestamp in list_of_timestamps:

        #convert js timestamp (ms) to python timestamp (s):
        dt = datetime.datetime.fromtimestamp(timestamp/1000.0)

        delta = (datetime.datetime.now() - dt)
        if delta.days > 0 and delta.days < n:
            output[delta.days] += 1
    return output


def list_days_LnD(n):
    ################################################################
    # takes a number of days
    # returns a list of timestamps, one for each day of the last n days
    # [timestamp of today, timestamp of yesterday, ...]
    ################################################################
    output = [None]*n
    now = datetime.datetime.now()
    for k in range(n):
        output[k] = (now - datetime.timedelta(days=k))
    return output


def js_timestamp_from_datetime(dt):
    return 1000 * mktime(dt.timetuple())


def hc_readify(list_of_timestamps, n):
    occurences = count_views_LnD(list_of_timestamps, n)
    LnD = list_days_LnD(n)
    output = []
    for i in range(1, n+1):
        output.append([js_timestamp_from_datetime(LnD[-i]), occurences[-i]])
    return output


###############################################################################
#
# chart data formatting python timestamps
#
###############################################################################

def count_views_LnD_py(list_of_timestamps, n):
    ################################################################
    # takes a list of timestamps and a number of days (n)
    # returns a list of number of occurences over the last n days
    # [occurences today, occurences yesterday, ...]
    ################################################################
    output = [0]*n
    for timestamp in list_of_timestamps:
        delta = (datetime.datetime.now() - parser.parse(timestamp).replace(tzinfo=None))
        if delta.days > 0 and delta.days < n:
            output[delta.days] += 1
    return output


def hc_readify_py(list_of_timestamps, n):
    ################################################################
    # takes a list of timestamps and a number of days (n)
    # returns a list of tuples ("%Y-%m-%d", number of occurences) over the last n days
    # ordered from n days ago to today
    ################################################################
    occurences = count_views_LnD_py(list_of_timestamps, n)
    LnD = list_days_LnD(n)
    output = []
    for i in range(1, n+1):
        output.append([LnD[-i].strftime("%Y-%m-%d"), occurences[-i]])
    return output


###############################################################################
#
# Latex to HTML
#
###############################################################################

def replfunc1(matchobj):
    if len(matchobj.group(0)) < 3:
        return "<br>"
    else:
        return matchobj.group(0)

"""cleaning2 = [
    (r'\\begin\{enumerate\}'    , r'<ol>'),
    (r'\\end\{enumerate\}'      , r'</ol>'),
    (r'\\begin\{itemize\}'      , r'<ul>'),
    (r'\\end\{itemize\}'        , r'</ul>'),
    (r'\\item\s*\[([^\]]*)\]'   , r'<br>$1&nbsp;'),
    (r'\\item'                  , r'\r\n<li>'),
    (r'(\\begin{array}(?:[^\\]+|\\(?!end{array}))*\\end{array})|(\\begin{cases}(?:[^\\]+|\\(?!end{cases}))*\\end{cases})|\\\\', replfunc1),]
"""

cleaning = [
    (r'\\begin\{enumerate\}((.|\n|\r)*?)\\end\{enumerate\}'     , r'<ol>\1</ol>'),
    (r'\\begin\{itemize\}((.|\n|\r)*?)\\end\{itemize\}'         , r'<ul>\1</ul>'),
    (r'\\item\s*\[([^\]]*)\]'                                   , r'<br>$1&nbsp;'),
    (r'\\item'                                                  , r'\r\n<li>'),
    (r'(\\begin{array}(?:[^\\]+|\\(?!end{array}))*\\end{array})|(\\begin{cases}(?:[^\\]+|\\(?!end{cases}))*\\end{cases})|\\\\', replfunc1),  #pour remplacer les "//" (sauts de ligne) mais seulement lorsqu'ils ne sont pas à l'interieur des environnements array et cases pour lesquels ils ont une signification.
    (r'\\paragraph\{(.*?)\}'                                    , r'<br><br><div class=\"paragraph-number\">\1</div>')
    ]

#(r'\\begin\{center\}\\includegraphics\{(.*?)\}\\end\{center\}'                              , r'<br><img src="data:image/png;base64,---base64 code here---" alt="graphique" width="100%" /><br>')

"""with open("path/to/file.png", "rb") as f:
    data = f.read()
    print data.encode("base64")"""


def latex_to_html(strinput):
    stroutput = strinput
    for group in cleaning:
        pattern   = group[0]
        repl      = group[1]
        string    = stroutput
        stroutput = re.sub(pattern, repl, string)
    return stroutput


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
    \\[ P = \\gamma \\prod_{i = 1}^{q} (X - X_{i})^{\\alpha_{i}}\\]
    avec $deg(P) = n \\ge 1$ et $deg(P') = n-1$.

    $X_{i}$ est racine de $P'$ d'ordre $(\\alpha_{i} - 1)$ (cours). Donc les racines multiples de $P'$ sont aussi racines de $P$.

    \\paragraph{2}
    On procède en deux étapes:
    \\begin{itemize}
    \\item  Les $X_{i}$ sont racines de $P'$ avec une somme des ordres égale à : $\\sum_{i = 1}^{q}(\\alpha_{i} - 1) = n-q$

    \\item On applique le théorème de Rolle à $P$ sur chaque $]X_{i},X_{i}+1[$ pour obtenir $q-1$ racines supplémentaires de $P'$.
    \\end{itemize}
    On a donc trouvé au total : $(n-q) + (q-1) = n-1 $ racines réelles de $P'$. Or $P'$ est de degré $n-1$. Donc $P'$ est scindé.

    \\paragraph{3}
    Si $P \\in \\mathbb{C}[X]$:
    Ce résultat n'est plus valable. Voici un contre exemple:
    $P(X) = (X-1)^{3} + 1$ est scindé dans $\\mathbb{C}$ mais n'admet pas comme racine $1$ qui est pourtant racine multiple de $P' = 3(X-1)^{2}$.
    """

solution2 = "a) $r:\\theta  \\mapsto r(\\theta ) = \\sqrt {\\cos 2\\theta } $ est définie et continue sur les intervalles $\\left[ { - \\pi  / 4,\\pi  / 4} \\right] + k\\pi $ avec $k \\in \\mathbb{Z}$.\\\\\r\nLa fonction $r$ est de classe ${\\mathcal{C}}^\\infty  $ sur les intervalles $\\left] { - \\pi  / 4,\\pi  / 4} \\right[ + k\\pi $ avec $k \\in \\mathbb{Z}$.\\\\\r\n$r(\\theta  + \\pi ) = r(\\theta )$ donc $M(\\theta  + \\pi )$ est l'image du point $M(\\theta )$ par la symétrie de centre $O$.\\\\\r\n$r( - \\theta ) = r(\\theta )$ donc $M( - \\theta )$ est l'image du point $M(\\theta )$ par la symétrie d'axe $(Ox)$\\\\\r\nOn peut limiter l'étude à l'intervalle $\\left[ {0,\\pi  / 4} \\right]$. La courbe obtenue sera complétée par les symétries de centre $O$ et d'axe $(Ox)$.\\\\\r\nOn a le tableau de variation\r\n$$\r\n\\begin{array}{c|ccc|}\r\n \\theta  & 0 & {} & {\\pi  / 4}  \\\\\r\n\\hline\r\n {r(\\theta )} & 1 &  \\searrow  & 0  \\\\\r\n\\hline\r\n\\end{array}\r\n$$\r\nEtude en $\\theta  = 0$.\\\\\r\n$r(0) = 1$ et $r'(0) = 0$.\\\\\r\nIl y a une tangente orthoradiale.\\\\\r\nEtude en $\\theta  = \\pi  / 4$.\\\\\r\n$r(\\pi  / 4) = 0$, il s'agit d'un passage par l'origine.\r\n$$\r\n\\begin{array}{c|ccc|}\r\n \\theta  & {} & {\\pi  / 4} & {}  \\\\\r\n\\hline\r\n {r(\\theta )} &  +  & 0 & {\\mid \\mid }  \\\\\r\n\\hline\r\n\\end{array}\r\n$$\r\nIl y a une demi-tangente en $M(\\pi  / 4) = O$ qui est la droite d'équation polaire $\\theta  = \\pi  / 4$.\\\\\r\n\\texttt{\\textbf{plot([sqrt(cos(2*t)), t, t=0..2*Pi], coords=polar, numpoints=200, xtickmarks=3, ytickmarks=3);}}\r\n\\begin{center}\\includegraphics{Cor0292100001}\\end{center}\r\nLemniscate de Bernoulli\r\nb) On a\r\n$$\\frac{{{\\text{d}}s}}{{{\\text{d}}\\theta }} = \\frac{1}{{\\sqrt {\\cos 2\\theta } }}$$\r\nUne détermination angulaire $\\alpha $ s'obtient par $\\alpha  = \\theta  + V$ avec \r\n$$\\left\\{ \r\n\\begin{gathered}\r\n  \\cos V =  - \\sin 2\\theta  \\hfill \\\\\r\n  \\sin V = \\cos 2\\theta  \\hfill \\\\ \r\n\\end{gathered}\r\n \\right.$$\r\n$V = \\frac{\\pi }{2} + 2\\theta $ convient puis $\\alpha  = \\frac{\\pi }{2} + 3\\theta $. \\\\\r\nOn en déduit\r\n$$\\gamma  = \\frac{{{\\mathrm{d}}\\alpha }}{{{\\mathrm{d}}s}} = \\frac{{{\\mathrm{d}}\\alpha }}{{{\\mathrm{d}}\\theta }}\\frac{{{\\mathrm{d}}\\theta }}{{{\\mathrm{d}}s}} = 3\\sqrt {\\cos 2\\theta } $$\r\nc) L'aire délimitée par ${\\mathcal{C}}$ peut-être calculée par une intégrale curviligne en prenant soin de considérer un parcours en sens direct de la courbe.\\\\\r\nPour $\\theta $ allant de $ - \\pi  / 4$ à $\\pi  / 4$, la boucle de droite est parcourue en sens direct et par considération de symétrie\r\n$${\\mathcal{A}} = \\oint_\\Gamma  {\\frac{1}{2}r^2 \\,{\\mathrm{d}}\\theta }  = 2\\int_{ - \\pi  / 4}^{\\pi  / 4} {\\cos 2\\theta \\,{\\mathrm{d}}\\theta }  = 1$$\r\n"


###############################################################################
#
# Log stats
#
###############################################################################

def view(exo_id, user_id):
    view = View(exo_id=exo_id, user_id=user_id)
    view.save()

def flag(exo_id, user_id):
    flag = Flag(exo_id=exo_id, user_id=user_id)
    flag.save()

def request(exo_id, user_id):
    request = Request(exo_id=exo_id, user_id=user_id)
    request.save()


if __name__ == "__main__":
    newstr = latex_to_html(solution2)
    print newstr
